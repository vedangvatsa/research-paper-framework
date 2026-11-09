#!/usr/bin/env python3
"""Convert agentic_web_readiness_50k.md to ICLR LaTeX. Adapted from the
agent-infrastructure-stack builder: same conventions plus code spans,
underscore handling, horizontal-rule skipping, and markdown figures."""
import re

with open('agentic_web_readiness_50k.md', 'r') as f:
    md = f.read()

title_match = re.search(r'^#\s+(.+)$', md, re.MULTILINE)
if not title_match:
    raise ValueError('The manuscript must have a top-level title')

# ═══════════════════════════════════════════════
# EXTRACT SECTIONS
# ═══════════════════════════════════════════════
abstract_match = re.search(r'## Abstract\n+(.*?)\n\n_\*\*Keywords\*\*_', md, re.DOTALL)
abstract = abstract_match.group(1).strip()

keywords_match = re.search(r'_\*\*Keywords\*\*_: (.*?)\n', md)
keywords = keywords_match.group(1).strip() if keywords_match else ''

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
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{').replace('}', '\\}')
    text = text.replace('±', '$\\pm$')
    return text


def escape_latex_cell(text):
    """Escape LaTeX special chars in table cells only."""
    text = re.sub(r'\$(\d)', r'\\$\1', text)
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('&', '\\&')  # Escape & in cell content
    text = text.replace('_', '\\_')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('{', '\\{').replace('}', '\\}')
    text = text.replace('±', '$\\pm$')
    return text


def extract_code_spans(text):
    """Pull out `code` spans; return (text with placeholders, list of raw)."""
    codes = []
    def stash(m):
        codes.append(m.group(1))
        return f'\x00CODE{len(codes) - 1}\x00'
    return re.sub(r'`([^`]+)`', stash, text), codes


def restore_code_spans(text, codes):
    """Restore code spans in the body font for a visually consistent paper."""
    for i, raw in enumerate(codes):
        safe = ('\\nolinkurl{' + raw + '}' if re.fullmatch(r'[a-f0-9]{64}', raw)
                else escape_latex_text(raw))
        text = text.replace(f'\x00CODE{i}\x00', safe)
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
    text, codes = extract_code_spans(text)    # Markdown links [text](url) -> \href (before escaping touches braces)
    links = []
    maths = []

    def stash_math(m):
        maths.append(m.group(1))
        return f'\x00MATH{len(maths) - 1}\x00'

    text = re.sub(r'(?<!\\)\$([^\n$]+)\$', stash_math, text)

    def stash_link(m):
        links.append((m.group(1), m.group(2)))
        return f'\x00LINK{len(links) - 1}\x00'

    text = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', stash_link, text)
    text = escape_latex_text(text)
    text = convert_inline_formatting(text)
    text = convert_citations(text)
    text = convert_quotes(text)
    text = restore_code_spans(text, codes)
    for i, expression in enumerate(maths):
        text = text.replace(f'\x00MATH{i}\x00', '$' + expression + '$')
    for i, (label, url) in enumerate(links):
        label = escape_latex_text(label)
        text = text.replace(f'\x00LINK{i}\x00', f'\\href{{{url}}}{{{label}}}')
    return text


def urlize_cell(text):
    """Typeset endpoint paths with line breaks but without PDF hyperlinks."""
    # Table cells use the body font for inline code, matching running text.
    text = text.replace('`', '')
    paths = []

    def stash(m):
        raw = m.group(0)
        # Leave trailing punctuation outside the URL (",", ".", ")", ...)
        trail = ''
        while raw and raw[-1] in ',.;:)':
            trail = raw[-1] + trail
            raw = raw[:-1]
        paths.append(raw)
        return f'\x00URL{len(paths) - 1}\x00' + trail

    text = re.sub(r'/[A-Za-z0-9._~:/?#@!$&\'()*+,;=%-]+', stash, text)
    text = escape_latex_cell(text)
    text = convert_citations(text)
    for i, raw in enumerate(paths):
        text = text.replace(f'\x00URL{i}\x00', '\\nolinkurl{' + raw + '}')
    return text


def render_table(rows, caption=None):
    """Convert markdown table rows to LaTeX tabular."""
    header_cells = [c.strip() for c in rows[0].split('|')[1:-1]]
    ncols = len(header_cells)

    data_rows = []
    for row in rows[2:]:  # skip header + separator
        cells = [c.strip() for c in row.split('|')[1:-1]]
        if len(cells) != ncols:
            raise ValueError(f'Table row has {len(cells)} cells, expected {ncols}: {row}')
        data_rows.append(cells)

    # Column spec: use natural l columns; resizebox will scale to fit
    col_spec = 'l' * ncols

    # Catalog rows are long even when there are fewer than 30 of them.
    # Permit page breaks and repeat their header instead of stranding a heading
    # above a large blank area while an unbreakable table moves to the next page.
    is_catalog = ncols in (3, 4) and header_cells[:2] == ['Check', 'Request']
    use_longtable = is_catalog or len(data_rows) > 30

    # Long cells need a smaller font to fit the column
    max_cell = max((len(c) for row in data_rows for c in row), default=0)
    table_size = '\\footnotesize' if max_cell > 60 else '\\small'

    lines = []
    if use_longtable:
        lines.append('\\begingroup')
        lines.append('\\footnotesize')
        lines.append('\\setlength{\\tabcolsep}{3pt}')
        lines.append('\\setlength{\\LTleft}{0pt}')
        lines.append('\\setlength{\\LTright}{0pt plus 1fill}')
        if caption:
            cap_escaped = escape_latex_text(caption)
            lines.append(f'\\captionof{{table}}{{{cap_escaped}}}')
        if is_catalog:
            fractions = [0.19, 0.34, 0.47] if ncols == 3 else [0.16, 0.29, 0.35, 0.20]
        elif ncols == 5 and header_cells[0] == 'Check':
            fractions = [0.44, 0.14, 0.14, 0.14, 0.14]
        else:
            fractions = [1 / ncols] * ncols
        col_spec = ''.join(
            '>{\\raggedright\\arraybackslash}p{\\dimexpr'
            + f'{fraction:.4f}\\columnwidth-2\\tabcolsep\\relax}}'
            for fraction in fractions
        )
        lines.append('\\begin{longtable}{' + col_spec + '}')
    else:
        lines.append('\\begin{table}[H]')
        lines.append('\\centering')
        lines.append(table_size)
        lines.append('\\setlength{\\tabcolsep}{3pt}')
        lines.append('\\sloppy')
        if caption:
            cap_escaped = escape_latex_text(caption)
            lines.append(f'\\caption{{{cap_escaped}}}')
    # Longtables manage their own width; other tables use wrapping columns.
    if not use_longtable:
        if ncols >= 3:
            ragged_x = '>{\\raggedright\\arraybackslash}X'
            if ncols == 3:
                if header_cells[0] == 'Category':
                    col_spec = ('>{\\raggedright\\arraybackslash}p{3.2cm}'
                                '>{\\raggedright\\arraybackslash}p{8.0cm}'
                                '>{\\raggedleft\\arraybackslash}X')
                else:
                    first_width = {'Check': '6.2cm', 'Rank range': '4.1cm',
                                   'Checks passing together': '4.1cm', 'Readiness area': '3.0cm'}.get(header_cells[0], '2.0cm')
                    col_spec = '>{\\raggedright\\arraybackslash}p{' + first_width + '}' + ragged_x * 2
            elif ncols == 4:
                first_width = {'Measure': '3.0cm', 'Check': '4.0cm', 'Rank group': '3.2cm'}.get(header_cells[0], '1.65cm')
                col_spec = '>{\\raggedright\\arraybackslash}p{' + first_width + '}' + ragged_x * 3
            else:
                col_spec = ragged_x * ncols
            lines.append('\\begin{tabularx}{\\columnwidth}{' + col_spec + '}')
        else:
            ragged_x = '>{\\raggedright\\arraybackslash}X'
            lines.append('\\begin{tabularx}{\\columnwidth}{' + ragged_x * ncols + '}')
    lines.append('\\toprule')

    # Header row
    h_cells = [f'\\textbf{{{urlize_cell(c)}}}' for c in header_cells]
    lines.append(' & '.join(h_cells) + ' \\\\')
    lines.append('\\midrule')
    if use_longtable:
        lines.append('\\endhead')

    # Data rows (paths break via \url, [N] stays a real cite)
    for cells in data_rows:
        d_cells = [urlize_cell(c) for c in cells]
        lines.append(' & '.join(d_cells) + ' \\\\')

    lines.append('\\bottomrule')
    if use_longtable:
        lines.append('\\end{longtable}')
        lines.append('\\endgroup')
    else:
        lines.append('\\end{tabularx}')
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
    in_appendix = False

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

        # Horizontal rule: skip (section spacing is automatic)
        if line.strip() == '---':
            flush_para()
            output_blocks.append('')
            i += 1
            continue

        # Fenced code block -> verbatim
        if line.strip() == '$$':
            flush_para()
            if in_table:
                in_table = False
                output_blocks.append(render_table(table_rows, table_caption))
                table_rows = []
                table_caption = None
            i += 1
            math_lines = []
            while i < len(lines) and lines[i].strip() != '$$':
                math_lines.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError('Unclosed display-math block')
            # Keep the display attached to its introducing paragraph so TeX's
            # normal pre-display penalty prevents an orphan equation next page.
            while output_blocks and not output_blocks[-1]:
                output_blocks.pop()
            output_blocks.append('\\[\n' + '\n'.join(math_lines) + '\n\\]')
            i += 1
            continue

        if line.strip() == '```':
            flush_para()
            if in_table:
                in_table = False
                output_blocks.append(render_table(table_rows, table_caption))
                table_caption = None
                table_rows = []
            i += 1
            code_lines = []
            while i < len(lines) and lines[i].strip() != '```':
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            output_blocks.append('\\begin{verbatim}\n' + '\n'.join(code_lines) + '\n\\end{verbatim}')
            continue

        # Section headings (appendix stays unnumbered)
        if line.startswith('## '):
            flush_para()
            title = line[3:].strip()
            title = re.sub(r'^\d+(?:\.\d+)*\.?\s+', '', title)
            title = escape_latex_text(title)
            in_appendix = title.lower().startswith('appendix')
            if in_appendix or title == 'Data and Code':
                output_blocks.append(f'\\section*{{{title}}}')
            else:
                output_blocks.append(f'\\section{{{title}}}')
            i += 1
            continue

        if line.startswith('### '):
            flush_para()
            title = line[4:].strip()
            title = re.sub(r'^\d+(?:\.\d+)*\.?\s+', '', title)
            title = escape_latex_text(title)
            command = '\\subsection*' if in_appendix else '\\subsection'
            output_blocks.append(f'{command}{{{title}}}')
            i += 1
            continue

        if line.startswith('#### '):
            flush_para()
            title = line[5:].strip()
            title = re.sub(r'^\d+(?:\.\d+)*\.?\s+', '', title)
            title = escape_latex_text(title)
            command = '\\subsubsection*' if in_appendix else '\\subsubsection'
            output_blocks.append(f'{command}{{{title}}}')
            i += 1
            continue

        # Markdown image -> figure with PNG/JPG asset
        img_match = re.match(r'!\[(.*?)\]\((.*?)\)\s*$', line.strip())
        if img_match:
            flush_para()
            if in_table:
                in_table = False
                output_blocks.append(render_table(table_rows, table_caption))
                table_caption = None
                table_rows = []
            cap, asset = img_match.group(1).strip(), img_match.group(2).strip()
            cap = escape_latex_text(cap)
            # Strip leading "Figure N. " from caption (LaTeX numbers it)
            cap = re.sub(r'^Figure \d+\.\s*', '', cap)
            output_blocks.append(
                '\\begin{figure}[htbp]\n\\centering\n'
                '\\includegraphics[width=0.95\\columnwidth]{' + asset + '}\n'
                '\\caption{' + cap + '}\n\\end{figure}'
            )
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
    # Entries may be separated by blank lines or single newlines
    entries = re.split(r'\n\s*\n|\n(?=\d+\.\s)', refs_text.strip())
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
            # Convert markdown links [display](url) to \href{}{}
            def clean_md_link(m):
                display, url = m.group(1), m.group(2)
                show = re.sub(r'^https?://(www\.)?', '', display).rstrip('/')
                return f'\\href{{{url}}}{{\\nolinkurl{{{show}}}}}'
            text = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', clean_md_link, text)
            # Convert any remaining bare URLs to \href{}.
            # Skip URLs already inside \href{...} from the pass above.
            def clean_url(m):
                url = m.group(1)
                raw_url = url.replace('\\_', '_')
                display = re.sub(r'^https?://(www\.)?', '', url).rstrip('/')
                return f'\\href{{{raw_url}}}{{\\nolinkurl{{{display}}}}}'
            text = re.sub(r'(?<!\{)(https?://[^\s\}]+)', clean_url, text)
            bib_items.append(f'\\bibitem{{ref{num}}}\n{text}\n')

    return '\\small\n\\begin{thebibliography}{65}\n\\raggedright\n\n' + '\n'.join(bib_items) + '\n\\end{thebibliography}'


# ═══════════════════════════════════════════════
# PROCESS
# ═══════════════════════════════════════════════
abstract_tex = process_paragraph(abstract)

body_tex = md_to_latex(body)

bib_tex = build_bibliography(refs_text)

keywords_tex = ''
if keywords:
    keywords_tex = '\n\n\\par\\medskip\n\\noindent{\\small \\textit{Keywords:} ' + escape_latex_text(keywords) + '}\n'

template = r"""\documentclass{article}
\usepackage{iclr2024_conference,times}

\usepackage[T1]{fontenc}
\usepackage{textcomp}
\usepackage[hyphens]{url}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{url}
\urlstyle{same}
\usepackage{booktabs}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{float}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{caption}
\captionsetup[table]{skip=6pt}

\iclrfinalcopy
\setcitestyle{numbers,square}
\hyphenpenalty=5000
\tolerance=1000
\emergencystretch=2em
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\definecolor{ReferenceBlue}{HTML}{0645AD}
\hypersetup{
  pdftitle={MANUSCRIPT_TITLE},
  pdfauthor={Vedang Ratan Vatsa},
  pdfsubject={Public-web measurement and recorded readiness signals},
  pdflang={en-US},
  pdfdisplaydoctitle=true,
  colorlinks=true,
  urlcolor=ReferenceBlue,
  citecolor=black,
  linkcolor=black
}

\title{MANUSCRIPT_TITLE}

\author{Vedang Ratan Vatsa \\
\href{https://veda.ng}{veda.ng}}

\begin{document}
\raggedbottom

\maketitle

\begin{abstract}
""" + abstract_tex + keywords_tex + r"""
\end{abstract}

""" + body_tex + r"""

""" + bib_tex + r"""

\end{document}
"""

# Remove any \lhead that my earlier fix might have left
template = template.replace('\\lhead{Preprint. Under review.}\n', '')
template = template.replace('MANUSCRIPT_TITLE', escape_latex_text(title_match.group(1)))

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
