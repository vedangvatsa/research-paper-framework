#!/usr/bin/env python3
"""Convert state-of-ai-research-2026.md to proper ICLR LaTeX. 
Adapted from agent-infrastructure-stack/build_tex.py"""
import re, os, shutil

PAPER_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(PAPER_DIR, 'state-of-ai-research-2026.md')
STY_SRC = os.path.join(PAPER_DIR, 'agent-infrastructure-stack', 'iclr2024_conference.sty')
OUT_DIR = os.path.join(PAPER_DIR, 'latex_build')

os.makedirs(OUT_DIR, exist_ok=True)

# Copy .sty file
shutil.copy2(STY_SRC, OUT_DIR)

# Copy figures
fig_src = os.path.join(PAPER_DIR, 'figures')
fig_dst = os.path.join(OUT_DIR, 'figures')
if os.path.exists(fig_dst):
    shutil.rmtree(fig_dst)
shutil.copytree(fig_src, fig_dst)

with open(SRC, 'r') as f:
    md = f.read()

# ═══════════════════════════════════════════════
# EXTRACT SECTIONS
# ═══════════════════════════════════════════════
abstract_match = re.search(r'## Abstract\n\n(.*?)\n\n_\*\*Keywords\*\*_', md, re.DOTALL)
abstract = abstract_match.group(1).strip()

body_match = re.search(r'---\n\n(## 1\. Introduction.*?)## References', md, re.DOTALL)
body = body_match.group(1).strip()

refs_match = re.search(r'## References\n\n(.*)', md, re.DOTALL)
refs_text = refs_match.group(1).strip()


def escape_latex_text(text):
    """Escape LaTeX special chars in running text."""
    # Unicode to LaTeX conversions (must come before other escapes)
    text = text.replace('§', '\\S{}')
    text = text.replace('\u2014', '---')  # em-dash
    text = text.replace('\u2013', '--')   # en-dash
    text = text.replace('\u2018', '`')    # left single quote
    text = text.replace('\u2019', "'")    # right single quote
    text = text.replace('\u201C', '``')   # left double quote
    text = text.replace('\u201D', "''")   # right double quote
    text = re.sub(r'(?<!\\)\$(\d)', r'\\$\1', text)
    text = re.sub(r'(?<!\\)%', r'\\%', text)
    text = re.sub(r'(?<!\\)&', r'\\&', text)
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    # Convert backtick code spans to \texttt
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    return text


def escape_latex_cell(text):
    """Escape LaTeX special chars in table cells only."""
    text = re.sub(r'\$(\d)', r'\\$\1', text)
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('&', '\\&')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('_', '\\_')
    # Convert **bold** to \textbf{}
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    return text


def convert_citations(text):
    """Convert [XX] and [XX, YY] to \\cite{refXX}."""
    def cite_replace(m):
        inner = m.group(1)
        parts = [p.strip() for p in inner.split(',')]
        if all(p.isdigit() for p in parts):
            refs = ','.join(f'ref{p}' for p in parts)
            return f'\\cite{{{refs}}}'
        return m.group(0)
    return re.sub(r'\[(\d+(?:\s*,\s*\d+)*)\]', cite_replace, text)


def convert_inline_formatting(text):
    """Convert bold, italic markdown to LaTeX."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\\textit{\1}', text)
    return text


def convert_quotes(text):
    """Convert straight quotes to LaTeX quotes."""
    text = re.sub(r'"([^"]*)"', r"``\1''", text)
    return text


def process_paragraph(text):
    """Full processing pipeline for a paragraph of running text."""
    text = escape_latex_text(text)
    text = convert_inline_formatting(text)
    text = convert_citations(text)
    text = convert_quotes(text)
    return text


def render_table(rows, caption=None):
    """Convert markdown table rows to LaTeX tabular."""
    header_cells = [c.strip() for c in rows[0].split('|')[1:-1]]
    ncols = len(header_cells)

    data_rows = []
    for row in rows[2:]:  # skip header + separator
        cells = [c.strip() for c in row.split('|')[1:-1]]
        while len(cells) < ncols:
            cells.append('')
        data_rows.append(cells[:ncols])

    col_spec = 'l' * ncols

    lines = []
    lines.append('\\begin{table}[H]')
    lines.append('\\centering')
    lines.append('\\footnotesize')
    if caption:
        cap_escaped = escape_latex_text(caption)
        lines.append(f'\\caption{{{cap_escaped}}}')
    use_resize = False
    lines.append(f'\\begin{{tabular}}{{{col_spec}}}')
    lines.append('\\toprule')

    h_cells = [f'\\textbf{{{escape_latex_cell(c)}}}' for c in header_cells]
    lines.append(' & '.join(h_cells) + ' \\\\')
    lines.append('\\midrule')

    for cells in data_rows:
        d_cells = [escape_latex_cell(c) for c in cells]
        lines.append(' & '.join(d_cells) + ' \\\\')

    lines.append('\\bottomrule')
    lines.append('\\end{tabular}')
    if use_resize:
        lines.append('}')
    lines.append('\\end{table}')

    return '\n'.join(lines)


def md_to_latex(text):
    """Convert markdown body to LaTeX."""
    lines_list = text.split('\n')
    output_blocks = []
    current_para = []
    in_table = False
    table_rows = []
    table_caption = None

    def flush_para():
        nonlocal current_para
        if current_para:
            para_text = '\n'.join(current_para)
            output_blocks.append(process_paragraph(para_text))
            current_para = []

    i = 0
    while i < len(lines_list):
        line = lines_list[i]

        if not line.strip():
            if in_table:
                in_table = False
                output_blocks.append(render_table(table_rows, table_caption))
                table_caption = None
                table_rows = []
            else:
                flush_para()
            output_blocks.append('')
            i += 1
            continue

        # Skip figure markdown links (we insert figures manually)
        if line.startswith('!['):
            flush_para()
            # Extract figure path
            fig_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if fig_match:
                caption_text = fig_match.group(1)
                fig_path = fig_match.group(2)
                # Per-figure size overrides to avoid page gaps
                fig_sizes = {
                    'fig_established_methods': 0.85,
                    'fig_llm_explosion': 0.75,
                    'fig_rising_methods': 0.85,
                    'fig_citation_dist': 0.75,
                    'fig_countries': 0.80,
                    'fig_llm_china_us': 0.80,
                    'fig_hype_cycle': 1.0,
                    'fig_china_vs_us': 0.80,
                }
                fig_width = 1.0
                for key, size in fig_sizes.items():
                    if key in fig_path:
                        fig_width = size
                        break
                # Convert to LaTeX figure
                cap_tex = escape_latex_text(caption_text)
                output_blocks.append(f"""\\begin{{figure}}[H]
\\centering
\\includegraphics[width={fig_width}\\textwidth]{{{fig_path}}}
\\caption{{{cap_tex}}}
\\end{{figure}}""")
            i += 1
            continue

        # Section headings
        if line.startswith('#### '):
            flush_para()
            title = line[5:].strip()
            title = re.sub(r'^\d+\.\d+\.\d+\s+', '', title)
            title = escape_latex_text(title)
            output_blocks.append(f'\\subsubsection{{{title}}}')
            i += 1
            continue

        if line.startswith('### '):
            flush_para()
            title = line[4:].strip()
            title = re.sub(r'^\d+\.\d+\s+', '', title)
            title = escape_latex_text(title)
            output_blocks.append(f'\\subsection{{{title}}}')
            i += 1
            continue

        if line.startswith('## '):
            flush_para()
            title = line[3:].strip()
            title = re.sub(r'^\d+\.\s+', '', title)
            title = escape_latex_text(title)
            output_blocks.append(f'\\section{{{title}}}')
            i += 1
            continue

        # Table caption
        if line.startswith('**Table ') and line.endswith('**'):
            flush_para()
            table_caption = line[2:-2]
            table_caption = re.sub(r'^Table \d+\.\s*', '', table_caption)
            i += 1
            continue

        # Table row
        if line.strip().startswith('|') and '|' in line[1:]:
            if not in_table:
                flush_para()
                in_table = True
                table_rows = []
            table_rows.append(line)
            i += 1
            continue

        if in_table:
            in_table = False
            output_blocks.append(render_table(table_rows, table_caption))
            table_caption = None
            table_rows = []
            continue

        # Numbered list items - group consecutive ones
        if re.match(r'^\d+\.\s', line):
            flush_para()
            output_blocks.append('\\begin{enumerate}')
            item_text = re.sub(r'^\d+\.\s+', '', line)
            item_text = process_paragraph(item_text)
            output_blocks.append(f'\\item {item_text}')
            i += 1
            while i < len(lines_list):
                if re.match(r'^\d+\.\s', lines_list[i]):
                    item_text = re.sub(r'^\d+\.\s+', '', lines_list[i])
                    item_text = process_paragraph(item_text)
                    output_blocks.append(f'\\item {item_text}')
                    i += 1
                elif lines_list[i].strip() == '':
                    # Skip blank lines between list items
                    i += 1
                else:
                    break
            output_blocks.append('\\end{enumerate}')
            continue

        # Bullet list items
        if line.startswith('- '):
            flush_para()
            output_blocks.append('\\begin{itemize}')
            while i < len(lines_list) and lines_list[i].startswith('- '):
                item_text = lines_list[i][2:]
                item_text = process_paragraph(item_text)
                output_blocks.append(f'\\item {item_text}')
                i += 1
            output_blocks.append('\\end{itemize}')
            continue

        # Horizontal rules
        if line.strip() == '---':
            flush_para()
            i += 1
            continue

        # Regular text
        current_para.append(line)
        i += 1
    result = '\n'.join(output_blocks)

    # Post-process: merge consecutive tables into side-by-side layout
    result = merge_consecutive_tables(result)

    return result


def merge_consecutive_tables(tex):
    """Find consecutive \\begin{table}...\\end{table} pairs and place side by side."""
    # Split into table blocks and non-table blocks
    table_re = re.compile(r'(\\begin\{table\}\[H\].*?\\end\{table\})', re.DOTALL)
    parts = table_re.split(tex)
    # parts alternates: text, table, text, table, text, ...

    merged = []
    i = 0
    while i < len(parts):
        if i + 2 < len(parts) and parts[i].strip() == '' and table_re.match(parts[i-1] if i > 0 else ''):
            # This doesn't work well with split. Use a different approach.
            pass
        merged.append(parts[i])
        i += 1

    # Simpler approach: find and replace consecutive table pairs
    result = []
    blocks = table_re.split(tex)
    # blocks = [text0, table1, text1, table2, text2, ...]
    first_merge = True
    i = 0
    while i < len(blocks):
        if table_re.match(blocks[i]):
            # This is a table block. Check if next non-empty text leads to another table.
            if (i + 2 < len(blocks) and
                blocks[i+1].strip() == '' and
                table_re.match(blocks[i+2])):
                # Merge these two tables side-by-side
                block1 = blocks[i]
                block2 = blocks[i+2]
                cap1 = re.search(r'\\caption\{([^}]*)\}', block1)
                cap2 = re.search(r'\\caption\{([^}]*)\}', block2)
                tab1 = re.search(r'(\\begin\{tabular\}.*?\\end\{tabular\})', block1, re.DOTALL)
                tab2 = re.search(r'(\\begin\{tabular\}.*?\\end\{tabular\})', block2, re.DOTALL)
                if cap1 and cap2 and tab1 and tab2:
                    if first_merge:
                        # Convert tabular to tabularx with X for first column (only for first pair with long labels)
                        def to_tabularx(tab_str):
                            s = tab_str
                            s = re.sub(r'\\begin\{tabular\}\{(l+)\}',
                                       lambda m: '\\begin{tabularx}{\\textwidth}{X' + 'l' * (len(m.group(1)) - 1) + '}',
                                       s)
                            s = s.replace('\\end{tabular}', '\\end{tabularx}')
                            return s
                        content1 = to_tabularx(tab1.group(1))
                        content2 = to_tabularx(tab2.group(1))
                        first_merge = False
                    else:
                        content1 = tab1.group(1)
                        content2 = tab2.group(1)
                    merged_table = (
                        f'\\begin{{table}}[H]\n'
                        f'\\centering\\footnotesize\n'
                        f'\\begin{{minipage}}[t]{{0.48\\textwidth}}\n\\centering\n{cap1.group(0)}\n{content1}\n\\end{{minipage}}\n'
                        f'\\hfill\n'
                        f'\\begin{{minipage}}[t]{{0.48\\textwidth}}\n\\centering\n{cap2.group(0)}\n{content2}\n\\end{{minipage}}\n'
                        f'\\end{{table}}'
                    )
                    result.append(merged_table)
                    i += 3  # skip table1, gap, table2
                    continue
            # Single table, keep as-is
            result.append(blocks[i])
        else:
            result.append(blocks[i])
        i += 1
    return ''.join(result)


def build_bibliography(refs_text):
    """Convert [N] references to thebibliography."""
    entries = re.findall(r'\[(\d+)\]\s*(.*?)(?=\n\n\[|\Z)', refs_text, re.DOTALL)
    bib_items = []
    for num, text in entries:
        text = text.strip()
        text = text.replace('&', '\\&')
        text = text.replace('%', '\\%')
        text = text.replace('_', '\\_')
        text = re.sub(r'(?<!\\)\$', r'\\$', text)
        # Extract and convert URLs - handle markdown links first
        text = re.sub(r'\[(https?://[^\]]+)\]\([^\)]+\)', lambda m: '\\url{' + m.group(1).replace('\\_', '_') + '}', text)
        # Then standalone URLs
        text = re.sub(r'(?<!\{)(https?://[^\s]+)', lambda m: '\\url{' + m.group(1).replace('\\_', '_') + '}', text)
        bib_items.append(f'\\bibitem{{ref{num}}}\n{text}\n')

    return '\\small\n\\begin{thebibliography}{99}\n\\raggedright\n\n' + '\n'.join(bib_items) + '\n\\end{thebibliography}'


# ═══════════════════════════════════════════════
# PROCESS
# ═══════════════════════════════════════════════
abstract_tex = process_paragraph(abstract)
body_tex = md_to_latex(body)
bib_tex = build_bibliography(refs_text)

template = r"""\documentclass{article}
\usepackage{iclr2024_conference,times}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsfonts}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{float}
\usepackage{tabularx}
\usepackage{caption}
\captionsetup[table]{skip=6pt}
\hyphenpenalty=5000
\tolerance=1000

\iclrfinalcopy
\setcitestyle{numbers,square}

\title{State of AI Research}

\author{Vedang Ratan Vatsa \\\\
Founder, Hashtag Web3 \\\\
\texttt{vedangvats@gmail.com}}

\begin{document}
\raggedbottom

\maketitle

\begin{abstract}
""" + abstract_tex + r"""
\end{abstract}

""" + body_tex + r"""

\clearpage
""" + bib_tex + r"""

\end{document}
"""

def merge_consecutive_tables(tex_content):
    """Find consecutive table environments in the generated LaTeX and merge them side-by-side."""
    table_pattern = re.compile(r'\\begin\{table\}\[t!\](.*?)\\end\{table\}', re.DOTALL)
    
    matches = list(table_pattern.finditer(tex_content))
    if not matches:
        return tex_content
        
    replacements = []
    i = 0
    while i < len(matches) - 1:
        end_curr = matches[i].end()
        start_next = matches[i+1].start()
        between = tex_content[end_curr:start_next].strip()
        if not between:
            # We found consecutive tables! Merge them
            table1_inner = matches[i].group(1)
            table2_inner = matches[i+1].group(1)
            
            # Extract caption and tabular from Table 1
            caption1_match = re.search(r'\\caption\{(.*?)\}', table1_inner)
            tabular1_match = re.search(r'\\begin\{tabular\}(.*?)\\end\{tabular\}', table1_inner, re.DOTALL)
            
            # Extract caption and tabular from Table 2
            caption2_match = re.search(r'\\caption\{(.*?)\}', table2_inner)
            tabular2_match = re.search(r'\\begin\{tabular\}(.*?)\\end\{tabular\}', table2_inner, re.DOTALL)
            
            if tabular1_match and tabular2_match:
                caption1 = f"\\caption{{{caption1_match.group(1)}}}" if caption1_match else ""
                tabular1 = f"\\begin{{tabular}}{tabular1_match.group(1)}\\end{{tabular}}"
                
                caption2 = f"\\caption{{{caption2_match.group(1)}}}" if caption2_match else ""
                tabular2 = f"\\begin{{tabular}}{tabular2_match.group(1)}\\end{{tabular}}"
                
                merged_table = f"""\\begin{{table}}[t!]
\\centering
\\footnotesize
\\setlength{{\\tabcolsep}}{{2pt}}
\\begin{{minipage}}[t]{{0.52\\textwidth}}
\\centering
{caption1}
\\vspace{{2pt}}
{tabular1}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.46\\textwidth}}
\\centering
{caption2}
\\vspace{{2pt}}
{tabular2}
\\end{{minipage}}
\\end{{table}}"""
                replacements.append((matches[i].start(), matches[i+1].end(), merged_table))
                i += 2 # skip next table
                continue
        i += 1
        
    # Apply replacements from end to start to keep indices valid
    new_content = tex_content
    for start, end, rep in reversed(replacements):
        new_content = new_content[:start] + rep + new_content[end:]
        
    return new_content

template = merge_consecutive_tables(template)

out_path = os.path.join(OUT_DIR, 'paper.tex')
with open(out_path, 'w') as f:
    f.write(template)

# Stats
cite_count = len(re.findall(r'\\cite\{', template))
bibitem_count = len(re.findall(r'\\bibitem\{', template))
section_count = len(re.findall(r'\\section\{', template))
subsection_count = len(re.findall(r'\\subsection\{', template))
table_count = len(re.findall(r'\\begin\{table\}', template))
figure_count = len(re.findall(r'\\begin\{figure\}', template))

print(f"Written {out_path} ({len(template)} chars)")
print(f"  \\cite:        {cite_count}")
print(f"  \\bibitem:     {bibitem_count}")
print(f"  \\section:     {section_count}")
print(f"  \\subsection:  {subsection_count}")
print(f"  tables:       {table_count}")
print(f"  figures:      {figure_count}")
