import docx
import os

drive_folder = r"C:\Google Drive"
matches = []
for root, dirs, files in os.walk(drive_folder):
    for f in files:
        if "Constats" in f and f.endswith(".docx"):
            matches.append(os.path.join(root, f))

target_path = matches[0]
doc = docx.Document(target_path)

os.makedirs("docs", exist_ok=True)
with open("docs/constats_dump.txt", "w", encoding="utf-8") as out:
    out.write(f"DOCUMENT: {target_path}\n\n")
    for i, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if txt:
            out.write(f"[P{i}] {txt}\n")

print(f"Dumped {len(doc.paragraphs)} paragraphs to scratch/constats_dump.txt")
