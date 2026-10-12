#!/usr/bin/env python3
"""Check manuscript structure and rendered artifacts, not scientific validity."""

from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/agentic_commerce_paper.md'
REVISION = '2026-10-13'


def run(*args):
    return subprocess.check_output(args, text=True)


def words(text):
    return re.findall(r'[a-z0-9]+', unicodedata.normalize('NFKC', text).lower())


def restore_line_hyphenation(text, expected):
    missing = expected - Counter(words(text))
    restored = []

    def join_if_expected(match):
        joined = match[1] + match[2]
        tokens = words(joined)
        if len(tokens) == 1 and missing[tokens[0]] > 0:
            missing[tokens[0]] -= 1
            restored.append(tokens[0])
            return joined
        return match[0]

    # Only join line-end splits needed to recover an expected source word.
    # Original compounds such as "AI-assisted" keep their separate tokens.
    text = re.sub(r'([^\W\d_]+)-[ \t]*\n[ \t]*([^\W\d_]+)', join_if_expected, text)
    return text, restored


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manuscript_units(body):
    units = []
    for block in re.split(r'\n\s*\n', body.split('## Abstract\n', 1)[1]):
        if not block.strip() or block.startswith(('#', '---', '_**Keywords', '**Table')):
            continue
        units.extend(block.splitlines()[2:] if block.startswith('|') else [block])
    return units


class BoundingBoxes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pages = []
        self.word = None

    def handle_starttag(self, tag, attrs):
        if tag == 'page':
            self.pages.append({**dict(attrs), 'words': []})
        elif tag == 'word':
            self.word = {**dict(attrs), 'text': ''}

    def handle_data(self, data):
        if self.word is not None:
            self.word['text'] += data

    def handle_endtag(self, tag):
        if tag == 'word':
            self.pages[-1]['words'].append(self.word)
            self.word = None


def main():
    source = PAPER.read_text()
    author_block = source.split('## Abstract', 1)[0]
    author_names = re.findall(r'\*\*([^*]+)\*\*', author_block)
    author_urls = set(re.findall(r'\]\((https://[^)]+)\)', author_block))
    body, references = source.split('## References\n', 1)
    entries = re.findall(r'^(\d+)\. (.+)$', references, re.M)
    reference_ids = {int(number) for number, _ in entries}
    assert [int(number) for number, _ in entries] == list(range(1, len(entries) + 1))
    citations = {int(number) for group in re.findall(r'\[(\d+(?:,\s*\d+)*)\]', body) for number in re.findall(r'\d+', group)}
    assert citations == reference_ids, {'missing_or_unused_references': sorted(citations ^ reference_ids)}
    urls = set(re.findall(r'\]\((https://[^)]+)\)', references))
    assert len(urls) == len(entries), 'Each reference needs its own linked source'
    assert all(re.search(r'\]\(https://[^)]+\)', entry) for _, entry in entries)
    sections = re.findall(r'^## (\d+)\.', body, re.M)
    assert list(map(int, sections)) == list(range(1, len(sections) + 1))
    captions = re.findall(r'^\*\*Table (\d+)\.', body, re.M)
    assert list(map(int, captions)) == list(range(1, len(captions) + 1))
    assert all(len(re.findall(r'\bTable ' + number + r'\b', body)) >= 2 for number in captions)
    assert not re.search(r'[\u2013\u2014]|\\(?:frac|begin|sum)|\$\$', body)
    assert not re.search(r'!\[', body), 'Old unverified charts must not be embedded'
    abstract = body.split('## Abstract\n', 1)[1].split('_**Keywords**_', 1)[0]
    assert len(abstract.split()) <= 250
    units = manuscript_units(body)
    if '--list-units' in sys.argv:
        for index, unit in enumerate(units, 1):
            print(f'U{index:02d}: {unit}\n')
        return

    plain = run('pandoc', str(PAPER), '--to=plain')
    expected = Counter(words(plain))
    without_headings = re.sub(r'^#{1,3} .+$', '', source, flags=re.M)
    prose = subprocess.check_output(['pandoc', '--from=markdown', '--to=plain'], input=without_headings, text=True)
    expected_prose = Counter(words(prose))
    audit = (PAPER.parent / 'agentic_commerce_fact_check.md').read_text()
    assert f'Reviewed manuscript SHA-256: `{digest(PAPER)}`' in audit, 'Fact-check record belongs to a different manuscript revision'
    audited = re.findall(r'^\| U(\d+) \|', audit, re.M)
    assert list(map(int, audited)) == list(range(1, len(units) + 1)), 'Fact-check coverage does not match the manuscript'
    banned = r'\b(?:shift|implications|significant|striking|fundamental|simultaneously|synthesize|noteworthy|consequently|thus|hence|thereby|highlight|emerged|emerging|encompass|streamline|reshape|redefine|reimagine|reconfigure|delve|tapestry|testament|multifaceted|pivotal|seamless|synergy|democratize|empower|notably|furthermore|moreover|landscape|paradigm|unprecedented|leverage|foster|facilitate|holistic|transformative|spearhead|bolster|underscore|underscores|unlock|realm|catalyst|revolutionize|embark|beacon|navigating)\b'
    assert not re.search(banned, body, re.I), 'Unwanted wording in manuscript prose'
    tex = (PAPER.parent / 'agentic-commerce/template.tex').read_text()
    log = (PAPER.parent / 'agentic-commerce/template.log').read_text()
    assert r'\usepackage{iclr2024_conference,times}' in tex and r'\iclrfinalcopy' in tex
    assert r'\usepackage{microtype}' in tex and r'\raggedbottom' in tex
    assert r'\clearpage' in tex and r'\raggedright' in tex
    assert r'\definecolor{ReferenceBlue}{HTML}{0645AD}' in tex
    assert 'urlcolor=ReferenceBlue' in tex
    assert not re.search(r'Overfull \\[hv]box|undefined references|Citation .+ undefined', log)
    style = PAPER.parent / 'agentic-commerce/iclr2024_conference.sty'
    reference_style = style.parent / 'framework-reference/iclr2024_conference.sty'
    assert digest(style) == digest(reference_style), 'Framework style differs from pinned source'
    literature = PAPER.parent / 'agentic-commerce/literature-expansion'
    selection = json.loads((literature / 'selection.json').read_text())
    research_ids = selection['existing_research_references'] + [item['reference'] for item in selection['added_research']]
    assert len(research_ids) == len(set(research_ids)) and set(research_ids) <= reference_ids
    for item in selection['added_research']:
        retrieval = json.loads((literature / f"{item['source']}-retrieval.json").read_text())
        assert digest(literature / retrieval['file']) == retrieval['sha256'], f"Source snapshot changed: {item['source']}"
    report = {
        'scope': 'Structure, citation mapping, PDF text, links, margins, and copy consistency; not a validation of scientific claims.',
        'paper_revision': REVISION,
        'source_sha256': digest(PAPER),
        'authors': author_names,
        'author_links': sorted(author_urls),
        'references': len(entries),
        'research_works': len(research_ids),
        'added_research_snapshots_verified': len(selection['added_research']),
        'numbered_sections': len(sections),
        'tables': len(captions),
        'abstract_words': len(abstract.split()),
        'plain_text_words': len(plain.split()),
        'audited_units': len(units),
        'framework_commit': '4681f29ae80006ca659e9f706c7148e98f537122',
        'main_format': 'ICLR-style LaTeX and Tectonic',
        'latex_overfull_boxes_or_undefined_references': False,
        'banned_body_word_hits': 0,
        'pdfs': [],
    }
    for suffix, horizontal_margin in [('', 108), ('_ieee', 54)]:
        pdf = PAPER.with_name(f'{PAPER.stem}{suffix}.pdf')
        extracted = run('pdftotext', '-layout', str(pdf), '-')
        reference_words = expected if suffix else expected_prose
        extracted, restored = restore_line_hyphenation(extracted, reference_words)
        actual = Counter(words(extracted))
        missing = reference_words - actual
        coverage = 1 - sum(missing.values()) / sum(reference_words.values())
        assert not missing, {'file': str(pdf), 'missing_tokens': dict(missing)}
        if not suffix:
            compact = re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKC', extracted).lower())
            for heading in re.findall(r'^#{1,3} (.+)$', source, re.M):
                text = re.sub(r'^[\d.]+\s+', '', heading)
                assert re.sub(r'[^a-z0-9]', '', text.lower()) in compact, f'Missing native heading: {heading}'
            assert 'AI-Scientist Generated Preprint' not in extracted
        links = run('pdfinfo', '-url', str(pdf))
        assert all(url in links for url in urls), 'PDF lost a reference link'
        assert all(url in links for url in author_urls), 'PDF lost an author link'
        bbox = BoundingBoxes()
        bbox.feed(run('pdftotext', '-bbox', str(pdf), '-'))
        pages = bbox.pages
        assert pages
        outside = []
        for index, page in enumerate(pages, 1):
            width = float(page['width'])
            height = float(page['height'])
            page_words = page['words']
            assert page_words, f'Blank page {index}'
            for word in page_words:
                x0, y0, x1, y1 = (float(word[key]) for key in ('xmin', 'ymin', 'xmax', 'ymax'))
                if not suffix and word['text'] == str(index) and y0 > height - 45 and abs((x0 + x1) / 2 - width / 2) < 10:
                    continue
                bottom_margin = 70 if suffix else 56
                if x0 < horizontal_margin - 2 or x1 > width - horizontal_margin + 2 or y0 < 70 or y1 > height - bottom_margin:
                    outside.append((index, word['text'], x0, y0, x1, y1))
        assert not outside, {'out_of_margin_text': outside[:20]}
        report['pdfs'].append({
            'file': str(pdf.relative_to(ROOT)), 'pages': len(pages),
            'sha256': digest(pdf), 'word_coverage': coverage,
            'hyphenated_line_breaks_restored': restored,
            'missing_tokens': dict(missing), 'all_reference_links_present': True,
            'all_author_links_present': True,
            'text_outside_margins': len(outside),
        })

    if '--local-only' not in sys.argv:
        published = Path.home() / 'Downloads/Paper to publish' / PAPER.with_suffix('.pdf').name
        assert digest(published) == digest(PAPER.with_suffix('.pdf'))
        report['publication_copy_matches'] = True
    target = ROOT / f'reports/agentic_commerce_validation_{REVISION}.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
