#!/usr/bin/env python3
"""Convert agent_infrastructure_stack.md to proper ICLR LaTeX. v2"""
import re

with open('agent_infrastructure_stack.md', 'r') as f:
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
    text = re.sub(r'(?<!\\)\$(\d)', r'\\$\1', text)
    text = re.sub(r'(?<!\\)%', r'\\%', text)
    text = re.sub(r'(?<!\\)&', r'\\&', text)
    text = text.replace('#', '\\#')
    return text


def escape_latex_cell(text):
    """Escape LaTeX special chars in table cells only."""
    text = re.sub(r'\$(\d)', r'\\$\1', text)
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('&', '\\&')  # Escape & in cell content
    text = text.replace('~', '\\textasciitilde{}')
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
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\\textit{\1}', text)
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

    # Column spec: use natural l columns; resizebox will scale to fit
    col_spec = 'l' * ncols

    lines = []
    lines.append('\\begin{table}[H]')
    lines.append('\\centering')
    lines.append('\\small')
    if caption:
        cap_escaped = escape_latex_text(caption)
        lines.append(f'\\caption{{{cap_escaped}}}')
    # Only use resizebox for tables with 4+ columns to avoid
    # stretching narrow tables (like 2-column tables) to full width
    if ncols >= 3:
        lines.append('\\resizebox{\\textwidth}{!}{')
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
    if ncols >= 3:
        lines.append('}')  # close resizebox
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
            output_blocks.append(process_paragraph(para_text))
            current_para = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Empty line = paragraph break
        if not line.strip():
            if in_table:
                # End of table
                in_table = False
                output_blocks.append(render_table(table_rows, table_caption))
                table_caption = None
                table_rows = []
            else:
                flush_para()
            output_blocks.append('')
            i += 1
            continue

        # Section headings
        if line.startswith('## '):
            flush_para()
            title = line[3:].strip()
            title = re.sub(r'^\d+\.\s+', '', title)
            title = escape_latex_text(title)
            output_blocks.append(f'\\section{{{title}}}')
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

        # Table caption: **Table N. Title**
        if line.startswith('**Table ') and line.endswith('**'):
            flush_para()
            table_caption = line[2:-2]
            table_caption = re.sub(r'^Table \d+\.\s*', '', table_caption)
            i += 1
            continue

        # Table row (pipe-delimited)
        if line.strip().startswith('|') and '|' in line[1:]:
            if not in_table:
                flush_para()
                in_table = True
                table_rows = []
            table_rows.append(line)
            i += 1
            continue

        # If we were in a table but this line isn't a table row, end the table
        if in_table:
            in_table = False
            output_blocks.append(render_table(table_rows, table_caption))
            table_caption = None
            table_rows = []
            # Don't increment — process this line normally
            continue

        # Regular text line
        current_para.append(line)
        i += 1

    # Flush remaining
    if in_table:
        output_blocks.append(render_table(table_rows, table_caption))
    flush_para()

    return '\n'.join(output_blocks)


def build_bibliography(refs_text):
    """Convert numbered references to thebibliography."""
    entries = re.split(r'\n\n+', refs_text.strip())
    bib_items = []
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        match = re.match(r'^(\d+)\.\s*(.*)', entry, re.DOTALL)
        if match:
            num = match.group(1)
            text = match.group(2).strip()
            # Escape
            text = text.replace('&', '\\&')
            text = text.replace('%', '\\%')
            text = re.sub(r'(?<!\\)\$', r'\\$', text)
            # Escape underscores in bibliography text
            text = text.replace('_', '\\_')
            # Convert URLs to \url{}
            # Clean URLs: remove https://www. or https:// prefix for display
            def clean_url(m):
                url = m.group(1)
                # Unescape underscores in the actual URL for hyperref
                raw_url = url.replace('\\_', '_')
                display = re.sub(r'^https?://(www\.)?', '', url).rstrip('/')
                return f'\\href{{{raw_url}}}{{{display}}}'
            text = re.sub(r'(https?://[^\s]+)', clean_url, text)
            bib_items.append(f'\\bibitem{{ref{num}}}\n{text}\n')

    return '\\small\n\\begin{thebibliography}{65}\n\\raggedright\n\n' + '\n'.join(bib_items) + '\n\\end{thebibliography}'


# ═══════════════════════════════════════════════
# PROCESS
# ═══════════════════════════════════════════════
abstract_tex = process_paragraph(abstract)

# Fix Gini in abstract
abstract_tex = abstract_tex.replace(
    "extreme capital concentration (a Gini coefficient of approximately 0.78 across company funding, higher than US household income inequality)",
    "extreme capital concentration (the top 10 deals account for 78\\% of total capital)"
)

body_tex = md_to_latex(body)

# Table 1 stays as [H] - do not change to floating placement
# [H] forces exact placement, preventing paragraph splits

# Insert market map figure AFTER Table 1 (not before) so Table 1
# fills the bottom of page 3 and the large figure starts on page 4
table1_end = "\\end{table}"
figure_latex = r"""
\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{market_map.pdf}
\caption{The Agent Infrastructure Stack market map (mid-2026). Each horizontal bar represents one infrastructure layer, ordered by dependency (bottom to top). Company chips show disclosed funding. Italic names indicate acquired companies with their acquirer. Platform bundlers absorbing multiple layers appear at the bottom.}
\label{fig:market_map}
\end{figure}
"""
# Insert market map figure right before Section 4 (Market Map Analysis)
# so the layer descriptions flow naturally on page 3 and fill up the space under Table 1.
section4_str = "\\section{Market Map Analysis}"
sec4_pos = body_tex.find(section4_str)
if sec4_pos > 0:
    body_tex = body_tex[:sec4_pos] + "\n" + figure_latex + "\n" + body_tex[sec4_pos:]

# Fix Gini in body
body_tex = body_tex.replace(
    'At 0.78, the agent infrastructure market is more unequal than US household income distribution (Gini ~0.49) and comparable to global wealth distribution.',
    'At 0.78, the funding distribution is heavily concentrated even by venture capital standards, where power-law outcomes are the norm.'
)

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
\usepackage{caption}
\captionsetup[table]{skip=6pt}

\iclrfinalcopy
\setcitestyle{numbers,square}

\title{The Agent Infrastructure Stack}

\author{Vedang Ratan Vatsa \\
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

# Remove any \lhead that my earlier fix might have left
template = template.replace('\\lhead{Preprint. Under review.}\n', '')

with open('template.tex', 'w') as f:
    f.write(template)

# Stats
cite_count = len(re.findall(r'\\cite\{', template))
bibitem_count = len(re.findall(r'\\bibitem\{', template))
section_count = len(re.findall(r'\\section\{', template))
subsection_count = len(re.findall(r'\\subsection\{', template))
table_count = len(re.findall(r'\\begin\{table\}', template))

print(f"Written template.tex ({len(template)} chars)")
print(f"  \\cite:       {cite_count}")
print(f"  \\bibitem:    {bibitem_count}")
print(f"  \\section:    {section_count}")
print(f"  \\subsection: {subsection_count}")
print(f"  tables:      {table_count}")

# Verify table integrity
lines = template.split('\n')
in_tab = False
expected_cols = 0
issues = 0
for ln, line in enumerate(lines, 1):
    if '\\begin{tabular}' in line:
        in_tab = True
        spec_match = re.search(r'\\begin\{tabular\}\{([^}]+)\}', line)
        if spec_match:
            spec = spec_match.group(1)
            expected_cols = len(re.findall(r'[lcrp]', spec))
    if '\\end{tabular}' in line:
        in_tab = False
        expected_cols = 0
    if in_tab and '\\\\' in line and line.strip() not in ('\\toprule', '\\midrule', '\\bottomrule'):
        # Strip escaped ampersands (content), then count bare & (column separators)
        stripped = line.replace('\\&', '')
        bare_amps = stripped.count('&')
        if expected_cols > 0 and bare_amps != expected_cols - 1:
            issues += 1
            print(f"  WARNING: table row at line {ln} has {bare_amps} separators, expected {expected_cols - 1}: {line[:80]}")
if issues:
    print(f"  Table issues found: {issues}")
else:
    print(f"  Table integrity: OK")

