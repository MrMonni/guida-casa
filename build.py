"""Crea la guida pronta all'uso.

Uso:  python3 build.py

Produce:
  index.html  -> file unico da aprire anche senza internet (doppio clic)
  sito/       -> cartella da pubblicare online (Netlify o simili):
                 index.html + icona per la schermata Home + funzionamento offline
"""
import base64
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]

now = datetime.now()
versione = f"{now.day} {MESI[now.month - 1]} {now.year}, ore {now:%H:%M}"

images = {
    p.stem: "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    for p in sorted((SRC / "img").glob("*.png"))
}
html = (SRC / "template.html").read_text(encoding="utf-8")
html = html.replace("/*__IMAGES__*/", "const IMG = " + json.dumps(images) + ";")
html = html.replace("/*__DATA__*/", (SRC / "data.js").read_text(encoding="utf-8"))
html = html.replace("__VERSIONE__", versione)

out = ROOT / "index.html"
out.write_text(html, encoding="utf-8")

sito = ROOT / "sito"
if sito.exists():
    shutil.rmtree(sito)
sito.mkdir()
(sito / "index.html").write_text(html, encoding="utf-8")
for f in (SRC / "app").iterdir():
    if f.name == "sw.js":
        (sito / "sw.js").write_text(f.read_text(encoding="utf-8").replace("__VERSION__", now.strftime("%Y%m%d%H%M%S")), encoding="utf-8")
    else:
        shutil.copy(f, sito / f.name)

print(f"Creato {out} ({out.stat().st_size // 1024} KB, {len(images)} immagini)")
print(f"Cartella da pubblicare: {sito}  (versione del {versione})")
