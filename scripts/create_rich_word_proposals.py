# -*- coding: utf-8 -*-
"""
Générateur du Document Word Officiel Détaillé & Vulgarisé :
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
        p_hdr.text = "Lab-DRA | SIMACCUEIL — Guide Méthodologique Opérationnel & Vulgarisé"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.style.font.name = "Calibri"
        p_hdr.style.font.size = Pt(8.5)
        p_hdr.style.font.color.rgb = COLOR_MUTED
        
        # Footer
        ftr = s.footer
        p_ftr = ftr.paragraphs[0]
        p_ftr.text = "HECh / HEL — Jérôme Foguenne (Chercheur Principal)  |  Guide Méthodologique Approfondi"
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

def build_rich_word():
    doc = Document()
    add_header_footer(doc)
    
    # Page de titre
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
    r_title = p_title.add_run("GUIDE MÉTHODOLOGIQUE OPÉRATIONNEL & VULGARISÉ")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run("Trois Propositions Méthodologiques Détaillées pour le Projet SIMACCUEIL\nOculométrie Mobile (Pupil Labs Neon), Didactique Professionnelle & Accueil Hôtelier (Upselling & Réclamations)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12.5)
    r_sub.font.color.rgb = COLOR_CHARCOAL

    # Table cartouche métadonnées
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Chercheur Principal", "Jérôme Foguenne (HECh / HEL)"),
        ("Ancrage Théorique", "État de l'art consolidé (22 références académiques majeures)"),
        ("Matériel d'Expérimentation", "Lunettes d'Eye Tracking Mobile Pupil Labs Neon (200 Hz), Écran PMS & Tablette"),
        ("Destinataires & Finalités", "Conseil de Recherche Lab-DRA, corps professoral HECh/HEL & partenaires hôteliers")
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

    # GLOSSAIRE VULGARISÉ
    h_gl = doc.add_paragraph()
    h_gl.paragraph_format.space_before = Pt(12)
    h_gl.paragraph_format.space_after = Pt(6)
    r_gl = h_gl.add_run("1. Avant-propos : Glossaire & Principes Clés Vulgarisés")
    r_gl.font.name = "Calibri"
    r_gl.font.size = Pt(16)
    r_gl.font.bold = True
    r_gl.font.color.rgb = COLOR_NAVY

    glossary_items = [
        ("Oculométrie mobile (Eye Tracking mobile)", "Technique de mesure du regard au moyen de lunettes légères (Pupil Labs Neon). Elle permet aux participants de bouger librement et d'interagir face-à-face avec une personne réelle tout en consultant un écran."),
        ("Fixation & Saccade", "Une fixation est un arrêt du regard (au moins 100 ms) où le cerveau traite l'information. Une saccade est le saut rapide (20-40 ms) d'un point à un autre, pendant lequel la vision est neutralisée."),
        ("Zones d'Intérêt (AOI - Areas of Interest)", "Régions découpées sur l'image pour quantifier l'attention (AOI statiques sur l'écran d'ordinateur fixe vs AOI dynamiques sur le visage du client en mouvement ou la tablette)."),
        ("Charge cognitive (CLT)", "Quantité d'effort mental mobilisée en mémoire de travail. La charge extrinsèque est le gaspillage d'énergie causé par un logiciel mal maîtrisé ; son automatisation libère de l'espace mental pour regarder le client."),
        ("PMS (Property Management System)", "Logiciel hôtelier utilisé à la réception pour vérifier les réservations, attribuer les chambres et enregistrer les arrivées."),
        ("Upselling", "Technique commerciale proposant au client une prestation supérieure à celle réservée (chambre surclassée, suite, options) moyennant un supplément tarifaire négocié."),
        ("EMME (Eye-Movement Modelling Examples)", "Méthode d'apprentissage par observation où l'étudiant visionne une vidéo montrant les gestes d'un expert avec la superposition dynamique de son regard.")
    ]
    for term, defn in glossary_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.left_indent = Inches(0.2)
        p_item.paragraph_format.space_after = Pt(4)
        r_t = p_item.add_run(f"• {term} : ")
        r_t.font.bold = True
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = COLOR_TEAL
        r_d = p_item.add_run(defn)
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = COLOR_CHARCOAL

    # TABLEAU COMPARATIF
    p_tb_title = doc.add_paragraph()
    p_tb_title.paragraph_format.space_before = Pt(14)
    p_tb_title.paragraph_format.space_after = Pt(6)
    p_tb_title.add_run("Tableau Comparatif des Trois Trajectoires Méthodologiques").font.bold = True
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
        ("Équipement requis", "1 paire de lunettes Neon (réceptionniste).", "1 paire de lunettes Neon (étudiant pré/post-tests).", "2 paires de lunettes Neon synchronisées en Wi-Fi NTP."),
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

    # SECTION 2 : PROPOSITION 1
    h_p1 = doc.add_paragraph()
    h_p1.paragraph_format.space_before = Pt(12)
    h_p1.paragraph_format.space_after = Pt(4)
    r_p1 = h_p1.add_run("2. PROPOSITION 1 : Approche Comparativo-Développementale (Novices vs Experts)")
    r_p1.font.name = "Calibri"
    r_p1.font.size = Pt(15)
    r_p1.font.bold = True
    r_p1.font.color.rgb = COLOR_NAVY

    doc.add_paragraph("Intitulé vulgarisé : « Observer pour comprendre : Qu'est-ce qui différencie le regard d'un réceptionniste débutant de celui d'un professionnel expérimenté face à un client ? »").runs[0].font.italic = True

    # 2.1 Justification
    p_j1 = doc.add_paragraph()
    p_j1.paragraph_format.space_before = Pt(8)
    p_j1.add_run("2.1. Justification théorique vulgarisée & Ancrage dans l'état de l'art").font.bold = True
    p_j1.runs[0].font.color.rgb = COLOR_TEAL

    p_j1_txt = doc.add_paragraph()
    p_j1_txt.paragraph_format.line_spacing = 1.15
    p_j1_txt.add_run(
        "Pourquoi comparer des étudiants débutants, des étudiants de fin de cursus et des professionnels en poste ?\n"
        "1. L'œil de l'expert va droit au but : Gegenfurtner et al. (2011) démontrent sur 73 études que les experts ne regardent pas 'plus' de choses, mais regardent mieux et plus vite. "
        "Le professionnel ignore les informations inutiles pour cibler immédiatement la case essentielle sur l'écran (hypothèse de réduction de l'information).\n"
        "2. Le logiciel monopolise l'esprit du débutant : Selon Beckmann (2010), le manque de familiarité avec un logiciel sature la mémoire de travail (charge extrinsèque). "
        "L'étudiant débutant n'a plus assez d'espace mental pour regarder le client. À l'inverse, chez l'expert, la manipulation du PMS est automatisée, libérant son regard pour la relation.\n"
        "3. La vision professionnelle : Goodwin (1994) et Wolff et al. (2016) prouvent que l'expertise confère une vision panoramique distribuée, détectant les indices critiques que le novice ignore.\n"
        "4. Le Quiet Eye : Vickers (2016) montre que les experts stabilisent leur regard (au moins 100 ms) juste avant une action décisive. Nous testons si cette pause oculaire stabilise la persuasion en upselling.\n"
        "5. Validation de la qualité relationnelle : Cortina et al. (2015) ont établi que les mesures d'eye tracking mobile convergent fidèlement avec les grilles d'évaluation de la qualité de service."
    )

    # 2.2 Plan
    p_pl1 = doc.add_paragraph()
    p_pl1.add_run("2.2. Plan opérationnel du projet (Phasage sur 12 mois)").font.bold = True
    p_pl1.runs[0].font.color.rgb = COLOR_TEAL

    p1_phases = [
        ("Mois 1-2 (Cadrage & Test Pilote)", "Scénarisation de 2 cas (Upselling multicanal selon Denizci Guillet, 2020 et Réclamation selon Ruki, 2023). Standardisation des comédiens jouant les clients. Calibrage des AOI écran et tablette selon Hooge et al. (2024)."),
        ("Mois 3-5 (Recueil sur 60 participants)", "Passation de 60 sujets équipés des lunettes Neon (20 Novices B1, 20 Intermédiaires B3, 20 Professionnels 4*-5*). Session de 35 minutes par sujet : accueil, 2 simulations enregistrées (yeux 200 Hz, vidéo HD, audio, logs) et questionnaire d'effort mental."),
        ("Mois 6-8 (Traitement & Vision par ordinateur)", "Détection semi-automatique des AOI écran, tablette et visage client par le pipeline IA de De Beugher et al. (2014). Double codage en aveugle de la qualité relationnelle par des enseignants (grille CLASS)."),
        ("Mois 9-12 (Analyses statistiques & Livrables)", "Analyses ANOVA à mesures répétées, formalisation du 'Guide des Bonnes Pratiques Visuelles en Réception' pour l'HECh et soumission d'article scientifique.")
    ]
    for ph_t, ph_d in p1_phases:
        p_ph = doc.add_paragraph()
        p_ph.paragraph_format.left_indent = Inches(0.2)
        p_ph.paragraph_format.space_after = Pt(2)
        r_pht = p_ph.add_run(f"• {ph_t} : ")
        r_pht.font.bold = True
        p_ph.add_run(ph_d)

    # 2.3 Grille
    p_g1 = doc.add_paragraph()
    p_g1.paragraph_format.space_before = Pt(8)
    p_g1.add_run("2.3. Grille complète des indicateurs opérationnels (Proposition 1)").font.bold = True
    p_g1.runs[0].font.color.rgb = COLOR_TEAL

    t_g1 = doc.add_table(rows=7, cols=4)
    t_g1.alignment = WD_TABLE_ALIGNMENT.CENTER
    g_headers = ["Indicateur vulgarisé", "Mode de calcul", "Signification pour la recherche", "Ancrage État de l'Art"]
    for c_idx, h_text in enumerate(g_headers):
        cell = t_g1.rows[0].cells[c_idx]
        style_cell(cell, bg_color=HEX_NAVY, top_pad=80, bot_pad=80, left_pad=80, right_pad=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    g1_data = [
        ("Temps passé sur l'écran (%)", "(Temps fixation écran / Durée totale) * 100.", "Mesure si l'opérateur est prisonnier de son outil informatique.", "Beckmann (2010) (Charge extrinsèque)"),
        ("Temps pour trouver l'info clé (ms)", "Chronomètre jusqu'à la 1re fixation sur le statut de chambre.", "Prouve si l'opérateur sait où regarder sans hésiter.", "Gegenfurtner et al. (2011) (Modèle holistique)"),
        ("Ratio Visage / Écran", "Temps regard client / Temps regard écran.", "Ratio < 0.5 = communication rompue ; > 1.2 = relation prépondérante.", "Wolff et al. (2016) (Vision distribuée)"),
        ("Regard fixe avant parole (Quiet Eye)", "Durée (ms) de la fixation stable juste avant d'annoncer l'offre.", "Indique le temps de préparation mentale et de contrôle émotionnel.", "Vickers (2016) (Quiet Eye)"),
        ("Fréquence des sourires sincères", "Nombre de sourires authentiques (Duchenne) relevés sur la vidéo.", "Différencie la chaleur naturelle du simple masque commercial forcé.", "Hennig-Thurau et al. (2006) (Travail émotionnel)"),
        ("Taux de succès de l'upselling", "Résultat binaire (Surclassement accepté : Oui / Non) et montant.", "Mesure la performance commerciale concrète de l'interaction.", "Denizci Guillet (2020) & Ruki (2023)")
    ]
    for r_idx, r_data in enumerate(g1_data):
        row = t_g1.rows[r_idx + 1]
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            style_cell(cell, bg_color=bg, top_pad=50, bot_pad=50, left_pad=60, right_pad=60)
            cell.paragraphs[0].add_run(val).font.size = Pt(8)

    doc.add_page_break()

    # SECTION 3 : PROPOSITION 2
    h_p2 = doc.add_paragraph()
    h_p2.paragraph_format.space_before = Pt(12)
    h_p2.paragraph_format.space_after = Pt(4)
    r_p2 = h_p2.add_run("3. PROPOSITION 2 : Approche Didactique & Vicariante (Interventionnelle par EMME)")
    r_p2.font.name = "Calibri"
    r_p2.font.size = Pt(15)
    r_p2.font.bold = True
    r_p2.font.color.rgb = COLOR_NAVY

    doc.add_paragraph("Intitulé vulgarisé : « Apprendre à travers les yeux d'un expert : Des capsules vidéo montrant le regard d'un professionnel permettent-elles aux étudiants de mieux réussir l'accueil ? »").runs[0].font.italic = True

    # 3.1 Justification
    p_j2 = doc.add_paragraph()
    p_j2.paragraph_format.space_before = Pt(8)
    p_j2.add_run("3.1. Justification théorique vulgarisée & Ancrage dans l'état de l'art").font.bold = True
    p_j2.runs[0].font.color.rgb = COLOR_TEAL

    p_j2_txt = doc.add_paragraph()
    p_j2_txt.paragraph_format.line_spacing = 1.15
    p_j2_txt.add_run(
        "Pourquoi utiliser des vidéos enrichies du regard de l'expert pour former les étudiants ?\n"
        "1. Rendre visible l'invisible sans distraire : Jarodzka et al. (2012) démontrent qu'un simple cercle rouge sur une vidéo distrait l'apprenant. "
        "En revanche, la technique du 'Spotlight' (zone regardée nette, environnement périphérique estompé à 40%) guide doucement l'attention sans détruire la vue d'ensemble.\n"
        "2. Accélérer l'apprentissage visuel : Seppänen & Gegenfurtner (2012) confirment qu'observer le parcours oculaire d'un enseignant chevronné aide les étudiants à adopter un balayage méthodique.\n"
        "3. Éviter le piège de la redondance : Van Gog et al. (2009) ont prouvé que cumuler une trace visuelle avec de longs discours audio sature la mémoire de travail. "
        "Les capsules doivent donc être très courtes (2 min 30) et ciblées sur des gestes professionnels précis.\n"
        "4. Les silences comme révélateur didactique : Elling et al. (2012) révèlent que les silences face à l'écran (27% du temps) traduisent souvent une surcharge cognitive. "
        "L'efficacité de la formation se mesurera par la réduction des silences de blocage face au client."
    )

    # 3.2 Plan
    p_pl2 = doc.add_paragraph()
    p_pl2.add_run("3.2. Plan opérationnel du projet (Phasage sur 10 mois)").font.bold = True
    p_pl2.runs[0].font.color.rgb = COLOR_TEAL

    p2_phases = [
        ("Mois 1-3 (Production des capsules)", "Tournage de 4 cas modèles sous lunettes Neon avec un chef de réception confirmé. Développement informatique du filtre vidéo Spotlight (Python/FFmpeg). Scénarisation de capsules de 2 min 30 avec voix off sobre."),
        ("Mois 4-6 (Essai comparatif randomisé RCT)", "50 étudiants de Bachelier en Gestion Hôtelière répartis par tirage au sort (25 en Groupe Expérimental Spotlight vs 25 en Groupe Contrôle classique). Protocole : Pré-test T0 (simulation sous Neon) -> 3 semaines d'apprentissage -> Post-test T1 (nouvelle simulation sous Neon)."),
        ("Mois 7-8 (Traitement des gains & silences)", "Calcul des deltas de progression Delta(T1 - T0). Analyse chronométrique des silences de blocage (> 2 s) selon Elling et al. (2012) et mesure de l'effort mental sur l'échelle de Paas."),
        ("Mois 9-10 (Déploiement curriculaire HECh)", "Mise à disposition pérenne des capsules sur Moodle HECh/HEL et journée de dissémination pédagogique pour les formateurs.")
    ]
    for ph_t, ph_d in p2_phases:
        p_ph = doc.add_paragraph()
        p_ph.paragraph_format.left_indent = Inches(0.2)
        p_ph.paragraph_format.space_after = Pt(2)
        r_pht = p_ph.add_run(f"• {ph_t} : ")
        r_pht.font.bold = True
        p_ph.add_run(ph_d)

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
        ("Gain d'attention client (Delta RC)", "% Temps regard client en T1 moins % en T0.", "Valide que l'étudiant ose lever les yeux de son écran vers le client.", "Jarodzka et al. (2012) (Guidage Spotlight)"),
        ("Gain de fluidité logicielle (Delta EP)", "Temps perdu à chercher sur le PMS en T0 moins ce temps en T1.", "Démontre que la modélisation a transmis la trajectoire visuelle experte.", "Seppänen & Gegenfurtner (2012) (Modélisation)"),
        ("Baisse des silences bloquants", "Durée cumulée des silences > 2 s avec regard figé sur l'ordinateur.", "Prouve que l'étudiant ne subit plus de surcharge mentale bloquante.", "Elling et al. (2012) (Traitement des silences)"),
        ("Score d'allègement mental", "Différence de note sur l'échelle de Paas (1 à 9 points).", "Confirme que le dispositif a rendu l'activité plus fluide et moins stressante.", "Van Gog et al. (2009) & Beckmann (2010)"),
        ("Score de persuasion en upselling", "Grille sur 20 points évaluant la mise en valeur des bénéfices chambre.", "Mesure la conversion concrète de l'aisance visuelle en succès commercial.", "Ruki (2023) & Otterbring et al. (2014)"),
        ("Score d'écoute (Réclamation)", "Note sur 20 portant sur l'attitude calme et l'absence de coupure de parole.", "Démontre la capacité à gérer l'incident sans se cacher derrière l'écran.", "Tickle-Degnen & Rosenthal (1990)")
    ]
    for r_idx, r_data in enumerate(g2_data):
        row = t_g2.rows[r_idx + 1]
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            style_cell(cell, bg_color=bg, top_pad=50, bot_pad=50, left_pad=60, right_pad=60)
            cell.paragraphs[0].add_run(val).font.size = Pt(8)

    doc.add_page_break()

    # SECTION 4 : PROPOSITION 3
    h_p3 = doc.add_paragraph()
    h_p3.paragraph_format.space_before = Pt(12)
    h_p3.paragraph_format.space_after = Pt(4)
    r_p3 = h_p3.add_run("4. PROPOSITION 3 : Approche Énactive & Interactionnelle Dyadique (Dual Eye Tracking & Cours d'Action)")
    r_p3.font.name = "Calibri"
    r_p3.font.size = Pt(15)
    r_p3.font.bold = True
    r_p3.font.color.rgb = COLOR_NAVY

    doc.add_paragraph("Intitulé vulgarisé : « Se regarder, se comprendre, s'écouter : Que se passe-t-il vraiment dans les yeux et dans la tête du réceptionniste et du client pendant qu'ils se parlent ? »").runs[0].font.italic = True

    # 4.1 Justification
    p_j3 = doc.add_paragraph()
    p_j3.paragraph_format.space_before = Pt(8)
    p_j3.add_run("4.1. Justification théorique vulgarisée & Ancrage dans l'état de l'art").font.bold = True
    p_j3.runs[0].font.color.rgb = COLOR_TEAL

    p_j3_txt = doc.add_paragraph()
    p_j3_txt.paragraph_format.line_spacing = 1.15
    p_j3_txt.add_run(
        "Pourquoi équiper le client ET le réceptionniste de lunettes en même temps, puis faire un débriefing d'autoconfrontation ?\n"
        "1. La communication est une danse à deux : Rogers et al. (2018) prouvent en dual eye tracking que les interlocuteurs ne se regardent pas dans les yeux en continu. "
        "L'aversion visuelle est normale pour réfléchir ; l'enjeu est de savoir quand rétablir le contact.\n"
        "2. Le rythme de l'attention partagée : Wohltjen & Wheatley (2021) révèlent dans PNAS que le contact oculaire marque le sommet de la connexion, suivi immédiatement d'une rupture "
        "salutaire pour permettre à chacun de penser. Alterner entre le client et la tablette d'upselling est la respiration naturelle de l'échange.\n"
        "3. Le rapport interpersonnel synchronisé : Tickle-Degnen & Rosenthal (1990) fondent le rapport sur l'attention mutuelle et la coordination. Deux paires de lunettes mesurent "
        "si le client et le réceptionniste regardent la tablette au même moment.\n"
        "4. Comprendre le vécu intérieur (Cours d'action) : Theureau / Durand (2016) développent l'autoconfrontation : revoir sa vidéo oculaire permet à l'étudiant d'expliciter ce qu'il ressentait.\n"
        "5. Faire émerger les intuitions cachées : La méthode CDM de Crandall, Klein & Hoffman (2006) fait verbaliser les dilemmes inconscients face aux tensions du client."
    )

    # 4.2 Plan
    p_pl3 = doc.add_paragraph()
    p_pl3.add_run("4.2. Plan opérationnel du projet (Phasage sur 12 mois)").font.bold = True
    p_pl3.runs[0].font.color.rgb = COLOR_TEAL

    p3_phases = [
        ("Mois 1-2 (R&D Technique Dyadique)", "Synchronisation réseau local Wi-Fi NTP de 2 paires de lunettes Neon (< 5 ms). Aménagement scénographique du comptoir d'accueil avec tablette orientable (Otterbring et al., 2014)."),
        ("Mois 3-5 (Collecte & Autoconfrontation)", "20 binômes complets (20 étudiants B3 face à 5 profils de clients comédiens). Session de 1h15 : 15 min d'interaction sous double Neon immédiatement suivie de 45 min d'entretien d'autoconfrontation avec l'étudiant (Theureau, 2016)."),
        ("Mois 6-8 (Modélisation mixte)", "Calcul de la synchronie des regards par récurrence croisée (CRQA). Découpage des paroles d'autoconfrontation en unités d'action-signe (UAS)."),
        ("Mois 9-12 (Synthèse & Monographie)", "Croisement des moments de rupture oculaire avec les peurs verbalisées par les étudiants. Rédaction de la monographie Lab-DRA sur l'intelligence relationnelle.")
    ]
    for ph_t, ph_d in p3_phases:
        p_ph = doc.add_paragraph()
        p_ph.paragraph_format.left_indent = Inches(0.2)
        p_ph.paragraph_format.space_after = Pt(2)
        r_pht = p_ph.add_run(f"• {ph_t} : ")
        r_pht.font.bold = True
        p_ph.add_run(ph_d)

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
        ("Regard les yeux dans les yeux (%)", "Intersection des deux regards dans la zone des yeux de l'autre.", "Révèle la fréquence réelle et la brièveté du contact visuel social.", "Rogers et al. (2018) (Dual Eye Tracking)"),
        ("Regard commun sur la tablette", "Durée où les 2 paires de lunettes fixent ensemble la tablette (+/- 200 ms).", "Marqueur d'attention conjointe : regarder l'offre commerciale ensemble.", "Wohltjen & Wheatley (2021) & Otterbring (2014)"),
        ("Délai de réaction à la parole", "Temps (ms) mis par le réceptionniste à regarder le client dès qu'il parle.", "Mesure la vivacité de l'écoute active perçue par le client.", "Tickle-Degnen & Rosenthal (1990) (Coordination)"),
        ("Délai de contagion du sourire", "Temps entre le sourire du réceptionniste et l'apaisement facial du client.", "Teste l'efficacité de la contagion émotionnelle face à une plainte.", "Hennig-Thurau et al. (2006) (Contagion émotionnelle)"),
        ("Unités d'Action-Signe (UAS)", "Découpage du verbatim en autoconfrontation (intentions, peurs, actions).", "Permet de comprendre le sens que l'étudiant donnait à son comportement.", "Theureau / Durand (2016) (Cours d'action)"),
        ("Dilemmes décisionnels exprimés", "Nombre de conflits intérieurs verbalisés (ex. : peur d'insister pour l'upselling).", "Met au jour les freins psychologiques bloquant la vente.", "Crandall, Klein & Hoffman (2006) (Méthode CDM)")
    ]
    for r_idx, r_data in enumerate(g3_data):
        row = t_g3.rows[r_idx + 1]
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            style_cell(cell, bg_color=bg, top_pad=50, bot_pad=50, left_pad=60, right_pad=60)
            cell.paragraphs[0].add_run(val).font.size = Pt(8)

    doc.add_page_break()

    # SECTION 5 : RECOMMANDATION STRATÉGIQUE
    h_rec = doc.add_paragraph()
    h_rec.paragraph_format.space_before = Pt(12)
    h_rec.paragraph_format.space_after = Pt(6)
    r_rec = h_rec.add_run("5. Recommandations Stratégiques pour Jérôme Foguenne")
    r_rec.font.name = "Calibri"
    r_rec.font.size = Pt(15)
    r_rec.font.bold = True
    r_rec.font.color.rgb = COLOR_NAVY

    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.line_spacing = 1.15
    p_rec.add_run(
        "1. Option Recommandée pour l'HECh (Impact Formation Immédiat) :\n"
        "Si votre priorité est de valoriser immédiatement l'achat de vos lunettes Pupil Labs Neon auprès de votre direction et de vos étudiants en créant un outil de cours innovant, "
        "choisissez la PROPOSITION 2 (Intervention Didactique EMME Spotlight). En 10 mois, vous disposez d'un dispositif pédagogique novateur, testé scientifiquement et utilisable chaque année avec vos étudiants sur Moodle.\n\n"
        "2. Option Recommandée pour la Recherche Pure (Publications Internationales) :\n"
        "Si votre objectif prioritaire est de positionner le Lab-DRA au plus haut niveau scientifique pour attirer des financements de recherche externe, commencez par la PROPOSITION 1 (Comparatif Experts/Novices) en Année 1. "
        "Elle posera les bases objectives indispensables pour aborder ensuite la PROPOSITION 3 (Dyadique) dans le cadre d'un doctorat ou d'un projet de recherche pluriannuel d'envergure."
    )

    # Sauvegarde
    os.makedirs(os.path.dirname(LOCAL_DOCX), exist_ok=True)
    doc.save(LOCAL_DOCX)
    print(f"✅ Document Word enrichi généré avec succès dans : {LOCAL_DOCX}")

    try:
        shutil.copy2(LOCAL_DOCX, DRIVE_DOCX)
        print(f"✅ Document copié avec succès sur Google Drive : {DRIVE_DOCX}")
    except PermissionError:
        alt_drive = DRIVE_DOCX.replace(".docx", " (Mis a jour).docx")
        shutil.copy2(LOCAL_DOCX, alt_drive)
        print(f"⚠️ Fichier verrouillé par Word, copié sous : {alt_drive}")

if __name__ == "__main__":
    build_rich_word()
