import docx
import re
import json

doc = docx.Document(r"C:/Google Drive/Prépas light/HECh/Projet recherche/Constats Etats de l'art.docx")

sections = []
current_sec = {"title": "START", "paragraphs": []}

for p in doc.paragraphs:
    txt = p.text.strip()
    if not txt:
        continue
    if re.match(r"^Texte\s+[\d\w\.]+", txt, re.IGNORECASE):
        sections.append(current_sec)
        current_sec = {"title": txt, "paragraphs": []}
    else:
        current_sec["paragraphs"].append(txt)
sections.append(current_sec)

# Save to a structured file
with open("docs/constats_structured.json", "w", encoding="utf-8") as f:
    json.dump(sections, f, ensure_ascii=False, indent=2)

print(f"Saved {len(sections)} sections to docs/constats_structured.json")
for i, s in enumerate(sections):
    if s["title"] != "START":
        print(f"{i}: {s['title'][:70]} (p={len(s['paragraphs'])})")
