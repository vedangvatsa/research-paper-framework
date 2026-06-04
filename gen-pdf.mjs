import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(__dirname, 'agent_infrastructure_stack.html');
const pdfPath = path.join(__dirname, 'agent_infrastructure_stack.pdf');

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
await page.pdf({
  path: pdfPath,
  format: 'Letter',
  margin: { top: '1in', bottom: '1in', left: '1.5in', right: '1.5in' },
  printBackground: true,
});
await browser.close();
console.log(`PDF saved to ${pdfPath}`);
