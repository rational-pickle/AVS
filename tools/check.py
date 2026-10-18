"""Render every slide in EN and FR, screenshot, and report overflow."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
import asyncio, json, sys, os
from playwright.async_api import async_playwright

SRC = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "avs-gen2-client-deck.html")
OUT = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / "shots")
FORCE = sys.argv[3] if len(sys.argv) > 3 else ""   # e.g. "DejaVu Sans" to test a wide fallback font
ONLY = os.environ.get("ONLY")
os.makedirs(OUT, exist_ok=True)

PROBE = r"""
(() => {
  const s = document.querySelector('.slide.active');
  const R = s.getBoundingClientRect();
  const sc = R.width / 1600;
  const issues = [];
  const vis = el => { const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden' && el.getClientRects().length; };
  const refs = s.querySelector('.refs');
  const refTop = refs && vis(refs) ? refs.getBoundingClientRect().top : null;
  const body = s.querySelector('.s-body');
  const limitB = (refTop ? refTop - 6 : R.bottom - 50 * sc);
  if (body) {
    body.querySelectorAll('*').forEach(el => {
      if (!vis(el) || el.closest('.refs') || el.closest('svg')) return;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      if (r.bottom > limitB + 1) issues.push(['bottom', el.tagName + '.' + (el.className||''), Math.round((r.bottom - limitB)/sc)]);
      if (r.right > R.right - 40*sc + 1) issues.push(['right', el.tagName + '.' + (el.className||''), Math.round((r.right - (R.right-40*sc))/sc)]);
    });
    body.querySelectorAll('td,th,pre,li,p,h3,span').forEach(el => {
      if (!vis(el)) return;
      if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow !== 'visible') issues.push(['hscroll', el.tagName, el.scrollWidth - el.clientWidth]);
    });
  }
  if (refs && vis(refs) && refs.scrollWidth > refs.clientWidth + 2) issues.push(['refs-trunc', '', refs.scrollWidth - refs.clientWidth]);
  const h2 = s.querySelector('.s-head h2');
  if (h2) { const lines = Math.round(h2.getBoundingClientRect().height / (42*1.12*sc)); if (lines > 1) issues.push(['title-lines', lines, '']); }
  // svg text overflow: text bbox outside the svg viewBox
  s.querySelectorAll('svg').forEach(sv => {
    const vb = sv.viewBox.baseVal; if (!vb) return;
    sv.querySelectorAll('text').forEach(tx => {
      if (!vis(tx)) return;
      const b = tx.getBBox();
      if (b.x < vb.x - 1 || b.y < vb.y - 1 || b.x + b.width > vb.x + vb.width + 1 || b.y + b.height > vb.y + vb.height + 1)
        issues.push(['svg-text-out', tx.textContent.slice(0, 40), Math.round(Math.max(vb.x - b.x, b.x + b.width - vb.width, vb.y - b.y, b.y + b.height - vb.height))]);
    });
  });
  return issues;
})()
"""

# text-in-box check: a label wider than the rect immediately preceding it
BOXPROBE = r"""
(() => {
  const s = document.querySelector('.slide.active');
  const out = [];
  s.querySelectorAll('svg rect').forEach(r => {
    let n = r.nextElementSibling; let k = 0;
    while (n && n.tagName === 'text' && k < 4) {
      if (getComputedStyle(n).display !== 'none') {
        const b = n.getBBox(); const x = +r.getAttribute('x'), w = +r.getAttribute('width'), y = +r.getAttribute('y'), h = +r.getAttribute('height');
        if (b.width > 0 && (b.x < x - 0.5 || b.x + b.width > x + w + 0.5) && w > 30 && h < 400)
          out.push([n.textContent.slice(0, 50), Math.round(b.width - w)]);
      }
      n = n.nextElementSibling; k++;
    }
  });
  return out;
})()
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1600, "height": 900})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        await pg.goto("file://" + SRC)
        if FORCE:
            await pg.add_style_tag(content=f':root{{--font:"{FORCE}"}} body, .dg text {{font-family:"{FORCE}" !important}}')
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        report = {}
        for lang in ("en", "fr"):
            await pg.evaluate(f"avsDeck.setLang('{lang}')")
            for i in range(n):
                if ONLY and str(i + 1) not in ONLY.split(","):
                    continue
                await pg.evaluate(f"avsDeck.go({i})")
                await pg.wait_for_timeout(260)
                iss = await pg.evaluate(PROBE)
                bx = await pg.evaluate(BOXPROBE)
                if bx:
                    iss += [["box-text", a, d] for a, d in bx]
                if iss:
                    report[f"{lang}-{i + 1}"] = iss
                await pg.screenshot(path=f"{OUT}/{lang}-{i + 1:02d}.png")
        json.dump(report, open(OUT + "/report.json", "w"), ensure_ascii=False, indent=1)
        for k, v in report.items():
            print(k, " ; ".join(f"{a[0]}:{str(a[1])[:38]}:{a[2]}" for a in v))
        print("errors:", errors[:10])
        await b.close()

asyncio.run(main())
