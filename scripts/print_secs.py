import docx
import re

doc = docx.Document(r"C:/Google Drive/Prépas light/HECh/Projet recherche/Constats Etats de l'art.docx")

current_sec = {"title": "START", "paragraphs": []}
secs = []
for p in doc.paragraphs:
    txt = p.text.strip()
    if not txt:
        continue
    if re.match(r"^Texte\s+[\d\w\.]+", txt, re.IGNORECASE):
        secs.append(current_sec)
        current_sec = {"title": txt, "paragraphs": []}
    else:
        current_sec["paragraphs"].append(txt)
secs.append(current_sec)

for i in [0, 1, 2]:
    print(f"=== SEC {i}: {secs[i]['title']} ===")
    for p in secs[i]["paragraphs"]:
        print(f"  {p}")
