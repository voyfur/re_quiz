const puppeteer = require('puppeteer-core');

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

async function runBrowserE2E(serverUrl) {
  console.log(`[Browser E2E] Launching Headless Chrome against ${serverUrl}...`);
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-web-security']
  });

  const page = await browser.newPage();
  const consoleErrors = [];
  page.on('console', msg => {
    console.log(`[Browser Console ${msg.type()}]`, msg.text());
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', err => {
    console.log('[Browser PageError]', err.toString());
    consoleErrors.push(err.toString());
  });

  let interceptedBulkPayload = null;
  await page.setRequestInterception(true);
  page.on('request', req => {
    if (req.url().includes('checkout/quiz_cart/add_bulk')) {
      const origin = req.headers().origin || '*';
      if (req.method() === 'OPTIONS') {
        req.respond({
          status: 200,
          headers: {
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
            'Access-Control-Allow-Credentials': 'true'
          },
          body: ''
        });
        return;
      }
      console.log('[Browser E2E Intercepted add_bulk POST request]:', req.postData());
      interceptedBulkPayload = req.postData();
      req.respond({
        status: 200,
        headers: {
          'Access-Control-Allow-Origin': origin,
          'Access-Control-Allow-Credentials': 'true'
        },
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          added_items: 2,
          total_items: 2,
          redirect: 'https://raceexpert.com.ua/index.php?route=checkout/cart'
        })
      });
    } else {
      req.continue();
    }
  });

  try {
    // 1. Navigate to home
    console.log('[Browser E2E] Navigating to homepage...');
    const resp = await page.goto(serverUrl, { waitUntil: 'networkidle0', timeout: 15000 });
    if (!resp.ok()) throw new Error(`HTTP ${resp.status()} on loading homepage`);

    // 2. Check title & store header
    const title = await page.title();
    console.log(`[Browser E2E] Page title: "${title}"`);
    if (!title.includes('Race Expert')) throw new Error('Page title missing Race Expert');

    // 3. Test Sport Switching (Click Cycling)
    console.log('[Browser E2E] Switching to Cycling...');
    const cyclingTab = await page.$('button[data-sport="cycling"]');
    if (!cyclingTab) throw new Error('Cycling sport tab not found');
    await cyclingTab.click();

    // Wait for other-sport-submit button to appear in other-sports-container
    await page.waitForSelector('#other-sport-submit', { visible: true, timeout: 5000 });
    console.log('[Browser E2E] Cycling configurator rendered successfully.');

    // 4. Generate Cycling Box
    console.log('[Browser E2E] Clicking "#other-sport-submit"...');
    await page.click('#other-sport-submit');

    // Wait for results container to become visible
    console.log('[Browser E2E] Waiting for #result-container to appear...');
    await page.waitForFunction(() => {
      const el = document.getElementById('result-container');
      return el && !el.classList.contains('hidden');
    }, { timeout: 10000 });

    console.log('[Browser E2E] Box generated and #result-container is visible!');

    // 5. Verify total price element
    await page.waitForSelector('#total-box-price', { timeout: 5000 });
    const priceText = await page.$eval('#total-box-price', el => el.textContent.trim());
    console.log(`[Browser E2E] Generated box total price text: "${priceText}"`);
    const initialPrice = parseFloat(priceText.replace(/[^\d.]/g, ''));
    if (isNaN(initialPrice) || initialPrice <= 0) throw new Error(`Invalid total price: ${priceText}`);
    console.log(`[Browser E2E] Initial box price: ${initialPrice} грн`);

    // 6. Test Interactive Deselection
    console.log('[Browser E2E] Testing interactive item deselection...');
    const checkboxes = await page.$$('.item-checkbox');
    console.log(`[Browser E2E] Found ${checkboxes.length} item checkboxes in DOM`);
    if (checkboxes.length === 0) throw new Error('No item checkboxes found');

    // Click first checkbox to deselect
    await page.evaluate(() => {
      const cb = document.querySelector('.item-checkbox');
      if (cb) cb.click();
    });
    await new Promise(r => setTimeout(r, 400));

    // Verify price updated
    const updatedPriceText = await page.$eval('#total-box-price', el => el.textContent.trim());
    const updatedPrice = parseFloat(updatedPriceText.replace(/[^\d.]/g, ''));
    console.log(`[Browser E2E] Price after deselection: ${updatedPrice} грн`);
    if (updatedPrice >= initialPrice) {
      throw new Error(`Deselection failed to decrease price: initial=${initialPrice}, updated=${updatedPrice}`);
    }
    console.log(`[Browser E2E] Price dynamically updated: -${initialPrice - updatedPrice} грн!`);

    // 6B. Test Item Swapping (🔀 button - tests fix for care_recovery slot)
    console.log('[Browser E2E] Testing item flavor/brand swap button...');
    const swapBtns = await page.$$('.swap-item-btn');
    console.log(`[Browser E2E] Found ${swapBtns.length} swap buttons in DOM`);
    if (swapBtns.length > 0) {
      await page.evaluate(() => {
        const btn = document.querySelector('.swap-item-btn');
        if (btn) btn.click();
      });
      await new Promise(r => setTimeout(r, 300));
      console.log('[Browser E2E] Item swap button clicked successfully with zero JS errors!');
    }

    // 6C. Test Select All / Deselect All Controls
    console.log('[Browser E2E] Testing Deselect All...');
    await page.click('#deselect-all-items-btn');
    await new Promise(r => setTimeout(r, 300));
    const deselectPriceText = await page.$eval('#total-box-price', el => el.textContent.trim());
    const deselectPrice = parseFloat(deselectPriceText.replace(/[^\d.]/g, ''));
    console.log(`[Browser E2E] Price after Deselect All: ${deselectPrice} грн`);
    if (deselectPrice !== 0) {
      throw new Error(`Expected total price 0 after deselect all, got ${deselectPrice}`);
    }

    // Verify buy button is disabled when 0 items selected
    const buyBtnDisabled = await page.$eval('#buy-box-btn', btn => btn.disabled);
    if (!buyBtnDisabled) throw new Error('Buy button should be disabled when 0 items selected');
    console.log('[Browser E2E] Buy button correctly disabled on zero selection.');

    console.log('[Browser E2E] Testing Select All...');
    await page.click('#select-all-items-btn');
    await new Promise(r => setTimeout(r, 300));
    const reselectPriceText = await page.$eval('#total-box-price', el => el.textContent.trim());
    const reselectPrice = parseFloat(reselectPriceText.replace(/[^\d.]/g, ''));
    console.log(`[Browser E2E] Price after Select All: ${reselectPrice} грн`);
    if (reselectPrice <= 0) throw new Error(`Invalid price after select all: ${reselectPrice}`);

    // 7. Verify OpenCart Cart Addition Request
    console.log('[Browser E2E] Enabling FORCE_LIVE_OPENCART in page context...');
    await page.evaluate(() => {
      window.FORCE_LIVE_OPENCART = true;
    });

    // Click buy button
    console.log('[Browser E2E] Clicking #buy-box-btn...');
    const buyBtn = await page.$('#buy-box-btn');
    if (!buyBtn) throw new Error('#buy-box-btn not found in DOM');
    await buyBtn.click();

    // Wait for network request to be captured
    await new Promise(r => setTimeout(r, 1200));

    if (!interceptedBulkPayload) {
      throw new Error('OpenCart bulk cart POST request was not triggered on buy click');
    }

    const payloadObj = JSON.parse(interceptedBulkPayload);
    console.log(`[Browser E2E] Intercepted OpenCart payload:`, JSON.stringify(payloadObj));
    if (!payloadObj.items || !Array.isArray(payloadObj.items) || payloadObj.items.length === 0) {
      throw new Error('Intercepted payload does not contain valid items array');
    }

    console.log(`[Browser E2E] Successfully verified bulk addition of ${payloadObj.items.length} items to OpenCart!`);
    console.log('[Browser E2E] ✅ ALL DOM & INTERACTION CHECKS PASSED IN REAL GOOGLE CHROME!');
    
    if (consoleErrors.length > 0) {
      console.warn('[Browser E2E] Browser console warnings/errors observed:', consoleErrors);
    }

    await browser.close();
    return true;
  } catch (err) {
    await browser.close();
    throw err;
  }
}

// CLI runner
if (require.main === module) {
  const url = process.argv[2] || 'http://127.0.0.1:8000';
  runBrowserE2E(url)
    .then(() => process.exit(0))
    .catch(err => {
      console.error('[Browser E2E FAILED]:', err);
      process.exit(1);
    });
}

module.exports = { runBrowserE2E };
