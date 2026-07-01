const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function generatePDF(mode = 'plain') {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();

  const htmlPath = `file://${path.join(__dirname, '..', 'public', 'pdf-template.html')}?mode=${mode}`;

  try {
    await page.goto(htmlPath, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.waitForTimeout(2000);

    const pdf = await page.pdf({
      format: 'A4',
      printBackground: true,
      margin: { top: '15mm', bottom: '15mm', left: '10mm', right: '10mm' }
    });

    const outDir = path.join(__dirname, '..', 'public', 'assets', 'downloads');
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    const fname = mode === 'complete'
      ? 'ESTEBAN-MANUEL-LOPEZ-RIVERO-COMPLETO.pdf'
      : 'ESTEBAN-MANUEL-LOPEZ-RIVERO.pdf';
    const outPath = path.join(outDir, fname);
    fs.writeFileSync(outPath, pdf);

    console.log(`PDF generated: ${outPath}`);
    console.log(`Size: ${fs.statSync(outPath).size} bytes`);
  } catch (err) {
    console.error('PDF generation failed:', err);
  } finally {
    await browser.close();
  }
}

const mode = process.argv.includes('--complete') ? 'complete' : 'plain';
generatePDF(mode);
