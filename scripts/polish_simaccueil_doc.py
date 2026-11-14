import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.opc.constants import RELATIONSHIP_TYPE

DRIVE_DOC_PATH = r"C:\Google Drive\Prépas light\HECh\Projet recherche\SIMACCUEIL - PRojet de recherche.docx"
LOCAL_DOC_PATH = r"C:\Users\TrendingPC\.gemini\antigravity\scratch\Eye-Tracking\docs\SIMACCUEIL_Projet_de_recherche.docx"

HEX_NAVY = "1B365D"
HEX_TEAL = "0E86D4"
HEX_LIGHT_BG = "F4F6F9"
HEX_BOX_BG = "EDF2F7"

COLOR_NAVY = RGBColor(27, 54, 93)
COLOR_TEAL = RGBColor(14, 134, 212)
COLOR_CHARCOAL = RGBColor(44, 62, 80)
COLOR_MUTED = RGBColor(100, 110, 120)
COLOR_BLUE = RGBColor(17, 85, 204)

def style_cell(cell, bg_color=None, top_pad=80, bot_pad=80, left_pad=120, right_pad=120, border_left=None):
    tcPr = cell._tc.get_or_add_tcPr()
    if bg_color:
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        tcPr.append(shd)
    mar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top_pad}" w:type="dxa"/><w:bottom w:w="{bot_pad}" w:type="dxa"/><w:left w:w="{left_pad}" w:type="dxa"/><w:right w:w="{right_pad}" w:type="dxa"/></w:tcMar>')
    tcPr.append(mar)
    if border_left:
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="{border_left.get("sz", 24)}" w:space="0" w:color="{border_left.get("color", "1B365D")}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(borders)

def add_hyperlink(paragraph, text, url, color_rgb=COLOR_BLUE, underline=True, bold=False):
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = parse_xml(f'<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{r_id}"/>')
    new_run = parse_xml(f'<w:r {nsdecls("w")}><w:rPr/></w:r>')
    r_text = parse_xml(f'<w:t {nsdecls("w")}>{text}</w:t>')
    new_run.append(r_text)
    r_obj = docx.text.run.Run(new_run, paragraph)
    r_obj.font.name = "Calibri"
    r_obj.font.color.rgb = color_rgb
    r_obj.font.underline = underline
    r_obj.font.bold = bold
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

def create_fiche_box(doc, text_id, title, ref_apa, drive_file, drive_url, doi_url, resume, contribution):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    c.width = Inches(6.5)
    style_cell(c, bg_color=HEX_LIGHT_BG, top_pad=140, bot_pad=140, left_pad=180, right_pad=180, border_left={"sz": 24, "color": HEX_NAVY})
    
    p_t = c.paragraphs[0]
    p_t.paragraph_format.space_before = Pt(4)
    p_t.paragraph_format.space_after = Pt(8)
    r_t = p_t.add_run(f"{text_id} — {title}")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(11)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_NAVY

    p_m1 = c.add_paragraph()
    p_m1.paragraph_format.space_after = Pt(2)
    r_m1_l = p_m1.add_run("• Référence officielle (APA 7e) : ")
    r_m1_l.font.name = "Calibri"
    r_m1_l.font.size = Pt(8.5)
    r_m1_l.font.bold = True
    r_m1_l.font.color.rgb = COLOR_CHARCOAL
    r_m1_v = p_m1.add_run(ref_apa)
    r_m1_v.font.name = "Calibri"
    r_m1_v.font.size = Pt(8.5)
    r_m1_v.font.color.rgb = COLOR_MUTED

    p_m2 = c.add_paragraph()
    p_m2.paragraph_format.space_after = Pt(2)
    r_m2_l = p_m2.add_run("• 🔗 Liens d'accès direct : ")
    r_m2_l.font.name = "Calibri"
    r_m2_l.font.size = Pt(8.5)
    r_m2_l.font.bold = True
    r_m2_l.font.color.rgb = COLOR_CHARCOAL
    add_hyperlink(p_m2, "Accéder au fichier PDF (Google Drive)", drive_url, color_rgb=COLOR_BLUE, bold=True)
    r_sep = p_m2.add_run(" | ")
    r_sep.font.name = "Calibri"
    r_sep.font.size = Pt(8.5)
    r_sep.font.color.rgb = COLOR_MUTED
    add_hyperlink(p_m2, "Consulter l'article officiel (Lien DOI Éditeur)", doi_url, color_rgb=COLOR_TEAL, bold=False)

    p_m3 = c.add_paragraph()
    p_m3.paragraph_format.space_after = Pt(8)
    r_m3_l = p_m3.add_run("• Fichier source vérifié : ")
    r_m3_l.font.name = "Calibri"
    r_m3_l.font.size = Pt(8.5)
    r_m3_l.font.bold = True
    r_m3_l.font.color.rgb = COLOR_CHARCOAL
    r_m3_v = p_m3.add_run(f"{drive_file} (Dépôt Google Drive : Ressources)")
    r_m3_v.font.name = "Calibri"
    r_m3_v.font.size = Pt(8.5)
    r_m3_v.font.color.rgb = COLOR_MUTED

    p_r_t = c.add_paragraph()
    p_r_t.paragraph_format.space_after = Pt(2)
    r_rt = p_r_t.add_run("📖 Résumé de l'article (~100 mots)")
    r_rt.font.name = "Calibri"
    r_rt.font.size = Pt(9.5)
    r_rt.font.bold = True
    r_rt.font.color.rgb = COLOR_NAVY

    p_r = c.add_paragraph()
    p_r.paragraph_format.space_after = Pt(8)
    p_r.paragraph_format.line_spacing = 1.15
    r_r = p_r.add_run(resume)
    r_r.font.name = "Calibri"
    r_r.font.size = Pt(9)
    r_r.font.color.rgb = COLOR_CHARCOAL

    p_c_t = c.add_paragraph()
    p_c_t.paragraph_format.space_after = Pt(2)
    r_ct = p_c_t.add_run("🎯 Contribution méthodologique au projet SIMACCUEIL (~100 mots)")
    r_ct.font.name = "Calibri"
    r_ct.font.size = Pt(9.5)
    r_ct.font.bold = True
    r_ct.font.color.rgb = COLOR_TEAL

    p_c = c.add_paragraph()
    p_c.paragraph_format.space_after = Pt(4)
    p_c.paragraph_format.line_spacing = 1.15
    r_c = p_c.add_run(contribution)
    r_c.font.name = "Calibri"
    r_c.font.size = Pt(9)
    r_c.font.color.rgb = COLOR_CHARCOAL

    return tbl

def polish_doc():
    print("Loading:", DRIVE_DOC_PATH)
    doc = docx.Document(DRIVE_DOC_PATH)
    body = doc.element.body

    # 1. Harmoniser les titres de l'État de l'art (28 Références -> 25 Références retenues)
    for p in doc.paragraphs[:20]:
        if "Fiches Analytiques Détaillées (28 Références)" in p.text:
            for r in p.runs:
                if "28" in r.text:
                    r.text = r.text.replace("28 Références", "25 Références retenues, numérotées 01 à 28")
            print("Harmonized section 1.2 heading:", p.text)
        elif "Tableau Synthétique des 25 Références Retenues" in p.text:
            for r in p.runs:
                if "25 Références Retenues" in r.text:
                    r.text = r.text.replace("25 Références Retenues", "25 Références Retenues (numérotées 01 à 28)")
            print("Harmonized section 1.1 heading:", p.text)

    # 2. Séparer Texte 26 et Texte 27 (actuellement fusionnés dans doc.tables[23])
    t23 = doc.tables[23]
    if len(t23.rows) == 2 and "Texte 26" in t23.rows[0].cells[0].text and "Texte 27" in t23.rows[1].cells[0].text:
        print("Splitting merged Table 23 (Texte 26 + Texte 27)...")
        # Supprimer la 2e ligne de t23
        tr2 = t23.rows[1]._tr
        t23._tbl.remove(tr2)

        # Créer la fiche individuelle pour Texte 27
        temp_doc = docx.Document()
        t27_box = create_fiche_box(
            temp_doc,
            "Texte 27",
            "Activité du manager de réception à l’épreuve de la digitalisation : cas d’un projet d’accueil en mobilité dans une chaîne hôtelière internationale",
            "Flandrin, P., van de Leemput, C., & Hellemans, C. (2021). Activité du manager de réception à l’épreuve de la digitalisation : cas d’un projet d’accueil en mobilité dans une chaîne hôtelière internationale. Activités, 18(2), 1–28. https://doi.org/10.4000/activites.6760",
            "27 - Flandrin.pdf",
            "https://drive.google.com/file/d/1AJYJD8BBRfFuvyTXuiUwOMMK4l2g-sXp/view?usp=sharing",
            "https://doi.org/10.4000/activites.6760",
            (
                "Dans cet article d'ergonomie et de psychologie du travail, Pierre Flandrin et ses collègues analysent l'activité réelle "
                "du manager de réception et des équipes d'accueil au sein de trois établissements d'une chaîne hôtelière internationale "
                "confrontés à la digitalisation. Les auteurs étudient deux dimensions : la gestion quotidienne instrumentée (PMS, yield management, "
                "suivi des flux) et l'expérimentation d'un accueil « en mobilité » via smartphone. L'analyse révèle un effet controversé : la technologie "
                "renforce les contraintes gestionnaires et le contrôle procédural, tout en réduisant les marges de manœuvre des salariés. "
                "Face à cette rigidité, les managers multiplient les régulations et les simulations pour tenter de préserver l'autonomie et le travail émotionnel des réceptionnistes."
            ),
            (
                "Cet article apporte à SIMACCUEIL un ancrage empirique direct en réception hôtelière francophone. Flandrin et al. documentent "
                "la tension structurelle entre l'encadrement logiciel (écrans, procédures) et la relation humaine en face-à-face, qu'ils mesuraient "
                "jusqu'alors par l'observation vidéo des mouvements de tête. SIMACCUEIL franchit un cap méthodologique décisif en substituant "
                "à ces approximations la précision biométrique des lunettes Pupil Labs Neon, quantifiant au millième de seconde les bascules attentionnelles "
                "entre l'outil numérique (tablette, PMS) et le visage du voyageur. En outre, leurs préconisations sur la coconception amont et la simulation "
                "dynamique confortent pleinement la modélisation de nos scénarios de négociation commerciale et de réclamation client."
            )
        )
        p_space = parse_xml(f'<w:p {nsdecls("w")}><w:pPr><w:spacing w:after="240"/></w:pPr></w:p>')
        t23._tbl.addnext(p_space)
        p_space.addnext(t27_box._tbl)
        print("Split Texte 26 and Texte 27 into two separate boxed tables!")

    # 3. Ajouter la Synthèse Problématisée (1.3) et Questions de Recherche juste avant Section 2
    sec2_start = None
    for p in doc.paragraphs:
        if p.text.startswith("2. Cadre Méthodologique Opérationnel"):
            sec2_start = p._p
            break

    # Vérifier si 1.3 n'existe pas déjà
    has_13 = any("1.3. Synthèse Problématisée" in p.text for p in doc.paragraphs)
    if sec2_start is not None and not has_13:
        print("Inserting Section 1.3 (Synthèse Problématisée & Questions de Recherche)...")
        def ins_p(text="", space_before=Pt(0), space_after=Pt(6), bold=False, size=Pt(10), color=COLOR_CHARCOAL, italic=False):
            p_xml = parse_xml(f'<w:p {nsdecls("w")}/>')
            sec2_start.addprevious(p_xml)
            p_obj = docx.text.paragraph.Paragraph(p_xml, doc)
            p_obj.paragraph_format.space_before = space_before
            p_obj.paragraph_format.space_after = space_after
            p_obj.paragraph_format.line_spacing = 1.15
            if text:
                r = p_obj.add_run(text)
                r.font.name = "Calibri"
                r.font.size = size
                r.font.bold = bold
                r.font.italic = italic
                r.font.color.rgb = color
            return p_obj

        ins_p("1.3. Synthèse Problématisée de l'État de l'Art et Questions de Recherche", space_before=Pt(16), space_after=Pt(8), bold=True, size=Pt(12.5), color=COLOR_TEAL)

        ins_p(
            "Au terme de cette revue de la littérature structurée autour de 25 travaux de référence, un constat transversal s'impose : l'activité de réception hôtelière contemporaine se situe à l'intersection de trois tensions majeures rarement étudiées de manière intégrée."
        )

        ins_p(
            "Premièrement, sur le plan ergonomique et organisationnel, la digitalisation accélérée des comptoirs d'accueil (PMS, tablettes mobiles, outils de yield management) transforme profondément le métier (Flandrin et al., 2021 ; Denizci Guillet, 2020 ; Ruki, 2023). Loin de libérer mécaniquement du temps relationnel, les interfaces numériques introduisent de nouvelles contraintes procédurales et une charge cognitive accrue (Beckmann, 2010), plaçant le professionnel dans une situation permanente d'attention partagée entre l'écran et le voyageur. Cette tension s'accompagne d'un travail émotionnel intense (Giacomel, 2019 ; Hennig-Thurau et al., 2006), particulièrement lors de la gestion des imprévus ou des réclamations, où le professionnel doit maintenir son homéostasie émotionnelle tout en préservant la qualité du rapport interpersonnel (Tickle-Degnen & Rosenthal, 1990)."
        )

        ins_p(
            "Deuxièmement, sur le plan cognitif et pédagogique, les travaux sur l'expertise visuelle (Goodwin, 1994 ; Gegenfurtner et al., 2011 ; Wolff et al., 2016) et l'analyse du cours d'action (Theureau, 2015 ; Crandall et al., 2006) démontrent que les professionnels expérimentés mobilisent une « vision professionnelle » largement implicite. Ils savent prélever rapidement les indices pertinents sur leur environnement sans rompre la continuité de l'interaction. Or, ces savoirs perceptifs tacites demeurent difficiles à objectiver et à transmettre dans les formations classiques sans recourir à des dispositifs de mise en visibilité du regard (Van Gog et al., 2009 ; Jarodzka et al., 2012) et à une démarche réflexive structurée (Perrenoud, 2001)."
        )

        ins_p(
            "Troisièmement, sur le plan méthodologique, l'essor de l'oculométrie mobile et des protocoles dyadiques (Rogers et al., 2018 ; Wohltjen & Wheatley, 2021 ; Hooge et al., 2026) ouvre une voie inédite. Alors que la quasi-totalité des recherches en hôtellerie et tourisme se limitent encore à l'observation externe, à des entretiens rétrospectifs ou à des tests d'utilisabilité sur écran fixe (Scott et al., 2017), l'équipement simultané des deux interlocuteurs permet enfin de capter la dynamique réciproque du regard en situation écologique."
        )

        ins_p(
            "Le chaînon manquant (Research Gap) identifié par cet état de l'art réside précisément dans le couplage entre l'oculométrie mobile dyadique et l'analyse réflexive située au sein de micro-situations instrumentées de réception hôtelière. C'est pour combler ce vide scientifique et pédagogique que le projet SIMACCUEIL formule trois questions de recherche exploratoires :",
            bold=False
        )

        # Encadré Questions de Recherche
        tbl_qr = doc.add_table(rows=1, cols=1)
        tbl_qr.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_qr = tbl_qr.rows[0].cells[0]
        c_qr.width = Inches(6.5)
        style_cell(c_qr, bg_color=HEX_BOX_BG, top_pad=120, bot_pad=120, left_pad=180, right_pad=180, border_left={"sz": 24, "color": HEX_TEAL})
        p_qt = c_qr.paragraphs[0]
        p_qt.paragraph_format.space_after = Pt(6)
        r_qt = p_qt.add_run("Questions de Recherche Exploratoires (SIMACCUEIL)")
        r_qt.font.name = "Calibri"
        r_qt.font.size = Pt(10.5)
        r_qt.font.bold = True
        r_qt.font.color.rgb = COLOR_NAVY

        qrs = [
            ("QR1 (Dynamique attentionnelle dyadique) : ", "Comment les bascules attentionnelles et les épisodes de regard mutuel (eye contact) s'organisent-ils entre le réceptionniste et le client selon la nature de l'outil numérique mobilisé (co-attention sur tablette partagée vs attention divisée lors de l'encodage sur logiciel PMS) ?"),
            ("QR2 (Charge cognitive et travail émotionnel) : ", "Dans quelle mesure les indicateurs oculométriques (durées de fixation sur écran, latences de réengagement visuel, évitements du regard) permettent-ils d'objectiver les points de friction ergonomiques et les stratégies de régulation émotionnelle face aux demandes complexes ou réclamations ?"),
            ("QR3 (Faisabilité et transfert formatif) : ", "Comment l'autoconfrontation à ces traces visuelles dyadiques synchronisées soutient-elle l'explicitation des savoirs professionnels implicites et la conception de dispositifs de formation innovants pour le secteur hôtelier ?")
        ]
        for q_prefix, q_txt in qrs:
            pq = c_qr.add_paragraph()
            pq.paragraph_format.space_after = Pt(4)
            pq.paragraph_format.line_spacing = 1.15
            rq1 = pq.add_run("• " + q_prefix)
            rq1.font.name = "Calibri"
            rq1.font.size = Pt(9.5)
            rq1.font.bold = True
            rq1.font.color.rgb = COLOR_NAVY
            rq2 = pq.add_run(q_txt)
            rq2.font.name = "Calibri"
            rq2.font.size = Pt(9.5)
            rq2.font.color.rgb = COLOR_CHARCOAL

        sec2_start.addprevious(tbl_qr._tbl)
        ins_p("", space_after=Pt(6))
        print("Inserted Section 1.3 and Research Questions box!")

    # 4. Restaurer la phrase complète du Point 2 dans Section 2.6
    for p in doc.paragraphs:
        if "2. Ingénierie de Formation Hôtelière Haute Performance" in p.text and "Horeca Formation" not in p.text:
            p.text = ""
            r_b = p.add_run("• 2. Ingénierie de Formation Hôtelière Haute Performance (Initiale et Continue) : ")
            r_b.font.name = "Calibri"
            r_b.font.size = Pt(10)
            r_b.font.bold = True
            r_b.font.color.rgb = COLOR_CHARCOAL
            r_t = p.add_run(
                "Pour le département des sciences économiques et de gestion hôtelière de la HECh, SIMACCUEIL fournira des modules de micro-learning "
                "directement intégrables dans les cursus de Bachelier. En formation continue pour adultes, ces ressources seront mises à disposition "
                "des structures de formation sectorielle (notamment les centres de compétences Horeca Formation Wallonie et Bruxelles) pour former "
                "le personnel en poste aux bonnes pratiques d'accueil instrumenté."
            )
            r_t.font.name = "Calibri"
            r_t.font.size = Pt(10)
            r_t.font.color.rgb = COLOR_CHARCOAL
            print("Restored full text of Point 2 in Section 2.6!")

    # 5. Nettoyer la Bibliographie : supprimer Nolte (2026) et classer Giacomel (2019) par ordre alphabétique
    bib_heading = None
    for p in doc.paragraphs:
        if p.text.strip().startswith("Bibliographie"):
            bib_heading = p._p
            break

    if bib_heading is not None:
        print("Cleaning and sorting Bibliography...")
        # Supprimer Nolte et Giacomel existants
        curr = bib_heading.getnext()
        giacomel_elem = None
        goodwin_elem = None
        to_remove_bib = []
        while curr is not None:
            if curr.tag.endswith('p'):
                t_nodes = curr.xpath('.//w:t')
                txt = ''.join([t.text for t in t_nodes])
                if txt.startswith("Nolte, D."):
                    to_remove_bib.append(curr)
                elif txt.startswith("Giacomel, A."):
                    giacomel_elem = curr
                elif txt.startswith("Goodwin, C."):
                    goodwin_elem = curr
            curr = curr.getnext()

        for elem in to_remove_bib:
            body.remove(elem)
            print("Removed Nolte et al. (2026) from Bibliography.")

        if giacomel_elem is not None and goodwin_elem is not None:
            body.remove(giacomel_elem)
            goodwin_elem.addprevious(giacomel_elem)
            print("Moved Giacomel, A. (2019) before Goodwin, C. (1994) in Bibliography.")

    # Sauvegarde
    os.makedirs(os.path.dirname(LOCAL_DOC_PATH), exist_ok=True)
    doc.save(LOCAL_DOC_PATH)
    print("✅ Saved locally:", LOCAL_DOC_PATH)

    try:
        shutil.copy2(LOCAL_DOC_PATH, DRIVE_DOC_PATH)
        print("✅ Copied to Google Drive:", DRIVE_DOC_PATH)
    except PermissionError:
        alt = DRIVE_DOC_PATH.replace(".docx", " (Mis a jour).docx")
        shutil.copy2(LOCAL_DOC_PATH, alt)
        print("⚠️ Drive file locked, saved as:", alt)

if __name__ == "__main__":
    polish_doc()
