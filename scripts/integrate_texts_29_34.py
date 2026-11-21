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
HEX_BORDER = "D1D5DB"
HEX_ALT_ROW = "F9FAFC"

COLOR_NAVY = RGBColor(27, 54, 93)
COLOR_TEAL = RGBColor(14, 134, 212)
COLOR_CHARCOAL = RGBColor(44, 62, 80)
COLOR_MUTED = RGBColor(100, 110, 120)
COLOR_BLUE = RGBColor(17, 85, 204)

NEW_TEXTS = [
    {
        "id": "29",
        "label": "Texte 29",
        "pilier": "Pilier 7 : Compétences Commerciales & Upselling en Réception Hôtelière",
        "auteurs": "Ahn, J. J.",
        "annee": "2022",
        "titre": "Promoting hotel upselling: The effect of message appeal and delivery setting on consumer attitude and purchase intention",
        "revue": "Journal of Hospitality and Tourism Management, 52, 295–303",
        "doi": "https://doi.org/10.1016/j.jhtm.2022.07.009",
        "ref_apa": "Ahn, J. J. (2022). Promoting hotel upselling: The effect of message appeal and delivery setting on consumer attitude and purchase intention. Journal of Hospitality and Tourism Management, 52, 295–303. https://doi.org/10.1016/j.jhtm.2022.07.009",
        "resume": (
            "Cette étude expérimentale examine comment le cadre de délivrance d'une proposition de surclassement hôtelier "
            "(interaction en face-à-face à la réception versus environnement numérique) et la nature de l'argumentaire "
            "(appel émotionnel/expérientiel versus appel rationnel/économique) influencent l'attitude et l'intention d'achat "
            "du client. Les résultats démontrent que l'adéquation entre le message persuasif et le contexte relationnel "
            "conditionne fortement l'acceptation de l'upselling. En face-à-face, la posture d'interaction, la clarté "
            "informative et la réduction de la résistance psychologique sont déterminantes pour transformer une suggestion "
            "commerciale en valeur perçue plutôt qu'en pression intrusive."
        ),
        "contribution": (
            "Cet article complète directement Denizci Guillet (2020) et Ruki (2023) en ancrant la Micro-situation 1 "
            "(co-attention sur tablette) dans la psychologie du consommateur hôtelier. SIMACCUEIL mobilise ces résultats "
            "pour concevoir des scénarios d'upselling combinant support visuel tactile et dialogue en face-à-face : "
            "l'oculométrie dyadique permet d'observer comment le réceptionniste synchronise la présentation visuelle "
            "d'options expérientielles sur la tablette avec des retours réguliers au regard du client, évitant ainsi "
            "que la médiation numérique ne rompe la relation persuasive au comptoir."
        ),
    },
    {
        "id": "30",
        "label": "Texte 30",
        "pilier": "Pilier 7 : Compétences Commerciales & Upselling en Réception Hôtelière",
        "auteurs": "Jawabreh, O., Masa'Deh, R., Al Fayoumi, T., & Bareya, A.",
        "annee": "2022",
        "titre": "Customer Satisfaction Towards Communication Skills of Front Office Staff At the Hotel (Case Study Five Stars Hotels in Aqaba)",
        "revue": "GeoJournal of Tourism and Geosites, 44(4)",
        "doi": "https://doi.org/10.30892/gtg.44416-948",
        "ref_apa": "Jawabreh, O., Masa'Deh, R., Al Fayoumi, T., & Bareya, A. (2022). Customer Satisfaction Towards Communication Skills of Front Office Staff At the Hotel (Case Study Five Stars Hotels in Aqaba). GeoJournal of Tourism and Geosites, 44(4). https://doi.org/10.30892/gtg.44416-948",
        "resume": (
            "Menée auprès de clients et du personnel de réception d'établissements hôteliers cinq étoiles à Aqaba, "
            "cette étude empirique évalue l'influence des compétences communicationnelles du front-office sur la "
            "satisfaction globale des voyageurs. Les auteurs analysent plusieurs dimensions verbales et non verbales "
            "clés : l'écoute active, la clarté de l'expression, la réactivité dans le traitement des demandes, la posture "
            "corporelle et le maintien du contact visuel. Les résultats confirment que la maîtrise de ces micro-compétences "
            "relationnelles au comptoir d'accueil constitue un levier majeur de confiance, de perception de qualité "
            "de service et de fidélisation de la clientèle."
        ),
        "contribution": (
            "Jawabreh et al. fournissent à SIMACCUEIL des critères comportementaux concrets pour opérationnaliser le "
            "futur référentiel de compétences en gestion hôtelière (Section 2.6). Alors que leur étude s'appuie sur "
            "des questionnaires de satisfaction perçue, notre dispositif dyadique mesure objectivement l'une de leurs "
            "variables centrales — le contact visuel et l'écoute attentive — en quantifiant au millième de seconde "
            "comment l'usage des écrans (tablette ou PMS) affecte la disponibilité relationnelle du réceptionniste "
            "et le ressenti visuel du client."
        ),
    },
    {
        "id": "31",
        "label": "Texte 31",
        "pilier": "Pilier 8 : Ergonomie de l'Activité & Digitalisation de l'Accueil Hôtelier",
        "auteurs": "Bengsch, G.",
        "annee": "2016",
        "titre": "Interactional structures and engagement in service encounters: An investigation into communication at the hotel front desk",
        "revue": "Thèse de doctorat (Ph.D.), University of York (White Rose eTheses Online)",
        "doi": "https://etheses.whiterose.ac.uk/",
        "ref_apa": "Bengsch, G. (2016). Interactional structures and engagement in service encounters: An investigation into communication at the hotel front desk [Thèse de doctorat, University of York]. White Rose eTheses Online. https://etheses.whiterose.ac.uk/",
        "resume": (
            "Fondée sur l'analyse conversationnelle et multimodale d'interactions authentiques filmées à la réception "
            "d'hôtels, cette thèse examine l'organisation séquentielle des rencontres de service (check-in, demandes "
            "d'information) et la coordination entre parole, gestes, manipulation d'objets matériels et engagement visuel "
            "(gaze). L'auteure met en évidence la façon dont le réceptionniste gère la transition délicate entre "
            "l'attention portée à l'ordinateur de comptoir (saisie et vérification de dossier) et le maintien de l'engagement "
            "interactionnel avec le client, révélant les micro-ruptures attentionnelles causées par le travail sur écran."
        ),
        "contribution": (
            "Cette recherche constitue un socle analytique exceptionnel pour SIMACCUEIL car elle porte exactement sur la "
            "triade réceptionniste–client–écran au comptoir hôtelier. Elle inspire directement le codage séquentiel de "
            "nos vidéos dyadiques (distinction entre phases d'ouverture, de saisie PMS et de réengagement visuel), tout "
            "en permettant à notre protocole équipé de lunettes Pupil Labs Neon de dépasser l'observation vidéo externe "
            "pour capter avec précision les fixations fovéales mutuelles."
        ),
    },
    {
        "id": "32",
        "label": "Texte 32",
        "pilier": "Pilier 2 : Cognition Située, Travail Émotionnel & Dynamiques de l'Interaction Client-Réceptionniste",
        "auteurs": "Fernandes, T., Morgado, M., & Rodrigues, M. A.",
        "annee": "2018",
        "titre": "The role of employee emotional competence in service recovery encounters",
        "revue": "Journal of Services Marketing, 32(7), 835–849",
        "doi": "https://doi.org/10.1108/JSM-07-2017-0237",
        "ref_apa": "Fernandes, T., Morgado, M., & Rodrigues, M. A. (2018). The role of employee emotional competence in service recovery encounters. Journal of Services Marketing, 32(7), 835–849. https://doi.org/10.1108/JSM-07-2017-0237",
        "resume": (
            "Cette étude empirique analyse le rôle décisif des compétences émotionnelles du personnel en contact "
            "(Employee Emotional Competence — capacité à percevoir, comprendre et réguler ses propres émotions ainsi "
            "que celles du client) lors d'une défaillance de service et d'une réclamation. Les auteurs montrent que "
            "ces compétences émotionnelles améliorent directement la perception de justice interactionnelle par le client, "
            "renforcent la confiance post-réclamation et favorisent les intentions comportementales positives, au-delà "
            "des seules compensations matérielles ou procédurales offertes par l'entreprise."
        ),
        "contribution": (
            "Cet article ancre la Micro-situation 2 (gestion de réclamation sur PMS) dans le champ des compétences de "
            "service recovery. En complément de Giacomel (2019), Fernandes et al. permettent d'interpréter les prises "
            "d'indices visuels sur le visage du client mécontent comme des actes de perception émotionnelle essentiels "
            "à la justice interactionnelle. En autoscopie, les étudiants pourront analyser comment leurs éventuels "
            "évitements visuels sur l'écran PMS nuisent à cette compétence émotionnelle perçue."
        ),
    },
    {
        "id": "33",
        "label": "Texte 33",
        "pilier": "Pilier 2 : Cognition Située, Travail Émotionnel & Dynamiques de l'Interaction Client-Réceptionniste",
        "auteurs": "Lajante, M., & Remisch, D.",
        "annee": "2023",
        "titre": "Frontline Employees' Empathy in Service Recovery: A Systematic Literature Review and Agenda for the Future",
        "revue": "Customer Needs and Solutions, 10(1)",
        "doi": "https://doi.org/10.1007/s40547-023-00137-8",
        "ref_apa": "Lajante, M., & Remisch, D. (2023). Frontline Employees' Empathy in Service Recovery: A Systematic Literature Review and Agenda for the Future. Customer Needs and Solutions, 10(1). https://doi.org/10.1007/s40547-023-00137-8",
        "resume": (
            "À travers une revue systématique de la littérature, Mathieu Lajante et David Remisch synthétisent les "
            "mécanismes cognitifs et affectifs de l'empathie des employés de première ligne face à des clients mécontents "
            "ou en colère lors d'épisodes de réclamation. Les auteurs montrent comment l'empathie permet de désamorcer "
            "l'hostilité et de restaurer la relation de service, tout en soulignant une limite méthodologique majeure "
            "du domaine : le recours excessif aux mesures déclaratives et la nécessité d'intégrer des indicateurs "
            "comportementaux et physiologiques objectifs en situation réelle."
        ),
        "contribution": (
            "Cette revue systématique justifie directement l'originalité épistémologique et technique de SIMACCUEIL. "
            "En répondant explicitement à l'agenda de recherche formulé par Lajante et Remisch, notre dispositif "
            "substitue aux questionnaires auto-rapportés une observation biométrique et comportementale objective "
            "(oculométrie dyadique synchronisée à < 5 ms et traces audio-vidéo), permettant d'étudier comment l'empathie "
            "et la désescalade s'incarnent visuellement lors d'une plainte au comptoir."
        ),
    },
    {
        "id": "34",
        "label": "Texte 34",
        "pilier": "Pilier 2 : Cognition Située, Travail Émotionnel & Dynamiques de l'Interaction Client-Réceptionniste",
        "auteurs": "Lajante, M., & Tojib, D.",
        "annee": "2025",
        "titre": "Empathy in service recovery: a psychophysiological study of frontline employees' responses across communication channels",
        "revue": "Journal of Consumer Marketing",
        "doi": "https://doi.org/10.1108/JCM-01-2025-7577",
        "ref_apa": "Lajante, M., & Tojib, D. (2025). Empathy in service recovery: a psychophysiological study of frontline employees' responses across communication channels. Journal of Consumer Marketing. https://doi.org/10.1108/JCM-01-2025-7577",
        "resume": (
            "Cette étude psychophysiologique récente compare les réactions émotionnelles et empathiques des employés "
            "de front-office confrontés à des réclamations clients selon différents canaux de communication (face-à-face "
            "versus médiatisé). En mobilisant des mesures physiologiques en temps réel, les auteurs démontrent que "
            "l'expression d'une empathie authentique (deep acting) face à l'insatisfaction du client mobilise des "
            "ressources cognitives et affectives mesurables, dont l'intensité varie selon les contraintes du canal "
            "interactionnel et la proximité avec l'interlocuteur."
        ),
        "contribution": (
            "Publiée en 2025, cette référence de pointe valide la pertinence de l'approche biométrique et "
            "psychophysiologique retenue dans SIMACCUEIL. Elle renforce l'interprétation des marqueurs de charge "
            "attentionnelle et émotionnelle (pupillométrie sous contrôle de luminance, fréquence de clignement, durées "
            "de fixation) lors de la Micro-situation 2, tout en éclairant l'impact de la médiation par l'écran PMS "
            "sur l'effort empathique du futur professionnel de l'hôtellerie."
        ),
    },
]

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

def create_fiche_box(doc, item):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    c.width = Inches(6.5)
    style_cell(c, bg_color=HEX_LIGHT_BG, top_pad=140, bot_pad=140, left_pad=180, right_pad=180, border_left={"sz": 24, "color": HEX_NAVY})
    
    p_t = c.paragraphs[0]
    p_t.paragraph_format.space_before = Pt(4)
    p_t.paragraph_format.space_after = Pt(8)
    r_t = p_t.add_run(f"{item['label']} — {item['titre']}")
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
    r_m1_v = p_m1.add_run(item["ref_apa"])
    r_m1_v.font.name = "Calibri"
    r_m1_v.font.size = Pt(8.5)
    r_m1_v.font.color.rgb = COLOR_MUTED

    p_m2 = c.add_paragraph()
    p_m2.paragraph_format.space_after = Pt(8)
    r_m2_l = p_m2.add_run("• 🔗 Lien d'accès éditeur / dépôt : ")
    r_m2_l.font.name = "Calibri"
    r_m2_l.font.size = Pt(8.5)
    r_m2_l.font.bold = True
    r_m2_l.font.color.rgb = COLOR_CHARCOAL
    add_hyperlink(p_m2, item["doi"], item["doi"], color_rgb=COLOR_TEAL, bold=False)

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
    r_r = p_r.add_run(item["resume"])
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
    r_c = p_c.add_run(item["contribution"])
    r_c.font.name = "Calibri"
    r_c.font.size = Pt(9)
    r_c.font.color.rgb = COLOR_CHARCOAL

    return tbl

def integrate():
    print("Loading:", DRIVE_DOC_PATH)
    doc = docx.Document(DRIVE_DOC_PATH)
    body = doc.element.body

    # 1. Mettre à jour le décompte (25 -> 31, 01 à 28 -> 01 à 34)
    for p in doc.paragraphs[:20]:
        if "25 articles scientifiques" in p.text:
            for r in p.runs:
                if "25" in r.text:
                    r.text = r.text.replace("25", "31")
        elif "25 Références Retenues" in p.text:
            p.runs[0].text = "Tableau Synthétique des 31 Références Retenues (numérotées 01 à 34)"
            for r in p.runs[1:]:
                r.text = ""
        elif "Fiches Analytiques Détaillées" in p.text:
            p.runs[0].text = "1.2. Fiches Analytiques Détaillées (31 Références retenues, numérotées 01 à 34)"
            for r in p.runs[1:]:
                r.text = ""

    # 2. Ajouter les lignes 29-34 dans Table 0
    t0 = doc.tables[0]
    for item in NEW_TEXTS:
        if any(item["label"] in row.cells[0].text for row in t0.rows):
            continue
        row = t0.add_row()
        bg = HEX_ALT_ROW if len(t0.rows) % 2 == 1 else "FFFFFF"
        
        c0 = row.cells[0]
        c0.width = Inches(1.0)
        style_cell(c0, bg_color=bg, top_pad=70, bot_pad=70, left_pad=90, right_pad=90, border_bottom={"sz": 4, "color": HEX_BORDER})
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_hyperlink(p0, item["label"], item["doi"], color_rgb=COLOR_BLUE, bold=True)
        
        c1 = row.cells[1]
        c1.width = Inches(1.8)
        style_cell(c1, bg_color=bg, top_pad=70, bot_pad=70, left_pad=90, right_pad=90, border_bottom={"sz": 4, "color": HEX_BORDER})
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(f"{item['auteurs']} ({item['annee']})")
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_CHARCOAL
        
        c2 = row.cells[2]
        c2.width = Inches(3.7)
        style_cell(c2, bg_color=bg, top_pad=70, bot_pad=70, left_pad=90, right_pad=90, border_bottom={"sz": 4, "color": HEX_BORDER})
        p2 = c2.paragraphs[0]
        r2_t = p2.add_run(f"« {item['titre']} »\n")
        r2_t.font.name = "Calibri"
        r2_t.font.size = Pt(8.5)
        r2_t.font.bold = True
        r2_t.font.color.rgb = COLOR_NAVY
        add_hyperlink(p2, f"🌐 Lien Éditeur / Dépôt ({item['revue'][:30]}...)", item["doi"], color_rgb=COLOR_TEAL, bold=False)

    # 3. Insérer les Fiches Analytiques 29 à 34 juste après la Fiche 28
    tbl_28_elem = None
    for child in body:
        if child.tag.endswith('tbl'):
            t_str = ''.join([t.text for t in child.xpath('.//w:t')[:10]])
            if "Texte 28" in t_str:
                tbl_28_elem = child
                break

    if tbl_28_elem is not None:
        anchor = tbl_28_elem
        temp_doc = docx.Document()
        for item in NEW_TEXTS:
            # Vérifier si déjà présent
            already = any(item["label"] in ''.join([t.text for t in c.xpath('.//w:t')[:5]]) for c in body if c.tag.endswith('tbl'))
            if already:
                continue
            p_space = parse_xml(f'<w:p {nsdecls("w")}><w:pPr><w:spacing w:after="240"/></w:pPr></w:p>')
            anchor.addnext(p_space)
            box = create_fiche_box(temp_doc, item)
            p_space.addnext(box._tbl)
            anchor = box._tbl
        print("Inserted Fiches 29 to 34 after Texte 28!")

    # 4. Enrichir la Synthèse Problématisée (1.3) et la Méthodologie (2.2, 2.3, 2.6)
    for p in doc.paragraphs:
        if "Au terme de cette revue de la littérature structurée autour de 25 travaux" in p.text:
            p.runs[0].text = p.runs[0].text.replace("25 travaux", "31 travaux")
        elif "Premièrement, sur le plan ergonomique et organisationnel" in p.text:
            p.runs[0].text = (
                "Premièrement, sur le plan ergonomique, commercial et émotionnel, la digitalisation des comptoirs d'accueil "
                "(PMS, tablettes mobiles, outils de yield management) transforme profondément le métier (Flandrin et al., 2021 ; "
                "Denizci Guillet, 2020 ; Ruki, 2023). Les recherches spécifiques au front-office hôtelier montrent que la réussite "
                "d'une vente incitative (upselling) dépend de l'adéquation entre le message persuasif et le cadre d'interaction en "
                "face-à-face (Ahn, 2022), ainsi que des compétences verbales et du contact visuel (Jawabreh et al., 2022). Parallèlement, "
                "l'analyse multimodale au comptoir révèle que la manipulation informatique génère des micro-ruptures d'engagement visuel "
                "(Bengsch, 2016) et une charge cognitive accrue (Beckmann, 2010), tandis que la gestion des plaintes exige des "
                "compétences émotionnelles aiguës (Fernandes et al., 2018) et un travail d'empathie authentique coûteux sur le plan "
                "psychophysiologique (Giacomel, 2019 ; Hennig-Thurau et al., 2006 ; Lajante & Remisch, 2023 ; Lajante & Tojib, 2025)."
            )
        elif "Micro-situation 1 : Co-attention sur support numérique partagé" in p.text:
            p.text = ""
            rb = p.add_run("• Micro-situation 1 : Co-attention sur support numérique partagé (Tablette / Upselling commercial) : ")
            rb.font.name = "Calibri"; rb.font.size = Pt(10); rb.font.bold = True; rb.font.color.rgb = COLOR_CHARCOAL
            rt = p.add_run(
                "Dans cette scène de conseil et de vente incitative, le réceptionniste et le client consultent conjointement une "
                "tablette numérique interactive (catalogue d'options de surclassement, forfaits bien-être, excursions). S'appuyant sur "
                "Ahn (2022) et Ruki (2023), le scénario intègre des arguments expérientiels et rationnels. L'enjeu est d'analyser "
                "la dynamique d'attention conjointe (joint attention) et les compétences communicationnelles non verbales (Jawabreh et al., "
                "2022) : comment le professionnel guide-t-il le regard du client sur l'interface tactile tout en maintenant des retours "
                "au regard mutuel (Wohltjen & Wheatley, 2021 ; Rogers et al., 2018) pour susciter la confiance sans paraître intrusif ?"
            )
            rt.font.name = "Calibri"; rt.font.size = Pt(10); rt.font.color.rgb = COLOR_CHARCOAL
        elif "Micro-situation 2 : Attention partagée et multi-tâche sur logiciel de gestion" in p.text:
            p.text = ""
            rb = p.add_run("• Micro-situation 2 : Attention partagée et multi-tâche sur logiciel de gestion (PMS / Traitement d'une réclamation) : ")
            rb.font.name = "Calibri"; rb.font.size = Pt(10); rb.font.bold = True; rb.font.color.rgb = COLOR_CHARCOAL
            rt = p.add_run(
                "Cette scène confronte le réceptionniste à la gestion d'une réclamation client (erreur de facturation ou attribution "
                "de chambre non conforme) tout en manipulant le PMS au comptoir. Inspirée de l'analyse séquentielle des ruptures "
                "d'engagement visuel de Bengsch (2016) et des travaux sur le service recovery (Fernandes et al., 2018 ; Lajante & Remisch, "
                "2023), l'observation dyadique cartographie l'enfermement visuel sur l'écran (cognitive tunneling), la charge cognitive "
                "(Beckmann, 2010 ; Flandrin et al., 2021) et les marqueurs oculométriques et psychophysiologiques de l'empathie et de la "
                "régulation émotionnelle face à l'insatisfaction du client (Giacomel, 2019 ; Lajante & Tojib, 2025)."
            )
            rt.font.name = "Calibri"; rt.font.size = Pt(10); rt.font.color.rgb = COLOR_CHARCOAL
        elif "Indicateurs oculométriques et biométriques extraits" in p.text:
            p.text = ""
            rb = p.add_run("• Indicateurs oculométriques, séquentiels et biométriques extraits : ")
            rb.font.name = "Calibri"; rb.font.size = Pt(10); rb.font.bold = True; rb.font.color.rgb = COLOR_CHARCOAL
            rt = p.add_run(
                "Pour chaque dyade, le protocole extrait : le temps total et relatif de fixation par AOI, la latence de réengagement "
                "visuel vers l'interlocuteur (Time to Re-engage), les matrices de transition écran–visage inspirées du découpage séquentiel "
                "de Bengsch (2016), la durée de regard mutuel direct (mutual gaze), ainsi que les variations pupillométriques (sous "
                "contrôle de luminance) et la fréquence de clignements, proxies objectifs de la charge cognitive et de l'effort empathique "
                "(Lajante & Tojib, 2025)."
            )
            rt.font.name = "Calibri"; rt.font.size = Pt(10); rt.font.color.rgb = COLOR_CHARCOAL
        elif "1. Élaboration d'un Référentiel de Compétences Attentionnelles" in p.text:
            p.text = ""
            rb = p.add_run("• 1. Élaboration d'un Référentiel de Compétences Attentionnelles, Commerciales et Émotionnelles : ")
            rb.font.name = "Calibri"; rb.font.size = Pt(10); rb.font.bold = True; rb.font.color.rgb = COLOR_CHARCOAL
            rt = p.add_run(
                "Le projet produira une cartographie inédite des micro-habiletés requises pour concilier digitalisation et relation "
                "humaine chaleureuse. En intégrant les compétences communicationnelles identifiées par Jawabreh et al. (2022), les leviers "
                "de persuasion en upselling d'Ahn (2022) et les compétences émotionnelles de service recovery de Fernandes et al. (2018), "
                "ce référentiel définira des standards observables : rythmes de bascule regard-écran / regard-client, techniques de guidage "
                "visuel sur tablette, verbalisation de maintien de lien pendant l'encodage PMS et régulation du regard face aux plaintes "
                "(Giacomel, 2019 ; Lajante & Remisch, 2023)."
            )
            rt.font.name = "Calibri"; rt.font.size = Pt(10); rt.font.color.rgb = COLOR_CHARCOAL

    # 5. Ajouter les 6 nouvelles références dans la Bibliographie par ordre alphabétique
    bib_heading = None
    for p in doc.paragraphs:
        if p.text.strip().startswith("Bibliographie"):
            bib_heading = p._p
            break

    if bib_heading is not None:
        # Collecter tous les paragraphes de bibliographie existants
        bib_items = []
        curr = bib_heading.getnext()
        while curr is not None:
            if curr.tag.endswith('p'):
                txt = ''.join([t.text for t in curr.xpath('.//w:t')]).strip()
                if txt:
                    bib_items.append((txt, curr))
            curr = curr.getnext()

        existing_texts = [b[0] for b in bib_items]

        # Pour chaque nouvelle référence, insérer au bon endroit alphabétique
        for item in NEW_TEXTS:
            prefix = item["auteurs"].split(",")[0].strip()
            if any(prefix in et and item["annee"] in et for et in existing_texts):
                continue
            
            # Créer le paragraphe XML
            p_new = parse_xml(f'<w:p {nsdecls("w")}/>')
            p_obj = docx.text.paragraph.Paragraph(p_new, doc)
            p_obj.paragraph_format.space_after = Pt(4)
            p_obj.paragraph_format.line_spacing = 1.15
            p_obj.paragraph_format.left_indent = Inches(0.25)
            p_obj.paragraph_format.first_line_indent = Inches(-0.25)
            
            # Séparer le texte avant l'URL
            apa_no_url = item["ref_apa"].replace(item["doi"], "").strip()
            r = p_obj.add_run(apa_no_url + " ")
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_CHARCOAL
            add_hyperlink(p_obj, item["doi"], item["doi"], color_rgb=COLOR_TEAL, bold=False)

            # Trouver le premier élément existant qui vient après alphabétiquement
            inserted = False
            for b_txt, b_elem in bib_items:
                if item["ref_apa"].lower() < b_txt.lower():
                    b_elem.addprevious(p_new)
                    bib_items.append((item["ref_apa"], p_new))
                    bib_items.sort(key=lambda x: x[0].lower())
                    inserted = True
                    break
            if not inserted:
                bib_items[-1][1].addnext(p_new)
                bib_items.append((item["ref_apa"], p_new))

        print("Updated Bibliography in strict alphabetical order!")

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
    integrate()
