# -*- coding: utf-8 -*-
"""
Générateur du Traité Méthodologique Exhaustif (Word .docx) :
Propositions Méthodologiques Approfondies - Projet SIMACCUEIL
Haute École Charlemagne (HECh) / Haute École de Liège (HEL) / Lab-DRA
Chercheur Principal : Jérôme Foguenne
"""

import os
import sys
import shutil

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

LOCAL_DOCX = r"C:\Users\TrendingPC\.gemini\antigravity\scratch\Eye-Tracking\docs\Propositions_Methodologiques_SIMACCUEIL.docx"
DRIVE_DOCX = r"C:\Google Drive\Prépas light\HECh\Projet recherche\Propositions Methodologiques - SIMACCUEIL.docx"

COLOR_NAVY = RGBColor(27, 54, 93)      # #1B365D
COLOR_TEAL = RGBColor(14, 134, 212)    # #0E86D4
COLOR_CHARCOAL = RGBColor(44, 62, 80)  # #2C3E50
COLOR_MUTED = RGBColor(100, 110, 120)  # #646E78

HEX_NAVY = "1B365D"
HEX_TEAL = "0E86D4"
HEX_LIGHT_BG = "F4F6F9"
HEX_ALT_ROW = "F9FAFC"

def add_header_footer(doc):
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)
        
        # Header
        hdr = s.header
        p_hdr = hdr.paragraphs[0]
        p_hdr.text = "Lab-DRA | SIMACCUEIL — Traité Méthodologique Exhaustif & Opérationnel"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.style.font.name = "Calibri"
        p_hdr.style.font.size = Pt(8.5)
        p_hdr.style.font.color.rgb = COLOR_MUTED
        
        # Footer
        ftr = s.footer
        p_ftr = ftr.paragraphs[0]
        p_ftr.text = "HECh / HEL — Jérôme Foguenne (Chercheur Principal)  |  Traité de Recherche Appliquée"
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ftr.style.font.name = "Calibri"
        p_ftr.style.font.size = Pt(8.5)
        p_ftr.style.font.color.rgb = COLOR_MUTED

def style_cell(cell, bg_color=None, top_pad=100, bot_pad=100, left_pad=140, right_pad=140, border_left=None):
    tcPr = cell._tc.get_or_add_tcPr()
    if bg_color:
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{bg_color}"/>')
        tcPr.append(shd)
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top_pad}" w:type="dxa"/><w:bottom w:w="{bot_pad}" w:type="dxa"/><w:left w:w="{left_pad}" w:type="dxa"/><w:right w:w="{right_pad}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)
    if border_left:
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="{border_left.get("sz", 24)}" w:space="0" w:color="{border_left.get("color", HEX_NAVY)}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(borders)

def build_exhaustive_word():
    doc = Document()
    add_header_footer(doc)
    
    # ----------------------------------------------------
    # PAGE DE TITRE / CARTOUCHE OFFICIEL
    # ----------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(6)
    r_inst = p_inst.add_run("HAUTE ÉCOLE CHARLEMAGNE (HECh) — HAUTE ÉCOLE DE LIÈGE (HEL)\nLABORATOIRE DE RECHERCHE APPLIQUÉE LAB-DRA")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(10)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_TEAL

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("TRAITÉ MÉTHODOLOGIQUE EXHAUSTIF")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run("Trois Propositions Méthodologiques Complètes, Vulgarisées & Opérationnelles pour le Projet SIMACCUEIL\nOculométrie Mobile (Pupil Labs Neon), Didactique Professionnelle & Accueil Hôtelier (Upselling & Réclamations)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_CHARCOAL

    # Table cartouche métadonnées
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Chercheur Principal", "Jérôme Foguenne (HECh / HEL)"),
        ("Ancrage Théorique", "État de l'art consolidé (22 références académiques majeures)"),
        ("Matériel d'Expérimentation", "Lunettes d'Eye Tracking Mobile Pupil Labs Neon (200 Hz), Écran PMS & Tablette"),
        ("Finalités Stratégiques", "Dossier de candidature recherche, financements compétitifs & innovation curriculaire")
    ]
    for r_idx, (k, v) in enumerate(meta_data):
        c0, c1 = meta_table.rows[r_idx].cells
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        style_cell(c0, bg_color=HEX_LIGHT_BG, top_pad=80, bot_pad=80, left_pad=120, right_pad=120)
        style_cell(c1, bg_color="FFFFFF", top_pad=80, bot_pad=80, left_pad=120, right_pad=120)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_NAVY
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_CHARCOAL

    doc.add_page_break()

    # ----------------------------------------------------
    # SECTION 1 : CADRE GÉNÉRAL & GLOSSAIRE VULGARISÉ
    # ----------------------------------------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)
    r1 = h1.add_run("1. Cadre Général, Épistémologie & Glossaire Vulgarisé")
    r1.font.name = "Calibri"
    r1.font.size = Pt(16)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY

    p_in = doc.add_paragraph()
    p_in.paragraph_format.line_spacing = 1.15
    p_in.paragraph_format.space_after = Pt(8)
    p_in.add_run(
        "Au comptoir de réception d'un hôtel haut de gamme, le personnel est soumis à une injonction paradoxale permanente : "
        "d'un côté, une exigence relationnelle et empathique maximale (accueillir le client, pratiquer l'écoute active, apaiser une réclamation, "
        "négocier un surclassement) ; de l'autre, une contrainte procédurale et informatique lourde (manipuler le PMS, contrôler les tarifs, vérifier les disponibilités). "
        "Le projet SIMACCUEIL étudie cette tension à travers l'oculométrie mobile de dernière génération (Pupil Labs Neon). "
        "Afin de concilier la plus stricte rigueur académique et une accessibilité pédagogique totale, les concepts clés sont définis ci-après :"
    )

    glossary_items = [
        ("Oculométrie mobile (Wearable Eye Tracking)", "Technique de mesure continue du regard au moyen de lunettes légères (Pupil Labs Neon, 200 Hz). Contrairement aux systèmes de bureau qui imposent l'immobilité devant un écran d'ordinateur, ces lunettes permettent au réceptionniste d'interagir naturellement en face-à-face tout en consultant son logiciel et sa tablette."),
        ("Fixation & Saccade", "Une fixation est un arrêt stable du regard (au moins 100 ms) durant lequel le cerveau prélève et traite l'information visuelle nette. Une saccade est le saut ultra-rapide (20 à 40 ms) d'un point à un autre, pendant lequel le cerveau neutralise temporairement la vision pour éviter le flou de mouvement."),
        ("Zones d'Intérêt (AOI - Areas of Interest)", "Régions virtuelles découpées dans l'environnement pour comptabiliser les métriques du regard : AOI statiques sur l'écran fixe du PMS vs AOI dynamiques suivant le visage du client en mouvement ou la tablette manipulée."),
        ("Charge cognitive (Cognitive Load Theory - CLT)", "Quantité d'effort mental mobilisée dans la mémoire de travail. La charge extrinsèque est le gaspillage d'énergie causé par la mauvaise maîtrise d'un logiciel ; son automatisation libère des ressources pour observer le client."),
        ("PMS (Property Management System)", "Progiciel central d'exploitation hôtelière (planning des chambres, profils clients, facturation, assignation des clés)."),
        ("Upselling Multicanal", "Action commerciale consistant à proposer au voyageur une prestation supérieure (chambre plus spacieuse, vue, suite) moyennant un supplément de prix, en articulant les consultations préalables en ligne et la négociation physique en réception."),
        ("EMME (Eye-Movement Modelling Examples)", "Dispositif d'apprentissage par observation où l'étudiant visionne une vidéo montrant un expert en action avec la superposition dynamique de son regard."),
        ("Effet Spotlight", "Technique visuelle pour les vidéos EMME où la zone regardée par l'expert est maintenue en pleine clarté tandis que le reste de la scène est doucement estompé dans un voile flou, guidant le regard sans distraction."),
        ("Cours d'action & Autoconfrontation", "Paradigme ergonomique postulant que l'activité humaine est une construction de sens propre à l'acteur. L'entretien d'autoconfrontation consiste à faire visionner au participant sa propre vidéo sous eye tracking pour recueillir son point de vue sur son vécu intérieur.")
    ]
    for term, defn in glossary_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.left_indent = Inches(0.2)
        p_item.paragraph_format.space_after = Pt(3)
        r_t = p_item.add_run(f"• {term} : ")
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = COLOR_TEAL
        r_d = p_item.add_run(defn)
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = COLOR_CHARCOAL

    # TABLEAU COMPARATIF SYNTHÉTIQUE
    p_tb_title = doc.add_paragraph()
    p_tb_title.paragraph_format.space_before = Pt(14)
    p_tb_title.paragraph_format.space_after = Pt(6)
    p_tb_title.add_run("Matrice Comparée des Trois Propositions Méthodologiques").font.bold = True
    p_tb_title.runs[0].font.size = Pt(12)
    p_tb_title.runs[0].font.color.rgb = COLOR_NAVY

    cmp_table = doc.add_table(rows=6, cols=4)
    cmp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Critère", "Proposition 1 : Comparatif", "Proposition 2 : EMME", "Proposition 3 : Dyadique"]
    for c_idx, h_text in enumerate(headers):
        cell = cmp_table.rows[0].cells[c_idx]
        style_cell(cell, bg_color=HEX_NAVY, top_pad=80, bot_pad=80, left_pad=80, right_pad=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    rows_data = [
        ("Objectif vulgarisé", "Comprendre ce qui sépare l'œil d'un débutant de celui d'un expert.", "Tester si apprendre avec des vidéos 'Spotlight' rend plus efficace.", "Comprendre ce qui se passe dans les yeux des deux interlocuteurs."),
        ("Design expérimental", "Quasi-expérimental transversal (Novices vs Intermédiaires vs Experts).", "Essai contrôlé randomisé (RCT) pré-test / post-test.", "Mixte séquentiel (Dual Eye Tracking + Autoconfrontation)."),
        ("Équipement requis", "1 paire de lunettes Neon (réceptionniste).", "1 paire de lunettes Neon (étudiant pré/post-tests).", "2 paires de lunettes Neon synchronisées en Wi-Fi NTP (< 5 ms)."),
        ("Références mobilisées", "Beckmann (2010), Gegenfurtner (2011), Wolff (2016), Goodwin (1994), Cortina (2015), Vickers (2016).", "Jarodzka (2012), Seppänen (2012), Van Gog (2009), Elling (2012), Hooge (2024).", "Rogers (2018), Wohltjen (2021), Theureau (2016), Tickle-Degnen (1990), Crandall (2006)."),
        ("Livrable concret HECh", "Grille d'évaluation des compétences visuelles pour les examens.", "4 modules d'auto-formation vidéo 'Spotlight' sur Moodle.", "Guide méthodologique de débriefing réflexif pour formateurs.")
    ]
    for r_idx, r_data in enumerate(rows_data):
        row = cmp_table.rows[r_idx + 1]
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            style_cell(cell, bg_color=bg, top_pad=60, bot_pad=60, left_pad=80, right_pad=80)
            p = cell.paragraphs[0]
            if c_idx == 0:
                p.add_run(val).font.bold = True
                p.runs[0].font.size = Pt(8.5)
            else:
                p.add_run(val).font.size = Pt(8.5)

    doc.add_page_break()

    # ----------------------------------------------------
    # SECTION 2 : PROPOSITION 1 DÉTAILLÉE
    # ----------------------------------------------------
    h_p1 = doc.add_paragraph()
    h_p1.paragraph_format.space_before = Pt(12)
    h_p1.paragraph_format.space_after = Pt(4)
    r_p1 = h_p1.add_run("2. PROPOSITION 1 : Approche Comparativo-Développementale (Novices vs Experts)")
    r_p1.font.name = "Calibri"
    r_p1.font.size = Pt(15)
    r_p1.font.bold = True
    r_p1.font.color.rgb = COLOR_NAVY

    doc.add_paragraph("Intitulé académique : « La Vision Professionnelle en Action : Étude comparative transversale de l'allocation attentionnelle, de la charge cognitive et de la performance relationnelle en accueil hôtelier instrumenté »").runs[0].font.italic = True

    # 2.1 Justification
    p_j1 = doc.add_paragraph()
    p_j1.paragraph_format.space_before = Pt(8)
    p_j1.add_run("2.1. Justification théorique approfondie & Ancrage dans l'état de l'art").font.bold = True
    p_j1.runs[0].font.color.rgb = COLOR_TEAL

    p_j1_txt = doc.add_paragraph()
    p_j1_txt.paragraph_format.line_spacing = 1.15
    p_j1_txt.add_run(
        "Cette méthodologie repose sur les théories cognitives de l'expertise visuelle et du Naturalistic Decision Making (NDM) :\n"
        "1. Lois universelles du regard expert : La méta-analyse de Gegenfurtner, Lehtinen et Säljö (2011) sur 73 études établit que les experts fixent moins longtemps, "
        "éliminent l'information redondante (information reduction) et utilisent leur empan parafovéal pour atteindre plus rapidement l'information critique (modèle holistique). "
        "En réception hôtelière, l'expert ne cherche pas au hasard : il accède immédiatement au dossier d'upselling.\n"
        "2. Cadre de complexité et libération mentale : Beckmann (2010) démontre que la charge extrinsèque sature la mémoire de travail de l'opérateur non familier d'un outil. "
        "Chez l'expert, l'automatisation logicielle libère des ressources cérébrales, lui permettant de relever les yeux et de lire les signaux non verbaux du voyageur.\n"
        "3. La vision professionnelle située : Goodwin (1994) et Wolff et al. (2016) prouvent que l'expertise dote le professionnel d'une vision panoramique distribuée.\n"
        "4. Le Quiet Eye régulateur : Vickers (2016) démontre que la dernière fixation stabilisée avant une action décisive est 62% plus longue chez les experts. "
        "Nous testons si cette fixation calme sur le client ou le tarif renforce la persuasion commerciale.\n"
        "5. Validation low/high-inference : Cortina et al. (2015) attestent que les mesures d'eye tracking mobile convergent étroitement avec les notes de qualité de service attribuées par des observateurs indépendants.\n"
        "6. Référentiel d'upselling : Intégration des standards opérationnels du Ritz-Carlton Bali documentés par Ruki (2023) et de l'approche omnicanale de Denizci Guillet (2020)."
    )

    # 2.2 Scénarios détaillés
    p_sc1 = doc.add_paragraph()
    p_sc1.paragraph_format.space_before = Pt(8)
    p_sc1.add_run("2.2. Dispositif expérimental & Scénarisation pas à pas").font.bold = True
    p_sc1.runs[0].font.color.rgb = COLOR_TEAL

    p_sc1_txt = doc.add_paragraph()
    p_sc1_txt.paragraph_format.line_spacing = 1.15
    p_sc1_txt.add_run(
        "• Échantillon (N = 60) : 20 Novices (B1 n'ayant jamais fait de stage), 20 Intermédiaires (B3 ayant validé leurs stages de réception) et 20 Professionnels chevronnés d'hôtels 4*-5* (minimum 3 ans d'ancienneté).\n"
        "• Scénario 1 - Upselling Multicanal (7 min) : Le client a réservé une Chambre Standard à 140 €/nuit. Une alerte PMS indique qu'il a consulté la Suite Exécutive en ligne. "
        "Le réceptionniste doit exploiter l'information, proposer le tarif préférentiel à 60 € de supplément par nuit et argumenter sur tablette tactile.\n"
        "• Scénario 2 - Réclamation Critique (7 min) : Le client arrive pressé pour une visioconférence urgente. Le PMS indique que sa chambre est bloquée suite à une fuite d'eau. "
        "Le réceptionniste doit écouter sans interrompre, maintenir le contact oculaire et proposer un salon de travail immédiat avec surclassement offert en Junior Suite après sa réunion.\n"
        "• Déroulement minuté (45 min par sujet) : Accueil & équipement Neon (10 min) -> Prise en main (5 min) -> Scénario 1 (7 min) -> Pause (3 min) -> Scénario 2 (7 min) -> Questionnaire NASA-TLX & Beckmann (8 min) -> Clôture (5 min)."
    )

    # 2.3 Grille d'indicateurs
    p_g1 = doc.add_paragraph()
    p_g1.paragraph_format.space_before = Pt(8)
    p_g1.add_run("2.3. Grille complète des indicateurs opérationnels (Proposition 1)").font.bold = True
    p_g1.runs[0].font.color.rgb = COLOR_TEAL

    t_g1 = doc.add_table(rows=8, cols=4)
    t_g1.alignment = WD_TABLE_ALIGNMENT.CENTER
    g_headers = ["Indicateur", "Métrique & Calcul", "Outil de Mesure", "Justification État de l'Art"]
    for c_idx, h_text in enumerate(g_headers):
        cell = t_g1.rows[0].cells[c_idx]
        style_cell(cell, bg_color=HEX_NAVY, top_pad=80, bot_pad=80, left_pad=80, right_pad=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    g1_data = [
        ("Dwell Time PMS (%)", "(Temps fixation écran / Durée totale) * 100", "Pupil Labs Neon (Surface AOI)", "Beckmann (2010) : Charge extrinsèque liée au manque d'automatisation logicielle."),
        ("TTFF Champ Tarifaire", "Latence (ms) jusqu'à la 1re fixation sur le surclassement", "Logs PMS synchronisés Neon", "Gegenfurtner et al. (2011) : Accès parafovéal plus rapide chez l'expert."),
        ("Ratio Regard Client / PMS", "Temps fixation Visage Client / Temps fixation Écran PMS", "Calcul automatique de ratio", "Wolff et al. (2016) : Mesure de la vision distribuée vs cécité écran."),
        ("Quiet Eye Duration (QED)", "Durée (ms) de la dernière fixation stable avant parole", "Microphone + Neon", "Vickers (2016) : Préparation cognitive et motrice optimale."),
        ("Duchenne Smile Frequency", "Nombre de sourires authentiques (contraction orbiculaire)", "Vidéo HD de face (codage FACS)", "Hennig-Thurau et al. (2006) : Authenticité vs travail émotionnel de surface."),
        ("Score de Rapport Non Verbal", "Score composite sur 7 points (attention, positivité, coordination)", "Grille CLASS (Cortina 2015)", "Tickle-Degnen & Rosenthal (1990) & Cortina (2015) : Validation par convergence."),
        ("Taux de Succès Upselling", "Variable binaire : 1 si surclassement accepté, 0 si refusé", "Log de clôture du PMS", "Denizci Guillet (2020) & Ruki (2023) : Performance commerciale finale.")
    ]
    for r_idx, r_data in enumerate(g1_data):
        row = t_g1.rows[r_idx + 1]
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            style_cell(cell, bg_color=bg, top_pad=50, bot_pad=50, left_pad=60, right_pad=60)
            cell.paragraphs[0].add_run(val).font.size = Pt(8)

    doc.add_page_break()

    # ----------------------------------------------------
    # SECTION 3 : PROPOSITION 2 DÉTAILLÉE
    # ----------------------------------------------------
    h_p2 = doc.add_paragraph()
    h_p2.paragraph_format.space_before = Pt(12)
    h_p2.paragraph_format.space_after = Pt(4)
    r_p2 = h_p2.add_run("3. PROPOSITION 2 : Approche Didactique & Vicariante (Interventionnelle par EMME)")
    r_p2.font.name = "Calibri"
    r_p2.font.size = Pt(15)
    r_p2.font.bold = True
    r_p2.font.color.rgb = COLOR_NAVY

    doc.add_paragraph("Intitulé académique : « Ingénierie Pédagogique par Modélisation du Regard (EMME) : Évaluation de l'impact d'un guidage attentionnel 'Spotlight' sur l'apprentissage des compétences d'accueil hôtelier »").runs[0].font.italic = True

    # 3.1 Justification
    p_j2 = doc.add_paragraph()
    p_j2.paragraph_format.space_before = Pt(8)
    p_j2.add_run("3.1. Justification théorique approfondie & Ancrage dans l'état de l'art").font.bold = True
    p_j2.runs[0].font.color.rgb = COLOR_TEAL

    p_j2_txt = doc.add_paragraph()
    p_j2_txt.paragraph_format.line_spacing = 1.15
    p_j2_txt.add_run(
        "Cette méthodologie interventionnelle s'appuie directement sur les sciences de l'apprentissage multimédia et de la didactique professionnelle :\n"
        "1. Modélisation oculaire par effet Spotlight : Jarodzka et al. (2012) démontrent qu'un simple cercle rouge sur une vidéo distrait l'apprenant. "
        "En revanche, la technique du 'Spotlight' (zone regardée nette, environnement périphérique estompé à 40%) guide doucement l'attention sans détruire la vue d'ensemble, "
        "produisant des gains diagnostiques durables sans guidage ultérieur.\n"
        "2. Accélération de l'inspection méthodique : Seppänen & Gegenfurtner (2012) confirment qu'observer le regard d'un enseignant chevronné aide les novices à structurer leur balayage visuel.\n"
        "3. Prévention de la redondance attentionnelle : Van Gog, Paas, Marcus, Ayres et Sweller (2009) ont prouvé qu'associer un flux de regard à de longs discours audio sature la mémoire de travail. "
        "Les capsules doivent être très courtes (2 min 30) et focalisées sur le sens des gestes professionnels.\n"
        "4. Les silences comme révélateur didactique : Elling, Lentz et de Jong (2012) révèlent que les silences face à l'écran (27% du temps) traduisent une surcharge cognitive. "
        "L'efficacité du dispositif se mesurera par la baisse des silences de blocage face au client.\n"
        "5. Rigueur des zones d'intérêt : Hooge et al. (2024) prescrivent de dimensionner les marges des AOI en tenant compte de la résolution angulaire pour garantir la reproductibilité."
    )

    # 3.2 Plan
    p_sc2 = doc.add_paragraph()
    p_sc2.paragraph_format.space_before = Pt(8)
    p_sc2.add_run("3.2. Dispositif expérimental & Essai contrôlé randomisé (RCT sur 10 mois)").font.bold = True
    p_sc2.runs[0].font.color.rgb = COLOR_TEAL

    p_sc2_txt = doc.add_paragraph()
    p_sc2_txt.paragraph_format.line_spacing = 1.15
    p_sc2_txt.add_run(
        "• Population (N = 50 étudiants de Bloc 2 en Gestion Hôtelière HECh/HEL) répartis par tirage au sort stratifié :\n"
        "  - Bras Expérimental (N = 25) : Formation enrichie des 4 capsules vidéo interactives EMME Spotlight.\n"
        "  - Bras Contrôle (N = 25) : Formation sur les mêmes cas avec vidéos conventionnelles sans regard et fiches mémo écrites.\n"
        "• Les 4 Capsules Spotlight (2 min 30 chacune) : Module 1 (Repérage de l'opportunité d'upselling sur PMS) -> Module 2 (Présentation de la suite sur tablette) -> "
        "Module 3 (Écoute active sans fuite visuelle lors d'une réclamation) -> Module 4 (Vérification rapide des disponibilités et annonce de compensation).\n"
        "• Protocole expérimental : Pré-test T0 (simulation sous Neon) -> 3 semaines d'intervention (45 min/semaine) -> Post-test T1 (nouveau scénario équivalent sous Neon)."
    )

    # 3.3 Grille
    p_g2 = doc.add_paragraph()
    p_g2.paragraph_format.space_before = Pt(8)
    p_g2.add_run("3.3. Grille complète des indicateurs opérationnels (Proposition 2)").font.bold = True
    p_g2.runs[0].font.color.rgb = COLOR_TEAL

    t_g2 = doc.add_table(rows=7, cols=4)
    t_g2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_idx, h_text in enumerate(g_headers):
        cell = t_g2.rows[0].cells[c_idx]
        style_cell(cell, bg_color=HEX_NAVY, top_pad=80, bot_pad=80, left_pad=80, right_pad=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    g2_data = [
        ("Gain Attentionnel Client", "% Temps regard client en T1 moins % en T0", "Pupil Labs Neon (AOI Visage Client)", "Jarodzka et al. (2012) : Transfert réussi du balayage visuel vers l'humain."),
        ("Réduction Errance PMS", "Temps perdu sur le PMS en T0 moins ce temps en T1", "Surface tracking sur écran PMS", "Seppänen & Gegenfurtner (2012) : Élimination des fixations parasites."),
        ("Silences Bloquants", "Durée cumulée des pauses verbales > 2 s avec regard figé", "Spectrogramme audio + tracker", "Elling, Lentz & de Jong (2012) : Révélateur de la saturation cognitive."),
        ("Effort Mental Ressenti", "Différence de score sur l'échelle psychométrique de Paas", "Questionnaire post-simulation", "Van Gog et al. (2009) & Beckmann (2010) : Allègement de l'effort mental."),
        ("Qualité Offre Upselling", "Score sur 20 points évalué par grille critériée", "Évaluation professorale", "Ruki (2023) & Denizci Guillet (2020) : Performance commerciale concrète."),
        ("Écoute Active Réclamation", "Durée cumulée de regard sur le client pendant l'exposé du grief", "AOI Visage sous Neon", "Tickle-Degnen & Rosenthal (1990) : Maintien de l'attention mutuelle.")
    ]
    for r_idx, r_data in enumerate(g2_data):
        row = t_g2.rows[r_idx + 1]
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            style_cell(cell, bg_color=bg, top_pad=50, bot_pad=50, left_pad=60, right_pad=60)
            cell.paragraphs[0].add_run(val).font.size = Pt(8)

    doc.add_page_break()

    # ----------------------------------------------------
    # SECTION 4 : PROPOSITION 3 DÉTAILLÉE
    # ----------------------------------------------------
    h_p3 = doc.add_paragraph()
    h_p3.paragraph_format.space_before = Pt(12)
    h_p3.paragraph_format.space_after = Pt(4)
    r_p3 = h_p3.add_run("4. PROPOSITION 3 : Approche Énactive & Interactionnelle Dyadique (Dual Eye Tracking & Cours d'Action)")
    r_p3.font.name = "Calibri"
    r_p3.font.size = Pt(15)
    r_p3.font.bold = True
    r_p3.font.color.rgb = COLOR_NAVY

    doc.add_paragraph("Intitulé académique : « Énaction et Synchronie Sociale : Analyse dyadique de l'interaction d'accueil hôtelier par double oculométrie mobile synchronisée et entretiens d'autoconfrontation du cours d'action »").runs[0].font.italic = True

    # 4.1 Justification
    p_j3 = doc.add_paragraph()
    p_j3.paragraph_format.space_before = Pt(8)
    p_j3.add_run("4.1. Justification théorique approfondie & Ancrage dans l'état de l'art").font.bold = True
    p_j3.runs[0].font.color.rgb = COLOR_TEAL

    p_j3_txt = doc.add_paragraph()
    p_j3_txt.paragraph_format.line_spacing = 1.15
    p_j3_txt.add_run(
        "Cette proposition à la pointe de la recherche mondiale étudie la relation comme un système dynamique couplé en temps réel :\n"
        "1. La réalité du regard social face-à-face (Dual Eye Tracking) : Rogers, Speelman, Guidetti et Longmuir (2018) prouvent dans Scientific Reports que le regard mutuel direct "
        "ne représente qu'une infime proportion du temps total. Détourner les yeux est indispensable pour réfléchir sans surcharge cognitive. "
        "Il est donc crucial de mesurer précisément à quel moment le contact visuel se rompt et se rétablit.\n"
        "2. Le rythme respiratoire de l'attention partagée : Wohltjen et Wheatley (2021) révèlent dans les PNAS que le contact visuel marque l'apogée de l'attention conjointe, "
        "suivi d'une désynchronisation salutaire permettant à chacun de penser par lui-même. Alterner entre le client et la tablette d'upselling est la respiration naturelle du dialogue.\n"
        "3. Le rapport interpersonnel synchronisé : Tickle-Degnen et Rosenthal (1990) fondent le rapport sur l'attention mutuelle et la coordination. Deux paires de lunettes mesurent "
        "si le client et le réceptionniste convergent sur la tablette au même moment.\n"
        "4. Le cours d'action et l'autoconfrontation : Theureau (recensé par Durand, 2016) postule qu'on ne peut comprendre l'activité sans le sens vécu par l'acteur. "
        "L'entretien d'autoconfrontation immédiat permet à l'étudiant de commenter sa propre vidéo oculaire pour expliciter ses doutes et ses intentions.\n"
        "5. L'explicitation des savoirs tacites : Crandall, Klein et Hoffman (2006) fournissent les techniques de relance de la Cognitive Task Analysis (CTA) pour faire émerger les arbitrages inconscients.\n"
        "6. L'authenticité affective : Hennig-Thurau et al. (2006) démontrent que seul le sourire authentique déclenche une contagion positive chez le client mécontent.\n"
        "7. L'orientation active de la tablette : Otterbring et al. (2014) prouvent que la signalétique passive est ignorée, justifiant la manipulation active du support commercial."
    )

    # 4.2 Protocole dyadique
    p_sc3 = doc.add_paragraph()
    p_sc3.paragraph_format.space_before = Pt(8)
    p_sc3.add_run("4.2. Dispositif dyadique & Méthodologie séquentielle (12 mois)").font.bold = True
    p_sc3.runs[0].font.color.rgb = COLOR_TEAL

    p_sc3_txt = doc.add_paragraph()
    p_sc3_txt.paragraph_format.line_spacing = 1.15
    p_sc3_txt.add_run(
        "• Infrastructure technique : Deux paires de lunettes Pupil Labs Neon connectées à un routeur Wi-Fi 6 dédié avec serveur NTP local (< 5 ms de décalage inter-lunettes).\n"
        "• Échantillon : 20 binômes complets (20 étudiants B3 face à 5 profils de clients comédiens standardisés).\n"
        "• Déroulement minuté d'une session (1h15 par étudiant) :\n"
        "  1. Équipement simultané des deux participants sous lunettes Neon (10 min).\n"
        "  2. Simulation écologique au comptoir avec tablette tactile et réclamation impromptue (15 min).\n"
        "  3. Transition immédiate en salle de débriefing (5 min).\n"
        "  4. Entretien d'autoconfrontation du cours d'action conduit par le chercheur (45 min) : l'étudiant visionne sa vidéo de scène enrichie de son regard et de celui du client, "
        "et verbalise au présent ce qu'il ressentait, craignait et décidait aux moments de rupture oculaire."
    )

    # 4.3 Grille
    p_g3 = doc.add_paragraph()
    p_g3.paragraph_format.space_before = Pt(8)
    p_g3.add_run("4.3. Grille complète des indicateurs opérationnels (Proposition 3)").font.bold = True
    p_g3.runs[0].font.color.rgb = COLOR_TEAL

    t_g3 = doc.add_table(rows=7, cols=4)
    t_g3.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_idx, h_text in enumerate(g_headers):
        cell = t_g3.rows[0].cells[c_idx]
        style_cell(cell, bg_color=HEX_NAVY, top_pad=80, bot_pad=80, left_pad=80, right_pad=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    g3_data = [
        ("Regard Mutuel Direct (%)", "Intersection simultanée des 2 regards dans les yeux de l'autre", "Calcul géométrique 3D sous Pupil Cloud", "Rogers et al. (2018) : Discontinuité réelle du contact visuel social."),
        ("Joint Attention Tablette", "Durée cumulée où les 2 flux fixent la tablette ensemble (+/- 200 ms)", "Surface AOI Tablette", "Wohltjen & Wheatley (2021) & Otterbring (2014) : Co-attention d'upselling."),
        ("Gaze Latency upon Speech", "Délai (ms) de retour du regard du réceptionniste dès que le client parle", "Audio multi-canaux + oculométrie", "Tickle-Degnen & Rosenthal (1990) : Coordination interactionnelle."),
        ("Sourire Duchenne Synchronisé", "Délai entre le sourire de l'employé et l'apaisement facial du client", "Encodage FACS vidéo scène frontale", "Hennig-Thurau et al. (2006) : Contagion affective authentique."),
        ("Unités d'Action-Signe (UAS)", "Découpage sémiotique du verbatim en unités d'expérience vécue", "Verbatim autoconfrontation", "Theureau / Durand (2016) : Reconstitution du sens pour l'acteur."),
        ("Dilemmes Décisionnels Exprimés", "Nombre de conflits intérieurs verbalisés durant l'autoconfrontation", "Questions CDM (Crandall)", "Crandall, Klein & Hoffman (2006) : Explicitation des savoirs tacites.")
    ]
    for r_idx, r_data in enumerate(g3_data):
        row = t_g3.rows[r_idx + 1]
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            style_cell(cell, bg_color=bg, top_pad=50, bot_pad=50, left_pad=60, right_pad=60)
            cell.paragraphs[0].add_run(val).font.size = Pt(8)

    doc.add_page_break()

    # ----------------------------------------------------
    # SECTION 5 : RECOMMANDATION STRATÉGIQUE FINALE
    # ----------------------------------------------------
    h_rec = doc.add_paragraph()
    h_rec.paragraph_format.space_before = Pt(12)
    h_rec.paragraph_format.space_after = Pt(6)
    r_rec = h_rec.add_run("5. Recommandations Décisionnelles pour Jérôme Foguenne")
    r_rec.font.name = "Calibri"
    r_rec.font.size = Pt(15)
    r_rec.font.bold = True
    r_rec.font.color.rgb = COLOR_NAVY

    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.line_spacing = 1.15
    p_rec.add_run(
        "1. Recommandation pour l'Impact Pédagogique Immédiat (Valorisation HECh/HEL) :\n"
        "Si votre objectif prioritaire est de valoriser immédiatement l'équipement Pupil Labs Neon auprès de la direction de la Haute École et des étudiants, "
        "déployez la PROPOSITION 2 (Intervention Didactique EMME Spotlight). En 10 mois, vous réalisez un essai contrôlé randomisé irréprochable et produisez 4 modules Moodle pérennes.\n\n"
        "2. Recommandation pour la Recherche Pure (Publications Internationales & Thèse) :\n"
        "Si votre ambition est de positionner le Lab-DRA au plus haut niveau de la recherche internationale, commencez par la PROPOSITION 1 (Comparatif Novices/Experts) en Année 1. "
        "Elle vous fournira les données normatives de base pour lancer ensuite la PROPOSITION 3 (Dyadique Dual Eye Tracking) dans le cadre d'un doctorat ou d'un projet financé d'envergure."
    )

    # Sauvegarde
    os.makedirs(os.path.dirname(LOCAL_DOCX), exist_ok=True)
    doc.save(LOCAL_DOCX)
    print(f"✅ Traité Word exhaustif généré avec succès dans : {LOCAL_DOCX}")

    try:
        shutil.copy2(LOCAL_DOCX, DRIVE_DOCX)
        print(f"✅ Traité copié avec succès sur Google Drive : {DRIVE_DOCX}")
    except PermissionError:
        alt_drive = DRIVE_DOCX.replace(".docx", " (Mis a jour).docx")
        shutil.copy2(LOCAL_DOCX, alt_drive)
        print(f"⚠️ Fichier verrouillé par Word, copié sous : {alt_drive}")

if __name__ == "__main__":
    build_exhaustive_word()
