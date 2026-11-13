"""
Script d'intégration du Texte 27 (Flandrin, van de Leemput & Hellemans, 2021) dans :
C:\\Google Drive\\Prépas light\\HECh\\Projet recherche\\SIMACCUEIL - PRojet de recherche.docx
"""
import copy
import os
import shutil
import sys
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DOCX_PATH = r"C:\Google Drive\Prépas light\HECh\Projet recherche\SIMACCUEIL - PRojet de recherche.docx"
BACKUP_PATH = r"C:\Google Drive\Prépas light\HECh\Projet recherche\SIMACCUEIL - PRojet de recherche.backup.docx"

TEXTE_ID = "Texte 27"
DRIVE_URL = "https://drive.google.com/file/d/1AJYJD8BBRfFuvyTXuiUwOMMK4l2g-sXp/view?usp=sharing"
DOI_URL = "https://doi.org/10.4000/activites.6760"

AUTEURS = "Flandrin, P., van de Leemput, C., & Hellemans, C."
ANNEE = "2021"
TITRE = "Activité du manager de réception à l’épreuve de la digitalisation : cas d’un projet d’accueil en mobilité dans une chaîne hôtelière internationale"
REVUE = "Activités, 18(2), 1–28"

RESUME = (
    "Dans cet article d'ergonomie et de psychologie du travail, Pierre Flandrin et ses collègues analysent l'activité réelle "
    "du manager de réception et des équipes d'accueil au sein de trois établissements d'une chaîne hôtelière internationale "
    "confrontés à la digitalisation. Les auteurs étudient deux dimensions : la gestion quotidienne instrumentée (PMS, yield management, "
    "suivi des flux) et l'expérimentation d'un accueil « en mobilité » via smartphone. L'analyse révèle un effet controversé : la technologie "
    "renforce les contraintes gestionnaires et le contrôle procédural, tout en réduisant les marges de manœuvre des salariés. "
    "Face à cette rigidité, les managers multiplient les régulations et les simulations pour tenter de préserver l'autonomie et le travail émotionnel des réceptionnistes."
)

CONTRIBUTION = (
    "Cet article apporte à SIMACCUEIL un ancrage empirique direct en réception hôtelière francophone. Flandrin et al. documentent "
    "la tension structurelle entre l'encadrement logiciel (écrans, procédures) et la relation humaine en face-à-face, qu'ils mesuraient "
    "jusqu'alors par l'observation vidéo des mouvements de tête. SIMACCUEIL franchit un cap méthodologique décisif en substituant "
    "à ces approximations la précision biométrique des lunettes Pupil Labs Neon, quantifiant au millième de seconde les bascules attentionnelles "
    "entre l'outil numérique (tablette, PMS) et le visage du voyageur. En outre, leurs préconisations sur la coconception amont et la simulation "
    "dynamique confortent pleinement la modélisation de nos scénarios de négociation commerciale et de réclamation client."
)


def add_hyperlink(paragraph, url, text, color="004C6D", bold=True, underline=True, font_size=Pt(9.5)):
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

    if underline:
        u = OxmlElement('w:u')
        u.set(qn('w:val'), 'single')
        rPr.append(u)

    if bold:
        b = OxmlElement('w:b')
        rPr.append(b)

    if font_size:
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(int(font_size.pt * 2)))
        rPr.append(sz)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


def style_cell(cell, bg_color=None, top_pad=60, bot_pad=60, left_pad=80, right_pad=80):
    tcPr = cell._tc.get_or_add_tcPr()
    if bg_color:
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{bg_color}"/>')
        tcPr.append(shd)
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top_pad}" w:type="dxa"/><w:bottom w:w="{bot_pad}" w:type="dxa"/><w:left w:w="{left_pad}" w:type="dxa"/><w:right w:w="{right_pad}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)


def run_update():
    print(f"1. Sauvegarde de sécurité dans : {BACKUP_PATH}...")
    shutil.copy2(DOCX_PATH, BACKUP_PATH)

    doc = docx.Document(DOCX_PATH)

    # 1. Mise à jour de la table de synthèse (Table 0)
    print("\n2. Ajout de la ligne Texte 27 dans le Tableau Synthétique (Table 0)...")
    t0 = doc.tables[0]
    row = t0.add_row()
    style_cell(row.cells[0], bg_color="FFFFFF")
    style_cell(row.cells[1], bg_color="FFFFFF")
    style_cell(row.cells[2], bg_color="FFFFFF")

    p0 = row.cells[0].paragraphs[0]
    p0.text = ""
    add_hyperlink(p0, DRIVE_URL, TEXTE_ID, color="004C6D", bold=True, underline=True, font_size=Pt(8.5))

    p1 = row.cells[1].paragraphs[0]
    p1.text = ""
    r1 = p1.add_run(f"{AUTEURS} ({ANNEE})")
    r1.font.size = Pt(8.5)

    p2 = row.cells[2].paragraphs[0]
    p2.text = ""
    r2 = p2.add_run(f"« {TITRE} »")
    r2.font.size = Pt(8)
    print("  ✅ Ligne Texte 27 ajoutée avec succès dans Table 0.")

    # 2. Ajout de la fiche détaillée pour Texte 27 (Table 24)
    print("\n3. Création de la fiche analytique détaillée pour Texte 27...")
    t23 = doc.tables[23]
    # Duplication propre de l'élément XML de la table 23
    new_tbl_element = copy.deepcopy(t23._tbl)
    # Insérer new_tbl_element immédiatement après t23 dans l'arbre XML
    t23._tbl.addnext(new_tbl_element)

    # Récupérer la nouvelle table sous forme d'objet Table python-docx
    new_table = docx.table.Table(new_tbl_element, doc)
    cell = new_table.rows[0].cells[0]

    # Vider les paragraphes clonés pour les remplacer par le contenu de Texte 27
    for p in cell.paragraphs:
        p._p.getparent().remove(p._p)

    # Paragraphe 0 : Titre et référence
    p_title = cell.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(4)
    r_head = p_title.add_run(f"Texte 27 — {TITRE}\n")
    r_head.font.name = "Calibri"
    r_head.font.size = Pt(11)
    r_head.font.bold = True
    r_head.font.color.rgb = RGBColor(27, 54, 93)

    r_ref = p_title.add_run(f"Référence officielle : {AUTEURS} ({ANNEE}). {TITRE}. {REVUE}.\n")
    r_ref.font.italic = True
    r_ref.font.size = Pt(9.5)
    r_ref.font.color.rgb = RGBColor(100, 110, 120)

    # Paragraphe 1 : Liens ressources
    p_links = cell.add_paragraph()
    p_links.paragraph_format.space_after = Pt(8)
    r_lnk_lbl = p_links.add_run("🔗 Accès aux ressources : ")
    r_lnk_lbl.font.bold = True
    r_lnk_lbl.font.size = Pt(9.5)
    r_lnk_lbl.font.color.rgb = RGBColor(44, 62, 80)

    add_hyperlink(p_links, DRIVE_URL, "Fichier Google Drive (27 - Flandrin.pdf...)", color="1155CC", bold=False, underline=True, font_size=Pt(9.5))
    r_sep = p_links.add_run("  |  ")
    r_sep.font.size = Pt(9.5)
    add_hyperlink(p_links, DOI_URL, "Lien Éditeur (DOI : 10.4000/activites.6760)", color="1155CC", bold=False, underline=True, font_size=Pt(9.5))

    # Paragraphe 2 : Résumé (~100 mots)
    p_res = cell.add_paragraph()
    p_res.paragraph_format.space_after = Pt(6)
    r_res_t = p_res.add_run("📖 Résumé de l'article (~100 mots) :\n")
    r_res_t.font.bold = True
    r_res_t.font.size = Pt(10)
    r_res_t.font.color.rgb = RGBColor(27, 54, 93)
    r_res_b = p_res.add_run(RESUME)
    r_res_b.font.size = Pt(10)
    r_res_b.font.color.rgb = RGBColor(44, 62, 80)

    # Paragraphe 3 : Contribution (~100 mots)
    p_con = cell.add_paragraph()
    p_con.paragraph_format.space_after = Pt(4)
    r_con_t = p_con.add_run("🎯 Contribution méthodologique au projet SIMACCUEIL (~100 mots) :\n")
    r_con_t.font.bold = True
    r_con_t.font.size = Pt(10)
    r_con_t.font.color.rgb = RGBColor(14, 134, 212)
    r_con_b = p_con.add_run(CONTRIBUTION)
    r_con_b.font.size = Pt(10)
    r_con_b.font.color.rgb = RGBColor(44, 62, 80)

    print("  ✅ Fiche détaillée Texte 27 créée et insérée après Texte 26.")

    # 3. Mise à jour des en-têtes et comptages dans les paragraphes
    print("\n4. Harmonisation des comptages (23 -> 24 Références)...")
    for p in doc.paragraphs:
        if "23 Références" in p.text:
            p.text = p.text.replace("23 Références", "24 Références")
            print(f"  ✅ Remplacé par '24 Références' : {p.text[:60]}")
        if "23 articles scientifiques" in p.text:
            p.text = p.text.replace("23 articles scientifiques", "24 articles scientifiques")
            print(f"  ✅ Remplacé par '24 articles' : {p.text[:60]}")

    # 4. Ajout de la référence dans la bibliographie finale
    print("\n5. Ajout de Flandrin et al. (2021) dans la bibliographie finale...")
    bib_inserted = False
    for i, p in enumerate(doc.paragraphs):
        if p.text.startswith("Elling, S., Lentz, L."):
            # Insérer après Elling
            p_flandrin = p._p.addnext(parse_xml(
                f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                f'<w:pPr><w:pStyle w:val="Normal"/></w:pPr>'
                f'<w:r><w:t>Flandrin, P., van de Leemput, C., &amp; Hellemans, C. (2021). Activité du manager de réception à l’épreuve de la digitalisation : cas d’un projet d’accueil en mobilité dans une chaîne hôtelière internationale. Activités, 18(2), 1–28. https://doi.org/10.4000/activites.6760</w:t></w:r>'
                f'</w:p>'
            ))
            bib_inserted = True
            print(f"  ✅ Référence bibliographique insérée alphabétiquement après Elling (P{i}).")
            break

    if not bib_inserted:
        p_last = doc.add_paragraph(f"{AUTEURS} ({ANNEE}). {TITRE}. {REVUE}. {DOI_URL}")
        print("  ✅ Référence bibliographique ajoutée en fin de document.")

    doc.save(DOCX_PATH)
    print(f"\n✅ Document principal sauvegardé avec succès dans : {DOCX_PATH}")


if __name__ == "__main__":
    run_update()
