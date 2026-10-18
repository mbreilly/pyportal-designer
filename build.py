"""Build index.html, the standalone PyPortal Display Designer.

The designer (src/designer.html) embeds the CircuitPython program
(device/code.py) so it can include it in every export. Run this after
changing either file:

    python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
page = (ROOT / "src" / "designer.html").read_text(encoding="utf-8")
code = (ROOT / "device" / "code.py").read_text(encoding="utf-8")
if "</script" in code:
    raise SystemExit("device/code.py must not contain '</script'")

page = page.replace("/*CODEPY*/", "\n" + code)
split = page.index('<div class="wrap">')
head, body = page[:split], page[split:]
html = (
    "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
    + head + "</head>\n<body>\n" + body + "</body>\n</html>\n"
)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("wrote index.html (%d KB)" % (len(html.encode()) // 1024))
