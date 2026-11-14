import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.opc.constants import RELATIONSHIP_TYPE

DRIVE_DOC_PATH = r"C:\Google Drive\Prépas light\HECh\Projet recherche\SIMACCUEIL - PRojet de recherche.docx"
LOCAL_DOC_PATH = r"C:\Users\TrendingPC\.gemini\antigravity\scratch\Eye-Tracking\docs\SIMACCUEIL_Projet_de_recherche.docx"

HEX_NAVY = "1B365D"
HEX_TEAL = "0E86D4"
HEX_LIGHT_BG = "F4F6F9"
HEX_BORDER = "D1D5DB"
HEX_ALT_ROW = "F9FAFC"

COLOR_NAVY = RGBColor(27, 54, 93)
COLOR_TEAL = RGBColor(14, 134, 212)
COLOR_CHARCOAL = RGBColor(44, 62, 80)
COLOR_MUTED = RGBColor(100, 110, 120)
COLOR_BLUE = RGBColor(17, 85, 204)

def style_cell(cell, bg_color=None, top_pad=80, bot_pad=80, left_pad=120, right_pad=120, border_bottom=None, border_left=None):
    tcPr = cell._tc.get_or_add_tcPr()
    if bg_color:
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        tcPr.append(shd)
    mar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top_pad}" w:type="dxa"/><w:bottom w:w="{bot_pad}" w:type="dxa"/><w:left w:w="{left_pad}" w:type="dxa"/><w:right w:w="{right_pad}" w:type="dxa"/></w:tcMar>')
    tcPr.append(mar)
    if border_bottom:
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="{border_bottom.get("sz", 4)}" w:space="0" w:color="{border_bottom.get("color", "D1D5DB")}"/></w:tcBorders>')
        tcPr.append(borders)
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

def build_simaccueil():
    print("Loading original document:", DRIVE_DOC_PATH)
    doc = docx.Document(DRIVE_DOC_PATH)

    # 1. Mise à jour des nombres dans l'introduction (24 -> 25)
    for p in doc.paragraphs[:15]:
        if "24" in p.text:
            p.text = p.text.replace("24 Références", "25 Références").replace("24 articles", "25 articles")
            print("Updated intro text:", p.text[:60])

    # 2. Mise à jour de la Table 0 (Tableau récapitulatif)
    t0 = doc.tables[0]
    has_28 = any("Texte 28" in row.cells[0].text for row in t0.rows)
    if not has_28:
        print("Adding row for Texte 28 in Table 0...")
        row = t0.add_row()
        bg = HEX_ALT_ROW if len(t0.rows) % 2 == 1 else "FFFFFF"
        drive_url_28 = "https://drive.google.com/file/d/1_IsYCXnvIa78QmbN_q98V-3bEwk-i5D_/view?usp=sharing"
        doi_url_28 = "https://doi.org/10.4000/tourisme.2471"
        
        # Col 0: N° Réf
        c0 = row.cells[0]
        c0.width = Inches(1.0)
        style_cell(c0, bg_color=bg, top_pad=70, bot_pad=70, left_pad=90, right_pad=90, border_bottom={"sz": 4, "color": HEX_BORDER})
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_hyperlink(p0, "Texte 28", drive_url_28, color_rgb=COLOR_BLUE, bold=True)
        
        # Col 1: Auteurs & Année
        c1 = row.cells[1]
        c1.width = Inches(1.8)
        style_cell(c1, bg_color=bg, top_pad=70, bot_pad=70, left_pad=90, right_pad=90, border_bottom={"sz": 4, "color": HEX_BORDER})
        p1 = c1.paragraphs[0]
        r1 = p1.add_run("Giacomel, A. (2019)")
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_CHARCOAL
        
        # Col 2: Titre & Cadre
        c2 = row.cells[2]
        c2.width = Inches(3.7)
        style_cell(c2, bg_color=bg, top_pad=70, bot_pad=70, left_pad=90, right_pad=90, border_bottom={"sz": 4, "color": HEX_BORDER})
        p2 = c2.paragraphs[0]
        r2_t = p2.add_run("« Les enjeux du travail émotionnel individuel et collectif dans les groupes hôteliers multinationaux : La complexité de l’équilibre émotionnel au service de l’homéostasie organisationnelle »\n")
        r2_t.font.name = "Calibri"
        r2_t.font.size = Pt(8.5)
        r2_t.font.bold = True
        r2_t.font.color.rgb = COLOR_NAVY
        add_hyperlink(p2, "🌐 Lien DOI Mondes du Tourisme", doi_url_28, color_rgb=COLOR_TEAL, bold=False)

    # 3. Insertion de la Fiche Analytique pour Texte 28
    body = doc.element.body
    tbl_27_elem = None
    for child in body:
        if child.tag.endswith('tbl'):
            text_nodes = child.xpath('.//w:t')
            t_str = ''.join([t.text for t in text_nodes[:10]])
            if "Texte 27" in t_str:
                tbl_27_elem = child
                break
    
    temp_doc = docx.Document()
    t28_box = create_fiche_box(
        temp_doc,
        "Texte 28",
        "Les enjeux du travail émotionnel individuel et collectif dans les groupes hôteliers multinationaux : La complexité de l’équilibre émotionnel au service de l’homéostasie organisationnelle",
        "Giacomel, A. (2019). Les enjeux du travail émotionnel individuel et collectif dans les groupes hôteliers multinationaux : La complexité de l’équilibre émotionnel au service de l’homéostasie organisationnelle. Mondes du Tourisme, 16. https://doi.org/10.4000/tourisme.2471",
        "28 - Giacomel.pdf",
        "https://drive.google.com/file/d/1_IsYCXnvIa78QmbN_q98V-3bEwk-i5D_/view?usp=sharing",
        "https://doi.org/10.4000/tourisme.2471",
        (
            "Issue d'une recherche doctorale menée dans cinq établissements Novotel parisiens (60 entretiens et observations directes), "
            "cette étude d'Aurore Giacomel explore le travail émotionnel (TE) individuel et collectif des équipes de réception et de restauration. "
            "L'auteure dépasse la dichotomie classique entre jeu en surface et jeu en profondeur d'Hochschild, montrant que les réceptionnistes "
            "mobilisent deux processus clés : le blocage immédiat des émotions négatives du client par routine protectrice et l'absorption émotionnelle "
            "avec régulation différée. L'article modélise un équilibre dynamique où l'homéostasie organisationnelle concilie le bien-être "
            "psychologique des professionnels et l'exigence de flexibilité et d'hyper-personnalisation du service hôtelier."
        ),
        (
            "Cet article fournit à SIMACCUEIL le cadre théorique pour interpréter les marqueurs oculométriques du travail émotionnel "
            "lors des simulations d'accueil hôtelier. Dans la micro-situation de gestion de réclamation client, le protocole dyadique permet "
            "d'objectiver les moments où le réceptionniste régule ses émotions face aux tensions verbales : évitement visuel défensif, "
            "fixation refuge sur l'écran du PMS ou maintien d'un regard engageant (eye contact). Le croisement des données d'eye-tracking "
            "(durées de fixation visage, dilatation pupillaire liée à la charge affective) avec les verbalisations en autoscopie permet "
            "d'analyser comment l'interaction instrumentée soutient ou fragilise l'équilibre émotionnel du professionnel face aux imprévus du service."
        )
    )
    t28_elem = t28_box._tbl

    if tbl_27_elem is not None:
        p_space = parse_xml(f'<w:p {nsdecls("w")}><w:pPr><w:spacing w:after="240"/></w:pPr></w:p>')
        tbl_27_elem.addnext(p_space)
        p_space.addnext(t28_elem)
        print("Inserted Fiche 28 table successfully after Texte 27!")

    # 4. Nettoyage de l'ancienne Section 2 et Remplacement par la Méthodologie Complète Révisée
    start_sec2_elem = None
    biblio_elem = None
    for child in body:
        if child.tag.endswith('p'):
            t_nodes = child.xpath('.//w:t')
            p_text = ''.join([t.text for t in t_nodes])
            if "Proposition de méthodologie" in p_text or "2. Cadre Méthodologique" in p_text:
                start_sec2_elem = child
            elif "Bibliographie" in p_text and biblio_elem is None:
                biblio_elem = child

    if start_sec2_elem is not None and biblio_elem is not None:
        print("Found boundaries of Section 2. Removing old content...")
        to_remove = []
        curr = start_sec2_elem
        while curr is not None and curr != biblio_elem:
            nxt = curr.getnext()
            to_remove.append(curr)
            curr = nxt
        
        for elem in to_remove:
            body.remove(elem)
        print(f"Removed {len(to_remove)} old Section 2 elements.")

    insert_point = biblio_elem

    def insert_p(text="", style=None, space_before=Pt(0), space_after=Pt(6), line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT):
        nonlocal insert_point
        p = parse_xml(f'<w:p {nsdecls("w")}/>')
        insert_point.addprevious(p)
        p_obj = docx.text.paragraph.Paragraph(p, doc)
        if style:
            p_obj.style = style
        p_obj.paragraph_format.space_before = space_before
        p_obj.paragraph_format.space_after = space_after
        p_obj.paragraph_format.line_spacing = line_spacing
        p_obj.alignment = align
        if text:
            r = p_obj.add_run(text)
            r.font.name = "Calibri"
        return p_obj

    def insert_heading(text, level=1):
        if level == 1:
            p = insert_p(text=text, space_before=Pt(18), space_after=Pt(10))
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
        elif level == 2:
            p = insert_p(text=text, space_before=Pt(14), space_after=Pt(6))
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(12.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_TEAL
        elif level == 3:
            p = insert_p(text=text, space_before=Pt(10), space_after=Pt(4))
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_CHARCOAL
        return p

    def insert_list_item(bold_prefix, text):
        p = insert_p(space_before=Pt(2), space_after=Pt(4))
        p.paragraph_format.left_indent = Inches(0.25)
        r_b = p.add_run(f"• {bold_prefix} : ")
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(10)
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_CHARCOAL
        r_t = p.add_run(text)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = COLOR_CHARCOAL
        return p

    def insert_tbl(tbl_obj):
        nonlocal insert_point
        insert_point.addprevious(tbl_obj._tbl)

    print("Building comprehensive Section 2...")

    # TITRE PRINCIPAL SECTION 2
    insert_heading("2. Cadre Méthodologique Opérationnel : Dispositif de Simulation Dyadique par Eye-Tracking Mobile et Valorisation Sectorielle", level=1)

    # 2.1 CADRAGE SCIENTIFIQUE ET REPOSITIONNEMENT
    insert_heading("2.1. Cadrage Scientifique et Repositionnement sur le Protocole Soumis (AiàP 26)", level=2)
    
    insert_p("Le projet SIMACCUEIL s'inscrit au cœur des défis contemporains de l'accueil et de la relation de service hôtelière. Les interactions au comptoir de réception constituent un terrain d'observation d'une grande complexité cognitive et relationnelle : le professionnel doit continuellement orchestrer son attention entre la présence bienveillante envers l'interlocuteur, le traitement d'une demande transactionnelle, la consultation de documents partagés et l'encodage précis sur des interfaces logicielles (PMS, yield management, tablettes numériques).")
    
    insert_p("Le constat de départ de cette recherche repose sur une limite méthodologique majeure identifiée dans la littérature : ces dynamiques attentionnelles fines et distribuées demeurent impossibles à objectiver précisément par les seuls entretiens a posteriori, les questionnaires ou l'observation vidéo externe. Ces méthodes traditionnelles n'enregistrent que des approximations posturales ou des reconstructions discursives, sans jamais accéder à la coordination temporelle et spatiale du regard en temps réel.")

    insert_p("Pour surmonter cette barrière, SIMACCUEIL adopte une approche résolument novatrice en mobilisant l'oculométrie mobile dyadique. Contrairement aux études classiques observant un travailleur isolé ou un écran fixe, notre dispositif équipe simultanément deux participants — un réceptionniste et un client — de lunettes d'eye-tracking mobile de dernière génération (Pupil Labs Neon). Cette captation conjointe permet de documenter en miroir la scène visuelle subjective de chacun des deux acteurs, et d'analyser scientifiquement la manière dont leurs attentions s'articulent, se synchronisent ou décrochent au fil de l'interaction.")

    insert_p("Conformément à la proposition soumise et validée dans le cadre de l'Appel Interne à Projet (AiàP 26 - SimAccueil V2), la présente phase ne prétend pas déployer immédiatement une étude quantitative de masse. Elle constitue une démarche exploratoire rigoureuse de faisabilité et de structuration méthodologique. L'objectif est de stabiliser les protocoles de passation, d'ajuster les scénarios réalistes, de valider l'infrastructure technique de synchronisation temporelle sub-5 millisecondes, d'établir les garanties éthiques et de concevoir des outils réutilisables pour la formation hôtelière et pour un déploiement futur à large échelle (projet FRHE).")

    # 2.2 LES DEUX MICRO-SITUATIONS
    insert_heading("2.2. Les Deux Micro-Situations Standardisées Centrées sur les Écrans", level=2)

    insert_p("Afin d'isoler les composantes clés de l'interaction instrumentée tout en garantissant une comparabilité scientifique stricte entre les dyades, le protocole repose sur deux micro-situations standardisées d'une durée de 5 à 7 minutes chacune, représentatives du quotidien professionnel de la réception hôtelière :")

    insert_list_item(
        "Micro-situation 1 : Co-attention sur support numérique partagé (Tablette / Upselling commercial)",
        "Dans cette scène de conseil et de vente incitative, le réceptionniste et le client consultent conjointement une information présentée sur une tablette numérique interactive (catalogue d'options de surclassement de chambre, forfaits bien-être, recommandations d'excursions touristiques locales). L'enjeu méthodologique est d'analyser la dynamique d'attention conjointe (joint attention) : comment le professionnel guide-t-il le regard du client à travers l'interface tactile tout en préservant le contact visuel mutuel (eye contact) ? Les travaux de Wohltjen et Wheatley (2021) et de Rogers et al. (2018) démontrent que ces bascules cycliques entre l'objet partagé et le visage régulent l'engagement cognitif et la confiance."
    )

    insert_list_item(
        "Micro-situation 2 : Attention partagée et multi-tâche sur logiciel de gestion (PMS / Traitement d'une demande complexe ou réclamation)",
        "Cette scène confronte le réceptionniste à une double contrainte opérationnelle : traiter la réclamation ou la demande spécifique d'un voyageur (problème de facturation, attribution de chambre non conforme) tout en manipulant le Property Management System (PMS) sur l'ordinateur de comptoir. Le professionnel doit maintenir un accueil empathique et professionnel tout en navigant dans les menus du logiciel, en vérifiant des disponibilités et en encodant des données. L'observation dyadique permet de cartographier les phénomènes de cécité attentionnelle (cognitive tunneling), d'évaluer la charge mentale liée à l'outil (Beckmann, 2010 ; Flandrin et al., 2021) et d'analyser le travail émotionnel mobilisé par le professionnel pour ne pas rompre le lien relationnel (Giacomel, 2019 ; Hennig-Thurau et al., 2006)."
    )

    insert_p("Afin d'éviter tout effet d'ordre et de garantir la cohérence des comparaisons intra et inter-sujets, ces deux micro-situations sont déroulées dans un ordre identique pour toutes les dyades de l'échantillon pilote.")

    # 2.3 ARCHITECTURE TECHNIQUE
    insert_heading("2.3. Architecture et Instrumentation Technique de Captation Dyadique", level=2)

    insert_p("Le dispositif expérimental s'appuie sur une chaîne d'acquisition biométrique haute fidélité conçue pour minimiser l'intrusion et préserver le naturel de l'échange :")

    insert_list_item(
        "Équipements oculométriques portables",
        "Deux paires de lunettes Pupil Labs Neon sont mobilisées en parallèle. Légères (moins de 50 grammes) et équipées de montures ergonomiques sans obstruction périphérique, elles intègrent deux caméras oculaires infrarouges opérant à 200 Hz avec suivi du regard basé sur des réseaux de neurones profonds embarqués (NeOnNet), ainsi qu'une caméra scène grand-angle HD 1080p @ 30 fps capturant le champ visuel subjectif de chaque participant."
    )

    insert_list_item(
        "Procédure de synchronisation temporelle fine (< 5 ms)",
        "La synchronisation des deux flux vidéo et oculométriques constitue le cœur névralgique du protocole dyadique. Elle est assurée par une double procédure : (1) synchronisation réseau automatique via le protocole Pupil Timesync sur réseau local dédié (NTP), alignant les horloges matérielles des deux unités d'enregistrement avec une précision inférieure à 5 millisecondes ; (2) validation par marqueur multimodal externe (clap visuel et acoustique calibré) au début et à la fin de chaque scénario pour sécuriser l'alignement temporel des flux."
    )

    insert_list_item(
        "Cartographie dynamique des Aires d'Intérêt (Dynamic AOIs)",
        "Grâce aux algorithmes de Surface Tracking de Pupil Cloud et à la détection automatique d'objets, plusieurs Aires d'Intérêt (AOI) sont définies : AOI Écran Tablette, AOI Écran PMS, AOI Clavier/Comptoir, AOI Visage du Client (avec segmentation fine Yeux / Bouche), et AOI Visage du Réceptionniste. Cette modélisation permet d'automatiser le calcul des temps de fixation et des trajectoires visuelles."
    )

    insert_list_item(
        "Indicateurs oculométriques et biométriques extraits",
        "Pour chaque dyade, le protocole extrait : le temps total et relatif de fixation par AOI, la latence avant le premier retour visuel vers l'interlocuteur (Time to Re-engage), la fréquence des transitions attentionnelles écran-visage, le pourcentage de temps en regard mutuel direct (mutual gaze), ainsi que les variations pupillométriques et la fréquence des clignements, proxies objectifs de la charge cognitive et du stress émotionnel."
    )

    # 2.4 PLANIFICATION EN 5 PHASES
    insert_heading("2.4. Planification Opérationnelle en Cinq Phases Structurées (Conformité Calendrier AiàP)", level=2)

    insert_p("Le projet déploie sa méthodologie exploratoire sur l'année académique 2026-2027 à travers cinq phases séquentielles rigoureusement articulées :")

    insert_list_item(
        "Phase 1 : Cadrage scientifique, méthodologique et éthique (Septembre – Octobre 2026)",
        "Consolidation de la note de cadrage théorique, validation des protocoles de recueil de données biométriques auprès du comité d'éthique de la Haute École, conformité RGPD (anonymisation des visages et des flux oculaires), rédaction des formulaires de consentement éclairé et formalisation de la charte de gestion des données."
    )

    insert_list_item(
        "Phase 2 : Conception des scénarios et préparation du terrain (Novembre – Décembre 2026)",
        "Rédaction détaillée des fiches rôles standardisées (réceptionniste professionnel / client complice avec profils psychologiques contrastés), scénarisation des déclencheurs transactionnels et des réclamations, conception des maquettes fonctionnelles sur tablette tactile et du simulateur PMS sur poste fixe, aménagement du comptoir de simulation au sein de l'environnement pédagogique de la HECh."
    )

    insert_list_item(
        "Phase 3 : Tests techniques et mise au point du pilote (Janvier – Février 2027)",
        "Banc d'essai matériel en conditions réelles : vérification de l'étalonnage des deux paires de Pupil Labs Neon, validation de la robustesse de la synchronisation réseau NTP (< 5 ms), évaluation du confort de port des participants, test des procédures de briefing et exécution de passations à blanc pour ajuster les consignes."
    )

    insert_list_item(
        "Phase 4 : Réalisation du pilote sur le terrain (Mars – Avril 2027)",
        "Conduite du protocole expérimental auprès d'un échantillon pilote de 4 à 6 dyades (mobilisant prioritairement des étudiants de bloc 3 en gestion hôtelière et des professionnels associés). Enregistrement simultané des flux vidéo subjectifs et oculométriques, recueil des traces audio et tenue du journal de bord des expérimentations."
    )

    insert_list_item(
        "Phase 5 : Analyse exploratoire, débriefing réflexif et valorisation (Mai – Juillet 2027)",
        "Post-traitement des données d'eye-tracking sous Pupil Cloud, extraction des métriques attentionnelles, conduite d'entretiens d'autoconfrontation avec les participants, formalisation d'une grille descriptive des épisodes critiques, rédaction du rapport de synthèse et élaboration de recommandations pédagogiques et sectorielles."
    )

    # 2.5 ARTICULATION PÉDAGOGIQUE ET RÉFLEXIVITÉ
    insert_heading("2.5. Articulation Pédagogique et Démarche Réflexive : L'Autoscopie et l'Hétéroscopie", level=2)

    insert_p("L'eye-tracking ne constitue pas seulement un instrument de mesure expérimentale ; il représente un puissant vecteur de développement professionnel et de médiation pédagogique. En s'appuyant sur les théories du cours d'action (Theureau, 2015 ; Durand, 2016) et la vision professionnelle (Goodwin, 1994), les traces oculométriques permettent de rendre visibles les savoirs tacites et d'objectiver l'activité réelle face aux représentations des apprenants.")

    insert_p("Le dispositif SIMACCUEIL articule deux démarches réflexives complémentaires :")

    insert_list_item(
        "Autoscopie guidée (autoconfrontation)",
        "L'apprenant revoit l'enregistrement de sa propre prestation avec incrustation dynamique de son point de fixation (gaze overlay). Confronté à la réalité objective de son comportement visuel, il est invité par le formateur à expliciter ses prises d'indices, à justifier ses temps d'hésitation ou à conscientiser ses moments d'absence relationnelle (regard figé sur l'écran au détriment du client). Cette pratique opérationnalise la démarche réflexive théorisée par Perrenoud (2001)."
    )

    insert_list_item(
        "Hétéroscopie (Eye Movement Modeling Example - EMME)",
        "L'apprenant observe l'activité enregistrée d'un professionnel expérimenté dont le regard est visualisé à l'écran. Comme l'ont démontré Van Gog et al. (2009), Jarodzka et al. (2012) et Seppänen & Gegenfurtner (2012), la visualisation de la stratégie visuelle experte combinée à des verbalisations pédagogiques guide l'attention des novices vers les zones d'information critiques du logiciel et les signaux non-verbaux essentiels du client, accélérant l'acquisition de compétences complexes."
    )

    # TABLEAUX MÉTHODOLOGIQUES
    p_t1_title = insert_p("Tableau 1 — Modalités d'analyse de l'activité mobilisées dans le dispositif SIMACCUEIL", style=None, space_before=Pt(8), space_after=Pt(4))
    p_t1_title.runs[0].font.bold = True
    p_t1_title.runs[0].font.size = Pt(9.5)
    p_t1_title.runs[0].font.color.rgb = COLOR_NAVY

    tbl_mod = doc.add_table(rows=4, cols=3)
    tbl_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_mod = ["Modalité", "Objet observé", "Démarche méthodologique & pédagogique"]
    widths_mod = [Inches(1.5), Inches(2.3), Inches(2.7)]
    for c_i, h_txt in enumerate(headers_mod):
        c = tbl_mod.rows[0].cells[c_i]
        c.width = widths_mod[c_i]
        style_cell(c, bg_color=HEX_NAVY, top_pad=80, bot_pad=80, left_pad=100, right_pad=100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_mod = [
        ("Autoscopie", "L’activité enregistrée de l’apprenant lui-même (vue subjective + regard)", "Entretien d'autoconfrontation : verbalisation rétrospective guidée, prise de conscience des fixations excessives sur écran et analyse réflexive (Perrenoud, 2001)."),
        ("Hétéroscopie (EMME)", "L’activité d’un professionnel expert par un apprenant", "Modélisation visuelle (Van Gog et al., 2009) : décodage de la vision professionnelle (Goodwin, 1994) et guidage attentionnel vers les indices pertinents du PMS et du client."),
        ("Analyse croisée dyadique", "Confrontation simultanée des deux flux (Réceptionniste + Client)", "Objectivation du décalage de perception : confrontation du regard du professionnel aux réactions visuelles réelles du client (Rogers et al., 2018 ; Wohltjen & Wheatley, 2021).")
    ]
    for r_i, (col0, col1, col2) in enumerate(data_mod):
        row = tbl_mod.rows[r_i + 1]
        bg = HEX_ALT_ROW if r_i % 2 == 1 else "FFFFFF"
        for c_i, txt in enumerate([col0, col1, col2]):
            c = row.cells[c_i]
            c.width = widths_mod[c_i]
            style_cell(c, bg_color=bg, top_pad=60, bot_pad=60, left_pad=80, right_pad=80, border_bottom={"sz": 4, "color": HEX_BORDER})
            p = c.paragraphs[0]
            r = p.add_run(txt)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_NAVY
            else:
                r.font.color.rgb = COLOR_CHARCOAL
    insert_tbl(tbl_mod)

    insert_p("", space_after=Pt(6))

    p_t2_title = insert_p("Tableau 2 — Typologie des supports vidéo exploités dans les débriefings", style=None, space_before=Pt(8), space_after=Pt(4))
    p_t2_title.runs[0].font.bold = True
    p_t2_title.runs[0].font.size = Pt(9.5)
    p_t2_title.runs[0].font.color.rgb = COLOR_NAVY

    tbl_sup = doc.add_table(rows=4, cols=2)
    tbl_sup.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_sup = [Inches(2.5), Inches(4.0)]
    for c_i, h_txt in enumerate(["Support Vidéo Oculométrique", "Fonction et Usage Pédagogique"]):
        c = tbl_sup.rows[0].cells[c_i]
        c.width = widths_sup[c_i]
        style_cell(c, bg_color=HEX_NAVY, top_pad=80, bot_pad=80, left_pad=100, right_pad=100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_sup = [
        ("Vidéo subjective avec point de regard incrusté (Gaze Overlay)", "Visualiser précisément l'exploration visuelle de l'interface PMS et les micro-regards portés sur le visage de l'interlocuteur."),
        ("Vidéo dyadique synchronisée côte-à-côte (Split-Screen Receptionist-Client)", "Observer en temps réel l'impact du comportement du réceptionniste sur l'attention du client (ex: décrochage visuel du client lorsque le réceptionniste fixe l'écran sans parler)."),
        ("Extraits courts d'incidents critiques (Micro-clips de 30 à 60s)", "Servir de catalyseur d'échange réflexif ciblé lors des séances de débriefing collectif, en confrontant les perceptions aux données biométriques objectives.")
    ]
    for r_i, (col0, col1) in enumerate(data_sup):
        row = tbl_sup.rows[r_i + 1]
        bg = HEX_ALT_ROW if r_i % 2 == 1 else "FFFFFF"
        for c_i, txt in enumerate([col0, col1]):
            c = row.cells[c_i]
            c.width = widths_sup[c_i]
            style_cell(c, bg_color=bg, top_pad=60, bot_pad=60, left_pad=80, right_pad=80, border_bottom={"sz": 4, "color": HEX_BORDER})
            p = c.paragraphs[0]
            r = p.add_run(txt)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_NAVY
            else:
                r.font.color.rgb = COLOR_CHARCOAL
    insert_tbl(tbl_sup)

    insert_p("", space_after=Pt(8))

    # 2.6 APPLICATIONS CONCRÈTES ET RETOMBÉES STRATÉGIQUES
    insert_heading("2.6. Applications Concrètes et Retombées Stratégiques pour les Secteurs de l'Hôtellerie et du Tourisme", level=2)

    insert_p("L'ambition de SIMACCUEIL dépasse le strict cadre expérimental de laboratoire pour s'ancrer dans des retombées professionnelles concrètes et directement transférables à l'industrie de l'hôtellerie, de l'hébergement touristique et des services d'accueil en Wallonie et à l'international :")

    insert_list_item(
        "1. Élaboration d'un Référentiel de Compétences Attentionnelles et Relationnelles",
        "Le projet produira une cartographie inédite des micro-habiletés requises pour concilier digitalisation et relation humaine chaleureuse. Ce référentiel définira des standards opérationnels observables : rythmes optimaux de bascule regard-écran / regard-client, techniques de guidage visuel sur support partagé, stratégies verbales de meublement cognitif (permettant d'éviter le silence pesant lors d'un encodage informatique lourd) et gestion du regard face à des clients agressifs pour préserver l'équilibre émotionnel (Giacomel, 2019)."
    )

    insert_list_item(
        "2. Ingénierie de Formation Hôtelière Haute Performance (Initiale et Continue)",
        "Pour le département des sciences économiques et de gestion hôtelière de la HECh, SIMACCUEIL fournira des modules de micro-learning directement intégrables dans les cursus de Bachelier. En formation continue pour adultes, ces ressources seront mises à disposition des structures de formation sectorielle (notamment les centres de compétences Horeca Formation Wallonie et Bruxelles) pour former le personnel en poste aux bonnes pratiques d'accueil instrumenté."
    )

    insert_list_item(
        "3. Recommandations Ergonomiques pour les Postes de Travail et le Design UX/UI des Logiciels Hôteliers",
        "En identifiant précisément les points de friction attentionnelle et les zones d'enfermement visuel générés par les écrans de comptoir (Flandrin et al., 2021), la recherche formulera des préconisations d'aménagement physique (hauteur des banques d'accueil, orientation des moniteurs, utilisation de tablettes sur bras articulés favorisant la co-attention). Sur le plan logiciel, les résultats guideront les éditeurs de PMS vers des interfaces utilisateur (UI) plus épurées, minimisant la charge cognitive (Beckmann, 2010) et favorisant la saisie en vision périphérique."
    )

    insert_list_item(
        "4. Partenariats Professionnels et Tremplin vers un Financement Pluriannuel FRHE",
        "En documentant la faisabilité scientifique et l'impact opérationnel du pilote dyadique, SIMACCUEIL dotera la Haute École de données probantes indispensables pour postuler avec succès aux appels à projets de recherche appliquée de plus grande envergure (Fonds de Recherche en Haute École - FRHE). Le projet servira également de plateforme de valorisation en partenariat avec les fédérations professionnelles (Fédération Horeca Wallonie, Horeca Bruxelles, Wallonie Belgique Tourisme), renforçant la visibilité et l'ancrage socio-économique de l'institution."
    )

    # 2.7 PRÉCAUTIONS MÉTHODOLOGIQUES ET ÉTHIQUES
    insert_heading("2.7. Précautions Méthodologiques, Déontologiques et Limites Épistémologiques", level=2)

    insert_p("La mise en œuvre de ce protocole exige plusieurs garanties épistémologiques et éthiques pour assurer la validité scientifique des résultats :")

    insert_list_item(
        "Distinction entre fixation fovéale et traitement cognitif conscient",
        "Conformément aux alertes de Hooge et al. (2026), une fixation oculaire sur un élément de l'écran ou sur le visage ne signifie pas mécaniquement que l'information a été comprise ou intégrée. L'analyse oculométrique quantitative doit impérativement être croisée avec l'analyse qualitative du cours d'action et les verbalisations en autoconfrontation."
    )

    insert_list_item(
        "Contrôle des biais rétrospectifs lors des débriefings",
        "Pour limiter les reconstructions a posteriori et la désirabilité sociale, les entretiens d'autoscopie sont conduits immédiatement après la simulation et s'appuient strictement sur les traces vidéo réelles du regard, guidés par un questionnement neutre et non-évaluateur."
    )

    insert_list_item(
        "Conformité éthique et protection stricte des données biométriques (RGPD)",
        "Les enregistrements vidéo et les données oculométriques constituent des données personnelles sensibles. Le protocole applique un chiffrement local des données, une anonymisation des fichiers et une procédure de consentement libre et éclairé garantissant le droit de retrait à tout moment sans incidence sur l'évaluation académique des participants."
    )

    # 5. Mise à jour de la Bibliographie
    print("Checking Bibliography entries...")
    bib_paras = []
    curr = biblio_elem.getnext()
    while curr is not None:
        if curr.tag.endswith('p'):
            t_nodes = curr.xpath('.//w:t')
            p_text = ''.join([t.text for t in t_nodes])
            bib_paras.append((curr, p_text))
        curr = curr.getnext()

    bib_texts = [bp[1] for bp in bib_paras]
    
    has_perrenoud = any("Perrenoud" in t for t in bib_texts)
    has_flandrin = any("Flandrin" in t for t in bib_texts)
    has_giacomel = any("Giacomel" in t for t in bib_texts)

    last_bib_elem = bib_paras[-1][0] if bib_paras else biblio_elem

    def append_bib_entry(ref_text, url_str):
        nonlocal last_bib_elem
        p_new = parse_xml(f'<w:p {nsdecls("w")}/>')
        last_bib_elem.addnext(p_new)
        last_bib_elem = p_new
        p_obj = docx.text.paragraph.Paragraph(p_new, doc)
        p_obj.paragraph_format.space_after = Pt(4)
        p_obj.paragraph_format.line_spacing = 1.15
        p_obj.paragraph_format.left_indent = Inches(0.25)
        p_obj.paragraph_format.first_line_indent = Inches(-0.25)
        r = p_obj.add_run(ref_text + " ")
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_CHARCOAL
        add_hyperlink(p_obj, url_str, url_str, color_rgb=COLOR_TEAL, bold=False)

    if not has_flandrin:
        print("Adding Flandrin to Bibliography...")
        append_bib_entry(
            "Flandrin, P., van de Leemput, C., & Hellemans, C. (2021). Activité du manager de réception à l’épreuve de la digitalisation : cas d’un projet d’accueil en mobilité dans une chaîne hôtelière internationale. Activités, 18(2), 1–28.",
            "https://doi.org/10.4000/activites.6760"
        )

    if not has_giacomel:
        print("Adding Giacomel to Bibliography...")
        append_bib_entry(
            "Giacomel, A. (2019). Les enjeux du travail émotionnel individuel et collectif dans les groupes hôteliers multinationaux : La complexité de l’équilibre émotionnel au service de l’homéostasie organisationnelle. Mondes du Tourisme, 16.",
            "https://doi.org/10.4000/tourisme.2471"
        )

    if not has_perrenoud:
        print("Adding Perrenoud to Bibliography...")
        append_bib_entry(
            "Perrenoud, Ph. (2001). Mettre la pratique réflexive au centre du projet de formation. Cahiers pédagogiques, (390), 43–45.",
            "https://www.unige.ch/fapse/SSE/teachers/perrenoud/php_main/php_2001/2001_13.html"
        )

    # Sauvegarde locale et copie sur Google Drive
    os.makedirs(os.path.dirname(LOCAL_DOC_PATH), exist_ok=True)
    doc.save(LOCAL_DOC_PATH)
    print("✅ Document sauvegardé localement avec succès :", LOCAL_DOC_PATH)

    try:
        shutil.copy2(LOCAL_DOC_PATH, DRIVE_DOC_PATH)
        print("✅ Document copié avec succès sur Google Drive :", DRIVE_DOC_PATH)
    except PermissionError:
        alt_drive_path = DRIVE_DOC_PATH.replace(".docx", " (Mis a jour).docx")
        shutil.copy2(LOCAL_DOC_PATH, alt_drive_path)
        print("⚠️ Fichier verrouillé sur Google Drive, copié sous :", alt_drive_path)

if __name__ == "__main__":
    build_simaccueil()
