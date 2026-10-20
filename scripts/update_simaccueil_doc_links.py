"""
Script d'actualisation des liens Google Drive dans :
C:\\Google Drive\\Prépas light\\HECh\\Projet recherche\\SIMACCUEIL - PRojet de recherche.docx

Remplace les liens génériques vers le dossier partagé par des liens directs
vers chaque fichier individuel dans le dossier "Ressources" de Google Drive.
"""
import os
import sys
import shutil
import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DOCX_PATH = r"C:\Google Drive\Prépas light\HECh\Projet recherche\SIMACCUEIL - PRojet de recherche.docx"
BACKUP_PATH = r"C:\Google Drive\Prépas light\HECh\Projet recherche\SIMACCUEIL - PRojet de recherche.backup.docx"

# Dictionnaire de correspondance exacte entre le numéro du texte et son ID Google Drive
FILE_IDS = {
    "Texte 01": ("01 - Taming a beast of burden – On some issues with the conceptualisation and operationalisation of cognitive load.docx", "1gGCFhaYKHcRynSGDbXXcH-DKjziICbjW"),
    "Texte 02": ("02 - Expertise Differences in the Comprehension of Visualizations a Meta-Analysis of Eye-Tracking.pdf", "1j836bEPcVegSD7IyKJLiD-FhxUyqtdZw"),
    "Texte 03": ("03 - VanGogetal_CiHB_2009.pdf", "1kK31uhfZb2T8aO0m6AAMSQxrI4OYCHya"),
    "Texte 04": ("04 - Goodwin - Professional vision.pdf", "1cLbFQyrU48W3CM7UfMAyC5zdHWwVxrh9"),
    "Texte 05": ("05 - Crandall, Klein & Hoffman - Working Minds - A Practitioner's Guide to Cognitive Task Analysis (Synthese).docx", "1iCkUb_RwUWRerLHRqMD2EVouQr7x8uZZ"),
    "Texte 06": ("06- Combining Concurrent Think-Aloud Protocols and Eye-Tracking Observations.pdf", "1n9GUyo3c2jF852WkVG1IHy3MVJLoFSQe"),
    "Texte 07": ("07 - « L'analyse de l'activité, le cours d'action et l'entreti.pdf", "1LYc0ZbAkw0uWyeKAcpPg3_VPQswfPjnt"),
    "Texte 08": ("08 - The fundamentals of eye tracking part 6.docx", "1WpfjSQVzfGjFSqzz0cSgoYOZTaHypcOR"),
    "Texte 10": ("10 - Conveying clinical reasoning based on visual observation.pdf", "1fUgjayUFALIzFcR34mlKUuRn_u0tixUd"),
    "Texte 11": ("11 - Seppanen_Gegenfurtner_2012_MedicalEducation.pdf", "1kfUGCbCXf6um-boKUf-7T6CzCMX1fqfk"),
    "Texte 12": ("12 - Using_dual_eye_tracking_to_uncover_personal_gaze_p.pdf", "1_WR8sBdnDiIjWbhhjz8VqO-q9jbfSJi1"),
    "Texte 13": ("13 - wohltjen_wheatley_PNAS_2021.pdf", "1YlBGQzA2bQdUXpOKyDcb9IGcno0po6L5"),
    "Texte 14": ("14 - The_Nature_of_Rapport_and_Its_Nonverbal_Correlates.pdf", "1atZQALH2d0Q2I4tsjSN_W8JDjVVcuJwa"),
    "Texte 15": ("15.a. - Are_All_Smiles_Created_Equal_How_Emotional_Contagi.pdf", "17a1zsoIaG8eTBzpxxJQhmgZSaywos8HI"),
    "Texte 16": ("16 - Front Desk Personnel Qualities and Skills in Applying Upselling Hotel Products.pdf", "1aSUbm9eQcRUhBVED61-bSYpJuKoltW9j"),
    "Texte 17": ("17 - Scott_2017_Areviewofeyetrackingresearch.pdf", "1C1_dEE94YxwJYz705AoaCQFFiN_1ivhR"),
    "Texte 19": ("21 - Teacher vision expert and novice teachers’ perception.pdf", "1U7nodFJtHP_saGMdamudFeQQ95F0U-6m"),
    "Texte 20": ("20 - Where Low and High Inference Data Converge.pdf", "1u5T2eXzK2mxlpIX5WhmAao77TYYgCtl7"),
    "Texte 22": ("22 - Origins and current issues in Quiet Eye research.pdf", "1hXznPjAdPPGs1m6MZ2ZUlHcvAVX5BkEz"),
    "Texte 23": ("23 - Vision (im)possible.pdf", "1xvbUDQ5LrW7sgZBMpcHYK4gTeiTudtuW"),
    "Texte 24.b": ("24.b - Automatic Analysis of In-the-Wild Mobile Eye-tracking Experiments.pdf", "1jFRsCwfS72bISrs43v7ewuBGIaxLkKll"),
    "Texte 25": ("25 - Online upselling Moving beyond offline upselling in the hotel industry.docx", "1sGG9c3pihIHaHiT3Vnrrh5fOSXMjnmwv"),
    "Texte 26": ("26 - Perrenoud.docx", "1LElcRhMKuY6xxUvmVhhX4RWvmLjg62iY"),
}

# Mapping table index -> texte key
TABLE_MAPPING = {
    1: "Texte 01",
    2: "Texte 02",
    3: "Texte 03",
    4: "Texte 04",
    5: "Texte 05",
    6: "Texte 06",
    7: "Texte 07",
    8: "Texte 08",
    9: "Texte 10",
    10: "Texte 11",
    11: "Texte 12",
    12: "Texte 13",
    13: "Texte 14",
    14: "Texte 15",
    15: "Texte 16",
    16: "Texte 17",
    17: "Texte 19",
    18: "Texte 20",
    19: "Texte 22",
    20: "Texte 23",
    21: "Texte 24.b",
    22: "Texte 25",
    23: "Texte 26",
}


def add_hyperlink_to_paragraph(paragraph, url, text, color="004C6D", bold=True):
    """Ajoute un lien hypertexte avec style dans un paragraphe."""
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    if color:
        c = OxmlElement('w:color')
        c.set(qn('w:val'), color)
        rPr.append(c)

    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    if bold:
        b = OxmlElement('w:b')
        rPr.append(b)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


def update_simaccueil_doc():
    print(f"Création de la sauvegarde de sécurité : {BACKUP_PATH}...")
    shutil.copy2(DOCX_PATH, BACKUP_PATH)

    doc = docx.Document(DOCX_PATH)

    print("\n1. Mise à jour des fiches analytiques détaillées (Tables 1 à 23)...")
    updated_fiches = 0
    for t_idx, txt_key in TABLE_MAPPING.items():
        fname, file_id = FILE_IDS[txt_key]
        direct_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

        table = doc.tables[t_idx]
        cell = table.rows[0].cells[0]
        # Le 2e paragraphe contient le lien vers Google Drive
        p_links = cell.paragraphs[1]

        # Chercher l'élément hyperlink vers Google Drive
        found = False
        for h in p_links._p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink'):
            r_id = h.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            if r_id and r_id in doc.part.rels:
                rel = doc.part.rels[r_id]
                if 'drive.google.com' in rel.target_ref:
                    rel._target = direct_url
                    found = True
                    break

        if found:
            updated_fiches += 1
            print(f"  ✅ {txt_key} (Table {t_idx:02d}) -> {direct_url}")
        else:
            print(f"  ⚠️ {txt_key} (Table {t_idx:02d}) : lien Drive non trouvé !")

    print(f"\nTotal fiches mises à jour : {updated_fiches} / 23")

    print("\n2. Mise à jour du Tableau Synthétique (Table 0)...")
    t0 = doc.tables[0]
    updated_t0 = 0
    for row_idx in range(1, len(t0.rows)):
        row = t0.rows[row_idx]
        cell_txt = row.cells[0].text.strip()
        if cell_txt in FILE_IDS:
            fname, file_id = FILE_IDS[cell_txt]
            direct_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

            # Remplacer le texte brut par un lien hypertexte direct cliquable
            p = row.cells[0].paragraphs[0]
            p.text = ""  # Vider le texte brut
            add_hyperlink_to_paragraph(p, direct_url, cell_txt, color="004C6D", bold=True)
            updated_t0 += 1
            print(f"  ✅ Table 0 Row {row_idx:02d} : {cell_txt} transformé en lien direct vers Google Drive")

    print(f"Total entrées Table 0 mises à jour : {updated_t0} / 23")

    print("\n3. Harmonisation des comptages (22 -> 23 Références)...")
    for p in doc.paragraphs:
        if "22 Références" in p.text:
            p.text = p.text.replace("22 Références", "23 Références")
            print(f"  ✅ Remplacé '22 Références' par '23 Références' dans paragraphe : {p.text[:60]}...")
        if "22 articles scientifiques" in p.text:
            p.text = p.text.replace("22 articles scientifiques", "23 articles scientifiques")
            print(f"  ✅ Remplacé '22 articles' par '23 articles' dans paragraphe : {p.text[:60]}...")

    doc.save(DOCX_PATH)
    print(f"\n✅ Document principal enregistré avec succès dans : {DOCX_PATH}")


if __name__ == "__main__":
    update_simaccueil_doc()
