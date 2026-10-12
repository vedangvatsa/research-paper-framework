import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { chromium } from 'playwright';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const papers = path.join(root, 'papers');
const stem = 'agentic_commerce_paper';
const archive = path.join(papers, 'agentic-commerce-archive', 'before-2026-10-12');
const publicationCopy = path.join(os.homedir(), 'Downloads', 'Paper to publish', `${stem}.pdf`);
const desktopCopy = path.join(os.homedir(), 'Desktop', `${stem}.pdf`);

if (process.argv.includes('--archive-only')) {
  fs.mkdirSync(archive, { recursive: true });
  for (const name of [
    `${stem}.md`, `${stem}.html`, `${stem}.pdf`, `${stem}_ieee.pdf`,
    'generate_charts.py', 'adoption_scurve.png', 'consumer_trust.png',
    'selection_bias.png', 'regulatory_comparison.png', 'risk_heatmap.png',
    'market_projections.png', 'demographic_trust.png', 'infrastructure_timeline.png',
  ]) {
    const source = path.join(papers, name);
    const destination = path.join(archive, name);
    if (fs.existsSync(source) && !fs.existsSync(destination)) {
      fs.copyFileSync(source, destination, fs.constants.COPYFILE_EXCL);
    }
  }
  for (const [source, name] of [[publicationCopy, 'publication-folder-original.pdf'], [desktopCopy, 'desktop-original.pdf']]) {
    const destination = path.join(archive, name);
    if (fs.existsSync(source) && !fs.existsSync(destination)) {
      try {
        fs.copyFileSync(source, destination, fs.constants.COPYFILE_EXCL);
      } catch (error) {
        if (source !== desktopCopy || error.code !== 'EPERM') throw error;
        console.warn(`Desktop backup unavailable: ${error.code}. Existing Desktop copy will be preserved.`);
      }
    }
  }
  console.log(`Archived existing paper artifacts in ${archive}`);
  process.exit(0);
}

if (!fs.existsSync(path.join(archive, `${stem}.md`))) {
  throw new Error('Archive the original manuscript with --archive-only before rebuilding.');
}

const markdown = path.join(papers, `${stem}.md`);
execFileSync('python3', [path.join(papers, 'agentic-commerce/build_tex.py'), '--compile'], { stdio: 'inherit' });
fs.copyFileSync(path.join(papers, 'agentic-commerce/template.pdf'), path.join(papers, `${stem}.pdf`));
const body = execFileSync('pandoc', [markdown, '--from=markdown', '--to=html5'], { encoding: 'utf8' });
const manuscript = fs.readFileSync(markdown, 'utf8');
const title = manuscript.split('\n')[0].replace(/^# /, '');
const authors = [...manuscript.split('## Abstract')[0].matchAll(/\*\*([^*]+)\*\*/g)].map(match => match[1]);
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const overrides = `
body { font-family: "Times New Roman", Times, serif; hyphens: none; }
p { orphans: 3; widows: 3; }
table { table-layout: fixed; break-inside: avoid; }
th, td { text-align: left; vertical-align: top; overflow-wrap: anywhere; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
p:has(> strong:only-child) { break-after: avoid; }
ul { break-inside: avoid; }
p:has(+ ul) { break-after: avoid; }
h2#references ~ ol { text-align: left; font-size: 8.5pt; line-height: 1.3; }
h2#references ~ ol li { margin-bottom: 0.65em; overflow-wrap: anywhere; break-inside: avoid; }
h2#references ~ ol p { text-indent: 0; }
h2#references ~ ol a { color: #0645ad; text-decoration: underline; text-underline-offset: 2px; }
.author-info p { text-align: center; text-indent: 0; }
.author-info { display: flex; justify-content: center; align-items: flex-start; gap: 2em; }
.author-entry p { margin: 0; }
.author-entry p > strong:only-child { display: inline; text-transform: none; font-variant: normal; margin: 0; }
.author-entry a { color: #0645ad; text-decoration: underline; }
@media screen { body { padding: 32px; } }
`;
const browser = await chromium.launch({
  headless: true,
  ...(process.env.CHROMIUM_EXECUTABLE ? { executablePath: process.env.CHROMIUM_EXECUTABLE } : {}),
});
try {
  for (const [suffix, cssName] of [['', 'pdf-style.css'], ['_ieee', 'pdf-style-ieee.css']]) {
    const css = fs.readFileSync(path.join(root, cssName), 'utf8').replace(/^@import[^\n]*$/gm, '');
    const htmlPath = path.join(papers, `${stem}${suffix}.html`);
    const pdfPath = path.join(papers, `${stem}${suffix}.pdf`);
    const formatOverrides = suffix ? 'body { line-height: 1.1; column-fill: balance; } h2#references ~ ol { font-size: 8pt; }' : '';
    fs.writeFileSync(htmlPath, `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>${escape(title)}</title><meta name="author" content="${escape(authors.join(', '))}"><style>${css}\n${overrides}\n${formatOverrides}</style></head><body>${body}</body></html>\n`);
    const page = await browser.newPage();
    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'load' });
    await page.emulateMedia({ media: 'print' });
    await page.evaluate(() => document.fonts.ready);
    if (suffix) {
      await page.pdf({ path: pdfPath, printBackground: true, preferCSSPageSize: true, displayHeaderFooter: false, tagged: true, outline: true });
    }
    const counts = await page.evaluate(() => ({
      title: document.querySelector('h1')?.textContent,
      tables: document.querySelectorAll('table').length,
      links: document.querySelectorAll('a[href^="http"]').length,
      authors: [...document.querySelectorAll('.author-entry strong')].map(author => author.textContent),
      authorWebsite: document.querySelector('.author-entry a')?.getAttribute('href'),
      referenceLinks: document.querySelectorAll('h2#references ~ ol a').length,
      blueUnderlinedReferenceLinks: [...document.querySelectorAll('h2#references ~ ol a')].filter(link => {
        const style = getComputedStyle(link);
        return style.color === 'rgb(6, 69, 173)' && style.textDecorationLine.includes('underline');
      }).length,
      missingImages: [...document.images].filter(image => !image.complete || image.naturalWidth === 0).length,
    }));
    if (counts.missingImages) throw new Error(`Missing image in ${htmlPath}`);
    if (JSON.stringify(counts.authors) !== JSON.stringify(authors) || counts.authorWebsite !== 'https://veda.ng') {
      throw new Error(`Author block failed in ${htmlPath}`);
    }
    if (!counts.referenceLinks || counts.referenceLinks !== counts.blueUnderlinedReferenceLinks) {
      throw new Error(`Reference-link styling failed in ${htmlPath}`);
    }
    console.log(JSON.stringify({ file: pdfPath, format: suffix ? 'IEEE-style HTML' : 'Framework ICLR LaTeX', ...counts }));
    await page.close();
  }
} finally {
  await browser.close();
}

for (const destination of process.argv.includes('--local-only') ? [] : [publicationCopy, desktopCopy]) {
  if (!fs.existsSync(path.dirname(destination))) throw new Error(`Missing output directory: ${path.dirname(destination)}`);
  if (destination === desktopCopy && fs.existsSync(destination) && !fs.existsSync(path.join(archive, 'desktop-original.pdf'))) {
    console.warn('Skipped existing Desktop PDF because its backup could not be read.');
    continue;
  }
  fs.copyFileSync(path.join(papers, `${stem}.pdf`), destination);
  console.log(`Updated ${destination}`);
}
