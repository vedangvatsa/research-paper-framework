#!/usr/bin/env python3
"""Build this review using the framework's formal ICLR-style LaTeX pipeline."""

from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'agentic_commerce_paper.md'
FRAMEWORK = '4681f29ae80006ca659e9f706c7148e98f537122'


def escape(text):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(replacements.get(char, char) for char in text)


def inline(text):
    tokens = re.split(r'(\[[^\]]+\]\(https://[^)]+\)|\[\d+(?:,\s*\d+)*\]|\*\*[^*]+\*\*|(?<!\*)\*[^*]+\*(?!\*))', text)
    result = []
    for token in tokens:
        link = re.fullmatch(r'\[([^\]]+)\]\((https://[^)]+)\)', token)
        citation = re.fullmatch(r'\[(\d+(?:,\s*\d+)*)\]', token)
        if link:
            label, url = link.groups()
            result.append(r'\href{' + url.replace('%', r'\%').replace('#', r'\#') + '}{' + escape(label) + '}')
        elif citation:
            result.append(r'\cite{' + ','.join('ref' + number for number in re.findall(r'\d+', citation[1])) + '}')
        elif token.startswith('**') and token.endswith('**'):
            result.append(r'\textbf{' + escape(token[2:-2]) + '}')
        elif token.startswith('*') and token.endswith('*'):
            result.append(r'\textit{' + escape(token[1:-1]) + '}')
        else:
            result.append(re.sub(r'"([^"]+)"', r"``\1''", escape(token)))
    return ''.join(result)


def table(block, caption):
    rows = [[cell.strip() for cell in line.strip().strip('|').split('|')] for line in block.splitlines()]
    columns = len(rows[0])
    assert columns == 3 and all(len(row) == columns for row in rows)
    parts = [r'\begin{table}[H]', r'\centering', r'\caption{' + inline(caption) + '}', r'\footnotesize',
             r'\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X@{}}', r'\toprule']
    parts.append(' & '.join(r'\textbf{' + inline(cell) + '}' for cell in rows[0]) + r' \\')
    parts.append(r'\midrule')
    for row in rows[2:]:
        parts.append(' & '.join(inline(cell) for cell in row) + r' \\[3pt]')
    parts.extend([r'\bottomrule', r'\end{tabularx}', r'\end{table}'])
    return '\n'.join(parts)


def body_tex(body):
    output, caption = [], None
    for block in re.split(r'\n\s*\n', body.strip()):
        if block == '---':
            continue
        if block.startswith('### '):
            output.append(r'\subsection{' + inline(re.sub(r'^### \d+\.\d+\s+', '', block)) + '}')
        elif block.startswith('## '):
            output.append(r'\section{' + inline(re.sub(r'^## \d+\.\s+', '', block)) + '}')
        elif block.startswith('**Table '):
            caption = re.sub(r'^\*\*Table \d+\.\s*|\*\*$', '', block)
        elif block.startswith('|'):
            assert caption, 'Missing table caption'
            output.append(table(block, caption))
            caption = None
        elif block.startswith('- '):
            output.append('\n'.join([r'\begin{itemize}'] + [r'\item ' + inline(line[2:]) for line in block.splitlines()] + [r'\end{itemize}']))
        else:
            output.append(inline(block))
    assert caption is None
    return '\n\n'.join(output)


def main():
    markdown = SOURCE.read_text()
    title = markdown.splitlines()[0][2:]
    author_entries = re.findall(r'<div class="author-entry">\s*(.*?)\s*</div>', markdown, re.S)
    assert author_entries, 'Missing author entries'
    author_names = [re.search(r'\*\*([^*]+)\*\*', entry)[1] for entry in author_entries]
    authors = r' \And '.join(
        r' \\ '.join(inline(row.strip()) for row in re.split(r'<br\s*/?>', entry) if row.strip())
        for entry in author_entries
    )
    abstract = re.search(r'## Abstract\s*\n(.*?)\n_\*\*Keywords\*\*_', markdown, re.S)[1].strip()
    keywords = re.search(r'_\*\*Keywords\*\*_: (.+)', markdown)[1]
    body, refs = markdown[markdown.index('## 1. Introduction'):].split('## References', 1)
    entries = re.findall(r'^(\d+)\. (.+)$', refs, re.M)
    bibliography = '\n\n'.join(r'\bibitem{ref' + number + '}\n' + inline(text) for number, text in entries)
    preamble = r'''\documentclass{article}
\usepackage{iclr2024_conference,times}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{float}
\usepackage{caption}
\captionsetup[table]{skip=6pt}
\iclrfinalcopy
\setcitestyle{numbers,square,comma}
\renewcommand{\headrulewidth}{0pt}
\hyphenpenalty=5000
\tolerance=1000
\emergencystretch=2em
\definecolor{ReferenceBlue}{HTML}{0645AD}
\hypersetup{colorlinks=true,urlcolor=ReferenceBlue,citecolor=black,linkcolor=black}
'''
    tex = preamble + '\n' + r'\hypersetup{pdftitle={' + escape(title) + '},pdfauthor={' + escape(', '.join(author_names)) + '}}\n'
    tex += r'\title{' + escape(title) + '}\n' + r'\author{' + authors + '}' + r'''
\begin{document}
\raggedbottom
\maketitle
\begin{abstract}
''' + inline(abstract) + r'''
\end{abstract}
\noindent\textit{\textbf{Keywords}: ''' + escape(keywords) + '}\n\n' + body_tex(body) + r'''
\clearpage
\begingroup
\small
\begin{thebibliography}{99}
\raggedright
''' + bibliography + r'''
\end{thebibliography}
\endgroup
\end{document}
'''
    (HERE / 'template.tex').write_text(tex)
    print(f'Built template.tex using framework {FRAMEWORK}; {len(entries)} bibliography entries')
    if '--compile' in sys.argv:
        subprocess.run(['tectonic', '--keep-logs', 'template.tex'], cwd=HERE, check=True)


if __name__ == '__main__':
    main()
