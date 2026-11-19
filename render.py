"""slides.html (каждый слайд — <section class="slide">) -> out/slide-NN.png. Размер берётся из самого слайда."""
import sys, pathlib
from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "slides.html").resolve()
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "out")
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
    pg.goto(src.as_uri())
    pg.evaluate("document.fonts.ready")
    slides = pg.query_selector_all("section.slide")
    for i, s in enumerate(slides, 1):
        s.screenshot(path=str(out / f"slide-{i:02d}.png"))
        over = s.evaluate("""el => [...el.querySelectorAll('*')].filter(n => {
            const r = n.getBoundingClientRect(), R = el.getBoundingClientRect();
            if (n.closest('[data-bleed]')) return false;
            const hasText = [...n.childNodes].some(c => c.nodeType === 3 && c.textContent.trim());
            return hasText && (r.right > R.right - 40 || r.bottom > R.bottom - 40 || r.left < R.left + 40 || r.top < R.top + 30);
        }).map(n => n.textContent.trim().slice(0, 40))""")
        if over:
            print(f"slide {i}: близко к краю/вылезает -> {over}")
    print(f"rendered {len(slides)} slides -> {out}/")
    b.close()
