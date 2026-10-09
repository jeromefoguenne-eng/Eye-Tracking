import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls
from docx.opc.constants import RELATIONSHIP_TYPE
import html

# Palette graphique académique et professionnelle (Lab-DRA / HECh)
COLOR_PRIMARY_HEX = "1A365D"      # Bleu marine profond
COLOR_SECONDARY_HEX = "2B6CB0"    # Bleu acier
COLOR_ACCENT_HEX = "0056B3"       # Bleu hyperlien / accent
COLOR_MUTED_HEX = "4A5568"        # Gris texte secondaire
COLOR_BG_LIGHT_HEX = "F7FAFC"     # Fond clair cartes/tableaux
COLOR_BORDER_HEX = "CBD5E0"       # Bordure gris neutre

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

def create_callout_box(doc, text_paragraphs, title="CADRAGE SCIENTIFIQUE DU CORPUS"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
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

# LE CORPUS STRICT DES 17 RESSOURCES DISPONIBLES DANS LE DOSSIER RESSOURCES
RESOURCES = [
    # PILIER 1 : Fondements Cognitifs, Expertise, Vision Professionnelle & Savoirs Tacites
    {
        "cat": "Pilier 1 : Fondements Cognitifs, Expertise, Vision Professionnelle & Savoirs Tacites",
        "num": "01",
        "authors": "Beckmann, J. F. (2010)",
        "title": "Taming a beast of burden – On some issues with the conceptualisation and operationalisation of cognitive load",
        "journal": "Learning and Instruction, 20(3), 250–264",
        "doi_text": "DOI: 10.1016/j.learninstruc.2009.02.024",
        "doi_url": "https://doi.org/10.1016/j.learninstruc.2009.02.024",
        "summary": "Cet article fondamental réexamine les postulats de la Cognitive Load Theory (CLT) et la distinction tripartite entre charge cognitive intrinsèque, extrinsèque et essentielle. L'auteur propose un cadre fondé sur la complexité pour dépasser la simple notion d'interactivité des éléments et dériver des estimations a priori de la charge mentale. L'étude empirique montre que la capacité individuelle de traitement détermine la mesure dans laquelle la complexité d'une tâche se traduit en surcharge cognitive. Dans le cadre de notre projet, cette recherche éclaire comment le multitâche au comptoir d'accueil (gérer le client tout en consultant le logiciel hôtelier) sature les ressources attentionnelles des novices, tandis que l'expertise permet de comprimer cette charge."
    },
    {
        "cat": "Pilier 1 : Fondements Cognitifs, Expertise, Vision Professionnelle & Savoirs Tacites",
        "num": "02",
        "authors": "Gegenfurtner, A., Lehtinen, E., & Säljö, R. (2011)",
        "title": "Expertise differences in the comprehension of visualizations: A meta-analysis of eye-tracking research in professional domains",
        "journal": "Educational Psychology Review, 23(4), 523–552",
        "doi_text": "DOI: 10.1007/s10648-011-9174-7",
        "doi_url": "https://doi.org/10.1007/s10648-011-9174-7",
        "summary": "Cette méta-analyse majeure synthétise des dizaines d'études comparant experts et novices à travers l'oculométrie dans divers contextes professionnels. Les résultats confirment trois lois universelles de l'expertise visuelle : les experts effectuent des fixations significativement plus courtes sur les zones redondantes, identifient les informations critiques beaucoup plus rapidement (temps de première fixation réduit), et présentent une plus grande flexibilité attentionnelle face aux imprévus. L'article démontre que les compétences incorporées d'un métier reposent sur des schémas perceptifs automatisés que l'eye tracking permet d'objectiver mathématiquement."
    },
    {
        "cat": "Pilier 1 : Fondements Cognitifs, Expertise, Vision Professionnelle & Savoirs Tacites",
        "num": "04",
        "authors": "Goodwin, C. (1994)",
        "title": "Professional Vision",
        "journal": "American Anthropologist, 96(3), 606–633",
        "doi_text": "DOI: 10.1525/aa.1994.96.3.02a00100",
        "doi_url": "https://doi.org/10.1525/aa.1994.96.3.02a00100",
        "summary": "Théorie séminale de la « vision professionnelle », cet article d'anthropologie cognitive démontre comment les membres d'une communauté de pratique apprennent à percevoir le monde selon des schémas socialement situés. Goodwin décompose l'expertise visuelle en trois pratiques : le codage (catégorisation perceptuelle), la mise en relief (highlighting, focalisation sur les indices saillants) et l'usage de représentations matérielles. Appliqué à l'accueil hôtelier, ce cadre explique comment le professionnel expert « lit » instantanément les indices non verbaux du client et les opportunités de surclassement, là où le novice ne perçoit qu'une situation administrative d'enregistrement standard."
    },
    {
        "cat": "Pilier 1 : Fondements Cognitifs, Expertise, Vision Professionnelle & Savoirs Tacites",
        "num": "05",
        "authors": "Crandall, B., Klein, G. A., & Hoffman, R. R. (2006)",
        "title": "Working Minds: A Practitioner's Guide to Cognitive Task Analysis",
        "journal": "The MIT Press, Cambridge, MA",
        "doi_text": "DOI: 10.7551/mitpress/7304.001.0001",
        "doi_url": "https://doi.org/10.7551/mitpress/7304.001.0001",
        "summary": "Ouvrage de référence internationale sur l'Analyse Cognitive des Tâches (Cognitive Task Analysis - CTA) et le Naturalistic Decision Making (NDM). Les auteurs fournissent les protocoles rigoureux (Critical Decision Method - CDM, Knowledge Audit, Concept Mapping) permettant d'extraire les connaissances tacites d'experts confrontés à des situations critiques et dynamiques. Couplée à l'oculométrie mobile moderne, la démarche CTA permet de surmonter le paradoxe de l'expertise (plus un professionnel est compétent, plus ses schémas sont automatisés et moins il est capable de les expliquer). L'enregistrement oculaire sert de support de remémoration (cued-recall) pour documenter la détection de micro-indices, les modèles mentaux et les décisions adaptatives."
    },
    {
        "cat": "Pilier 1 : Fondements Cognitifs, Expertise, Vision Professionnelle & Savoirs Tacites",
        "num": "07",
        "authors": "Theureau, J. (2016) / Durand, M. (2016)",
        "title": "Le cours d'action. L'enaction et l'expérience / L'analyse de l'activité et l'entretien d'auto-confrontation enrichi par les traces",
        "journal": "Activités, 13(1), Recension et prolongements théoriques",
        "doi_text": "DOI: 10.4000/activites.2769",
        "doi_url": "https://doi.org/10.4000/activites.2769",
        "summary": "Issu de l'ergonomie cognitive et de l'approche du cours d'action, ce cadre théorise l'entretien d'auto-confrontation. Un professionnel est confronté aux traces extrinsèques audiovisuelles de sa propre pratique pour documenter la dynamique de son expérience vécue et faire émerger les savoirs incorporés pré-réflexifs. Couplée à l'oculométrie mobile de dernière génération, la trace du regard agit comme un déclencheur mnésique exceptionnel : l'acteur est invité à expliciter le sens de ses réorientations visuelles au cours de l'interaction de service, révélant la rationalité sous-jacente de ses arbitrages relationnels."
    },

    # PILIER 2 : Méthodologie Oculométrique, Métriques & Dispositifs Mobiles
    {
        "cat": "Pilier 2 : Méthodologie Oculométrique, Métriques & Dispositifs Mobiles",
        "num": "08",
        "authors": "Hooge, I. T. C., Nyström, M., Niehorster, D. C., Andersson, R., Foulsham, T., Nuthmann, A., & Hessels, R. S. (2026)",
        "title": "The fundamentals of eye tracking part 6: Working with areas of interest",
        "journal": "Behavior Research Methods, 58(3)",
        "doi_text": "DOI: 10.3758/s13428-025-02598-6",
        "doi_url": "https://doi.org/10.3758/s13428-025-02598-6",
        "summary": "Cet article méthodologique fondamental de la série internationale sur l'oculométrie établit les règles d'or et les standards méthodologiques pour l'utilisation des Zones d'Intérêt (Areas of Interest - AOI). Les auteurs examinent les pièges de délimitation spatiale, l'impact des imprécisions de pointage et la gestion des AOI dynamiques dans les environnements réels. Dans notre projet de simulation d'accueil, cette publication fournit la rigueur statistique indispensable pour découper et analyser les AOI clés : visage du client, écran du logiciel PMS, terminal de paiement et documents promotionnels de surclassement."
    },
    {
        "cat": "Pilier 2 : Méthodologie Oculométrique, Métriques & Dispositifs Mobiles",
        "num": "09.a",
        "authors": "Pfeffer, T., & Dierkes, K. (2024)",
        "title": "Neon Pupillometry Test Report: An evaluation of Neon's pupillometry feature",
        "journal": "Pupil Labs GmbH Technical Report",
        "doi_text": "Rapport Technique Officiel Pupil Labs",
        "doi_url": "https://pupil-labs.com/products/neon/",
        "summary": "Rapport technique d'évaluation du système d'oculométrie mobile Pupil Labs Neon. Les auteurs documentent les performances de l'architecture NeonNet (réseau de neurones profond embarqué fonctionnant sans calibration utilisateur manuelle à 200 Hz). Ils démontrent la fiabilité de la pupillométrie physique (mesure absolue du diamètre pupillaire en millimètres, corrigée des distorsions d'angle). Cet outil permet de sonder en temps réel non seulement l'orientation spatiale du regard, mais également les variations physiologiques de la charge mentale et de l'éveil émotionnel lors des phases sensibles de négociation."
    },
    {
        "cat": "Pilier 2 : Méthodologie Oculométrique, Métriques & Dispositifs Mobiles",
        "num": "09.b",
        "authors": "Nolte, D., Walter, J. L., von Bassewitz, L., et al. (2026)",
        "title": "Mobile eye tracking in the real world: Best practices",
        "journal": "Journal of Vision, 26(2):6, 1–22",
        "doi_text": "DOI: 10.1167/jov.26.2.6",
        "doi_url": "https://doi.org/10.1167/jov.26.2.6",
        "summary": "Ce guide international de référence détaille les meilleures pratiques pour conduire des recherches en oculométrie mobile dans des contextes réels non contraints (« in the wild »). Les auteurs abordent la gestion des variations de luminosité, les mouvements de tête, les glissements mécaniques de la monture et l'alignement des flux de données avec les vidéos de scène. Ce texte constitue le socle procédural garantissant la validité écologique et la reproductibilité des enregistrements réalisés au comptoir d'accueil hôtelier du Lab-DRA."
    },

    # PILIER 3 : Didactique de l'Expertise Visuelle, EMME & Protocoles Verbaux
    {
        "cat": "Pilier 3 : Didactique de l'Expertise Visuelle, EMME & Protocoles Verbaux",
        "num": "03",
        "authors": "Van Gog, T., Jarodzka, H., Scheiter, K., Gerjets, P., & Paas, F. (2009)",
        "title": "Attention guidance during example study via the model's eye movements",
        "journal": "Computers in Human Behavior, 25(3), 785–794",
        "doi_text": "DOI: 10.1016/j.chb.2009.02.002",
        "doi_url": "https://doi.org/10.1016/j.chb.2009.02.002",
        "summary": "Les auteurs introduisent la méthodologie pionnière des EMME (Eye Movement Modeling Examples). En enregistrant le parcours oculaire d'un modèle expert et en le superposant sur la vidéo visionnée par les apprenants, on guide directement leur attention sur les zones stratégiques de la tâche. Combinée au protocole de verbalisation rétrospective guidée par le regard, cette technique permet d'accélérer l'apprentissage en matérialisant visuellement les prises de décision implicites qui échappent aux explications verbales traditionnelles."
    },
    {
        "cat": "Pilier 3 : Didactique de l'Expertise Visuelle, EMME & Protocoles Verbaux",
        "num": "06",
        "authors": "Elling, S., Lentz, L., & de Jong, M. (2012)",
        "title": "Combining concurrent think-aloud protocols and eye-tracking observations: An analysis of verbalizations and silences",
        "journal": "IEEE Transactions on Professional Communication, 55(3), 206–218",
        "doi_text": "DOI: 10.1109/TPC.2012.2206190",
        "doi_url": "https://doi.org/10.1109/TPC.2012.2206190",
        "summary": "Cette étude méthodologique rigoureuse compare l'impact de la réflexion à voix haute simultanée (concurrent think-aloud) et des protocoles rétrospectifs couplés à l'eye tracking. Les auteurs démontrent que verbaliser en temps réel pendant une tâche interactive induit une surcharge cognitive et modifie artificiellement le comportement naturel de l'opérateur. En revanche, le protocole rétrospectif guidé par la trace oculaire (gaze-cued RTA) préserve l'authenticité de l'interaction et génère des verbalisations réflexives d'une grande profondeur sur les silences et les fixations clés."
    },
    {
        "cat": "Pilier 3 : Didactique de l'Expertise Visuelle, EMME & Protocoles Verbaux",
        "num": "10",
        "authors": "Jarodzka, H., Balslev, T., Holmqvist, K., Nyström, M., Scheiter, K., Gerjets, P., & Eika, B. (2012)",
        "title": "Conveying clinical reasoning based on visual observation via eye-movement modelling examples",
        "journal": "Teaching and Learning in Medicine / Instructional Science",
        "doi_text": "DOI: 10.1080/10401334.2012.692283",
        "doi_url": "https://doi.org/10.1080/10401334.2012.692283",
        "summary": "Cette recherche empirique démontre l'efficacité des exemples modélisants du regard (EMME) pour transmettre des compétences de raisonnement complexes fondées sur l'observation visuelle. En visionnant la trajectoire oculaire de l'expert synchronisée avec ses commentaires pédagogiques, les apprenants améliorent considérablement leur précision diagnostique et adoptent des stratégies de balayage visuel calquées sur celles de l'expert. Ce dispositif valide le modèle de transfert pour l'hôtellerie : visionner la trajectoire du regard d'un réceptionniste expert permet aux étudiants d'intérioriser le tempo attentionnel nécessaire à la relation client."
    },
    {
        "cat": "Pilier 3 : Didactique de l'Expertise Visuelle, EMME & Protocoles Verbaux",
        "num": "11",
        "authors": "Seppänen, M., & Gegenfurtner, A. (2012)",
        "title": "Seeing through a teacher's eyes improves students' imaging interpretation",
        "journal": "Medical Education, 46(11), 1113–1114",
        "doi_text": "DOI: 10.1111/medu.12041",
        "doi_url": "https://doi.org/10.1111/medu.12041",
        "summary": "Publiée dans Medical Education, cette étude quasi-expérimentale teste l'impact du visionnage des mouvements oculaires d'un enseignant (« seeing through a teacher's eyes »). Les résultats démontrent que les apprenants du groupe expérimental améliorent significativement leur exactitude et leur sensibilité de diagnostic par rapport au groupe témoin. Leurs trajectoires oculaires montrent une augmentation marquée des fixations sur les zones pertinentes de la tâche et une diminution des fixations sur les zones redondantes. Cela confirme la puissance pédagogique du rejeu oculaire pour restructurer la perception des apprenants."
    },

    # PILIER 4 : Dynamique Sociale du Regard, Dual Eye Tracking & Interactions de Service / Upselling
    {
        "cat": "Pilier 4 : Dynamique Sociale du Regard, Dual Eye Tracking & Interactions de Service / Upselling",
        "num": "12",
        "authors": "Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M. (2018)",
        "title": "Using dual eye tracking to uncover personal gaze patterns during social interaction",
        "journal": "Scientific Reports, 8, Article 4271",
        "doi_text": "DOI: 10.1038/s41598-018-22726-7",
        "doi_url": "https://doi.org/10.1038/s41598-018-22726-7",
        "summary": "Cet article pionnier explore le Dual Eye Tracking (enregistrement simultané et synchronisé de deux participants lors d'une interaction face-à-face). Les auteurs quantifient les schémas de regard individuel et montrent que le contact visuel mutuel direct ne représente qu'une fraction ciblée du temps de parole, servant de régulateur clé des prises de tour (turn-taking) et de la coordination dyadique. Cette méthodologie fournit la matrice analytique pour mesurer comment un réceptionniste et un client synchronisent leurs regards autour des offres commerciales."
    },
    {
        "cat": "Pilier 4 : Dynamique Sociale du Regard, Dual Eye Tracking & Interactions de Service / Upselling",
        "num": "13",
        "authors": "Wohltjen, S., & Wheatley, T. (2021)",
        "title": "Eye contact marks the rise and fall of shared attention in conversation",
        "journal": "Proceedings of the National Academy of Sciences (PNAS), 118(37), e2106499118",
        "doi_text": "DOI: 10.1073/pnas.2106499118",
        "doi_url": "https://doi.org/10.1073/pnas.2106499118",
        "summary": "Publiée dans PNAS, cette recherche démontre que le contact oculaire agit comme un interrupteur dynamique de l'attention partagée (shared attention). Le contact visuel mutuel s'intensifie jusqu'à ce que la synchronie conversationnelle atteigne son pic, après quoi les interlocuteurs détournent spontanément le regard pour traiter cognitivement les informations et réguler leur charge mentale. Ce mécanisme neurocognitif est crucial pour l'upselling : le réceptionniste expert sait exactement quand capter le regard du client pour soutenir sa proposition, puis quand le détourner vers un support matériel pour lui laisser l'espace de délibération."
    },
    {
        "cat": "Pilier 4 : Dynamique Sociale du Regard, Dual Eye Tracking & Interactions de Service / Upselling",
        "num": "14",
        "authors": "Tickle-Degnen, L., & Rosenthal, R. (1990)",
        "title": "The Nature of Rapport and Its Nonverbal Correlates",
        "journal": "Psychological Inquiry, 1(4), 285–293",
        "doi_text": "DOI: 10.1207/s15327965pli0104_1",
        "doi_url": "https://doi.org/10.1207/s15327965pli0104_1",
        "summary": "Théorie majeure du « rapport interpersonnel », cet article postule que la connexion relationnelle réussie repose sur trois composantes non verbales dynamiques : l'attention mutuelle (mutual attentiveness), la positivité (positivity) et la coordination posturale/rythmique (coordination). Le regard y est identifié comme le levier central de l'attention mutuelle. Au comptoir d'accueil, l'établissement précoce de ce rapport est la condition préalable indispensable pour qu'une proposition de surclassement soit perçue comme un conseil personnalisé plutôt que comme une intrusion commerciale."
    },
    {
        "cat": "Pilier 4 : Dynamique Sociale du Regard, Dual Eye Tracking & Interactions de Service / Upselling",
        "num": "15",
        "authors": "Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D. (2006)",
        "title": "Are All Smiles Created Equal? How Emotional Contagion and Emotional Labor Affect Service Encounters",
        "journal": "Journal of Marketing, 70(3), 58–73",
        "doi_text": "DOI: 10.1509/jmkg.70.3.058",
        "doi_url": "https://doi.org/10.1509/jmkg.70.3.058",
        "summary": "Étude fondamentale en marketing des services sur la contagion émotionnelle et le travail émotionnel. Les auteurs démontrent que les clients perçoivent avec acuité la différence entre un sourire forcé (« jeu de surface » / surface acting) et un engagement relationnel authentique (« jeu en profondeur » / deep acting). La congruence du regard et la stabilité attentionnelle sont des marqueurs cruciaux d'authenticité. Un professionnel dont le regard reste rivé à son écran informatique trahit un manque d'engagement, ce qui dégrade la confiance et réduit drastiquement les chances de succès des initiatives d'upselling."
    },
    {
        "cat": "Pilier 4 : Dynamique Sociale du Regard, Dual Eye Tracking & Interactions de Service / Upselling",
        "num": "16",
        "authors": "Setyorini, A., & Putra, I. (2023)",
        "title": "Front Desk Personnel Qualities and Skills in Applying Upselling Hotel Products: Case Study of the Ritz Carlton Bali",
        "journal": "International Journal of Multicultural and Multireligious Understanding, 10(4), 550–558",
        "doi_text": "DOI: 10.18415/ijmmu.v10i4.4646",
        "doi_url": "https://doi.org/10.18415/ijmmu.v10i4.4646",
        "summary": "Cette étude de terrain qualitative analyse les compétences requises pour réussir l'upselling hôtelier en situation réelle de check-in. Les auteurs identifient trois facteurs de réussite : la parfaite maîtrise de l'inventaire, le cadrage tarifaire axé sur la valeur de l'expérience plutôt que sur le surcoût brut, et l'intelligence de situation (communication non verbale, observation de la fatigue ou des besoins implicites du voyageur). L'étude montre que les praticiens experts abordent l'upselling comme un service d'excellence, adaptant leur posture et leur tempo visuel au rythme du client."
    },
    {
        "cat": "Pilier 4 : Dynamique Sociale du Regard, Dual Eye Tracking & Interactions de Service / Upselling",
        "num": "17",
        "authors": "Scott, N., Zhang, R., Le, D., & Gao, J. (2017/2019)",
        "title": "A review of eye-tracking research in tourism",
        "journal": "Current Issues in Tourism, 22(10), 1244–1261",
        "doi_text": "DOI: 10.1080/13683500.2017.1367367",
        "doi_url": "https://doi.org/10.1080/13683500.2017.1367367",
        "summary": "Revue systématique de référence sur l'application de l'oculométrie dans les secteurs du tourisme et de l'hôtellerie. Les auteurs recensent les recherches menées sur l'attention visuelle appliquée aux interfaces numériques, aux supports promotionnels et aux environnements de service. L'article met en exergue l'impératif méthodologique de dépasser les mesures déclaratives classiques par des données biométriques directes et souligne le potentiel des technologies oculométriques portables pour investiguer les interactions de service en direct."
    }
]

# BIBLIOGRAPHIE EXHAUSTIVE STRICTEMENT LIMITÉE AUX 17 RESSOURCES DU DOSSIER
BIBLIO_ALL = [
    ("Ressource 01 : Beckmann, J. F. (2010). Taming a beast of burden – On some issues with the conceptualisation and operationalisation of cognitive load. Learning and Instruction, 20(3), 250–264.", "https://doi.org/10.1016/j.learninstruc.2009.02.024"),
    ("Ressource 02 : Gegenfurtner, A., Lehtinen, E., & Säljö, R. (2011). Expertise differences in the comprehension of visualizations: A meta-analysis of eye-tracking research in professional domains. Educational Psychology Review, 23(4), 523–552.", "https://doi.org/10.1007/s10648-011-9174-7"),
    ("Ressource 03 : Van Gog, T., Jarodzka, H., Scheiter, K., Gerjets, P., & Paas, F. (2009). Attention guidance during example study via the model's eye movements. Computers in Human Behavior, 25(3), 785–794.", "https://doi.org/10.1016/j.chb.2009.02.002"),
    ("Ressource 04 : Goodwin, C. (1994). Professional Vision. American Anthropologist, 96(3), 606–633.", "https://doi.org/10.1525/aa.1994.96.3.02a00100"),
    ("Ressource 05 : Crandall, B., Klein, G. A., & Hoffman, R. R. (2006). Working Minds: A Practitioner's Guide to Cognitive Task Analysis. The MIT Press, Cambridge, MA.", "https://doi.org/10.7551/mitpress/7304.001.0001"),
    ("Ressource 06 : Elling, S., Lentz, L., & de Jong, M. (2012). Combining concurrent think-aloud protocols and eye-tracking observations: An analysis of verbalizations and silences. IEEE Transactions on Professional Communication, 55(3), 206–218.", "https://doi.org/10.1109/TPC.2012.2206190"),
    ("Ressource 07 : Theureau, J. (2016) / Durand, M. (2016). Le cours d'action. L'enaction et l'expérience / L'analyse de l'activité et l'entretien d'auto-confrontation enrichi par les traces. Activités, 13(1).", "https://doi.org/10.4000/activites.2769"),
    ("Ressource 08 : Hooge, I. T. C., Nyström, M., Niehorster, D. C., Andersson, R., Foulsham, T., Nuthmann, A., & Hessels, R. S. (2026). The fundamentals of eye tracking part 6: Working with areas of interest. Behavior Research Methods, 58(3).", "https://doi.org/10.3758/s13428-025-02598-6"),
    ("Ressource 09.a : Pfeffer, T., & Dierkes, K. (2024). Neon Pupillometry Test Report: An evaluation of Neon's pupillometry feature. Pupil Labs GmbH Technical Report.", "https://pupil-labs.com/products/neon/"),
    ("Ressource 09.b : Nolte, D., Walter, J. L., von Bassewitz, L., et al. (2026). Mobile eye tracking in the real world: Best practices. Journal of Vision, 26(2):6, 1–22.", "https://doi.org/10.1167/jov.26.2.6"),
    ("Ressource 10 : Jarodzka, H., Balslev, T., Holmqvist, K., Nyström, M., Scheiter, K., Gerjets, P., & Eika, B. (2012). Conveying clinical reasoning based on visual observation via eye-movement modelling examples. Teaching and Learning in Medicine.", "https://doi.org/10.1080/10401334.2012.692283"),
    ("Ressource 11 : Seppänen, M., & Gegenfurtner, A. (2012). Seeing through a teacher's eyes improves students' imaging interpretation. Medical Education, 46(11), 1113–1114.", "https://doi.org/10.1111/medu.12041"),
    ("Ressource 12 : Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M. (2018). Using dual eye tracking to uncover personal gaze patterns during social interaction. Scientific Reports, 8, Article 4271.", "https://doi.org/10.1038/s41598-018-22726-7"),
    ("Ressource 13 : Wohltjen, S., & Wheatley, T. (2021). Eye contact marks the rise and fall of shared attention in conversation. Proceedings of the National Academy of Sciences (PNAS), 118(37), e2106499118.", "https://doi.org/10.1073/pnas.2106499118"),
    ("Ressource 14 : Tickle-Degnen, L., & Rosenthal, R. (1990). The Nature of Rapport and Its Nonverbal Correlates. Psychological Inquiry, 1(4), 285–293.", "https://doi.org/10.1207/s15327965pli0104_1"),
    ("Ressource 15 : Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D. (2006). Are All Smiles Created Equal? How Emotional Contagion and Emotional Labor Affect Service Encounters. Journal of Marketing, 70(3), 58–73.", "https://doi.org/10.1509/jmkg.70.3.058"),
    ("Ressource 16 : Setyorini, A., & Putra, I. (2023). Front Desk Personnel Qualities and Skills in Applying Upselling Hotel Products: Case Study of the Ritz Carlton Bali. International Journal of Multicultural and Multireligious Understanding, 10(4), 550–558.", "https://doi.org/10.18415/ijmmu.v10i4.4646"),
    ("Ressource 17 : Scott, N., Zhang, R., Le, D., & Gao, J. (2017/2019). A review of eye-tracking research in tourism. Current Issues in Tourism, 22(10), 1244–1261.", "https://doi.org/10.1080/13683500.2017.1367367")
]

def build_docx(docx_path):
    doc = docx.Document()
    
    for sec in doc.sections:
        sec.top_margin = Inches(1)
        sec.bottom_margin = Inches(1)
        sec.left_margin = Inches(1)
        sec.right_margin = Inches(1)
        sec.different_first_page_header_footer = True
        
        header = sec.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("État de l'Art Académique : Oculométrie Mobile & Interactions de Service | Lab-DRA")
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        footer = sec.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Projet de Recherche — HECh / HEL | ")
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        add_hyperlink(fp, "https://github.com/jeromefoguenne-eng/Eye-Tracking", "Dépôt GitHub du Projet", color="0056B3")

    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Titre principal
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_t = p_title.add_run("État de l'Art Académique Approfondi : Oculométrie Mobile (Pupil Labs), Révélation des Savoirs Tacites et Dynamiques Attentionnelles en Situation Professionnelle")
    run_t.font.size = Pt(21)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    run_auth = p_sub.add_run("Auteur : Jérôme Foguenne (Projet de recherche Lab-DRA — HECh / HEL)\n")
    run_auth.font.size = Pt(11.5)
    run_auth.font.bold = True
    run_auth.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    
    run_ver = p_sub.add_run("Édition : Octobre 2026 (Version Corpus Intégral — Dossier Ressources HECh)\n")
    run_ver.font.size = Pt(10)
    run_ver.font.italic = True
    run_ver.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
    
    add_hyperlink(p_sub, "https://github.com/jeromefoguenne-eng/Eye-Tracking", "Dépôt GitHub Officiel : https://github.com/jeromefoguenne-eng/Eye-Tracking", color="0056B3", bold=True)

    create_callout_box(
        doc,
        [
            "Ce document constitue l'état de l'art scientifique et méthodologique exhaustif du projet de recherche Lab-DRA (Haute École Charlemagne / Haute École de la Ville de Liège).",
            "Conformément aux exigences méthodologiques de traçabilité, chaque concept, modèle théorique et protocole expérimental mobilisé dans cette synthèse s'appuie EXCLUSIVEMENT sur les 17 ressources documentaires scientifiques archivées dans le dossier Ressources du projet.",
            "L'objectif central est de théoriser l'usage de l'oculométrie mobile écologique (Pupil Labs Neon) pour objectiver l'attention visuelle, révéler les compétences tacites d'experts et concevoir des dispositifs d'apprentissage par l'exemple (EMME) en situation d'accueil et d'upselling hôtelier."
        ],
        title="RÈGLE DE RIGUEUR : CORPUS EXCLUSIF DU DOSSIER RESSOURCES"
    )

    # 1. INTRODUCTION & PROBLÉMATIQUE DE RECHERCHE
    h1 = doc.add_heading("1. Introduction & Problématique de Recherche", level=1)
    h1.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_paragraph(
        "Dans les métiers de service, d'accueil et d'interaction commerciale — et tout particulièrement au comptoir de réception d'un établissement hôtelier —, "
        "l'excellence professionnelle repose sur un paradoxe bien connu en psychologie ergonomique : les compétences les plus déterminantes sont aussi les plus "
        "implicites, automatisées et difficiles à verbaliser pour les praticiens eux-mêmes (Crandall, Klein & Hoffman, 2006 ; Goodwin, 1994). "
        "Face à un client, un réceptionniste expert orchestre simultanément la relation interpersonnelle (écoute active, décodage des émotions, détection d'opportunités de surclassement) "
        "et le traitement d'informations administratives sur son logiciel de gestion (Property Management System - PMS)."
    )
    doc.add_paragraph(
        "L'évaluation conventionnelle de ces compétences a historiquement pâti de limites majeures : les questionnaires auto-déclarés rétrospectifs souffrent d'amnésie "
        "ou de rationalisation a posteriori, tandis que la captation vidéo externe à la troisième personne ne permet pas de savoir ce que l'opérateur a réellement perçu "
        "et traité au niveau fovéal (Scott et al., 2017/2019 ; Elling, Lentz & de Jong, 2012). "
        "L'intégration de l'oculométrie mobile de dernière génération — incarnée par les lunettes Pupil Labs Neon (Pfeffer & Dierkes, 2024 ; Nolte et al., 2026) — "
        "ouvre la voie à une objectivation mathématique et spatio-temporelle de l'attention visuelle en situation écologique naturelle."
    )

    # 2. VOLET 1 : FONDEMENTS COGNITIFS, EXPERTISE ET SAVOIRS TACITES
    h2 = doc.add_heading("2. Volet 1 : Fondements Cognitifs, Expertise & Savoirs Tacites", level=1)
    h2.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_paragraph(
        "La compréhension des mécanismes cognitifs sous-jacents à l'activité de service s'articule autour de cinq contributions théoriques majeures du corpus :"
    )

    doc.add_heading("2.1. Charge cognitive et limites de traitement de l'information (Beckmann, 2010)", level=2)
    doc.add_paragraph(
        "Dans sa réévaluation critique de la Cognitive Load Theory (CLT), Jens F. Beckmann (2010 - Ressource 01) démontre que la charge cognitive ne peut être appréhendée "
        "comme une entité monolithique. En proposant un cadre fondé sur la complexité intrinsèque de la tâche et les capacités individuelles de traitement, Beckmann met en évidence "
        "que les exigences attentionnelles dépendent directement du niveau d'expertise du sujet. Chez un novice, la consultation d'un écran informatique sature instantanément la mémoire de travail "
        "(charge cognitive élevée), bloquant sa capacité à percevoir les signaux émis par son interlocuteur. Chez un expert, ces routines sont automatisées, libérant des ressources cognitives "
        "essentielles pour l'ajustement relationnel et la négociation."
    )

    doc.add_heading("2.2. Lois universelles du regard expert : la méta-analyse de Gegenfurtner et al. (2011)", level=2)
    doc.add_paragraph(
        "La méta-analyse de référence conduite par Andreas Gegenfurtner, Erno Lehtinen et Roger Säljö (2011 - Ressource 02) sur des dizaines d'études oculométriques professionnelles "
        "confirme empiriquement la supériorité perceptive des experts : "
        "1° Les experts fixent significativement moins longtemps et moins fréquemment les zones non pertinentes ou redondantes de la tâche. "
        "2° Ils dirigent leur regard vers les indices critiques beaucoup plus rapidement (temps de première fixation réduit). "
        "3° Leurs fixations sur les éléments pertinents sont plus longues et plus stables, traduisant un encodage sémantique approfondi. "
        "Ces constantes fournissent les métriques quantitatives clés pour évaluer la progression des étudiants du Lab-DRA."
    )

    doc.add_heading("2.3. La Vision Professionnelle comme pratique située (Goodwin, 1994)", level=2)
    doc.add_paragraph(
        "Charles Goodwin (1994 - Ressource 04) a théorisé la notion de « Vision Professionnelle » (Professional Vision) : la capacité des praticiens d'un corps de métier à structurer "
        "perceptivement les événements du monde selon des schémas partagés. Goodwin décompose cette expertise en trois opérations discursives et corporelles : "
        "le codage (catégorisation instantanée des phénomènes), la mise en relief (highlighting, focalisation attentionnelle sur les traits saillants) et la manipulation d'artefacts matériels. "
        "Au comptoir d'accueil, le réceptionniste expert mobilise une vision professionnelle qui lui permet de discriminer en un coup d'œil la fatigue d'un voyageur d'affaires "
        "ou la réceptivité d'un couple en villégiature à une offre de suite supérieure."
    )

    doc.add_heading("2.4. L'Analyse Cognitive des Tâches (CTA) et le modèle NDM (Crandall, Klein & Hoffman, 2006)", level=2)
    doc.add_paragraph(
        "Beth Crandall, Gary Klein et Robert R. Hoffman (2006 - Ressource 05) ont formalisé la méthodologie de l'Analyse Cognitive des Tâches (CTA). "
        "Leur postulat central, issu du Naturalistic Decision Making (NDM), établit que l'expertise en situation réelle ne procède pas par calcul rationnel exhaustif d'options, "
        "mais par reconnaissance de configurations typiques (Recognition-Primed Decision - RPD). La CTA fournit les protocoles (Critical Decision Method - CDM, audit des connaissances) "
        "permettant d'interroger les bifurcations décisionnelles. L'oculométrie mobile vient enrichir cette approche en fournissant un support objectif de remémoration (cued-recall) "
        "qui empêche l'expert de déformer sa pratique a posteriori."
    )

    doc.add_heading("2.5. L'auto-confrontation enrichie par les traces dans le cours d'action (Theureau / Durand, 2016)", level=2)
    doc.add_paragraph(
        "L'approche du « cours d'action » théorisée par Jacques Theureau et analysée par Marc Durand (2016 - Ressource 07) pose que l'activité humaine est une én-action "
        "inséparable de son contexte d'émergence. Pour accéder à la part pré-réflexive de l'activité, la méthodologie de l'entretien d'auto-confrontation confronte l'acteur "
        "aux traces extrinsèques audiovisuelles de sa propre pratique. L'intégration de la trace oculaire (gaze overlay) constitue un déclencheur mnésique absolu : confronté à son propre regard, "
        "le praticien peut reconstituer avec précision la dynamique de ses préoccupations, de ses attentes et de ses prises d'indices."
    )

    # 3. VOLET 2 : MÉTHODOLOGIE OCULOMÉTRIQUE MOBILE ET ANALYSE SPATIO-TEMPORELLE
    h3 = doc.add_heading("3. Volet 2 : Méthodologie Oculométrique Mobile & Analyse Spatio-Temporelle", level=1)
    h3.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_heading("3.1. Rigueur d'analyse des Zones d'Intérêt (AOI) : Hooge et al. (2026)", level=2)
    doc.add_paragraph(
        "L'analyse quantitative des données oculométriques repose sur la définition rigoureuse des Zones d'Intérêt (Areas of Interest - AOI). "
        "Ignace T. C. Hooge et son consortium international (2026 - Ressource 08) démontrent que de nombreuses recherches pèchent par des délimitations arbitraires d'AOI "
        "ou par la non-prise en compte des marges d'erreur de pointage oculaire. L'article fournit les algorithmes recommandés pour quantifier le temps total de séjour (Total Dwell Time), "
        "le nombre d'entrées et les transitions visuelles entre zones cibles. Dans nos protocoles au Lab-DRA, quatre AOI dynamiques sont modélisées : "
        "le visage du client, l'écran du logiciel PMS, le terminal de paiement/carte de chambre, et le dépliant tarifaire d'upselling."
    )

    doc.add_heading("3.2. Meilleures pratiques de l'oculométrie mobile écologique : Nolte et al. (2026)", level=2)
    doc.add_paragraph(
        "Debora Nolte et ses collègues (2026 - Ressource 09.b) dressent le guide des meilleures pratiques pour déployer l'oculométrie portable en milieu réel. "
        "Les auteurs mettent en garde contre les artefacts classiques : le glissement de la monture (slippage) lors des mouvements de tête, l'erreur de parallaxe "
        "due à la distance variable des objets regardés, et l'impact des variations lumineuses ambiantes. Le respect de ces directives assure la robustesse des données recueillies "
        "lors des simulations d'accueil hôtelier au sein du laboratoire."
    )

    doc.add_heading("3.3. Évaluation technique de Pupil Labs Neon et pupillométrie physique : Pfeffer & Dierkes (2024)", level=2)
    doc.add_paragraph(
        "Le rapport technique de Thomas Pfeffer et Kai Dierkes (2024 - Ressource 09.a) évalue l'innovation de rupture portée par les lunettes Pupil Labs Neon. "
        "Grâce au réseau neuronal convolutif profond NeonNet, le système élimine totalement la procédure contraignante de calibration utilisateur manuelle, "
        "captant le regard à 200 Hz avec une insensibilité éprouvée aux glissements physiques. Par ailleurs, Neon intègre une mesure absolue et continue du diamètre pupillaire "
        "en millimètres, corrigée géométriquement des mouvements du globe oculaire. Cette métrique pupillométrique fournit une fenêtre objective non invasive sur les micro-variations "
        "de charge mentale et de réactivité émotionnelle lors des phases critiques de proposition tarifaire."
    )

    # 4. VOLET 3 : TECHNOPÉDAGOGIE DU REGARD, MODÉLISATION (EMME) ET PROTOCOLES VERBAUX
    h4 = doc.add_heading("4. Volet 3 : Technopédagogie du Regard, Modélisation (EMME) & Protocoles Verbaux", level=1)
    h4.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_heading("4.1. Guidage attentionnel par la trace oculaire (EMME) : Van Gog et al. (2009)", level=2)
    doc.add_paragraph(
        "Tamara Van Gog, Halszka Jarodzka et leurs co-auteurs (2009 - Ressource 03) ont posé les fondations des Exemples Modélisants du Regard (Eye Movement Modeling Examples - EMME). "
        "Leur recherche démontre que visionner un exemple vidéo sur lequel est superposé en transparence le curseur mobile du regard d'un expert permet de guider "
        "spécifiquement l'attention visuelle des apprenants vers les informations critiques. Ce guidage direct évite la dispersion attentionnelle des débutants et accélère "
        "la construction de représentations mentales cohérentes de la tâche."
    )

    doc.add_heading("4.2. Transmission du raisonnement visuel professionnel : Jarodzka et al. (2012)", level=2)
    doc.add_paragraph(
        "Halszka Jarodzka et ses collaborateurs (2012 - Ressource 10) démontrent comment les EMME peuvent être mobilisés pour expliciter le raisonnement clinique "
        "fondé sur l'observation visuelle. En associant la trace oculaire de l'expert à une verbalisation didactique structurée, les étudiants apprennent non seulement "
        "« ce qu'il faut regarder », mais également « pourquoi et dans quel ordre » il faut le regarder. Ce paradigme est directement transposable aux interactions de comptoir : "
        "les étudiants découvrent comment l'expert alterne son regard entre le client et l'écran à des moments stratégiquement opportuns."
    )

    doc.add_heading("4.3. Preuve expérimentale du transfert d'expertise : Seppänen & Gegenfurtner (2012)", level=2)
    doc.add_paragraph(
        "L'étude expérimentale de Marko Seppänen et Andreas Gegenfurtner (2012 - Ressource 11 dans Medical Education), intitulée « Seeing through a teacher's eyes », "
        "fournit la validation empirique du transfert : les étudiants ayant visionné les mouvements oculaires enregistrés d'un expert améliorent de façon statistiquement "
        "significative leur exactitude diagnostique par rapport au groupe contrôle. Leurs propres données d'eye tracking montrent une restructuration complète de leur parcours visuel, "
        "avec une diminution immédiate des fixations parasites sur les zones redondantes au profit des zones à forte valeur d'information."
    )

    doc.add_heading("4.4. Supériorité de l'explicitation rétrospective guidée par le regard : Elling et al. (2012)", level=2)
    doc.add_paragraph(
        "Sanne Elling, Leo Lentz et Menno de Jong (2012 - Ressource 06) comparent méthodologiquement la réflexion à voix haute simultanée (concurrent think-aloud) "
        "et la verbalisation rétrospective couplée au tracé oculométrique. Leurs conclusions sont décisives pour l'ingénierie du Lab-DRA : demander à un opérateur "
        "de verbaliser ses pensées en même temps qu'il interagit avec un client perturbe gravement la tâche, altère la relation interpersonnelle et dénature la dynamique oculaire. "
        "À l'inverse, l'enregistrement silencieux de la situation suivi d'une auto-confrontation rétrospective guidée par le regard (Gaze-Cued RTA) préserve l'authenticité de l'échange "
        "tout en stimulant une explicitation métacognitive d'une richesse inégalée."
    )

    # 5. VOLET 4 : DYNAMIQUES SOCIALES DU REGARD, DUAL EYE TRACKING ET INTERACTIONS DE SERVICE
    h5 = doc.add_heading("5. Volet 4 : Dynamiques Sociales du Regard, Dual Eye Tracking & Interactions de Service / Upselling", level=1)
    h5.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_heading("5.1. Analyse dyadique en face-à-face via le Dual Eye Tracking : Rogers et al. (2018)", level=2)
    doc.add_paragraph(
        "L'étude pionnière de Shane L. Rogers et son équipe (2018 - Ressource 12 dans Scientific Reports) établit la méthodologie du Dual Eye Tracking dans les interactions en face-à-face. "
        "En enregistrant simultanément les deux interlocuteurs d'une dyade, les chercheurs démontrent que le contact visuel mutuel direct (mutual gaze) est un comportement régulateur "
        "très sélectif : il survient à des instants précis pour ponctuer le discours, vérifier l'attention mutuelle et coordonner les transitions de parole. "
        "Dans l'interaction d'accueil hôtelier, cette méthodologie permet de quantifier la synchronisation visuelle entre le réceptionniste et le client lors de la négociation d'une chambre."
    )

    doc.add_heading("5.2. Montée et déclin de l'attention partagée en conversation : Wohltjen & Wheatley (2021)", level=2)
    doc.add_paragraph(
        "Publiée dans PNAS, la recherche de Sophie Wohltjen et Thalia Wheatley (2021 - Ressource 13) apporte un éclairage neurocognitif fondamental : le contact oculaire mutuel "
        "marque l'apogée de l'attention partagée entre deux individus. Cependant, un contact prolongé sans rupture provoque une surcharge cognitive. Les interlocuteurs "
        "détournent alors naturellement le regard pour réguler leur traitement mental. Cette découverte éclaire l'art de l'upselling : un réceptionniste chevronné capte le regard du client "
        "pour ancrer la valeur de son offre de surclassement, puis redirige adroitement son regard vers la documentation ou l'écran pour laisser au client l'espace cognitif nécessaire à sa décision."
    )

    doc.add_heading("5.3. Établissement du rapport interpersonnel et corrélats non verbaux : Tickle-Degnen & Rosenthal (1990)", level=2)
    doc.add_paragraph(
        "Linda Tickle-Degnen et Robert Rosenthal (1990 - Ressource 14) ont modélisé la dynamique du rapport interpersonnel à travers trois dimensions non verbales : "
        "l'attention mutuelle, la positivité et la coordination. Le regard attentif en est le pivot fonctionnel. Dans le secteur des services, l'établissement précoce de ce rapport "
        "au tout début du check-in conditionne l'acceptation ultérieure d'une proposition commerciale : si le réceptionniste n'a pas manifesté d'attention mutuelle soutenue avant d'aborder "
        "l'offre tarifaire, le client percevra l'upselling comme une vente forcée agressive."
    )

    doc.add_heading("5.4. Travail émotionnel, authenticité du sourire et contagion affective : Hennig-Thurau et al. (2006)", level=2)
    doc.add_paragraph(
        "Thorsten Hennig-Thurau et ses co-auteurs (2006 - Ressources 15.a et 15.b) démontrent dans le Journal of Marketing que les clients détectent avec une extrême finesse "
        "l'authenticité du comportement d'un employé de service. Un sourire mécanique relevant du « jeu de surface » (surface acting) suscite la méfiance, tandis qu'un engagement sincère "
        "(« jeu en profondeur » / deep acting) déclenche une contagion émotionnelle positive, augmentant significativement la satisfaction et la propension à l'achat. "
        "La fixité ou la fuite du regard vers l'écran informatique constitue le marqueur non verbal numéro un trahissant le jeu de surface au comptoir d'accueil."
    )

    doc.add_heading("5.5. Compétences terrain et qualités des réceptionnistes dans l'upselling hôtelier : Setyorini & Putra (2023)", level=2)
    doc.add_paragraph(
        "L'étude de terrain menée par Anak Setyorini et I Putu Putra (2023 - Ressource 16) au sein d'un établissement hôtelier de luxe analyse les compétences pratiques "
        "qui font la réussite de l'upselling. Les auteurs identifient que le succès repose sur une triade : la maîtrise parfaite de l'inventaire des chambres, "
        "le cadrage axé sur la valeur ajoutée pour le client (mettre en avant le confort et l'expérience plutôt que le supplément financier brut), et l'intelligence de situation. "
        "Les réceptionnistes en difficulté sont paralysés par la peur du rejet commercial et s'enferment derrière leur moniteur, tandis que les professionnels performants "
        "abordent l'upselling comme une extension naturelle du service d'accueil."
    )

    doc.add_heading("5.6. État de l'art de l'oculométrie dans l'hôtellerie et le tourisme : Scott et al. (2017/2019)", level=2)
    doc.add_paragraph(
        "Dans leur revue systématique publiée dans Current Issues in Tourism, Noel Scott, Rong Huang Zhang, Dung Le et Jun Gao (2017/2019 - Ressource 17) dressent le bilan "
        "des recherches mobilisant l'eye tracking dans le tourisme. Tout en soulignant la valeur ajoutée des données oculaires pour dépasser les biais déclaratifs, les auteurs appellent "
        "à élargir le champ des études fixes de laboratoire vers les interactions de face-à-face in situ grâce aux équipements portables légers. Notre projet Lab-DRA répond directement "
        "à cet appel scientifique en appliquant Pupil Labs Neon à l'interaction de réception hôtelière."
    )

    # 6. FICHES DE LECTURE ANALYTIQUES DÉTAILLÉES (LES 17 RESSOURCES DU DOSSIER)
    h6 = doc.add_heading("6. Fiches de Lecture Analytiques : Les 17 Ressources du Dossier", level=1)
    h6.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    current_cat = None
    for res in RESOURCES:
        if res["cat"] != current_cat:
            current_cat = res["cat"]
            h_cat = doc.add_heading(f"■ {current_cat}", level=2)
            h_cat.style.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "FFFFFF")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/><w:left w:val="single" w:sz="24" w:space="0" w:color="1A365D"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/><w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/></w:tcBorders>')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        run_fn = p.add_run(f"FICHE RESSOURCE {res['num']} : {res['authors']}\n")
        run_fn.bold = True
        run_fn.font.size = Pt(11)
        run_fn.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        run_tit = p.add_run(f"Titre : {res['title']}\n")
        run_tit.bold = True
        run_tit.font.size = Pt(10)
        run_tit.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        
        p_src = cell.add_paragraph()
        p_src.paragraph_format.space_before = Pt(1)
        p_src.paragraph_format.space_after = Pt(4)
        run_src = p_src.add_run(f"Revue / Source : {res['journal']} | ")
        run_src.font.size = Pt(9.5)
        run_src.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        add_hyperlink(p_src, res['doi_url'], res['doi_text'], color="0056B3", underline=True)
        
        p_sum = cell.add_paragraph()
        p_sum.paragraph_format.space_before = Pt(2)
        p_sum.paragraph_format.space_after = Pt(2)
        r_sum_title = p_sum.add_run("Résumé Analytique & Portée pour le Projet :\n")
        r_sum_title.bold = True
        r_sum_title.font.size = Pt(9.5)
        r_sum_title.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
        r_sum_txt = p_sum.add_run(res['summary'])
        r_sum_txt.font.size = Pt(9.5)
        r_sum_txt.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 7. BIBLIOGRAPHIE EXHAUSTIVE STRICTE
    h7 = doc.add_heading("7. Bibliographie Complète (Normes APA 7 - Corpus Exclusif)", level=1)
    h7.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    p_bib_note = doc.add_paragraph()
    r_bn = p_bib_note.add_run("Note méthodologique : Cette bibliographie est strictement restreinte aux 17 documents archivés dans le dossier Ressources de la recherche.")
    r_bn.font.size = Pt(9.5)
    r_bn.font.italic = True
    r_bn.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    for cit, url in BIBLIO_ALL:
        pb = doc.add_paragraph()
        pb.paragraph_format.left_indent = Inches(0.4)
        pb.paragraph_format.first_line_indent = Inches(-0.4)
        pb.paragraph_format.space_after = Pt(5)
        
        rcit = pb.add_run(cit + " ")
        rcit.font.size = Pt(9.5)
        rcit.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        
        add_hyperlink(pb, url, "[Consulter la ressource]", color="0056B3", underline=True)

    doc.save(docx_path)
    print(f"✅ Document Word généré avec succès dans : {docx_path}")

if __name__ == "__main__":
    local_path = os.path.abspath(r"C:\Users\TrendingPC\.gemini\antigravity\scratch\Eye-Tracking\docs\Etat_de_l_art_Eye_Tracking.docx")
    build_docx(local_path)
    
    # Copie automatique vers Google Drive
    gdrive_path = r"C:\Google Drive\Prépas light\HECh\Projet recherche\Etat de l art - Eye Tracking.docx"
    try:
        shutil.copy2(local_path, gdrive_path)
        print(f"✅ Fichier synchronisé avec succès sur Google Drive : {gdrive_path}")
    except Exception as e:
        print(f"⚠️ Erreur lors de la copie vers Google Drive : {e}")
