const { chromium } = require('playwright-core');

// card_t<N>.png: the active turn card with strategy and reply hidden; eda_t<N>.png: the EDA panel with that turn's window shaded
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 3 });
  await page.goto('http://localhost:5179/context/11/participant/11', { waitUntil: 'networkidle' });
  await page.waitForSelector('.turn-card');
  await page.addStyleTag({ content: '.turn-card-strategy, .turn-card-ai { display: none !important; }' });
  for (const t of process.argv.slice(2)) {
    const card = page.locator('.turn-card', { hasText: `Turn ${t} ` }).first();
    await card.scrollIntoViewIfNeeded();
    await card.click();
    await page.waitForTimeout(700);
    await card.screenshot({ path: `card_t${t}.png` });
    await page.screenshot({ path: `eda_t${t}.png`, clip: { x: 568, y: 16, width: 852, height: 228 } });
  }
  await browser.close();
})();
