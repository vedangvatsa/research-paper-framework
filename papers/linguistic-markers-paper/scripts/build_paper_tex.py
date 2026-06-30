#!/usr/bin/env python3
"""Convert paper/manuscript.md to proper ICLR LaTeX and package it."""
import re, os, shutil, subprocess

PROJECT_DIR = '/Users/vedang/ZCodeProject/research-paper-framework/papers/linguistic-markers-paper'
SRC = os.path.join(PROJECT_DIR, 'linguistic_markers_paper.md')
STY_SRC = os.path.join(PROJECT_DIR, 'latex_build', 'iclr2024_conference.sty')
OUT_DIR = os.path.join(PROJECT_DIR, 'latex_build')

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUT_DIR, 'figures'), exist_ok=True)

# Copy .sty file
if os.path.exists(STY_SRC) and os.path.dirname(STY_SRC) != OUT_DIR:
    shutil.copy2(STY_SRC, OUT_DIR)
    print(f"Copied {STY_SRC} to {OUT_DIR}")
elif os.path.exists(STY_SRC):
    print(f"STY file already in output directory")
else:
    print(f"Error: {STY_SRC} does not exist!")

with open(SRC, 'r', encoding='utf-8') as f:
    md = f.read()

# Extract abstract, body, references
abstract_match = re.search(r'## Abstract\n\n(.*?)\n\n_\*\*Keywords\*\*_', md, re.DOTALL)
if abstract_match:
    abstract = abstract_match.group(1).strip()
    # Remove **Background** etc. bold headers that aren't needed in LaTeX abstract
    abstract = re.sub(r'\*\*\w+\*\*\s*', '', abstract)
else:
    print("Warning: Abstract not found!")
    abstract = ""

body_match = re.search(r'(## 1\. Introduction.*?)## 7\. References', md, re.DOTALL)
if body_match:
    body = body_match.group(1).strip()
else:
    print("Warning: Body not found!")
    body = ""

refs_match = re.search(r'## 7\. References\n\n(.*)', md, re.DOTALL)
if refs_match:
    refs_text = refs_match.group(1).strip()
else:
    print("Warning: References not found!")
    refs_text = ""

def escape_latex_text(text):
    """Escape LaTeX special chars in running text."""
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
    text = text.replace('→', r'$\rightarrow$')
    
    def make_breakable(match):
        t = match.group(1)
        t = t.replace(',', ',\\allowbreak{}')
        t = t.replace('.', '.\\allowbreak{}')
        t = t.replace('\\_', '\\_\\allowbreak{}')
        t = t.replace(':', ':\\allowbreak{}')
        t = t.replace('|', '|\\allowbreak{}')
        return r'\texttt{' + t + '}'
    text = re.sub(r'`([^`]+)`', make_breakable, text)
    return text

def escape_latex_cell(text):
    """Escape LaTeX special chars in table cells only."""
    text = text.replace('±', r'\textpm{}')
    text = re.sub(r'\$(\d)', r'\\$\1', text)
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('&', '\\&')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('_', '\\_')
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    return text

def convert_citations(text):
    """Convert [XX] to \\cite{refXX}."""
    def cite_replace(m):
        inner = m.group(1)
        parts = [p.strip() for p in re.split(r'[,;]\s*', inner)]
        if all(p.isdigit() for p in parts):
            refs = ','.join(f'ref{p}' for p in parts)
            return f'\\cite{{{refs}}}'
        return m.group(0)
    return re.sub(r'\[(\d+(?:\s*[,;]\s*\d+)*)\]', cite_replace, text)

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
    lines.append('\\small')
    lines.append(f'\\begin{{tabular}}{{{col_spec}}}')
    lines.append('\\toprule')

    # Header row
    h_cells = [f'\\textbf{{{escape_latex_cell(c)}}}' for c in header_cells]
    lines.append(' & '.join(h_cells) + ' \\\\')
    lines.append('\\midrule')

    # Data rows
    for cells in data_rows:
        d_cells = [escape_latex_cell(c) for c in cells]
        lines.append(' & '.join(d_cells) + ' \\\\')

    lines.append('\\bottomrule')
    lines.append('\\end{tabular}')
    if caption:
        cap_escaped = escape_latex_text(caption)
        lines.append(f'\\caption{{{cap_escaped}}}')
    lines.append('\\end{table}')

    return '\n'.join(lines)

def md_to_latex(text):
    """Convert markdown body to LaTeX."""
    lines = text.split('\n')
    output_blocks = []
    current_para = []
    in_table = False
    table_rows = []
    table_caption = None

    def flush_para():
        nonlocal current_para
        if current_para:
            para_text = '\n'.join(current_para)
            if para_text.strip().startswith('- ') or para_text.strip().startswith('* '):
                items = re.split(r'\n[-*]\s+', para_text)
                list_lines = ['\\begin{itemize}']
                for item in items:
                    item_clean = re.sub(r'^[-*]\s+', '', item.strip()).strip()
                    if item_clean:
                        list_lines.append(f'  \\item {process_paragraph(item_clean)}')
                list_lines.append('\\end{itemize}')
                output_blocks.append('\n'.join(list_lines))
            elif re.match(r'^\d+\.\s', para_text.strip()):
                items = re.split(r'\n\d+\.\s+', para_text)
                list_lines = ['\\begin{enumerate}']
                for item in items:
                    item_clean = item.strip().lstrip('1234567890.').strip()
                    if item_clean:
                        list_lines.append(f'  \\item {process_paragraph(item_clean)}')
                list_lines.append('\\end{enumerate}')
                # Merge with previous enumerate block if it exists (skipping empty blocks)
                prev_enum_idx = None
                for j in range(len(output_blocks) - 1, -1, -1):
                    if output_blocks[j].strip() == '':
                        continue
                    if output_blocks[j].strip().endswith('\\end{enumerate}'):
                        prev_enum_idx = j
                    break
                if prev_enum_idx is not None:
                    prev_block = output_blocks[prev_enum_idx]
                    # Extract items from previous enumerate block
                    prev_stripped = prev_block.strip()
                    if prev_stripped.startswith('\\begin{enumerate}') and prev_stripped.endswith('\\end{enumerate}'):
                        prev_items = prev_stripped[len('\\begin{enumerate}'):-len('\\end{enumerate}')].strip()
                        new_items = '\n'.join(list_lines[1:-1])
                        output_blocks[prev_enum_idx] = f'\\begin{{enumerate}}\n{prev_items}\n{new_items}\n\\end{{enumerate}}'
                    else:
                        output_blocks.append('\n'.join(list_lines))
                else:
                    output_blocks.append('\n'.join(list_lines))
            else:
                rendered = process_paragraph(para_text)
                if re.match(r'\\textbf\{\d+\.', rendered):
                    rendered = '\\vspace{-3pt}\n' + rendered
                output_blocks.append(rendered)
            current_para = []

    i = 0
    while i < len(lines):
        line = lines[i]

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

        if line.startswith('## ') and not line.startswith('## References'):
            flush_para()
            title = line[3:].strip()
            title = re.sub(r'^([IVXLC]+|\d+)\.\s+', '', title)
            title = escape_latex_text(title)
            output_blocks.append(f'\\section{{{title}}}')
            i += 1
            continue

        if line.startswith('### '):
            flush_para()
            title = line[4:].strip()
            title = re.sub(r'^([A-Z]\.|\d+\.\d+)\s+', '', title)
            title = escape_latex_text(title)
            output_blocks.append(f'\\subsection{{{title}}}')
            i += 1
            continue

        if line.startswith('**Table ') and line.endswith('**'):
            flush_para()
            table_caption = line[2:-2]
            table_caption = re.sub(r'^Table \d+\.\s*', '', table_caption)
            i += 1
            continue

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

        fig_match = re.match(r'^!\[(.+?)\]\((.+?)\)$', line.strip())
        if fig_match:
            flush_para()
            caption = fig_match.group(1)
            img_path = fig_match.group(2)
            img_basename = os.path.splitext(os.path.basename(img_path))[0]
            # Sourced from workspace root or similar
            src_img = os.path.join(PROJECT_DIR, img_path)
            if os.path.exists(src_img):
                shutil.copy2(src_img, os.path.join(OUT_DIR, 'figures'))
                print(f"Copied figure {src_img} to {OUT_DIR}/figures")
            caption_tex = escape_latex_text(caption)
            fig_tex = (
                '\\begin{figure}[ht]\n'
                '\\centering\n'
                '\\vspace{-0.5em}\n'
                f'\\includegraphics[width=0.75\\textwidth,clip]{{figures/{img_basename}}}\n'
                '\\vspace{-0.5em}\n'
                f'\\caption{{{caption_tex}}}\n'
                '\\end{figure}'
            )
            output_blocks.append(fig_tex)
            i += 1
            continue

        current_para.append(line)
        i += 1

    if in_table:
        output_blocks.append(render_table(table_rows, table_caption))
    flush_para()

    return '\n'.join(output_blocks)

def build_bibliography(refs_text):
    """Convert numbered references to thebibliography with clean hyperlinks."""
    REF_URLS = {
        '1': 'https://doi.org/10.1017/CBO9780511621024',
        '2': 'https://scholar.google.com/scholar?q=Hyland+Metadiscourse+Exploring+Interaction+Writing+2005',
        '3': 'https://doi.org/10.1017/CBO9781139524599',
        '4': 'https://doi.org/10.1109/BigDataService58306.2023.00011',
        '5': 'https://arxiv.org/abs/2301.07597',
        '6': 'https://arxiv.org/abs/2303.11156',
        '7': 'https://arxiv.org/abs/2303.13408',
        '8': 'https://pdos.csail.mit.edu/archive/scigen/',
        '9': 'https://arxiv.org/abs/2301.11305',
        '10': 'https://arxiv.org/abs/2403.19074',
        '11': 'https://www.proquest.com/docview/305349212',
        '12': 'https://press.uchicago.edu/ucp/books/book/chicago/D/bo3631492.html',
        '13': 'https://arxiv.org/abs/2205.01833',
        '14': 'https://doi.org/10.1002/asi.21001',
        '15': 'https://arxiv.org/abs/2005.14165',
        '16': 'https://doi.org/10.1023/a:1010933404324',
        '17': 'https://arxiv.org/abs/2203.02155',
        '18': 'https://doi.org/10.3758/brm.42.2.381'
    }
    
    entries = re.split(r'\n\n+', refs_text.strip())
    bib_items = []
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        match = re.match(r'^\[(\d+)\]\s*(.*)', entry, re.DOTALL)
        if match:
            num = match.group(1)
            text = match.group(2).strip()
            text = text.replace('&', '\\&')
            text = text.replace('%', '\\%')
            text = re.sub(r'(?<!\\)\$', r'\\$', text)
            text = text.replace('_', '\\_')
            text = re.sub(r'(?<!\w)\*([^*]+?)\*(?!\w)', r'\\textit{\1}', text)
            
            url = REF_URLS.get(num, '')
            if url:
                raw_url = url  # Keep url raw for \href
                display = re.sub(r'^https?://(www\.)?', '', url).rstrip('/')
                # Escape special LaTeX chars in display text
                display_escaped = display.replace('_', '\\_').replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')
                text += f'. \\href{{{raw_url}}}{{{display_escaped}}}'
                
            bib_items.append(f'\\bibitem{{ref{num}}}\n{text}\n')

    return '\\small\n\\begin{thebibliography}{10}\n\\raggedright\n\n' + '\n'.join(bib_items) + '\n\\end{thebibliography}'

abstract_tex = process_paragraph(abstract)
body_tex = md_to_latex(body)
bib_tex = build_bibliography(refs_text)

template = r"""\documentclass{article}
\usepackage{iclr2024_conference,times}
\usepackage{amsmath}
\usepackage{textcomp}
\usepackage[htt]{hyphenat}

\tolerance=1500
\emergencystretch=2em
\hyphenpenalty=10000
\exhyphenpenalty=10000
\frenchspacing
\sloppy
\widowpenalty=150
\clubpenalty=150
\predisplaypenalty=0

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[colorlinks=true,linkcolor=blue!60!black,citecolor=blue!60!black,urlcolor=blue!60!black]{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsfonts}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{float}
\usepackage{caption}
\captionsetup{font=it}
\captionsetup[table]{skip=6pt}
\captionsetup[figure]{skip=6pt}

\iclrfinalcopy
\setcitestyle{numbers,square}

\title{Language Patterns in AI vs Human\\Scientific Abstracts}

\author{Vedang Ratan Vatsa \\
\href{https://veda.ng}{veda.ng} \textperiodcentered{} \href{mailto:vedangvats@gmail.com}{vedangvats@gmail.com}}

\begin{document}
\hypersetup{
  pdftitle={Language Patterns in AI vs Human Scientific Abstracts},
  pdfauthor={Vedang Ratan Vatsa},
  pdfsubject={Analysis of 200,000 Scientific Abstracts},
  pdfkeywords={LLM detection, corpus linguistics, metadiscourse, stylometrics, lexical diversity, scientific register},
  pdfcreator={Vedang Ratan Vatsa},
  pdfproducer={Vedang Ratan Vatsa}
}
\special{pdf:docinfo <<
/Title (Language Patterns in AI vs Human Scientific Abstracts)
/Author (Vedang Ratan Vatsa)
/Subject (Analysis of 200,000 Scientific Abstracts)
/Keywords (LLM detection, corpus linguistics, metadiscourse, stylometrics, lexical diversity, scientific register)
/Creator (Vedang Ratan Vatsa)
/Producer (Vedang Ratan Vatsa)
>>}
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

out_path = os.path.join(OUT_DIR, 'paper.tex')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(template)

print(f"Written {out_path} ({len(template)} chars)")

# Compile using tectonic
try:
    print("Compiling LaTeX to PDF using tectonic...")
    res = subprocess.run(['tectonic', 'paper.tex'], cwd=OUT_DIR, check=True, capture_output=True, text=True)
    print("Compilation successful.")
    pdf_src = os.path.join(OUT_DIR, 'paper.pdf')
    pdf_dest = os.path.join(PROJECT_DIR, 'linguistic_markers_paper.pdf')
    shutil.copy2(pdf_src, pdf_dest)
    print(f"Copied compiled PDF to {pdf_dest}")
    # Also copy to Desktop if exists
    desktop = '/Users/vedang/Desktop'
    if os.path.exists(desktop):
        shutil.copy2(pdf_src, os.path.join(desktop, 'linguistic_markers_paper.pdf'))
        print("Copied compiled PDF to Desktop")
except subprocess.CalledProcessError as e:
    print(f"Compilation failed with exit code {e.returncode}")
    print("Stdout:", e.stdout)
    print("Stderr:", e.stderr)
except Exception as ex:
    print(f"Compilation encountered error: {str(ex)}")
