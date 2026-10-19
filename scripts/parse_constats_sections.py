import docx
import os
import re

drive_folder = r"C:\Google Drive"
matches = []
for root, dirs, files in os.walk(drive_folder):
    for f in files:
        if "Constats" in f and f.endswith(".docx"):
            matches.append(os.path.join(root, f))

doc = docx.Document(matches[0])

sections = []
current_sec = {"title": "Header", "paragraphs": []}

for p in doc.paragraphs:
    txt = p.text.strip()
    if not txt:
        continue
    # Check if heading or starts with 'Texte '
    if re.match(r"^Texte\s+[\d\w\.]+", txt, re.IGNORECASE):
        sections.append(current_sec)
        current_sec = {"title": txt, "paragraphs": []}
    else:
        current_sec["paragraphs"].append(txt)
sections.append(current_sec)

print(f"Total sections detected: {len(sections)}")
for i, sec in enumerate(sections):
    print(f"\n[{i}] TITLE: {sec['title']}")
    print(f"    Paragraph count: {len(sec['paragraphs'])}")
    if sec['paragraphs']:
        print(f"    First p: {sec['paragraphs'][0][:120]}")
        print(f"    Last p: {sec['paragraphs'][-1][:120]}")
