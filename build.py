"""Genera index.html a partir de src/template.html, src/albums.json y src/descripciones.json.
Uso: python3 build.py"""
import json, pathlib
root = pathlib.Path(__file__).parent
albums = json.loads((root / "src/albums.json").read_text(encoding="utf-8"))
data = json.loads((root / "src/descripciones.json").read_text(encoding="utf-8"))
desc, problems = {}, []
for c in data["canciones"]:
    a = 31 if str(c["album_num"]).lower() == "extra" else int(c["album_num"]) - 1
    s = int(c["pista"]) - 1
    try:
        title = albums[a]["s"][s][0]
    except (IndexError, ValueError):
        problems.append(f"no existe: {c['album']} pista {c['pista']}"); continue
    if c.get("descripcion") and c.get("estado") != "sin_datos":
        desc[f"{a}-{s}"] = [c["descripcion"], 1 if c.get("estado") == "interpretacion" else 0]
js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
html = (root / "src/template.html").read_text(encoding="utf-8")
html = html.replace("__DATA__", js(albums)).replace("__DESC__", js(desc))
(root / "index.html").write_text(html, encoding="utf-8")
print(f"index.html listo: {len(desc)} descripciones ({sum(v[1] for v in desc.values())} interpretaciones)")
for p in problems: print("aviso:", p)
