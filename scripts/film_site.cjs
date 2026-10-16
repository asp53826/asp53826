#!/usr/bin/env node
/*
 * Films the live portfolio site into the profile README.
 *
 * A README cannot run JavaScript or embed a page, so instead CI opens the real
 * site in a real browser, drives it (cursor, keys, clicks), and records short
 * browser-framed loops. The README then shows the site as it is today, and the
 * daily workflow re-films it so the window never drifts from the live site.
 *
 *   node scripts/film_site.cjs                       # films https://asp53826.github.io
 *   SITE=http://127.0.0.1:4321 node scripts/film_site.cjs   # films a local build
 *
 * Needs: playwright (chromium) and ffmpeg (FFMPEG env var, else `ffmpeg` on PATH).
 * Writes: assets/live/lab.webp (smooth gradients compress far better as WebP)
 *         assets/live/{short-gamma,royale}.gif
 * On any failure the existing GIFs are left untouched.
 */
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const SITE = (process.env.SITE || 'https://asp53826.github.io').replace(/\/$/, '');
const SHOWN = 'asp53826.github.io';       // what the address bar displays
const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const OUT = path.join(__dirname, '..', 'assets', 'live');
const W = 1280, H = 720, BAR = 44;

// A browser window drawn around the real page (the page runs in the iframe).
const frame = (url, shown, accent) => `<!doctype html><html><body style="margin:0;background:#06090c">
<div style="width:${W}px;height:${BAR}px;display:flex;align-items:center;gap:8px;padding:0 16px;box-sizing:border-box;
  background:#0d1318;border-bottom:1px solid #1c2730;font:13px ui-monospace,SFMono-Regular,Menlo,monospace;color:#8aa0a8">
  <span style="width:12px;height:12px;border-radius:50%;background:#ff5f57"></span>
  <span style="width:12px;height:12px;border-radius:50%;background:#febc2e"></span>
  <span style="width:12px;height:12px;border-radius:50%;background:#28c840"></span>
  <span style="margin-left:18px;flex:1;max-width:560px;padding:6px 14px;border-radius:8px;background:#06090c;border:1px solid #1c2730">
    🔒&nbsp; <span style="color:#d8e5e8">${shown}</span></span>
  <span style="margin-left:auto;display:flex;align-items:center;gap:7px;color:${accent};letter-spacing:1.5px;font-size:11px">
    <span style="width:8px;height:8px;border-radius:50%;background:${accent};box-shadow:0 0 10px ${accent}"></span>LIVE · FILMED BY CI</span>
</div>
<iframe src="${url}" style="display:block;width:${W}px;height:${H - BAR}px;border:0"></iframe>
</body></html>`;

const SHOTS = [
  {
    name: 'lab', path: '/lab/', accent: '#7ce7a6', width: 960, fps: 10, format: 'webp',
    async run(page, snap) {
      await page.waitForTimeout(2500);                  // let the aurora warm up
      for (let i = 0; i < 44; i++) {                    // steer the aurora with a slow figure-eight
        const t = (i / 44) * Math.PI * 2;
        await page.mouse.move(640 + 420 * Math.sin(t), 380 + 160 * Math.sin(2 * t));
        await snap(90);
      }
    },
  },
  {
    name: 'short-gamma', path: '/lab/play/', accent: '#ffc53d', width: 640, fps: 6,
    async run(page, snap, f) {
      await page.waitForTimeout(1500);
      await f.getByRole('button', { name: /practice on a random one/i }).click();
      await page.waitForTimeout(800);
      await page.mouse.click(640, 400); await page.keyboard.press('Space');   // run the clock
      for (let i = 0; i < 30; i++) {
        if (i === 8) await page.keyboard.press('b');                           // buy 100 to hedge
        if (i === 18) await page.keyboard.press('s');
        await snap(260);
      }
    },
  },
  {
    name: 'royale', path: '/lab/royale/', accent: '#7aa2ff', width: 640, fps: 6,
    async run(page, snap, f) {
      await page.waitForTimeout(1500);
      await f.getByPlaceholder(/your name/i).fill('readme');
      await f.getByRole('button', { name: /play solo/i }).click();
      for (let i = 0; i < 30; i++) {
        if (i === 6) await f.locator('#buyBtn').click().catch(() => {});
        if (i === 16) await f.locator('#sellBtn').click().catch(() => {});
        await snap(280);
      }
    },
  },
];

async function film(browser, shot) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), `film-${shot.name}-`));
  const page = await browser.newPage({ viewport: { width: W, height: H }, colorScheme: 'dark' });
  await page.setContent(frame(SITE + shot.path, SHOWN + shot.path, shot.accent));
  const f = page.frameLocator('iframe');
  await page.frame({ url: /./ });
  await page.waitForLoadState('networkidle');
  let n = 0;
  const snap = async (ms) => { await page.waitForTimeout(ms); await page.screenshot({ path: path.join(dir, `${String(n++).padStart(3, '0')}.png`) }); };
  await shot.run(page, snap, f);
  await page.close();
  const ext = shot.format || 'gif';
  const out = path.join(OUT, `${shot.name}.${ext}`);
  const tmp = out + `.tmp.${ext}`;
  const input = ['-loglevel', 'error', '-y', '-framerate', String(shot.fps), '-i', path.join(dir, '%03d.png')];
  execFileSync(FFMPEG, ext === 'webp'
    ? [...input, '-vf', `scale=${shot.width}:-1:flags=lanczos`, '-c:v', 'libwebp_anim', '-q:v', '72', '-compression_level', '6', '-loop', '0', tmp]
    : [...input, '-vf', `scale=${shot.width}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle`, '-loop', '0', tmp]);
  fs.renameSync(tmp, out);                                // only replace once the new GIF is complete
  fs.rmSync(dir, { recursive: true, force: true });
  console.log(`filmed ${shot.name}: ${n} frames, ${(fs.statSync(out).size / 1024).toFixed(0)} KB`);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  let failed = 0;
  for (const shot of SHOTS) {
    try { await film(browser, shot); }
    catch (e) { failed++; console.log(`skipped ${shot.name}: ${e.message.split('\n')[0]} (kept previous GIF)`); }
  }
  await browser.close();
  process.exitCode = failed === SHOTS.length ? 1 : 0;
})();
