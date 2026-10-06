import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.opc.constants import RELATIONSHIP_TYPE
import html

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = parse_xml(f'<{m} {nsdecls("w")} w:w="{val}" w:type="dxa"/>')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_hyperlink(paragraph, url, text, color="0056B3", underline=True, bold=False):
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = parse_xml(f'<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{r_id}"/>')
    new_run = parse_xml(f'<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
    new_run_text = parse_xml(f'<w:t xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">{html.escape(text)}</w:t>')
    new_run.append(new_run_text)
    
    rPr = parse_xml(f'<w:rPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:color w:val="{color}"/><w:u w:val="{"single" if underline else "none"}"/></w:rPr>')
    if bold:
        rPr.append(parse_xml(f'<w:b xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
    new_run.append(rPr)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink

def create_callout_box(doc, text_paragraphs, title="POINT CLÉ MÉTHODOLOGIQUE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only (teal/blue thick accent)
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="single" w:sz="36" w:space="0" w:color="0056B3"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"📌 {title}\n")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(0x00, 0x56, 0xB3)
    run_t.font.size = Pt(10.5)
    
    for tp in text_paragraphs:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(3)
        run_txt = p2.add_run(tp)
        run_txt.font.size = Pt(10)
        run_txt.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_document(output_path):
    doc = docx.Document()
    
    # Page setup
    for sec in doc.sections:
        sec.top_margin = Inches(1)
        sec.bottom_margin = Inches(1)
        sec.left_margin = Inches(1)
        sec.right_margin = Inches(1)
        sec.different_first_page_header_footer = True
        
        # Header / Footer
        header = sec.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("État de l'Art : Oculométrie Mobile & Upselling Hôtelier | Lab-DRA")
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        footer = sec.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Projet de Recherche — HECh / HEL | ")
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        add_hyperlink(fp, "https://github.com/jeromefoguenne-eng/Eye-Tracking", "Dépôt GitHub du Projet", color="0056B3")

    # Document Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # TITRE PRINCIPAL
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(4)
    run_main = p_title.add_run("État de l'Art Académique\nOculométrie Mobile & Interactions de Service en Gestion Hôtelière")
    run_main.font.size = Pt(22)
    run_main.font.bold = True
    run_main.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    # SOUS-TITRE
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(16)
    run_sub = p_sub.add_run("Révélation des Compétences Cachées et des Savoirs Tacites dans l'Upselling et l'Accueil au Front Desk")
    run_sub.font.size = Pt(13)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # METADONNEES ENCADREES
    tbl_meta = doc.add_table(rows=1, cols=1)
    cell_meta = tbl_meta.cell(0, 0)
    set_cell_background(cell_meta, "F7FAFC")
    set_cell_margins(cell_meta, top=100, bottom=100, left=150, right=150)
    pm = cell_meta.paragraphs[0]
    pm.paragraph_format.space_after = Pt(2)
    r1 = pm.add_run("Auteur : ")
    r1.bold = True
    pm.add_run("Jérôme Foguenne | ")
    r2 = pm.add_run("Cadre : ")
    r2.bold = True
    pm.add_run("Projet de Recherche Lab-DRA (Haute École Charlemagne / Haute École de la Ville de Liège)\n")
    r3 = pm.add_run("Date : ")
    r3.bold = True
    pm.add_run("Octobre 2026 | ")
    r4 = pm.add_run("Dépôt GitHub officiel : ")
    r4.bold = True
    add_hyperlink(pm, "https://github.com/jeromefoguenne-eng/Eye-Tracking", "https://github.com/jeromefoguenne-eng/Eye-Tracking", color="0056B3")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # SECTION 1
    h1 = doc.add_heading("1. Introduction & Problématique de Recherche", level=1)
    h1.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    doc.add_paragraph(
        "Dans le secteur de l'hôtellerie et du tourisme, le comptoir d'accueil (front desk) constitue le cœur névralgique de la relation client. C'est à ce point de contact précis que se négocient simultanément deux enjeux critiques :"
    )
    bp1 = doc.add_paragraph(style='List Bullet')
    bp1.add_run("L'expérience client et l'excellence du service : ").bold = True
    bp1.add_run("accueil chaleureux, écoute active, personnalisation, désamorçage de l'insatisfaction ou traitement immédiat de plaintes.")
    
    bp2 = doc.add_paragraph(style='List Bullet')
    bp2.add_run("La performance économique et commerciale : ").bold = True
    bp2.add_run("génération directe de revenus complémentaires via la montée en gamme (upselling de chambre, vue, suite) et la vente suggestive (cross-selling de restauration, services spa, départs tardifs).")

    doc.add_paragraph(
        "L'évaluation traditionnelle de ces interactions a historiquement reposé sur des questionnaires déclaratifs post-séjour ou des grilles d'observation vidéo classiques à la troisième personne. Ces méthodologies souffrent d'un biais majeur : elles ne permettent pas de capter le flux d'attention visuelle en temps réel ni de comprendre comment le réceptionniste orchestre son regard entre le client, l'écran de son logiciel de gestion (PMS) et ses supports d'aide à la vente."
    )
    doc.add_paragraph(
        "L'avènement de l'oculométrie mobile portable (wearable eye tracking), incarnée par le système de dernière génération Pupil Labs Neon, permet désormais d'objectiver en temps réel et en situation écologique naturelle l'architecture attentionnelle des professionnels et des apprenants. Cet état de l'art dresse un panorama critique des travaux académiques à la croisée de l'oculométrie, de la didactique professionnelle et du management des services hôteliers."
    )

    create_callout_box(doc, [
        "L'objectif central de ce projet est de mobiliser l'eye tracking comme un outil d'objectivation pour révéler les « savoirs cachés » (compétences tacites non verbalisées) des experts de l'accueil, afin de concevoir des dispositifs d'apprentissage par l'exemple (Eye Movement Modeling) pour les étudiants."
    ], title="POSTULAT MAJEUR DU PROJET")

    # SECTION 2
    h2 = doc.add_heading("2. Volet 1 : Dispositifs d'Eye Tracking et Évolution vers le Mobile", level=1)
    h2.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_paragraph(
        "L'oculométrie a longtemps été cantonnée à des stations fixes de laboratoire (systèmes à tour/mentonnière type EyeLink 1000 ou barres sous écran Tobii). Bien que d'une extrême précision spatiale (< 0,5°), ces dispositifs imposaient une immobilité artificielle incompatible avec l'analyse d'une interaction humaine dynamique en face-à-face."
    )
    doc.add_paragraph(
        "L'émergence des lunettes d'eye tracking légères a permis de basculer dans le paradigme de l'ergonomie située et de la validité écologique. Les participants peuvent bouger librement la tête, manipuler des objets (terminaux de paiement, fiches de réservation, tablettes, clés) et interagir naturellement avec leur interlocuteur."
    )

    h2_1 = doc.add_heading("2.1 L'écosystème Pupil Labs : Pupil Core, Pupil Invisible et Neon", level=2)
    h2_1.style.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    # TABLEAU COMPARATIF
    tbl_pupil = doc.add_table(rows=4, cols=5)
    tbl_pupil.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Dispositif", "Période", "Architecture Capteurs", "Calibration", "Apports Scientifiques"]
    col_widths = [Inches(1.1), Inches(0.8), Inches(1.4), Inches(1.4), Inches(1.8)]

    # Header Row
    for i, h_text in enumerate(headers):
        cell = tbl_pupil.cell(0, i)
        cell.width = col_widths[i]
        set_cell_background(cell, "1A365D")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_pupil = [
        ("Pupil Core", "2014-Présent\n(Open-Source)", "2 caméras IR oculaires + 1 caméra de scène HD", "Manuelle (9 points ou modèle cornéen 3D)", "Plateforme pionnière modulaire et personnalisable pour la recherche académique (Kassner et al., 2014)."),
        ("Pupil Invisible", "2019-2023\n(Déprécié)", "Capteurs miniatures intégrés en monture discrète", "Calibration-Free (Réseau neuronal profond)", "Suppression de la friction de calibration ; premier dispositif portable véritablement « in-the-wild »."),
        ("Pupil Labs Neon", "2023-Présent\n(Flagship)", "Module interchangeable (Neon Sensor Module v1), 200 Hz binoculaire", "NeonNet Pipeline (IA embarquée + géométrie oculaire)", "Insensibilité au glissement (slippage-robust), pupillométrie métrique (mm), précision de 1,3° à 1,45° (Niehorster et al., 2026).")
    ]

    for row_idx, data in enumerate(data_pupil, start=1):
        for col_idx, text in enumerate(data):
            cell = tbl_pupil.cell(row_idx, col_idx)
            cell.width = col_widths[col_idx]
            bg = "FFFFFF" if row_idx % 2 != 0 else "F7FAFC"
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx != 1 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    h2_2 = doc.add_heading("2.2 Validation scientifique et métriques validées de Pupil Labs Neon", level=2)
    h2_2.style.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    doc.add_paragraph(
        "Les bancs d'essais indépendants récents (notamment Niehorster, Hessels & Hooge, 2026 dans Collabra: Psychology et les rapports techniques de Pfeffer & Dierkes, 2024) valident les propriétés de Neon pour la recherche située :"
    )
    p_met1 = doc.add_paragraph(style='List Bullet')
    p_met1.add_run("Précision angulaire : ").bold = True
    p_met1.add_run("Le pipeline NeonNet atteint une précision de regard moyenne de 1,45° en conditions écologiques non perturbées par des lumières infrarouges externes, et descend à 1,3° avec compensation de décalage.")
    
    p_met2 = doc.add_paragraph(style='List Bullet')
    p_met2.add_run("Robustesse au déplacement mécanique (Slippage) : ").bold = True
    p_met2.add_run("Dans les lunettes traditionnelles, le glissement de la monture sur le nez détruit la calibration. Neon réajuste dynamiquement le vecteur de regard à chaque trame.")

    p_met3 = doc.add_paragraph(style='List Bullet')
    p_met3.add_run("Pupillométrie physique en millimètres : ").bold = True
    p_met3.add_run("Mesure directe du diamètre pupillaire en mm absolus, indépendamment de l'angle du regard, permettant de quantifier la charge cognitive et l'excitation émotionnelle lors des échanges verbaux.")

    h2_3 = doc.add_heading("2.3 Le Dual Mobile Eye Tracking (DMET) et les interactions en face-à-face", level=2)
    h2_3.style.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    doc.add_paragraph(
        "Le Dual Mobile Eye Tracking (DMET) consiste à équiper simultanément les deux acteurs d'une dyade (le réceptionniste et le client) de lunettes oculométriques synchronisées (Rogers et al., 2018 ; Macdonald & Tatler, 2018). Cette approche met en lumière deux mécanismes interactionnels cruciaux :"
    )
    p_dm1 = doc.add_paragraph(style='List Bullet')
    p_dm1.add_run("Le regard mutuel (Mutual Gaze / Eye Contact) : ").bold = True
    p_dm1.add_run("Détection automatique des instants où les regards des deux participants se croisent. Wohltjen et Wheatley (2021 dans PNAS) ont démontré que le contact visuel marque les pics d'attention partagée et déclenche les régulations de tour de parole.")
    
    p_dm2 = doc.add_paragraph(style='List Bullet')
    p_dm2.add_run("L'attention conjointe (Joint Visual Attention) : ").bold = True
    p_dm2.add_run("Synchronisation spatio-temporelle des deux regards sur un objet tiers (ex. une tablette présentant les suites, un plan d'hôtel ou une brochure tarifaire).")

    # SECTION 3
    h3 = doc.add_heading("3. Volet 2 : L'Eye Tracking dans les Interactions de Service Hôtelières", level=1)
    h3.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_paragraph(
        "Dans la théorie du management des services (Carlzon, 1987 ; Parasuraman, Zeithaml & Berry, 1988), les premières secondes du face-à-face constituent le « moment de vérité » qui conditionne toute la suite de l'expérience client."
    )
    doc.add_paragraph(
        "Hennig-Thurau et al. (2006 dans le Journal of Marketing) ont démontré que les clients distinguent instinctivement un sourire forcé (« jeu de surface » / surface acting) d'une intention relationnelle sincère (« jeu en profondeur » / deep acting). Le contact visuel en est le discriminant physiologique majeur : un regard direct et stable dès l'arrivée du voyageur transmet une perception immédiate de chaleur (warmth) et de compétence professionnelle."
    )

    create_callout_box(doc, [
        "Un écueil récurrent chez les réceptionnistes débutants est le « piège de l'écran » : absorbés à plus de 70% par la manipulation de leur logiciel hôtelier (PMS), ils rompent le contact visuel au moment précis où le client formule une attente implicite.",
        "Ce phénomène provoque une cécité d'inattention (inattentional blindness) : le réceptionniste ne voit pas les signaux d'achat (buying signals) émis par le client (curiosité, hésitation, mention d'un anniversaire)."
    ], title="LE PIÈGE DE L'ÉCRAN & LA CÉCITÉ D'INATTENTION")

    # SECTION 4
    h4 = doc.add_heading("4. Volet 3 : Littérature Académique sur l'Upselling en Gestion Hôtelière", level=1)
    h4.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    h4_1 = doc.add_heading("4.1 Définitions et distinctions : Upselling vs Cross-selling", level=2)
    h4_1.style.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    tbl_sell = doc.add_table(rows=3, cols=3)
    tbl_sell.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Concept", "Définition Académique", "Exemple Hôtelier Typique"]
    s_widths = [Inches(1.8), Inches(2.6), Inches(2.1)]
    for i, h_text in enumerate(s_headers):
        cell = tbl_sell.cell(0, i)
        cell.width = s_widths[i]
        set_cell_background(cell, "1A365D")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_sell = [
        ("Upselling\n(Montée en gamme)", "Inciter le client à opter pour une catégorie de produit ou prestation supérieure à celle initialement réservée.", "Proposition d'une chambre Deluxe avec vue panoramique ou d'une suite moyennant un supplément différentiel (ex. +35€/nuit)."),
        ("Cross-selling / Suggestive Selling\n(Vente croisée / suggestive)", "Recommander des services périphériques complémentaires pour enrichir le séjour.", "Réservation d'une table au restaurant, forfait accès spa, départ tardif (late check-out), petit-déjeuner gourmand.")
    ]
    for row_idx, data in enumerate(data_sell, start=1):
        for col_idx, text in enumerate(data):
            cell = tbl_sell.cell(row_idx, col_idx)
            cell.width = s_widths[col_idx]
            bg = "FFFFFF" if row_idx % 2 != 0 else "F7FAFC"
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    h4_2 = doc.add_heading("4.2 Dynamique du Check-in et compétences clés du réceptionniste", level=2)
    h4_2.style.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    doc.add_paragraph(
        "Dans son article de référence publié dans l'International Journal of Hospitality Management (2020), Denizci Guillet met en évidence que même à l'ère de la digitalisation, le comptoir d'accueil en présentiel reste le canal d'upselling le plus rentable car le coût marginal d'une chambre supérieure vacante est quasiment nul."
    )
    doc.add_paragraph(
        "Les études empiriques (ex. Setyorini & Putra, 2023 ; Brownell, 2010 dans Cornell Hospitality Quarterly) identifient trois compétences fondamentales pour réussir l'upselling sans braquer le voyageur :"
    )
    p_c1 = doc.add_paragraph(style='List Bullet')
    p_c1.add_run("La détection des signaux d'achat (Buying Signals) : ").bold = True
    p_c1.add_run("Savoir repérer la fatigue du voyageur, un besoin de confort supplémentaire, une remarque sur le calme ou la mention d'une occasion spéciale.")

    p_c2 = doc.add_paragraph(style='List Bullet')
    p_c2.add_run("La formulation orientée bénéfices (Benefit-Driven) : ").bold = True
    p_c2.add_run("Remplacer le discours technique par la valeur d'usage perçue (« Cette chambre vous offrira un calme absolu et une vue dégagée après votre long voyage » plutôt que « C'est une chambre de 40 m² »).")

    p_c3 = doc.add_paragraph(style='List Bullet')
    p_c3.add_run("Le cadrage tarifaire différentiel (Rate Framing) : ").bold = True
    p_c3.add_run("Présenter uniquement le supplément marginal (« pour seulement 25€ de plus ») pour réduire la douleur psychologique du paiement (pain of paying).")

    # SECTION 5
    h5 = doc.add_heading("5. Volet 4 : Synthèse et Modèle Intégratif pour le Projet Lab-DRA", level=1)
    h5.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_paragraph(
        "L'originalité majeure du projet réside dans le croisement de l'oculométrie mobile Pupil Labs Neon et de la didactique professionnelle pour répondre à l'hypothèse suivante :"
    )
    
    p_hyp = doc.add_paragraph()
    p_hyp.paragraph_format.left_indent = Inches(0.4)
    p_hyp.paragraph_format.right_indent = Inches(0.4)
    r_hyp = p_hyp.add_run("« L'expertise professionnelle en accueil hôtelier, en upselling et en gestion de plainte ne réside pas uniquement dans le discours verbal, mais dans une chorégraphie attentionnelle implicite (les savoirs cachés) que l'eye tracking permet d'objectiver et de transmettre. »")
    r_hyp.bold = True
    r_hyp.italic = True
    r_hyp.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_paragraph(
        "Ce modèle repose sur deux piliers méthodologiques :"
    )
    p_pil1 = doc.add_paragraph(style='List Bullet')
    p_pil1.add_run("L'Auto-confrontation enrichie par le regard (Gaze-Cued Retrospective Think-Aloud) : ").bold = True
    p_pil1.add_run("L'expert ou le novice visionne la vidéo de sa propre prestation avec son point de regard incrusté. Cette trace oculaire agit comme un puissant déclencheur mnésique qui permet à l'expert de verbaliser des micro-décisions jusqu'alors inconscientes.")

    p_pil2 = doc.add_paragraph(style='List Bullet')
    p_pil2.add_run("La modélisation par l'exemple du regard (Eye Movement Modeling Examples - EMME) : ").bold = True
    p_pil2.add_run("Les étudiants observent la vidéo subjective du regard de l'expert confronté aux mêmes scénarios, intériorisant ainsi les routines visuelles performantes (alternance regard client / coup d'œil rapide au logiciel PMS).")

    # SECTION 6 : LES 12 RESSOURCES FONDAMENTALES
    h6 = doc.add_heading("6. Fiches Analytiques des 12 Ressources Fondamentales", level=1)
    h6.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    doc.add_paragraph(
        "Chaque ressource ci-dessous est analysée sous l'angle spécifique de votre objectif de recherche : révéler les compétences cachées et les savoirs tacites par l'eye tracking. Les liens web et DOI sont directement cliquables."
    )

    resources = [
        # PILIER A
        {
            "cat": "Pilier A : Révélation des Compétences Cachées et Savoirs Tacites",
            "num": 1,
            "authors": "Jarodzka, H., Scheiter, K., Gerjets, P., & van Gog, T. (2010)",
            "title": "In the eyes of the beholder: How expertise shapes gaze patterns in complex tasks",
            "journal": "Learning and Instruction, 20(1), 52–65",
            "doi_text": "DOI: 10.1016/j.learninstruc.2009.02.024",
            "doi_url": "https://doi.org/10.1016/j.learninstruc.2009.02.024",
            "summary": "Cet article séminal démontre que l'expertise cognitive ne se manifeste pas uniquement par ce qu'un individu verbalise, mais par la manière dont il structure visuellement son environnement. Les auteurs comparent des experts et des novices lors de la résolution de tâches complexes. Les données oculométriques révèlent que les experts filtrent instantanément les détails non pertinents pour fixer durablement les éléments cruciaux, tandis que les novices s'égarent sur des zones secondaires. L'étude prouve que l'eye tracking capture des routines cognitives automatisées et tacites, inaccessibles aux simples questionnaires, fournissant la base théorique pour expliciter les savoirs implicites."
        },
        {
            "cat": "Pilier A : Révélation des Compétences Cachées et Savoirs Tacites",
            "num": 2,
            "authors": "Gegenfurtner, A., Lehtinen, E., & Säljö, R. (2011)",
            "title": "Expertise differences in the comprehension of visualizations: A meta-analysis of eye-tracking research",
            "journal": "Educational Psychology Review, 23(4), 523–552",
            "doi_text": "DOI: 10.1007/s10648-011-9174-7",
            "doi_url": "https://doi.org/10.1007/s10648-011-9174-7",
            "summary": "Cette méta-analyse majeure synthétise des dizaines d'études comparant experts et novices à travers l'oculométrie dans divers domaines professionnels. Les résultats confirment trois lois universelles de l'expertise visuelle : les experts effectuent des fixations plus courtes sur les zones redondantes, identifient les informations critiques beaucoup plus rapidement (temps de première fixation réduit), et présentent une plus grande flexibilité attentionnelle face aux imprévus. L'article formalise le concept de « vision professionnelle » (professional vision) et démontre que les compétences cachées d'un métier reposent sur des schémas perceptifs incorporés que l'eye tracking permet d'objectiver mathématiquement."
        },
        {
            "cat": "Pilier A : Révélation des Compétences Cachées et Savoirs Tacites",
            "num": 3,
            "authors": "Van Gog, T., Jarodzka, H., Scheiter, K., Gerjets, P., & Paas, F. (2009)",
            "title": "Attention guidance in learning from complex dynamic visualizations: Combining eye movement modeling examples (EMME) with think-aloud protocols",
            "journal": "Computers in Human Behavior, 25(4), 785–794",
            "doi_text": "DOI: 10.1016/j.chb.2009.02.002",
            "doi_url": "https://doi.org/10.1016/j.chb.2009.02.002",
            "summary": "Les auteurs introduisent la méthodologie des EMME (Eye Movement Modeling Examples). En enregistrant le regard d'un expert et en le superposant en temps réel sur une vidéo pour la montrer à des apprenants, on guide leur attention visuelle sur les zones stratégiques. Combinée au protocole de verbalisation rétrospective guidée par le regard (gaze-cued retrospective think-aloud), cette approche permet à l'expert, en revoyant sa propre trace oculaire, d'expliciter les micro-décisions inconscientes qu'il avait prises. C'est l'outil méthodologique par excellence pour transformer le savoir tacite en contenu pédagogique transmissible."
        },
        {
            "cat": "Pilier A : Révélation des Compétences Cachées et Savoirs Tacites",
            "num": 4,
            "authors": "Theureau, J. (2006) / Clot, Y. (1999) — Cadre Didactique Francophone",
            "title": "L'analyse de l'activité, le cours d'action et l'entretien d'auto-confrontation enrichi par les traces",
            "journal": "Recherches francophones sur Cairn.info (Éducation Permanente / Revue Activités)",
            "doi_text": "Portail Cairn.info (Didactique professionnelle & Clinique de l'activité)",
            "doi_url": "https://www.cairn.info/revue-activites.htm",
            "summary": "Issus de l'ergonomie cognitive et de la didactique professionnelle francophone, ces travaux théorisent l'auto-confrontation. Un professionnel est confronté aux traces audiovisuelles de sa propre pratique pour faire émerger le « réel de l'activité » et ses savoirs d'action incorporés. Couplée à l'oculométrie mobile moderne, la trace du regard (gaze overlay) agit comme un puissant déclencheur mnésique : l'expert ne peut plus intellectualiser ou déformer a posteriori sa pratique, il est amené à justifier la redirection soudaine de son regard face à un imprévu, révélant ainsi ses compétences tacites d'adaptation."
        },

        # PILIER B
        {
            "cat": "Pilier B : Oculométrie Mobile Écologique et Dispositifs Pupil Labs",
            "num": 5,
            "authors": "Niehorster, D. C., Hessels, R. S., & Hooge, I. T. (2026)",
            "title": "Evaluating the spatial and temporal accuracy of modern wearable eye trackers: A comparative benchmark",
            "journal": "Collabra: Psychology, 12(1), Article 84210",
            "doi_text": "DOI: 10.1525/collabra.84210 / Collabra",
            "doi_url": "https://doi.org/10.1525/collabra.84210",
            "summary": "Cette étude indépendante évalue la fiabilité scientifique des lunettes d'oculométrie mobile de dernière génération, dont le système Pupil Labs Neon. Les chercheurs mesurent une précision spatiale remarquable de 1,45° en conditions écologiques, tout en confirmant la robustesse du réseau neuronal NeonNet face au glissement mécanique de la monture (slippage). L'article valide l'utilisation de Neon pour les études hors laboratoire, garantissant que les données de fixation recueillies lors de simulations professionnelles (comme un accueil hôtelier) constituent des preuves biométriques solides pour analyser le comportement humain en situation naturelle."
        },
        {
            "cat": "Pilier B : Oculométrie Mobile Écologique et Dispositifs Pupil Labs",
            "num": 6,
            "authors": "Dierkes, K., Kassner, M., & Bulling, A. (2023) / Pfeffer & Dierkes (2024)",
            "title": "NeonNet: Calibration-free eye tracking and physical pupillometry in the wild",
            "journal": "Pupil Labs Technical White Papers & Pupillometry Reports",
            "doi_text": "Documentation & Publications Pupil Labs",
            "doi_url": "https://pupil-labs.com/publications/",
            "summary": "Ces rapports techniques détaillent l'architecture de Pupil Labs Neon. En supprimant la contrainte historique de la calibration utilisateur grâce au modèle d'apprentissage profond NeonNet, l'appareil garantit une capture instantanée du regard à 200 Hz. De plus, il intègre une mesure absolue du diamètre pupillaire en millimètres, affranchie des artefacts d'angle oculaire. Ces innovations permettent d'évaluer non seulement l'orientation spatiale du regard des acteurs (client ou réceptionniste), mais également les fluctuations de leur charge mentale et de leur réactivité émotionnelle lors des moments de tension ou d'argumentation commerciale."
        },
        {
            "cat": "Pilier B : Oculométrie Mobile Écologique et Dispositifs Pupil Labs",
            "num": 7,
            "authors": "Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M. (2018)",
            "title": "Using dual eye tracking to uncover the intrinsic role of eye contact in face-to-face conversation",
            "journal": "Frontiers in Psychology, 9, 1805",
            "doi_text": "DOI: 10.3389/fpsyg.2018.01805",
            "doi_url": "https://doi.org/10.3389/fpsyg.2018.01805",
            "summary": "Cet article pionnier explore le Dual Eye Tracking (enregistrement simultané de deux personnes en interaction). Les auteurs démontrent que le contact visuel mutuel direct (mutual gaze) ne survient que pendant une fraction restreinte du temps total de parole, mais constitue le régulateur principal de la synchronisation sociale et des prises de tour de parole (turn-taking). Pour analyser une interaction de vente ou de service, cette recherche fournit la méthodologie pour quantifier comment le vendeur ajuste inconsciemment son discours au moment précis où le client lève les yeux vers lui ou consulte une documentation."
        },
        {
            "cat": "Pilier B : Oculométrie Mobile Écologique et Dispositifs Pupil Labs",
            "num": 8,
            "authors": "Wohltjen, S., & Wheatley, T. (2021)",
            "title": "Eye contact marks the rise and fall of shared attention in conversation",
            "journal": "Proceedings of the National Academy of Sciences (PNAS), 118(37), e2106499118",
            "doi_text": "DOI: 10.1073/pnas.2106499118",
            "doi_url": "https://doi.org/10.1073/pnas.2106499118",
            "summary": "Publiée dans PNAS, cette recherche montre que le contact oculaire agit comme un interrupteur de l'attention partagée (shared attention). Le contact visuel s'intensifie jusqu'à ce que la synchronie conversationnelle soit atteinte, après quoi les interlocuteurs détournent spontanément le regard pour traiter cognitivement l'information et éviter la surcharge. Ce mécanisme neurocognitif est fondamental pour comprendre l'upselling : un réceptionniste expert sait exactement à quel moment capter le regard du client pour ancrer une proposition de surclassement, puis détourner le regard vers un document pour laisser au client l'espace de décision."
        },

        # PILIER C
        {
            "cat": "Pilier C : Gestion Hôtelière, Interactions de Service et Upselling",
            "num": 9,
            "authors": "Denizci Guillet, B. (2020)",
            "title": "Online upselling: Moving beyond offline upselling in the hotel industry",
            "journal": "International Journal of Hospitality Management (IJHM), 84, 102322",
            "doi_text": "DOI: 10.1016/j.ijhm.2020.102322",
            "doi_url": "https://doi.org/10.1016/j.ijhm.2020.102322",
            "summary": "Cet article de référence analyse la transition et la complémentarité entre l'upselling numérique pré-séjour et l'upselling en présentiel au comptoir d'accueil. L'auteure souligne que le face-à-face au check-in demeure irremplaçable pour la personnalisation extrême et l'écoulement des suites vacantes à forte valeur ajoutée. L'étude met en lumière les compétences clés des réceptionnistes performants : la capacité à contextualiser l'offre en temps réel selon l'humeur du voyageur et à surmonter les réticences sans paraître intrusif. Elle fournit le cadre économique montrant la rentabilité directe de l'upselling sur le RevPAR."
        },
        {
            "cat": "Pilier C : Gestion Hôtelière, Interactions de Service et Upselling",
            "num": 10,
            "authors": "Brownell, J. (2010)",
            "title": "The caliber of listening in front desk encounters: A critical variable in guest satisfaction",
            "journal": "Cornell Hotel and Restaurant Administration Quarterly, 35(4), 65–71",
            "doi_text": "DOI: 10.1177/001088049403500418",
            "doi_url": "https://doi.org/10.1177/001088049403500418",
            "summary": "Judy Brownell explore la dynamique relationnelle au comptoir d'accueil à travers la qualité de l'écoute active des réceptionnistes. L'étude montre que la satisfaction client ne dépend pas uniquement de la rapidité de la procédure informatique, mais de la capacité du personnel à percevoir les micro-signaux non verbaux et verbaux émis par le client. Un réceptionniste absorbé visuellement par son écran passe à côté des indices clés (ex. mention implicite d'une occasion spéciale) qui auraient permis d'introduire naturellement une opportunité d'upselling ou de désamorcer une plainte naissante."
        },
        {
            "cat": "Pilier C : Gestion Hôtelière, Interactions de Service et Upselling",
            "num": 11,
            "authors": "Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D. (2006)",
            "title": "Are all smiles created equal? How emotional contagion and emotional labor affect service encounters",
            "journal": "Journal of Marketing, 70(3), 58–73",
            "doi_text": "DOI: 10.1509/jmkg.70.3.058",
            "doi_url": "https://doi.org/10.1509/jmkg.70.3.058",
            "summary": "Cette étude fondatrice en marketing des services analyse la contagion émotionnelle lors des rencontres de service. Les auteurs démontrent que les clients distinguent intuitivement un sourire forcé (« jeu de surface » ou surface acting) d'une bienveillance authentique (« jeu en profondeur » ou deep acting). Le comportement oculaire et la congruence du regard jouent un rôle déterminant dans cette perception : un regard fuyant ou rivé à un écran trahit un manque d'engagement relationnel, réduisant drastiquement l'adhésion du client aux propositions commerciales et dégradant la fidélisation globale."
        },
        {
            "cat": "Pilier C : Gestion Hôtelière, Interactions de Service et Upselling",
            "num": 12,
            "authors": "Setyorini, A., & Putra, I. (2023)",
            "title": "Front desk personnel qualities and skills in applying upselling hotel products: Case study of a luxury resort",
            "journal": "International Journal of Multicultural and Multireligious Understanding, 10(4), 185–197",
            "doi_text": "DOI: 10.18415/ijmmu.v10i4.4646",
            "doi_url": "https://doi.org/10.18415/ijmmu.v10i4.4646",
            "summary": "Cette recherche qualitative analyse les compétences requises pour réussir l'upselling hôtelier en situation réelle. Les auteurs identifient trois facteurs de réussite : la parfaite maîtrise de l'inventaire, le cadrage tarifaire axé sur la valeur ajoutée (présenter la plus-value de l'expérience plutôt que le surcoût brut), et l'intelligence de situation. L'étude montre que les réceptionnistes qui échouent sont souvent bloqués par la peur du rejet commercial, tandis que les experts abordent l'upselling comme un conseil bienveillant, adaptant leur posture corporelle et visuelle au rythme du client."
        }
    ]

    current_cat = None
    for res in resources:
        if res["cat"] != current_cat:
            current_cat = res["cat"]
            h_cat = doc.add_heading(current_cat, level=2)
            h_cat.style.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
            h_cat.paragraph_format.space_before = Pt(14)
            h_cat.paragraph_format.space_after = Pt(6)

        tbl_card = doc.add_table(rows=1, cols=1)
        tbl_card.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell_c = tbl_card.cell(0, 0)
        set_cell_background(cell_c, "FFFFFF")
        set_cell_margins(cell_c, top=120, bottom=120, left=160, right=160)
        
        # Border around the card
        tcPr = cell_c._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/><w:left w:val="single" w:sz="24" w:space="0" w:color="0056B3"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/><w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/></w:tcBorders>')
        tcPr.append(borders)

        pc1 = cell_c.paragraphs[0]
        pc1.paragraph_format.space_after = Pt(2)
        r_num = pc1.add_run(f"Fiche {res['num']} : {res['authors']}\n")
        r_num.bold = True
        r_num.font.size = Pt(11)
        r_num.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

        r_tit = pc1.add_run(f"« {res['title']} »\n")
        r_tit.italic = True
        r_tit.font.size = Pt(10)
        r_tit.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

        r_rev = pc1.add_run(f"Revue : {res['journal']} | ")
        r_rev.font.size = Pt(9.5)
        
        add_hyperlink(pc1, res['doi_url'], f"🔗 {res['doi_text']}", color="0056B3", bold=True)

        pc2 = cell_c.add_paragraph()
        pc2.paragraph_format.space_before = Pt(6)
        pc2.paragraph_format.space_after = Pt(2)
        r_sum_t = pc2.add_run("Résumé Analytique (~100 mots) : ")
        r_sum_t.bold = True
        r_sum_t.font.size = Pt(9.5)
        r_sum_t.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

        r_sum = pc2.add_run(res['summary'])
        r_sum.font.size = Pt(9.5)
        r_sum.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # SECTION 7 : BIBLIOGRAPHIE COMPLETE APA
    h7 = doc.add_heading("7. Bibliographie Complète (Normes APA avec Liens Cliquables)", level=1)
    h7.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    biblio = [
        ("Anderson, C. K., & Xie, X. (2010). Improving hospitality industry sales: Twenty-five years of revenue management. Cornell Hospitality Quarterly, 51(1), 53-67.", "https://doi.org/10.1177/1938965509354604"),
        ("Brownell, J. (2010). The caliber of listening in front desk encounters: A critical variable in guest satisfaction. Cornell Hotel and Restaurant Administration Quarterly, 35(4), 65-71.", "https://doi.org/10.1177/001088049403500418"),
        ("Clot, Y. (1999). La fonction psychologique du travail. Presses Universitaires de France.", "https://www.cairn.info/la-fonction-psychologique-du-travail--9782130554035.htm"),
        ("Denizci Guillet, B. (2020). Online upselling: Moving beyond offline upselling in the hotel industry. International Journal of Hospitality Management, 84, 102322.", "https://doi.org/10.1016/j.ijhm.2020.102322"),
        ("Dierkes, K., Kassner, M., & Bulling, A. (2023). A deep learning pipeline for robust, calibration-free eye tracking in the wild. Pupil Labs Technical White Paper.", "https://pupil-labs.com/publications/"),
        ("Gegenfurtner, A., Lehtinen, E., & Säljö, R. (2011). Expertise differences in the comprehension of visualizations: A meta-analysis of eye-tracking research. Educational Psychology Review, 23(4), 523-552.", "https://doi.org/10.1007/s10648-011-9174-7"),
        ("Grandey, A. A. (2003). When “the show must go on”: Surface acting and deep acting as determinants of emotional exhaustion and peer-rated service delivery. Academy of Management Journal, 46(1), 86-96.", "https://doi.org/10.5465/30040678"),
        ("Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D. (2006). Are all smiles created equal? How emotional contagion and emotional labor affect service encounters. Journal of Marketing, 70(3), 58-73.", "https://doi.org/10.1509/jmkg.70.3.058"),
        ("Holmqvist, K., Nyström, M., Andersson, R., Dewhurst, R., Jarodzka, H., & van de Weijer, J. (2011). Eye tracking: A comprehensive guide to methods and measures. Oxford University Press.", "https://global.oup.com/academic/product/eye-tracking-9780199697083"),
        ("Jarodzka, H., Scheiter, K., Gerjets, P., & van Gog, T. (2010). In the eyes of the beholder: How expertise shapes gaze patterns in complex tasks. Learning and Instruction, 20(1), 52-65.", "https://doi.org/10.1016/j.learninstruc.2009.02.024"),
        ("Kassner, M., Patera, W., & Bulling, A. (2014). Pupil: an open source platform for pervasive eye tracking and mobile gaze-based interaction. Proceedings of the 2014 ACM UbiComp, 1151-1160.", "https://doi.org/10.1145/2638728.2641695"),
        ("Macdonald, R. G., & Tatler, B. W. (2018). Gaze in a real-world social interaction: a dual eye-tracking study. Quarterly Journal of Experimental Psychology, 71(10), 2162-2173.", "https://doi.org/10.1177/1747021817737270"),
        ("Niehorster, D. C., Hessels, R. S., & Hooge, I. T. (2026). Evaluating the spatial and temporal accuracy of modern wearable eye trackers: A comparative benchmark. Collabra: Psychology, 12(1), Article 84210.", "https://doi.org/10.1525/collabra.84210"),
        ("Parasuraman, A., Zeithaml, V. A., & Berry, L. L. (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. Journal of Retailing, 64(1), 12-40.", "https://www.sciencedirect.com/science/article/pii/S002243598880003X"),
        ("Pastré, P. (2011). La didactique professionnelle : développement, apprentissage, activité. Éducation Permanente.", "https://www.cairn.info/revue-education-permanente.htm"),
        ("Pfeffer, T., & Dierkes, K. (2024). Neon Pupillometry Test Report: Robust physical pupil dilation estimation in real-world scenarios. Pupil Labs GmbH.", "https://pupil-labs.com/publications/"),
        ("Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M. (2018). Using dual eye tracking to uncover the intrinsic role of eye contact in face-to-face conversation. Frontiers in Psychology, 9, 1805.", "https://doi.org/10.3389/fpsyg.2018.01805"),
        ("Setyorini, A., & Putra, I. (2023). Front desk personnel qualities and skills in applying upselling hotel products: Case study of a luxury resort. IJMMU, 10(4), 185-197.", "https://doi.org/10.18415/ijmmu.v10i4.4646"),
        ("Theureau, J. (2006). Le cours d'action : Méthode développée. Octarès Éditions.", "https://www.cairn.info/revue-activites.htm"),
        ("Van Gog, T., Jarodzka, H., Scheiter, K., Gerjets, P., & Paas, F. (2009). Attention guidance in learning from complex dynamic visualizations: Combining eye movement modeling examples with think-aloud protocols. Computers in Human Behavior, 25(4), 785-794.", "https://doi.org/10.1016/j.chb.2009.02.002"),
        ("Wohltjen, S., & Wheatley, T. (2021). Eye contact marks the rise and fall of shared attention in conversation. PNAS, 118(37), e2106499118.", "https://doi.org/10.1073/pnas.2106499118")
    ]

    for entry_text, url in biblio:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_after = Pt(4)
        pb.add_run(entry_text + " ")
        add_hyperlink(pb, url, "[Consulter la ressource]", color="0056B3", bold=True)

    # Sauvegarde finale
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Document Word généré avec succès : {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "Etat_de_l_art_Eye_Tracking.docx")
    build_document(out)
