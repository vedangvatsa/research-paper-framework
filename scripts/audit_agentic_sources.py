#!/usr/bin/env python3
"""Archive the preceding revision and collect dated source records for inspection."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/agentic_commerce_paper.md'
WORK = ROOT / 'papers/agentic-commerce'
SNAPSHOT = WORK / 'sources/checked-2026-10-12'
FRAMEWORK_COMMIT = '4681f29ae80006ca659e9f706c7148e98f537122'


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'li', 'tr', 'section', 'br'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'li', 'tr', 'section'):
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    def text(self):
        return '\n'.join(line.strip() for line in ''.join(self.parts).splitlines() if line.strip()) + '\n'


def collect(item):
    key, url = item
    result = subprocess.run(
        ['curl', '-sL', '--max-time', '150' if key.startswith('paper-') else '50', '-w', '\nAUDIT_STATUS:%{http_code}\n%{url_effective}\n%{content_type}', url],
        capture_output=True,
    )
    body, marker, info = result.stdout.rpartition(b'\nAUDIT_STATUS:')
    fields = info.decode(errors='replace').splitlines() if marker else []
    status = int(fields[0]) if fields and fields[0].isdigit() else 0
    record = {'id': key, 'url': url, 'http_status': status, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
    if result.returncode or status != 200 or not body:
        record['access'] = 'unavailable through curl; requires a separate content check'
        record['error'] = result.stderr.decode(errors='replace').strip() or f'curl exit code {result.returncode}'
        if status == 200 and not body:
            record['error'] = 'HTTP 200 with an empty body; not accepted as retrieved evidence'
        return record
    record.update(final_url=fields[1], content_type=fields[2] if len(fields) > 2 else '')
    if body.startswith(b'%PDF'):
        extension = '.pdf'
    elif b'<html' in body[:2000].lower() or b'<!doctype' in body[:2000].lower():
        extension = '.html'
    else:
        extension = '.txt'
    target = SNAPSHOT / f'{key}{extension}'
    target.write_bytes(body)
    record.update(file=str(target.relative_to(WORK)), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
    if extension == '.html':
        parser = Text()
        parser.feed(body.decode(errors='replace'))
        target.with_suffix('.txt').write_text(parser.text())
    elif extension == '.pdf':
        subprocess.run(['pdftotext', '-layout', str(target), str(target.with_suffix('.txt'))], check=True)
    return record


def main():
    WORK.mkdir(exist_ok=True)
    if '--archive' in sys.argv:
        archive = ROOT / 'papers/agentic-commerce-archive/before-framework-audit'
        archive.mkdir(parents=True, exist_ok=True)
        for source in list(PAPER.parent.glob('agentic_commerce_paper*')) + [
            ROOT / 'scripts/build_agentic_commerce.mjs',
            ROOT / 'scripts/verify_agentic_commerce.py',
            ROOT / 'scripts/package_agentic_commerce.mjs',
        ]:
            if source.is_file() and not (archive / source.name).exists():
                shutil.copy2(source, archive / source.name)
        print(f'Preserved preceding revision: {archive}')
    if '--collect' in sys.argv:
        SNAPSHOT.mkdir(parents=True, exist_ok=True)
        references = PAPER.read_text().split('## References\n')[1]
        items = [(f'ref-{int(number):02}', url) for number, url in re.findall(r'^(\d+)\..*?\]\((https://[^)]+)\)', references, re.M)]
        items += [(f'paper-{identifier}', f'https://arxiv.org/pdf/{identifier}') for identifier in ('2508.02630v3', '2606.17698v3', '2609.28372v1')]
        with ThreadPoolExecutor(max_workers=4) as executor:
            records = list(executor.map(collect, items))
        (SNAPSHOT / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        for record in records:
            print(record['id'], record['http_status'], record.get('bytes', 0), record['url'])
    if '--framework' in sys.argv:
        folder = WORK / 'framework-reference'
        folder.mkdir(exist_ok=True)
        for remote in ('README.md', 'PAPER_FRAMEWORK.md', 'AI_INSTRUCTIONS.md', 'templates/review_paper.md', 'papers/agent-infrastructure-stack/build_tex.py', 'papers/agent-infrastructure-stack/iclr2024_conference.sty'):
            data = subprocess.check_output(['gh', 'api', f'repos/vedangvatsa/research-paper-framework/contents/{remote}?ref={FRAMEWORK_COMMIT}', '-H', 'Accept: application/vnd.github.raw+json'])
            (folder / Path(remote).name).write_bytes(data)
            if remote.endswith('.sty'):
                (WORK / 'iclr2024_conference.sty').write_bytes(data)
        (folder / 'COMMIT.txt').write_text(f'{FRAMEWORK_COMMIT}\n')
        print(f'Saved framework snapshot {FRAMEWORK_COMMIT}')
    if '--retry-aces' in sys.argv:
        result = collect(('paper-2508.02630v3', 'https://arxiv.org/pdf/2508.02630v3?download=1'))
        target = SNAPSHOT / 'manifest.json'
        records = json.loads(target.read_text())
        records = [result if record['id'] == result['id'] else record for record in records]
        target.write_text(json.dumps(records, indent=2) + '\n')
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
