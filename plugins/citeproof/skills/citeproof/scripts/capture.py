#!/usr/bin/env python3
"""CiteProof evidence capture.

Opens a web page, finds a verbatim fragment, highlights it, and saves a cropped
screenshot of the surrounding passage with the URL and capture date stamped on top.

Usage:
    python capture.py --url URL --find "verbatim fragment" --out evidence.png
                      [--padding 60] [--width 1280] [--timeout 30] [--lang es]

Exit codes:
    0  captured
    1  bad arguments / missing dependency
    2  page loaded but the fragment was not found
    3  page could not be loaded (network, block, timeout)

Requires: playwright (with a Chromium build) and Pillow.
    pip install playwright pillow && python -m playwright install chromium
"""
import argparse
import datetime as dt
import sys

FIND_JS = r"""
(frag) => {
  const norm = s => s.replace(/[‘’]/g, "'").replace(/[“”«»]/g, '"')
                     .replace(/[‐-―]/g, '-').replace(/\s+/g, ' ').toLowerCase();
  const target = norm(frag).trim();
  if (!target) return null;
  // Walk block elements from the most specific up; pick the smallest one containing the fragment.
  const blocks = Array.from(document.querySelectorAll('p,li,td,th,blockquote,dd,dt,figcaption,h1,h2,h3,h4,h5,h6,span,div,section,article'));
  let best = null, bestLen = Infinity;
  for (const el of blocks) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const t = norm(el.innerText || '');
    if (t.includes(target) && t.length < bestLen) { best = el; bestLen = t.length; }
  }
  if (!best) return null;
  // Highlight the matching text inside the block (text-node level, best effort).
  const walker = document.createTreeWalker(best, NodeFilter.SHOW_TEXT);
  const nodes = []; let n; while ((n = walker.nextNode())) nodes.push(n);
  let full = '', map = [];
  for (const node of nodes) { for (let i = 0; i < node.data.length; i++) { map.push([node, i]); } full += node.data; }
  const lowered = norm(full);
  // Rebuild index map for normalized string (collapse whitespace like norm()).
  let normIdx = [], out = '', prevSpace = false;
  for (let i = 0; i < full.length; i++) {
    let c = norm(full[i]); if (c === ' ' || /\s/.test(full[i])) { if (prevSpace) continue; c = ' '; prevSpace = true; } else prevSpace = false;
    out += c; normIdx.push(i);
  }
  const pos = out.indexOf(target);
  best.scrollIntoView({block: 'center'});
  if (pos >= 0) {
    const startI = normIdx[pos], endI = normIdx[Math.min(pos + target.length - 1, normIdx.length - 1)];
    const range = document.createRange();
    range.setStart(map[startI][0], map[startI][1]);
    range.setEnd(map[endI][0], map[endI][1] + 1);
    try {
      const mark = document.createElement('mark');
      mark.style.background = '#ffeb3b'; mark.style.color = 'inherit';
      mark.style.outline = '2px solid #f57f17';
      mark.appendChild(range.extractContents()); range.insertNode(mark);
    } catch (e) { best.style.background = '#fff59d'; }
  } else { best.style.background = '#fff59d'; }
  const r = best.getBoundingClientRect();
  return {x: r.x + window.scrollX, y: r.y + window.scrollY, w: r.width, h: r.height};
}
"""

DISMISS_JS = r"""
() => {
  const words = ['accept','agree','aceptar','acepto','entendido','ok','got it','allow all','accept all','aceptar todo'];
  for (const b of document.querySelectorAll('button, a[role=button]')) {
    const t = (b.innerText || '').trim().toLowerCase();
    if (t && t.length < 25 && words.some(w => t === w || t.startsWith(w))) { try { b.click(); } catch (e) {} }
  }
}
"""


def stamp(png_path, url, lang):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.open(png_path).convert("RGB")
    bar_h = 44
    out = Image.new("RGB", (img.width, img.height + bar_h), "white")
    out.paste(img, (0, bar_h))
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, img.width, bar_h], fill="#263238")
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    when = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    label = "Capturado" if lang == "es" else "Captured"
    text = f"{url}   ·   {label}: {when}"
    max_chars = max(20, img.width // 8)
    if len(text) > max_chars:
        text = text[: max_chars - 1] + "…"
    d.text((12, 13), text, fill="white", font=font)
    out.save(png_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", required=True)
    ap.add_argument("--find", required=True, help="verbatim fragment from the page")
    ap.add_argument("--out", required=True, help="output PNG path")
    ap.add_argument("--padding", type=int, default=60)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--timeout", type=int, default=30, help="seconds")
    ap.add_argument("--lang", default="es", choices=["es", "en"])
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Missing dependency: pip install playwright pillow && python -m playwright install chromium", file=sys.stderr)
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": a.width, "height": 900}, device_scale_factor=1.5)
        try:
            resp = page.goto(a.url, wait_until="domcontentloaded", timeout=a.timeout * 1000)
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            if resp is not None and resp.status >= 400:
                print(f"HTTP {resp.status} for {a.url}", file=sys.stderr)
                browser.close()
                return 3
        except Exception as e:  # network blocked, DNS, timeout
            print(f"Could not load page: {e}", file=sys.stderr)
            browser.close()
            return 3

        page.evaluate(DISMISS_JS)
        page.wait_for_timeout(500)
        box = page.evaluate(FIND_JS, a.find)
        if not box:
            print("Fragment not found on the page. Try a shorter, exact fragment.", file=sys.stderr)
            browser.close()
            return 2
        page.wait_for_timeout(300)
        doc_w = page.evaluate("document.documentElement.scrollWidth")
        x = max(0, box["x"] - a.padding)
        y = max(0, box["y"] - a.padding)
        w = min(box["w"] + 2 * a.padding, doc_w - x)
        h = min(box["h"] + 2 * a.padding, 1800)
        page.screenshot(path=a.out, full_page=True, clip={"x": x, "y": y, "width": max(w, 200), "height": max(h, 80)})
        browser.close()

    stamp(a.out, a.url, a.lang)
    print(f"Saved {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
