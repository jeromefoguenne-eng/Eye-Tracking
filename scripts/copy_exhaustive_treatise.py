import shutil

src = r"C:\Users\TrendingPC\.gemini\antigravity\brain\0dd572da-d04d-4b8f-a668-583293824702\traite_methodologique_exhaustif_simaccueil.md"
dst = r"C:\Users\TrendingPC\.gemini\antigravity\scratch\Eye-Tracking\docs\traite_methodologique_exhaustif_simaccueil.md"

shutil.copy2(src, dst)
print("Copied to repo docs successfully.")
