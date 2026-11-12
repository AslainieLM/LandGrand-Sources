const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const sharp = require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');

(async () => {
  const root = __dirname;
  const draft = fs.readFileSync('D:/Projects/LandGrand-Sources/LandGrand/Manuscript/Drafts/Chapter III Technical Background.md', 'utf8');
  const graph = draft.match(/```mermaid\s*\n([\s\S]*?)\n```/)[1];
  fs.writeFileSync(path.join(root, 'proposed-flow.mmd'), graph + '\n');
  let browser;
  try {
    browser = await chromium.launch({headless: true, channel: 'msedge'});
    const page = await browser.newPage({viewport: {width: 1400, height: 1100}});
    await page.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>');
    await page.addScriptTag({url: 'https://cdn.jsdelivr.net/npm/mermaid@10.9.3/dist/mermaid.min.js'});
    const result = await page.evaluate(async (source) => {
      mermaid.initialize({startOnLoad: false, securityLevel: 'strict', theme: 'base', themeVariables: {fontFamily: 'Arial', fontSize: '16px', primaryColor: '#f4f6f8', primaryTextColor: '#111827', primaryBorderColor: '#374151', lineColor: '#374151', edgeLabelBackground: '#ffffff', background: '#ffffff'}, flowchart: {htmlLabels: false, useMaxWidth: false, nodeSpacing: 32, rankSpacing: 42}});
      const valid = await mermaid.parse(source);
      const rendered = await mermaid.render('landGrandFlow', source);
      return {svg: rendered.svg, parsed: !!valid};
    }, graph);
    fs.writeFileSync(path.join(root, 'proposed-flow.svg'), result.svg);
    const png = path.join(root, 'proposed-flow.png');
    await sharp(Buffer.from(result.svg)).flatten({background: '#ffffff'}).png().toFile(png);
    const dimensions = await sharp(png).metadata();
    const report = {parser: 'Mermaid 10.9.3', browser: 'isolated headless Microsoft Edge', parsed: result.parsed, svg: path.join(root, 'proposed-flow.svg'), png, width: dimensions.width, height: dimensions.height, liveObsidianChecked: false};
    fs.writeFileSync(path.join(root, 'diagram-check.json'), JSON.stringify(report, null, 2));
    process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  } finally {
    if (browser) await browser.close();
  }
})().catch(error => { process.stderr.write(String(error.stack || error) + '\n'); process.exitCode = 1; });
