import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const parent = path.join(os.homedir(), 'Downloads', 'Paper to publish');
const destination = path.join(parent, 'Agentic Commerce');
const revision = '2026-10-13';
const validationPath = `reports/agentic_commerce_validation_${revision}.json`;
if (!fs.existsSync(parent)) throw new Error(`Missing publication directory: ${parent}`);
const updating = fs.existsSync(destination);
if (updating && !process.argv.includes('--update')) throw new Error(`Preserving existing folder: ${destination}. Use --update for a checked update.`);
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
let previousMainHash;
const managed = new Set();
if (updating) {
  const previous = JSON.parse(fs.readFileSync(path.join(destination, 'MANIFEST.json'), 'utf8'));
  previousMainHash = previous.files.find(file => file.path === 'papers/agentic_commerce_paper.pdf')?.sha256;
  if (!/^[a-f0-9]{64}$/.test(previousMainHash ?? '')) throw new Error('Previous manifest has no valid main-PDF hash');
  for (const file of previous.files) {
    managed.add(file.path);
    const target = path.resolve(destination, file.path);
    if (!target.startsWith(destination + path.sep)) throw new Error(`Invalid managed path: ${file.path}`);
    if (hash(fs.readFileSync(target)) !== file.sha256) throw new Error(`Preserving locally edited file: ${file.path}`);
  }
  const saved = path.join(destination, 'revisions', `before-${previousMainHash}`);
  for (const name of [...previous.files.map(file => file.path), 'MANIFEST.json']) {
    const target = path.join(saved, name);
    if (!fs.existsSync(target)) {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.copyFileSync(path.join(destination, name), target, fs.constants.COPYFILE_EXCL);
    }
  }
}

const mainSource = path.join(root, 'papers/agentic_commerce_paper.pdf');
const looseMain = path.join(parent, 'agentic_commerce_paper.pdf');
if (fs.existsSync(looseMain)) {
  const existingHash = hash(fs.readFileSync(looseMain));
  if (existingHash !== previousMainHash && existingHash !== hash(fs.readFileSync(mainSource))) {
    throw new Error(`Preserving separately edited publication PDF: ${looseMain}`);
  }
}
fs.copyFileSync(mainSource, looseMain);
execFileSync('python3', [path.join(root, 'scripts/verify_agentic_commerce.py')], { stdio: 'inherit' });

const files = [
  'papers/agentic_commerce_paper.md',
  'papers/agentic_commerce_paper.pdf',
  'papers/agentic_commerce_paper_ieee.pdf',
  'papers/agentic_commerce_paper.html',
  'papers/agentic_commerce_paper_ieee.html',
  'papers/agentic_commerce_paper_protocol.md',
  'papers/agentic_commerce_paper_sources.md',
  'papers/agentic_commerce_paper_review.md',
  'papers/agentic_commerce_fact_check.md',
  'scripts/audit_agentic_sources.py',
  'scripts/expand_agentic_review.py',
  'scripts/build_agentic_commerce.mjs',
  'scripts/verify_agentic_commerce.py',
  'scripts/render_agentic_pages.py',
  'scripts/package_agentic_commerce.mjs',
  'scripts/quality_check.sh',
  'scripts/verify_references.sh',
  'pdf-style.css',
  'pdf-style-ieee.css',
  'reports/agentic_commerce_validation_2026-10-12.json',
  validationPath,
  'reports/agentic-commerce-first-page.png',
  'reports/agentic-commerce-protocol-table.png',
  'reports/agentic-commerce-ieee-references.png',
  'reports/agentic-commerce-main-references.png',
  'reports/agentic-commerce-study-comparison.png',
  'reports/agentic-commerce-security-table.png',
  'reports/agentic-commerce-conclusion.png',
];
function includeFolder(relative) {
  for (const entry of fs.readdirSync(path.join(root, relative), { withFileTypes: true })) {
    if (entry.name.startsWith('.') || entry.name === '__pycache__') continue;
    if (entry.isDirectory()) includeFolder(`${relative}/${entry.name}`);
    else if (entry.isFile()) files.push(`${relative}/${entry.name}`);
  }
}
includeFolder('papers/agentic-commerce-archive');
includeFolder('papers/agentic-commerce');
for (const relative of files) {
  if (!fs.statSync(path.join(root, relative)).isFile()) throw new Error(`Missing file: ${relative}`);
  const target = path.join(destination, relative);
  if (updating && fs.existsSync(target) && !managed.has(relative)
    && hash(fs.readFileSync(target)) !== hash(fs.readFileSync(path.join(root, relative)))) {
    throw new Error(`Preserving untracked publication file: ${relative}`);
  }
}
fs.mkdirSync(destination, { recursive: true });
const manifest = [];
function record(relative) {
  const data = fs.readFileSync(path.join(destination, relative));
  manifest.push({ path: relative, bytes: data.length, sha256: hash(data) });
}
for (const relative of files) {
  const source = path.join(root, relative);
  const target = path.join(destination, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(source, target);
  if (hash(fs.readFileSync(source)) !== hash(fs.readFileSync(target))) throw new Error(`Copy mismatch: ${relative}`);
  record(relative);
}

const dependency = JSON.parse(fs.readFileSync(path.join(root, 'node_modules/playwright/package.json'), 'utf8')).version;
const validation = JSON.parse(fs.readFileSync(path.join(root, validationPath), 'utf8'));
const mainPages = validation.pdfs.find(file => file.file === 'papers/agentic_commerce_paper.pdf').pages;
const alternatePages = validation.pdfs.find(file => file.file === 'papers/agentic_commerce_paper_ieee.pdf').pages;
const paperTitle = fs.readFileSync(path.join(root, 'papers/agentic_commerce_paper.md'), 'utf8').split('\n')[0].replace(/^# /, '');
fs.writeFileSync(path.join(destination, 'package.json'), `${JSON.stringify({
  name: 'agentic-commerce-paper', version: revision.replaceAll('-', '.'), private: true,
  description: 'Sources and reproducible document build for the agentic commerce review.',
  scripts: {
    build: 'node scripts/build_agentic_commerce.mjs --local-only',
    verify: 'python3 scripts/verify_agentic_commerce.py --local-only',
  },
  devDependencies: { playwright: dependency },
}, null, 2)}\n`);
record('package.json');

fs.writeFileSync(path.join(destination, 'README.md'), `# Agentic Commerce

## Start here

- [Main paper, framework ICLR-style PDF](papers/agentic_commerce_paper.pdf) - ${mainPages} pages.
- [Alternate IEEE-style PDF](papers/agentic_commerce_paper_ieee.pdf) - ${alternatePages} pages.
- [Editable manuscript](papers/agentic_commerce_paper.md).
- [Browser-readable version](papers/agentic_commerce_paper.html).

**Title:** ${paperTitle}.

Authors: ${validation.authors.join(', ')}. Website: [veda.ng](https://veda.ng). Revised October 13, 2026.

The review uses plain language, ${validation.tables} tables, and ${validation.references} linked references, including ${validation.research_works} research works. Its audit covers ${validation.audited_units} prose blocks and table rows. It contains no complex mathematics. Human experiments, agent tests, field-data analysis, theory, reviews, legal scholarship, vendor surveys, and product announcements are distinguished. Fifteen research works does not mean fifteen independent experiments.

## Included material

- \`papers/\`: manuscript, both PDFs, both standalone HTML layouts, research protocol, source ledger, and quality review.
- \`papers/agentic_commerce_fact_check.md\`: full paragraph/table-row audit and corrections.
- \`papers/agentic-commerce/\`: LaTeX builder, template, ICLR style file, compiled PDF/log, pinned framework reference, and dated source records.
- \`papers/agentic-commerce/literature-expansion/\`: study comparison matrix, selection record, twelve added full-text sources, discovery metadata, searches, and retrieval hashes/errors.
- \`papers/agentic-commerce-archive/before-2026-10-12/\`: superseded manuscript, PDFs, HTML, original chart script and images, and the original publication-folder PDF. These old charts contain unsupported claims and are retained only for provenance.
- \`papers/agentic-commerce-archive/before-academic-expansion/\`: preceding manuscript, PDFs, audit, and supporting records.
- \`scripts/\`: build, verification, packaging, language-check, and reference-link-check tools.
- \`reports/\`: artifact validation, hashes, and images used to inspect the final layout.
- Stylesheets and a minimal, pinned Playwright dependency manifest for the document build.
- \`MANIFEST.json\`: file sizes and SHA-256 hashes for the packaged files.

The source log and fact-check record explain the evidence. Accessible source documents are saved for the audit; notes identify alternate checks for curl-blocked pages. No original experimental dataset is claimed. The review report records unavailable API-based checks and the limits of AI-assisted review. Earlier delivered-folder snapshots are preserved under \`revisions/\`, including \`before-academic-expansion/\`.

## Paper format

The main PDF uses the formal pipeline in the requested repository, pinned at commit \`4681f29ae80006ca659e9f706c7148e98f537122\`: Markdown to LaTeX, the ICLR style with Times, and Tectonic. References are numbered and left-aligned on a new page. HTML is a reading copy; it is not the source of the main PDF. The IEEE-style PDF is an alternate layout.

## Rebuild

Requirements: Node.js, Python 3, Tectonic, Pandoc, Poppler (pdfinfo and pdftotext), and Chromium through Playwright.

Run from this folder:

~~~sh
npm install
npx playwright install chromium
npm run build
npm run verify
~~~

The build uses local styles and does not request remote fonts. The package commands use \`--local-only\`, so rebuilding updates files inside this folder. An existing Chromium can be selected with the \`CHROMIUM_EXECUTABLE\` environment variable. Exact PDF bytes may differ with fonts or browser versions; content, links, and margins are checked separately.

To build only the formal paper:

~~~sh
python3 papers/agentic-commerce/build_tex.py --compile
~~~

That command produces \`papers/agentic-commerce/template.pdf\`. The full build also updates the named main PDF and reading copies.

For references and style:

~~~sh
bash scripts/verify_references.sh papers/agentic_commerce_paper.md
bash scripts/quality_check.sh papers/agentic_commerce_paper.md
~~~

See the review report for permitted bibliography-style flags and source-access details. The last link check returned 28 HTTP 200 and twelve HTTP 403 responses. The specific blocked sources were inspected through alternate routes, not validated by the status code.
`);
record('README.md');
fs.writeFileSync(path.join(destination, 'MANIFEST.json'), `${JSON.stringify({
  created: new Date().toISOString(), paper_revision: revision, files: manifest,
}, null, 2)}\n`);
console.log(JSON.stringify({ folder: destination, files: manifest.length + 1, bytes: manifest.reduce((total, item) => total + item.bytes, 0), copied_files_verified: files.length }, null, 2));
