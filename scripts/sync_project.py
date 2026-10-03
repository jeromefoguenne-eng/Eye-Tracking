"""
Script d'automatisation de synchronisation Git pour le projet Eye Tracking.
Synchronise l'ensemble des scripts, notebooks et documentations vers :
https://github.com/jeromefoguenne-eng/Eye-Tracking.git
"""
import os
import sys
import subprocess
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_cmd(cmd, cwd=REPO_DIR):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode


def auto_sync(custom_message=None):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Verification des modifications dans le projet Eye-Tracking...")
    
    status, _, _ = run_cmd("git status --porcelain")
    if not status:
        print("Aucune modification detectee. Le depot est deja parfaitement a jour sur GitHub.")
        return True

    # Analyse des fichiers modifies pour generer un message automatique si non specifie
    if not custom_message:
        lines = status.split("\n")
        changed_sections = set()
        for l in lines:
            parts = l.strip().split()
            if len(parts) >= 2:
                path = parts[-1]
                top_dir = path.split("/")[0] if "/" in path else (path.split("\\")[0] if "\\" in path else path)
                changed_sections.add(top_dir)
        
        desc = ", ".join(sorted(list(changed_sections))) if changed_sections else "fichiers"
        commit_msg = f"update(eye-tracking): maj {desc} [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
    else:
        commit_msg = custom_message

    print(f"Indexation et commit : '{commit_msg}'...")
    run_cmd("git add .")
    out, err, code = run_cmd(f'git commit -m "{commit_msg}"')
    if code != 0 and "nothing to commit" in out:
        print("Rien a committer.")
        return True

    print("Push vers GitHub (jeromefoguenne-eng/Eye-Tracking)...")
    gh_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if gh_token:
        push_cmd = f"git push https://{gh_token}@github.com/jeromefoguenne-eng/Eye-Tracking.git main"
    else:
        push_cmd = "git push origin main"
    
    p_out, p_err, p_code = run_cmd(push_cmd)
    if p_code == 0:
        print("✅ Synchronisation GitHub terminee avec succes !")
        return True
    else:
        # Tenter vers master si main n'est pas encore la branche par defaut
        print("Tentative de repli sur la branche par defaut...")
        p_out2, p_err2, p_code2 = run_cmd("git push origin HEAD")
        if p_code2 == 0:
            print("✅ Synchronisation GitHub terminee avec succes via HEAD !")
            return True
        print(f"❌ Erreur lors du push : {p_err or p_out or p_err2 or p_out2}")
        return False


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else None
    auto_sync(msg)
