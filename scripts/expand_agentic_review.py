#!/usr/bin/env python3
"""Save search and full-text records for the expanded narrative review."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.parse import quote, urlencode

from audit_agentic_sources import Text

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'papers/agentic-commerce/literature-expansion'


def fetch(url, timeout=120):
    result = subprocess.run(['curl', '-sL', '--max-time', str(timeout), '-w', '\nREVIEW_STATUS:%{http_code}', url], capture_output=True)
    body, marker, status = result.stdout.rpartition(b'\nREVIEW_STATUS:')
    if result.returncode or not marker or status != b'200' or not body:
        raise RuntimeError(f'curl={result.returncode}, HTTP={status.decode(errors="replace")}, bytes={len(body)}')
    return body


def metadata(doi):
    url = 'https://api.openalex.org/works/https://doi.org/' + doi
    key = doi.replace('/', '_')
    try:
        raw = fetch(url)
        (OUT / f'metadata-{key}.json').write_bytes(raw)
        data = json.loads(raw)
        return {
            'title': data['title'], 'doi': data['doi'], 'year': data['publication_year'],
            'locations': [{'page': item.get('landing_page_url'), 'pdf': item.get('pdf_url'), 'source': (item.get('source') or {}).get('display_name')} for item in data.get('locations', [])],
        }
    except Exception as error:
        return {'doi': doi, 'error': str(error)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if '--archive' in sys.argv:
        archive_name = 'before-academic-expansion'
        if '--archive-name' in sys.argv:
            archive_name = sys.argv[sys.argv.index('--archive-name') + 1]
            if not archive_name.replace('-', '').replace('_', '').isalnum():
                raise ValueError('Invalid archive name')
        archive = ROOT / 'papers/agentic-commerce-archive' / archive_name
        archive.mkdir(exist_ok=True)
        names = list((ROOT / 'papers').glob('agentic_commerce_*'))
        names += [ROOT / 'scripts' / name for name in ('build_agentic_commerce.mjs', 'verify_agentic_commerce.py', 'package_agentic_commerce.mjs')]
        for source in names:
            if source.is_file() and not (archive / source.name).exists():
                shutil.copy2(source, archive / source.name)
        print(f'Archived preceding revision in {archive}')
    if '--metadata' in sys.argv:
        dois = ['10.1037/xge0000033', '10.1287/mnsc.2016.2643', '10.1016/j.obhdp.2018.12.005', '10.1177/0022243719851788', '10.1177/0022242920957347', '10.1287/mksc.19.1.4.15178', '10.1287/mksc.2017.1072', '10.1287/mnsc.43.12.1676']
        with ThreadPoolExecutor(max_workers=3) as executor:
            result = list(executor.map(metadata, dois))
        (OUT / 'candidate-metadata.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))
    if '--search' in sys.argv:
        queries = ['agentic commerce consumer delegation trust', 'AI shopping agents consumer control experiment', 'algorithmic recommendation agent consumer experiment', 'shopping agent prompt injection']
        for index, query in enumerate(queries, 1):
            url = 'https://api.openalex.org/works?' + urlencode({'search': query, 'per-page': 8, 'select': 'id,doi,title,publication_year,open_access,best_oa_location'})
            try:
                data = json.loads(fetch(url))
                record = {'query': query, 'url': url, 'date': datetime.now(timezone.utc).isoformat(), 'response': data}
                (OUT / f'search-{index}.json').write_text(json.dumps(record, indent=2) + '\n')
                print(query)
                for work in data.get('results', []):
                    print(work['publication_year'], work['title'], work.get('doi'), work.get('open_access', {}).get('oa_url'))
            except Exception as error:
                print(query, str(error))
    if '--source' in sys.argv:
        position = sys.argv.index('--source')
        key, url = sys.argv[position + 1:position + 3]
        if not key.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Invalid source identifier')
        try:
            raw = fetch(url, 180)
            extension = '.pdf' if raw.startswith(b'%PDF') else '.html'
            target = OUT / f'{key}{extension}'
            target.write_bytes(raw)
            if extension == '.pdf':
                subprocess.run(['pdftotext', '-layout', str(target), str(target.with_suffix('.txt'))], check=True)
            else:
                parser = Text()
                parser.feed(raw.decode(errors='replace'))
                target.with_suffix('.txt').write_text(parser.text())
            result = {'id': key, 'url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat(), 'file': target.name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        except Exception as error:
            result = {'id': key, 'url': url, 'error': str(error)}
        (OUT / f'{key}-retrieval.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))
    if '--dspace' in sys.argv:
        position = sys.argv.index('--dspace')
        base, handle, key = sys.argv[position + 1:position + 4]
        item = json.loads(fetch(base + '/server/api/pid/find?' + urlencode({'id': handle})))
        (OUT / f'{key}-repository.json').write_text(json.dumps(item, indent=2) + '\n')
        bundles = json.loads(fetch(item['_links']['bundles']['href']))['_embedded']['bundles']
        original = next(bundle for bundle in bundles if bundle['name'] == 'ORIGINAL')
        streams = json.loads(fetch(original['_links']['bitstreams']['href']))['_embedded']['bitstreams']
        for stream in streams:
            if stream['name'].lower().endswith('.pdf'):
                subprocess.run([sys.executable, __file__, '--source', key, stream['_links']['content']['href']], check=True)
                print(item['name'], stream['name'])
                break
    if '--crossref' in sys.argv:
        doi = sys.argv[sys.argv.index('--crossref') + 1]
        data = json.loads(fetch('https://api.crossref.org/works/' + doi))
        (OUT / ('crossref-' + doi.replace('/', '_') + '.json')).write_text(json.dumps(data, indent=2) + '\n')
        work = data['message']
        print(json.dumps({key: work.get(key) for key in ('title', 'author', 'container-title', 'published', 'published-print', 'published-online', 'volume', 'issue', 'page', 'link', 'relation', 'update-to')}, indent=2))


if __name__ == '__main__':
    main()
