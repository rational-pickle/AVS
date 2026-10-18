from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
import asyncio, sys
from playwright.async_api import async_playwright

SRC = str(ROOT / "avs-gen2-client-deck.html")
OUT = str(ROOT / "shots")
import os; os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1440, "height": 900})
        pg = await ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://" + SRC + "#10")
        await pg.wait_for_timeout(300)
        r = {}
        r["start_idx_from_hash"] = await pg.evaluate("avsDeck.i")
        # notes
        await pg.keyboard.press("n")
        await pg.wait_for_timeout(200)
        r["notes_open"] = await pg.evaluate("document.body.classList.contains('notes-open')")
        r["notes_len"] = await pg.evaluate("document.getElementById('notesPane').innerText.length")
        await pg.screenshot(path=f"{OUT}/func-notes-en.png")
        await pg.keyboard.press("l")
        await pg.wait_for_timeout(200)
        r["lang_after_L"] = await pg.evaluate("document.documentElement.dataset.lang")
        r["notes_fr_sample"] = (await pg.evaluate("document.getElementById('notesPane').innerText"))[:120]
        await pg.screenshot(path=f"{OUT}/func-notes-fr.png")
        await pg.keyboard.press("n")
        await pg.keyboard.press("l")
        # deep dive skipping
        await pg.keyboard.press("d")
        await pg.wait_for_timeout(100)
        seq = []
        await pg.evaluate("avsDeck.go(0)")
        for _ in range(60):
            seq.append(await pg.evaluate("avsDeck.i"))
            await pg.keyboard.press("ArrowRight")
        visited = sorted(set(seq))
        skips = await pg.evaluate("Array.from(document.querySelectorAll('.slide')).map((s,i)=>s.dataset.skip==='1'?i:null).filter(x=>x!==null)")
        r["deep_off_visited_skippable"] = [i for i in visited if i in skips]
        r["deep_off_visited_count"] = len(visited)
        await pg.keyboard.press("d")
        # overview
        await pg.keyboard.press("o")
        await pg.wait_for_timeout(200)
        r["overview_buttons"] = await pg.evaluate("document.querySelectorAll('#overview button[data-k]').length")
        await pg.screenshot(path=f"{OUT}/func-overview.png")
        await pg.keyboard.press("Escape")
        # notes present on every slide in both languages
        r["slides_missing_notes"] = await pg.evaluate("""Array.from(document.querySelectorAll('.slide')).map((s,i)=>{
            const en=s.querySelector('.notes .l-en'), fr=s.querySelector('.notes .l-fr');
            return (!en||en.textContent.trim().length<40||!fr||fr.textContent.trim().length<40)?i+1:null}).filter(x=>x)""")
        # every l-en has an l-fr sibling count parity
        r["lang_parity"] = await pg.evaluate("[document.querySelectorAll('.l-en').length, document.querySelectorAll('.l-fr').length]")
        # presenter window
        await pg.evaluate("avsDeck.go(14)")
        async with ctx.expect_page() as pinfo:
            await pg.keyboard.press("p")
        pw = await pinfo.value
        await pw.set_viewport_size({"width": 1280, "height": 820})
        await pw.wait_for_timeout(500)
        await pg.evaluate("avsDeck.next()")
        await pw.wait_for_timeout(400)
        r["pw_title"] = await pw.evaluate("document.getElementById('pwT').textContent")
        r["pw_has_preview"] = await pw.evaluate("!!document.querySelector('#pvCur .slide')")
        await pw.keyboard.press("ArrowRight")
        await pw.wait_for_timeout(300)
        r["idx_after_pw_key"] = await pg.evaluate("avsDeck.i")
        await pw.screenshot(path=f"{OUT}/func-presenter.png")
        # print to pdf
        pdf = await pg.pdf(path=f"{OUT}/deck-print-test.pdf", width="1600px", height="900px", print_background=True, prefer_css_page_size=True)
        print(r)
        print("errors:", errs)
        await b.close()

asyncio.run(main())
