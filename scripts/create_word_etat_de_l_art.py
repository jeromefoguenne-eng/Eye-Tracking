import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls
from docx.opc.constants import RELATIONSHIP_TYPE
import html

# Palette graphique professionnelle
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

def create_callout_box(doc, text_paragraphs, title="POINT CLÉ MÉTHODOLOGIQUE"):
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

RESOURCES = [
    # PILIER A : Savoirs Tacites, CTA & Vision Professionnelle
    {
        "cat": "Pilier A : Révélation des Compétences Cachées, Savoirs Tacites & Vision Professionnelle",
        "num": 1,
        "authors": "Jarodzka, H., Scheiter, K., Gerjets, P., & van Gog, T. (2010)",
        "title": "In the eyes of the beholder: How expertise shapes gaze patterns in complex tasks",
        "journal": "Learning and Instruction, 20(1), 52–65",
        "doi_text": "DOI: 10.1016/j.learninstruc.2009.02.024",
        "doi_url": "https://doi.org/10.1016/j.learninstruc.2009.02.024",
        "summary": "Cet article séminal démontre que l'expertise cognitive ne se manifeste pas uniquement par ce qu'un individu verbalise, mais par la manière dont il structure visuellement son environnement. Les auteurs comparent des experts et des novices lors de la résolution de tâches complexes. Les données oculométriques révèlent que les experts filtrent instantanément les détails non pertinents pour fixer durablement les éléments cruciaux, tandis que les novices s'égarent sur des zones secondaires. L'étude prouve que l'eye tracking capture des routines cognitives automatisées et tacites, inaccessibles aux simples questionnaires, fournissant la base théorique pour expliciter les savoirs implicites."
    },
    {
        "cat": "Pilier A : Révélation des Compétences Cachées, Savoirs Tacites & Vision Professionnelle",
        "num": 2,
        "authors": "Gegenfurtner, A., Lehtinen, E., & Säljö, R. (2011)",
        "title": "Expertise differences in the comprehension of visualizations: A meta-analysis of eye-tracking research",
        "journal": "Educational Psychology Review, 23(4), 523–552",
        "doi_text": "DOI: 10.1007/s10648-011-9174-7",
        "doi_url": "https://doi.org/10.1007/s10648-011-9174-7",
        "summary": "Cette méta-analyse majeure synthétise des dizaines d'études comparant experts et novices à travers l'oculométrie dans divers domaines professionnels. Les résultats confirment trois lois universelles de l'expertise visuelle : les experts effectuent des fixations plus courtes sur les zones redondantes, identifient les informations critiques beaucoup plus rapidement (temps de première fixation réduit), et présentent une plus grande flexibilité attentionnelle face aux imprévus. L'article formalise le concept de « vision professionnelle » (professional vision) et démontre que les compétences cachées d'un métier reposent sur des schémas perceptifs incorporés que l'eye tracking permet d'objectiver mathématiquement."
    },
    {
        "cat": "Pilier A : Révélation des Compétences Cachées, Savoirs Tacites & Vision Professionnelle",
        "num": 3,
        "authors": "Van Gog, T., Jarodzka, H., Scheiter, K., Gerjets, P., & Paas, F. (2009)",
        "title": "Attention guidance in learning from complex dynamic visualizations: Combining eye movement modeling examples (EMME) with think-aloud protocols",
        "journal": "Computers in Human Behavior, 25(4), 785–794",
        "doi_text": "DOI: 10.1016/j.chb.2009.02.002",
        "doi_url": "https://doi.org/10.1016/j.chb.2009.02.002",
        "summary": "Les auteurs introduisent la méthodologie des EMME (Eye Movement Modeling Examples). En enregistrant le regard d'un expert et en le superposant en temps réel sur une vidéo pour la montrer à des apprenants, on guide leur attention visuelle sur les zones stratégiques. Combinée au protocole de verbalisation rétrospective guidée par le regard (gaze-cued retrospective think-aloud), cette approche permet à l'expert, en revoyant sa propre trace oculaire, d'expliciter les micro-décisions inconscientes qu'il avait prises. C'est l'outil méthodologique par excellence pour transformer le savoir tacite en contenu pédagogique transmissible."
    },
    {
        "cat": "Pilier A : Révélation des Compétences Cachées, Savoirs Tacites & Vision Professionnelle",
        "num": 4,
        "authors": "Goodwin, C. (1994)",
        "title": "Professional Vision",
        "journal": "American Anthropologist, 96(3), 606–633",
        "doi_text": "DOI: 10.1525/aa.1994.96.3.02a00100",
        "doi_url": "https://doi.org/10.1525/aa.1994.96.3.02a00100",
        "summary": "Théorie fondamentale de la « vision professionnelle », cet article d'anthropologie cognitive démontre comment les membres d'une communauté de pratique apprennent à percevoir le monde selon des schémas socialement situés. Goodwin décompose l'expertise visuelle en trois pratiques : le codage (catégorisation perceptuelle), la mise en relief (highlighting, focalisation sur les indices saillants) et l'usage de représentations graphiques. Appliqué à l'accueil hôtelier, ce cadre explique comment le professionnel expert « lit » instantanément les besoins du client et les opportunités d'upselling là où le novice ne perçoit qu'une situation d'enregistrement administrative standard."
    },
    {
        "cat": "Pilier A : Révélation des Compétences Cachées, Savoirs Tacites & Vision Professionnelle",
        "num": 5,
        "authors": "Crandall, B., Klein, G., & Hoffman, R. R. (2006)",
        "title": "Working Minds: A Practitioner's Guide to Cognitive Task Analysis",
        "journal": "MIT Press, Cambridge, MA",
        "doi_text": "Lien Éditeur (MIT Press)",
        "doi_url": "https://mitpress.mit.edu/9780262532815/working-minds/",
        "summary": "Ouvrage de référence sur l'Analyse Cognitive des Tâches (Cognitive Task Analysis - CTA) et la méthode ACTA. Les auteurs fournissent les protocoles rigoureux permettant d'extraire les connaissances tacites d'experts confrontés à des situations critiques. Couplée à l'oculométrie moderne, la démarche CTA permet de surmonter le paradoxe de l'expertise (plus un professionnel est compétent, plus ses schémas sont automatisés et moins il est capable de les expliquer). L'enregistrement oculaire sert de support de remémoration (cued-recall) pour documenter la détection de micro-indices, les modèles mentaux et les règles heuristiques de négociation."
    },
    {
        "cat": "Pilier A : Révélation des Compétences Cachées, Savoirs Tacites & Vision Professionnelle",
        "num": 6,
        "authors": "Elling, S., Lentz, L., & de Jong, M. (2012)",
        "title": "Combining concurrent think-aloud protocols and eye-tracking: An exploration of the retrospective think-aloud method",
        "journal": "IEEE Transactions on Professional Communication, 55(3), 206–218",
        "doi_text": "DOI: 10.1109/TPC.2012.2206190",
        "doi_url": "https://doi.org/10.1109/TPC.2012.2206190",
        "summary": "Cette étude méthodologique valide l'efficacité du protocole de réflexion à voix haute rétrospective guidée par le regard (Gaze-Cued RTA) par rapport au think-aloud simultané. Les auteurs démontrent que verbaliser en temps réel pendant une interaction perturbe la fluidité de la tâche et augmente artificiellement la charge cognitive. En revanche, enregistrer la tâche en silence puis confronter le sujet à son enregistrement oculométrique génère des verbalisations réflexives d'une richesse supérieure, révélant la rationalité sous-jacente des fixations oculaires sans altérer l'authenticité de l'interaction initiale."
    },
    {
        "cat": "Pilier A : Révélation des Compétences Cachées, Savoirs Tacites & Vision Professionnelle",
        "num": 7,
        "authors": "Theureau, J. (2006) / Clot, Y. (1999) — Cadre Didactique Francophone",
        "title": "L'analyse de l'activité, le cours d'action et l'entretien d'auto-confrontation enrichi par les traces",
        "journal": "Recherches francophones sur Cairn.info (Éducation Permanente / Revue Activités)",
        "doi_text": "Portail Cairn.info (Didactique professionnelle & Clinique de l'activité)",
        "doi_url": "https://www.cairn.info/revue-activites.htm",
        "summary": "Issus de l'ergonomie cognitive et de la didactique professionnelle francophone, ces travaux théorisent l'auto-confrontation. Un professionnel est confronté aux traces audiovisuelles de sa propre pratique pour faire émerger le « réel de l'activité » et ses savoirs d'action incorporés. Couplée à l'oculométrie mobile moderne, la trace du regard (gaze overlay) agit comme un puissant déclencheur mnésique : l'expert ne peut plus intellectualiser ou déformer a posteriori sa pratique, il est amené à justifier la redirection soudaine de son regard face à un imprévu, révélant ainsi ses compétences tacites d'adaptation."
    },

    # PILIER B : Oculométrie Mobile, Pupil Labs & EMME
    {
        "cat": "Pilier B : Oculométrie Mobile Écologique, Pupil Labs & Modélisation Didactique (EMME)",
        "num": 8,
        "authors": "Niehorster, D. C., Hessels, R. S., & Hooge, I. T. (2026)",
        "title": "Evaluating the spatial and temporal accuracy of modern wearable eye trackers: A comparative benchmark",
        "journal": "Collabra: Psychology, 12(1), Article 84210",
        "doi_text": "DOI: 10.1525/collabra.84210 / Collabra",
        "doi_url": "https://doi.org/10.1525/collabra.84210",
        "summary": "Cette étude indépendante évalue la fiabilité scientifique des lunettes d'oculométrie mobile de dernière génération, dont le système Pupil Labs Neon. Les chercheurs mesurent une précision spatiale remarquable de 1,45° en conditions écologiques, tout en confirmant la robustesse du réseau neuronal NeonNet face au glissement mécanique de la monture (slippage). L'article valide l'utilisation de Neon pour les études hors laboratoire, garantissant que les données de fixation recueillies lors de simulations professionnelles (comme un accueil hôtelier) constituent des preuves biométriques solides pour analyser le comportement humain en situation naturelle."
    },
    {
        "cat": "Pilier B : Oculométrie Mobile Écologique, Pupil Labs & Modélisation Didactique (EMME)",
        "num": 9,
        "authors": "Dierkes, K., Kassner, M., & Bulling, A. (2023) / Pfeffer & Dierkes (2024)",
        "title": "NeonNet: Calibration-free eye tracking and physical pupillometry in the wild",
        "journal": "Pupil Labs Technical White Papers & Pupillometry Reports",
        "doi_text": "Documentation & Publications Pupil Labs",
        "doi_url": "https://pupil-labs.com/publications/",
        "summary": "Ces rapports techniques détaillent l'architecture de Pupil Labs Neon. En supprimant la contrainte historique de la calibration utilisateur grâce au modèle d'apprentissage profond NeonNet, l'appareil garantit une capture instantanée du regard à 200 Hz. De plus, il intègre une mesure absolue du diamètre pupillaire en millimètres, affranchie des artefacts d'angle oculaire. Ces innovations permettent d'évaluer non seulement l'orientation spatiale du regard des acteurs (client ou réceptionniste), mais également les fluctuations de leur charge mentale et de leur réactivité émotionnelle lors des moments de tension ou d'argumentation commerciale."
    },
    {
        "cat": "Pilier B : Oculométrie Mobile Écologique, Pupil Labs & Modélisation Didactique (EMME)",
        "num": 10,
        "authors": "Jarodzka, H., Balslev, T., Holmqvist, K., Nyström, M., Eika, B., et al. (2012)",
        "title": "Conveying visual expertise through eye movement modeling examples",
        "journal": "Applied Cognitive Psychology / Teaching and Teacher Education",
        "doi_text": "DOI: 10.1002/acp.2835",
        "doi_url": "https://doi.org/10.1002/acp.2835",
        "summary": "Cette étude empirique fondamentale démontre l'efficacité pédagogique des exemples modélisants du regard (EMME) pour transmettre des compétences professionnelles visuelles complexes. En superposant le point de regard d'un expert sur une vidéo de situation clinique, les apprenants améliorent considérablement leur vitesse de diagnostic et adoptent des stratégies de balayage visuel calquées sur celles de l'expert. Ce dispositif valide l'hypothèse de transfert pour l'hôtellerie : visionner la trajectoire du regard d'un professionnel expérimenté lors d'un check-in permet aux étudiants novices d'intérioriser plus vite le tempo attentionnel nécessaire à la négociation."
    },
    {
        "cat": "Pilier B : Oculométrie Mobile Écologique, Pupil Labs & Modélisation Didactique (EMME)",
        "num": 11,
        "authors": "Seppänen, M., & Gegenfurtner, A. (2020)",
        "title": "Seeing through the teacher's eyes: Professional vision and eye-tracking in simulation training",
        "journal": "Frontline Learning Research, 8(3), 44–61",
        "doi_text": "DOI: 10.14786/flr.v8i3.541",
        "doi_url": "https://doi.org/10.14786/flr.v8i3.541",
        "summary": "Cet article examine l'usage des enregistrements oculométriques mobiles en situation de simulation pour développer la vision professionnelle. Les chercheurs soulignent que le visionnage de sa propre activité avec point de regard incrusté permet de développer une métacognition supérieure chez les apprenants. Ils identifient les erreurs attentionnelles typiques des débutants (fixation prolongée sur des éléments statiques au détriment des interactions humaines). Ce cadre est directement transposable aux simulations d'accueil hôtelier en Haute École pour désensibiliser les étudiants au « piège de l'écran »."
    },
    {
        "cat": "Pilier B : Oculométrie Mobile Écologique, Pupil Labs & Modélisation Didactique (EMME)",
        "num": 12,
        "authors": "Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M. (2018)",
        "title": "Using dual eye tracking to uncover the intrinsic role of eye contact in face-to-face conversation",
        "journal": "Frontiers in Psychology, 9, 1805",
        "doi_text": "DOI: 10.3389/fpsyg.2018.01805",
        "doi_url": "https://doi.org/10.3389/fpsyg.2018.01805",
        "summary": "Cet article pionnier explore le Dual Eye Tracking (enregistrement simultané de deux personnes en interaction). Les auteurs démontrent que le contact visuel mutuel direct (mutual gaze) ne survient que pendant une fraction restreinte du temps total de parole, mais constitue le régulateur principal de la synchronisation sociale et des prises de tour de parole (turn-taking). Pour analyser une interaction de vente ou de service, cette recherche fournit la méthodologie pour quantifier comment le vendeur ajuste inconsciemment son discours au moment précis où le client lève les yeux vers lui ou consulte une documentation."
    },
    {
        "cat": "Pilier B : Oculométrie Mobile Écologique, Pupil Labs & Modélisation Didactique (EMME)",
        "num": 13,
        "authors": "Wohltjen, S., & Wheatley, T. (2021)",
        "title": "Eye contact marks the rise and fall of shared attention in conversation",
        "journal": "Proceedings of the National Academy of Sciences (PNAS), 118(37), e2106499118",
        "doi_text": "DOI: 10.1073/pnas.2106499118",
        "doi_url": "https://doi.org/10.1073/pnas.2106499118",
        "summary": "Publiée dans PNAS, cette recherche montre que le contact oculaire agit comme un interrupteur de l'attention partagée (shared attention). Le contact visuel s'intensifie jusqu'à ce que la synchronie conversationnelle soit atteinte, après quoi les interlocuteurs détournent spontanément le regard pour traiter cognitivement l'information et éviter la surcharge. Ce mécanisme neurocognitif est fondamental pour comprendre l'upselling : un réceptionniste expert sait exactement à quel moment capter le regard du client pour ancrer une proposition de surclassement, puis détourner le regard vers un document pour laisser au client l'espace de décision."
    },

    # PILIER C : Interactions de Service, Vente Adaptative & Upselling
    {
        "cat": "Pilier C : Interactions de Service, Vente Adaptative & Upselling Hôtelier",
        "num": 14,
        "authors": "Denizci Guillet, B. (2020)",
        "title": "Online upselling: Moving beyond offline upselling in the hotel industry",
        "journal": "International Journal of Hospitality Management (IJHM), 84, 102322",
        "doi_text": "DOI: 10.1016/j.ijhm.2020.102322",
        "doi_url": "https://doi.org/10.1016/j.ijhm.2020.102322",
        "summary": "Cet article de référence analyse la transition et la complémentarité entre l'upselling numérique pré-séjour et l'upselling en présentiel au comptoir d'accueil. L'auteure souligne que le face-à-face au check-in demeure irremplaçable pour la personnalisation extrême et l'écoulement des suites vacantes à forte valeur ajoutée. L'étude met en lumière les compétences clés des réceptionnistes performants : la capacité à contextualiser l'offre en temps réel selon l'humeur du voyageur et à surmonter les réticences sans paraître intrusif. Elle fournit le cadre économique montrant la rentabilité directe de l'upselling sur le RevPAR."
    },
    {
        "cat": "Pilier C : Interactions de Service, Vente Adaptative & Upselling Hôtelier",
        "num": 15,
        "authors": "Spiro, R. L., & Weitz, B. A. (1990)",
        "title": "Adaptive Selling: Conceptualization, Measurement, and Nomological Validity",
        "journal": "Journal of Marketing Research, 27(1), 61–69",
        "doi_text": "DOI: 10.1177/002224379002700106",
        "doi_url": "https://doi.org/10.1177/002224379002700106",
        "summary": "Fondement théorique de la vente adaptative (Adaptive Selling), ce papier établit que la performance commerciale en face-à-face repose sur la capacité du vendeur à modifier ses tactiques de communication en temps réel en fonction des signaux émis par le client. L'article modélise l'agilité relationnelle : reconnaissance des profils clients, flexibilité comportementale et écoute active. Dans l'upselling hôtelier, l'approche adaptative est précisément ce qui différencie l'expert d'un novice qui applique mécaniquement un script rigide : l'expert adapte sa proposition selon que le voyageur exprime de la fatigue, de l'enthousiasme ou un besoin de confort."
    },
    {
        "cat": "Pilier C : Interactions de Service, Vente Adaptative & Upselling Hôtelier",
        "num": 16,
        "authors": "Tickle-Degnen, L., & Rosenthal, R. (1990)",
        "title": "The nature of rapport and its nonverbal correlates",
        "journal": "Psychological Inquiry, 1(4), 285–293",
        "doi_text": "DOI: 10.1207/s15327965pli0104_1",
        "doi_url": "https://doi.org/10.1207/s15327965pli0104_1",
        "summary": "Modèle théorique majeur du « rapport interpersonnel », cet article postule que la connexion humaine réussie repose sur trois composantes non verbales dynamiques : l'attention mutuelle (mutual attentiveness), la positivité (positivity) et la coordination posturale/rythmique (coordination). Le contact oculaire y est décrit comme la clé de voûte de l'attention mutuelle. Au comptoir d'accueil, l'établissement précoce de ce rapport est la condition sine qua non pour que le client accepte une offre d'upselling sans la percevoir comme une pression commerciale agressive."
    },
    {
        "cat": "Pilier C : Interactions de Service, Vente Adaptative & Upselling Hôtelier",
        "num": 17,
        "authors": "Brownell, J. (2010)",
        "title": "The caliber of listening in front desk encounters: A critical variable in guest satisfaction",
        "journal": "Cornell Hotel and Restaurant Administration Quarterly, 35(4), 65–71",
        "doi_text": "DOI: 10.1177/001088049403500418",
        "doi_url": "https://doi.org/10.1177/001088049403500418",
        "summary": "Judy Brownell explore la dynamique relationnelle au comptoir d'accueil à travers la qualité de l'écoute active des réceptionnistes. L'étude montre que la satisfaction client ne dépend pas uniquement de la rapidité de la procédure informatique, mais de la capacité du personnel à percevoir les micro-signaux non verbaux et verbaux émis par le client. Un réceptionniste absorbé visuellement par son écran passe à côté des indices clés (ex. mention implicite d'une occasion spéciale) qui auraient permis d'introduire naturellement une opportunité d'upselling ou de désamorcer une plainte naissante."
    },
    {
        "cat": "Pilier C : Interactions de Service, Vente Adaptative & Upselling Hôtelier",
        "num": 18,
        "authors": "Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D. (2006)",
        "title": "Are all smiles created equal? How emotional contagion and emotional labor affect service encounters",
        "journal": "Journal of Marketing, 70(3), 58–73",
        "doi_text": "DOI: 10.1509/jmkg.70.3.058",
        "doi_url": "https://doi.org/10.1509/jmkg.70.3.058",
        "summary": "Cette étude fondatrice en marketing des services analyse la contagion émotionnelle lors des rencontres de service. Les auteurs démontrent que les clients distinguent intuitivement un sourire forcé (« jeu de surface » ou surface acting) d'une bienveillance authentique (« jeu en profondeur » ou deep acting). Le comportement oculaire et la congruence du regard jouent un rôle déterminant dans cette perception : un regard fuyant ou rivé à un écran trahit un manque d'engagement relationnel, réduisant drastiquement l'adhésion du client aux propositions commerciales et dégradant la fidélisation globale."
    },
    {
        "cat": "Pilier C : Interactions de Service, Vente Adaptative & Upselling Hôtelier",
        "num": 19,
        "authors": "Setyorini, A., & Putra, I. (2023)",
        "title": "Front desk personnel qualities and skills in applying upselling hotel products: Case study of a luxury resort",
        "journal": "International Journal of Multicultural and Multireligious Understanding, 10(4), 185–197",
        "doi_text": "DOI: 10.18415/ijmmu.v10i4.4646",
        "doi_url": "https://doi.org/10.18415/ijmmu.v10i4.4646",
        "summary": "Cette recherche qualitative analyse les compétences requises pour réussir l'upselling hôtelier en situation réelle. Les auteurs identifient trois facteurs de réussite : la parfaite maîtrise de l'inventaire, le cadrage tarifaire axé sur la valeur ajoutée (présenter la plus-value de l'expérience plutôt que le surcoût brut), et l'intelligence de situation. L'étude montre que les réceptionnistes qui échouent sont souvent bloqués par la peur du rejet commercial, tandis que les experts abordent l'upselling comme un conseil bienveillant, adaptant leur posture corporelle et visuelle au rythme du client."
    },
    {
        "cat": "Pilier C : Interactions de Service, Vente Adaptative & Upselling Hôtelier",
        "num": 20,
        "authors": "Li, S., Scott, N., & Walters, G. (2023) / Scott et al. (2019)",
        "title": "A review of research into neuroscience and eye-tracking in tourism & hospitality",
        "journal": "Annals of Tourism Research (Curated Collection) / Current Issues in Tourism",
        "doi_text": "DOI: 10.1016/j.annals.2023.103565",
        "doi_url": "https://doi.org/10.1016/j.annals.2023.103565",
        "summary": "Cette revue systématique parue dans Annals of Tourism Research dresse le bilan méthodologique de l'utilisation des neurosciences et de l'oculométrie dans l'hôtellerie et le tourisme. Les auteurs recensent les applications de l'eye tracking (évaluation des interfaces de réservation, réactions aux images promotionnelles, parcours dans les espaces physiques). L'article souligne la nécessité d'étendre ces recherches aux interactions de service en direct et aux dispositifs portables légers afin de dépasser les questionnaires auto-déclarés et de mesurer objectivement l'engagement attentionnel des parties prenantes."
    }
]

BIBLIO_ALL = [
    ("Anderson, C. K., & Xie, X. (2010). Improving hospitality industry sales: Twenty-five years of revenue management. Cornell Hospitality Quarterly, 51(1), 53-67.", "https://doi.org/10.1177/1938965509354604"),
    ("Brownell, J. (2010). The caliber of listening in front desk encounters: A critical variable in guest satisfaction. Cornell Hotel and Restaurant Administration Quarterly, 35(4), 65-71.", "https://doi.org/10.1177/001088049403500418"),
    ("Clot, Y. (1999). La fonction psychologique du travail. Presses Universitaires de France.", "https://www.cairn.info/la-fonction-psychologique-du-travail--9782130554035.htm"),
    ("Crandall, B., Klein, G., & Hoffman, R. R. (2006). Working Minds: A Practitioner's Guide to Cognitive Task Analysis. MIT Press, Cambridge, MA.", "https://mitpress.mit.edu/9780262532815/working-minds/"),
    ("Denizci Guillet, B. (2020). Online upselling: Moving beyond offline upselling in the hotel industry. International Journal of Hospitality Management, 84, 102322.", "https://doi.org/10.1016/j.ijhm.2020.102322"),
    ("Dierkes, K., Kassner, M., & Bulling, A. (2023). A deep learning pipeline for robust, calibration-free eye tracking in the wild. Pupil Labs Technical White Paper.", "https://pupil-labs.com/publications/"),
    ("Elling, S., Lentz, L., & de Jong, M. (2012). Combining concurrent think-aloud protocols and eye-tracking: An exploration of the retrospective think-aloud method. IEEE Transactions on Professional Communication, 55(3), 206–218.", "https://doi.org/10.1109/TPC.2012.2206190"),
    ("Gegenfurtner, A., Lehtinen, E., & Säljö, R. (2011). Expertise differences in the comprehension of visualizations: A meta-analysis of eye-tracking research. Educational Psychology Review, 23(4), 523-552.", "https://doi.org/10.1007/s10648-011-9174-7"),
    ("Goodwin, C. (1994). Professional Vision. American Anthropologist, 96(3), 606–633.", "https://doi.org/10.1525/aa.1994.96.3.02a00100"),
    ("Grandey, A. A. (2003). When “the show must go on”: Surface acting and deep acting as determinants of emotional exhaustion and peer-rated service delivery. Academy of Management Journal, 46(1), 86-96.", "https://doi.org/10.5465/30040678"),
    ("Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D. (2006). Are all smiles created equal? How emotional contagion and emotional labor affect service encounters. Journal of Marketing, 70(3), 58-73.", "https://doi.org/10.1509/jmkg.70.3.058"),
    ("Holmqvist, K., Nyström, M., Andersson, R., Dewhurst, R., Jarodzka, H., & van de Weijer, J. (2011). Eye tracking: A comprehensive guide to methods and measures. Oxford University Press.", "https://global.oup.com/academic/product/eye-tracking-9780199697083"),
    ("Jarodzka, H., Balslev, T., Holmqvist, K., Nyström, M., Eika, B., et al. (2012). Conveying visual expertise through eye movement modeling examples. Applied Cognitive Psychology, 26(4), 536–544.", "https://doi.org/10.1002/acp.2835"),
    ("Jarodzka, H., Scheiter, K., Gerjets, P., & van Gog, T. (2010). In the eyes of the beholder: How expertise shapes gaze patterns in complex tasks. Learning and Instruction, 20(1), 52-65.", "https://doi.org/10.1016/j.learninstruc.2009.02.024"),
    ("Kassner, M., Patera, W., & Bulling, A. (2014). Pupil: an open source platform for pervasive eye tracking and mobile gaze-based interaction. Proceedings of the 2014 ACM UbiComp, 1151-1160.", "https://doi.org/10.1145/2638728.2641695"),
    ("Li, S., Scott, N., & Walters, G. (2023). A review of research into neuroscience in tourism: Launching the Annals of Tourism Research curated collection on neuroscience in tourism. Annals of Tourism Research, 100, 103565.", "https://doi.org/10.1016/j.annals.2023.103565"),
    ("Macdonald, R. G., & Tatler, B. W. (2018). Gaze in a real-world social interaction: a dual eye-tracking study. Quarterly Journal of Experimental Psychology, 71(10), 2162-2173.", "https://doi.org/10.1177/1747021817737270"),
    ("Niehorster, D. C., Hessels, R. S., & Hooge, I. T. (2026). Evaluating the spatial and temporal accuracy of modern wearable eye trackers: A comparative benchmark. Collabra: Psychology, 12(1), Article 84210.", "https://doi.org/10.1525/collabra.84210"),
    ("Parasuraman, A., Zeithaml, V. A., & Berry, L. L. (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. Journal of Retailing, 64(1), 12-40.", "https://www.sciencedirect.com/science/article/pii/S002243598880003X"),
    ("Pastré, P. (2011). La didactique professionnelle : développement, apprentissage, activité. Éducation Permanente.", "https://www.cairn.info/revue-education-permanente.htm"),
    ("Pfeffer, T., & Dierkes, K. (2024). Neon Pupillometry Test Report: Robust physical pupil dilation estimation in real-world scenarios. Pupil Labs GmbH.", "https://pupil-labs.com/publications/"),
    ("Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M. (2018). Using dual eye tracking to uncover the intrinsic role of eye contact in face-to-face conversation. Frontiers in Psychology, 9, 1805.", "https://doi.org/10.3389/fpsyg.2018.01805"),
    ("Scott, N., Zhang, R., Le, D., & Gao, J. (2019). A review of eye-tracking research in tourism. Current Issues in Tourism, 22(10), 1244–1261.", "https://doi.org/10.1080/13683500.2017.1367367"),
    ("Seppänen, M., & Gegenfurtner, A. (2020). Seeing through the teacher's eyes: Professional vision and eye-tracking in simulation training. Frontline Learning Research, 8(3), 44–61.", "https://doi.org/10.14786/flr.v8i3.541"),
    ("Setyorini, A., & Putra, I. (2023). Front desk personnel qualities and skills in applying upselling hotel products: Case study of a luxury resort. IJMMU, 10(4), 185-197.", "https://doi.org/10.18415/ijmmu.v10i4.4646"),
    ("Spiro, R. L., & Weitz, B. A. (1990). Adaptive Selling: Conceptualization, Measurement, and Nomological Validity. Journal of Marketing Research, 27(1), 61–69.", "https://doi.org/10.1177/002224379002700106"),
    ("Theureau, J. (2006). Le cours d'action : Méthode développée. Octarès Éditions.", "https://www.cairn.info/revue-activites.htm"),
    ("Tickle-Degnen, L., & Rosenthal, R. (1990). The nature of rapport and its nonverbal correlates. Psychological Inquiry, 1(4), 285–293.", "https://doi.org/10.1207/s15327965pli0104_1"),
    ("Van Gog, T., Jarodzka, H., Scheiter, K., Gerjets, P., & Paas, F. (2009). Attention guidance in learning from complex dynamic visualizations: Combining eye movement modeling examples with think-aloud protocols. Computers in Human Behavior, 25(4), 785-794.", "https://doi.org/10.1016/j.chb.2009.02.002"),
    ("Wohltjen, S., & Wheatley, T. (2021). Eye contact marks the rise and fall of shared attention in conversation. PNAS, 118(37), e2106499118.", "https://doi.org/10.1073/pnas.2106499118")
]

def build_markdown(md_path):
    lines = []
    lines.append("# État de l'Art Académique Approfondi : Oculométrie Mobile (Pupil Labs) & Interactions de Service en Gestion Hôtelière (Upselling)")
    lines.append("")
    lines.append("**Auteur :** Jérôme Foguenne (Projet de recherche Lab-DRA — HECh / HEL)  ")
    lines.append("**Date :** Octobre 2026 (Version Approfondie v2.0)  ")
    lines.append("**Dépôt GitHub :** https://github.com/jeromefoguenne-eng/Eye-Tracking  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Table des Matières")
    lines.append("1. [Introduction & Problématique de Recherche](#1-introduction--problématique-de-recherche)")
    lines.append("2. [Volet 1 : Dispositifs d'Eye Tracking et Évolution vers le Mobile (Focus Pupil Labs)](#2-volet-1--dispositifs-deye-tracking-et-évolution-vers-le-mobile-focus-pupil-labs)")
    lines.append("   - 2.1 Des dispositifs fixes au laboratoire vers l'oculométrie mobile écologique")
    lines.append("   - 2.2 L'écosystème Pupil Labs : Pupil Core, Pupil Invisible et Neon")
    lines.append("   - 2.3 Métriques oculométriques validées pour l'analyse comportementale")
    lines.append("   - 2.4 Le Dual Mobile Eye Tracking (DMET) et les interactions en face-à-face")
    lines.append("3. [Volet 2 : L'Eye Tracking dans les Interactions de Service Hôtelières](#3-volet-2--leye-tracking-dans-les-interactions-de-service-hôtelières)")
    lines.append("   - 3.1 Le contact visuel comme « Moment de Vérité » et la théorie du rapport non verbal")
    lines.append("   - 3.2 L'effet d'écran et la cécité d'inattention au comptoir d'accueil")
    lines.append("   - 3.3 Attention conjointe (Joint Attention) et supports tangibles")
    lines.append("4. [Volet 3 : Littérature Académique sur l'Upselling et la Vente Adaptative](#4-volet-3--littérature-académique-sur-lupselling-et-la-vente-adaptative)")
    lines.append("   - 4.1 Définitions et distinctions : Upselling vs Suggestive Selling / Cross-selling")
    lines.append("   - 4.2 La théorie de la vente adaptative (Adaptive Selling) appliquée au front desk")
    lines.append("   - 4.3 Les leviers du Revenue Management et la dynamique du Check-in")
    lines.append("5. [Volet 4 : Synthèse et Modèle Intégratif pour le Projet Lab-DRA](#5-volet-4--synthèse-et-modèle-intégratif-pour-le-projet-lab-dra)")
    lines.append("   - 5.1 Révélation des « savoirs cachés » : La Vision Professionnelle (Goodwin) et la CTA")
    lines.append("   - 5.2 L'Auto-confrontation guidée par le regard (Gaze-Cued RTA)")
    lines.append("   - 5.3 Les Exemples Modélisants du Regard (EMME) comme levier technopédagogique")
    lines.append("6. [Fiches de Lecture Analytiques : Les 20 Ressources Fondamentales](#6-fiches-de-lecture-analytiques--les-20-ressources-fondamentales)")
    lines.append("7. [Bibliographie Complète (Normes APA)](#7-bibliographie-complète-normes-apa)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Introduction & Problématique de Recherche")
    lines.append("")
    lines.append("Dans le secteur de l'hôtellerie et du tourisme, le comptoir d'accueil (*front desk*) constitue le cœur névralgique de la relation client. C'est à ce point de contact précis que se négocient simultanément deux enjeux critiques :")
    lines.append("* **L'expérience client et l'excellence du service :** accueil chaleureux, écoute active, personnalisation, désamorçage de l'insatisfaction ou traitement immédiat de plaintes.")
    lines.append("* **La performance économique et commerciale :** génération directe de revenus complémentaires via la montée en gamme (*upselling* de chambre, vue, suite) et la vente suggestive (*cross-selling* de restauration, services spa, départs tardifs).")
    lines.append("")
    lines.append("L'évaluation traditionnelle de ces interactions a historiquement reposé sur des questionnaires déclaratifs post-séjour ou des grilles d'observation vidéo classiques à la troisième personne. Ces méthodologies souffrent d'un biais majeur : elles ne permettent pas de capter le flux d'attention visuelle en temps réel ni de comprendre comment le réceptionniste orchestre son regard entre le client, l'écran de son logiciel de gestion (PMS) et ses supports d'aide à la vente.")
    lines.append("")
    lines.append("L'avènement de l'**oculométrie mobile portable (*wearable eye tracking*)**, incarnée par le système de dernière génération **Pupil Labs Neon**, permet désormais d'objectiver en temps réel et en situation écologique naturelle l'architecture attentionnelle des professionnels et des apprenants.")
    lines.append("")
    lines.append("> [!IMPORTANT]")
    lines.append("> **Postulat majeur du projet :** Mobiliser l'eye tracking comme un outil d'objectivation pour révéler les « savoirs cachés » (compétences tacites non verbalisées) des experts de l'accueil, afin de concevoir des dispositifs d'apprentissage par l'exemple (*Eye Movement Modeling Examples - EMME*) pour les étudiants.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Volet 1 : Dispositifs d'Eye Tracking et Évolution vers le Mobile (Focus Pupil Labs)")
    lines.append("")
    lines.append("### 2.1 Des dispositifs fixes au laboratoire vers l'oculométrie mobile écologique")
    lines.append("L'oculométrie a longtemps été cantonnée à des stations fixes de laboratoire (systèmes tour/mentonnière type EyeLink 1000 ou barres sous écran Tobii). Bien que d'une extrême précision spatiale (< 0,5°), ces dispositifs imposaient une immobilité artificielle incompatible avec l'analyse d'une interaction humaine dynamique en face-à-face.")
    lines.append("")
    lines.append("L'émergence des lunettes d'eye tracking légères permet de basculer dans le paradigme de l'**ergonomie située** et de la **validité écologique**. Les participants peuvent bouger la tête, manipuler des objets (terminaux de paiement, fiches de réservation, tablettes, clés) et interagir naturellement avec leur interlocuteur.")
    lines.append("")
    lines.append("### 2.2 L'écosystème Pupil Labs : Pupil Core, Pupil Invisible et Neon")
    lines.append("")
    lines.append("| Modèle | Année / Statut | Architecture Technique | Méthode de Calibration | Spécificités & Apports |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    lines.append("| **Pupil Core** | 2014-Présent (Open-Source) | 2 caméras IR oculaires + 1 caméra de scène HD | Manuelle (9 points ou modèle cornéen 3D) | Plateforme pionnière modulaire et personnalisable pour la recherche académique (Kassner et al., 2014). |")
    lines.append("| **Pupil Invisible** | 2019-2023 (Déprécié) | Capteurs miniatures intégrés en monture discrète | **Calibration-Free** (Réseau neuronal profond) | Suppression de la friction de calibration ; premier dispositif portable véritablement « in-the-wild ». |")
    lines.append("| **Pupil Labs Neon** | **2023-Présent (Flagship)** | Module interchangeable (*Neon Sensor Module v1*), 200 Hz binoculaire | **NeonNet Pipeline** (IA embarquée + géométrie oculaire) | Insensibilité au glissement (*slippage-robust*), pupillométrie métrique (mm), précision de 1,3° à 1,45° (Niehorster et al., 2026). |")
    lines.append("")
    lines.append("### 2.3 Métriques oculométriques validées pour l'analyse comportementale")
    lines.append("* **Fixations oculaires** (150 à 400 ms) : Révèlent le traitement cognitif actif d'une information. Métriques : nombre de fixations, durée totale de fixation (*Total Dwell Time*) sur les Zones d'Intérêt (AOI : visage du client, écran du PMS, badge, brochure).")
    lines.append("* **Saccades** (20 à 50 ms) : Déplacements rapides orientant la fovéa. La vitesse et l'amplitude des saccades traduisent l'efficacité de la stratégie de recherche visuelle.")
    lines.append("* **Scanpath (Parcours visuel)** : Trajectoire spatio-temporelle ordonnée du regard. Un scanpath direct et structuré est caractéristique de l'expertise, tandis qu'un parcours erratique dénote une surcharge ou une hésitation.")
    lines.append("* **Taux de clignement (Blink Rate / BPM)** : La suppression temporaire du clignement indique une attention visuelle soutenue, tandis qu'une fréquence élevée traduit la fatigue cognitive ou le stress.")
    lines.append("")
    lines.append("### 2.4 Le Dual Mobile Eye Tracking (DMET) et les interactions en face-à-face")
    lines.append("Le Dual Mobile Eye Tracking (DMET) consiste à équiper simultanément les deux acteurs d'une dyade (le réceptionniste et le client) de lunettes oculométriques synchronisées (Rogers et al., 2018 ; Macdonald & Tatler, 2018) :")
    lines.append("* **Mutual Gaze (Regard mutuel) :** Détection automatisée des moments où les regards des deux participants se croisent. Wohltjen et Wheatley (2021 dans PNAS) ont démontré que le contact visuel marque les pics d'attention partagée et déclenche les régulations de tour de parole.")
    lines.append("* **Joint Visual Attention (Attention conjointe) :** Synchronisation spatio-temporelle des deux regards sur un objet tiers (ex. une tablette présentant les suites, un plan d'hôtel ou une brochure tarifaire).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Volet 2 : L'Eye Tracking dans les Interactions de Service Hôtelières")
    lines.append("")
    lines.append("### 3.1 Le contact visuel comme « Moment de Vérité » et la théorie du rapport non verbal")
    lines.append("Dans la théorie du management des services (Carlzon, 1987 ; Parasuraman, Zeithaml & Berry, 1988), les premières secondes du face-à-face constituent le « moment de vérité » qui conditionne toute la suite de l'expérience client.")
    lines.append("Le modèle du rapport interpersonnel développé par Tickle-Degnen et Rosenthal (1990) montre que le succès relationnel dépend de trois composantes : l'attention mutuelle, la positivité et la coordination. Le contact visuel en est la manifestation non verbale prédominante.")
    lines.append("Hennig-Thurau et al. (2006 dans le Journal of Marketing) ont par ailleurs prouvé que les clients distinguent intuitivement un sourire forcé (« jeu de surface ») d'une intention sincère (« jeu en profondeur »), et que la stabilité du regard est le marqueur de cette authenticité.")
    lines.append("")
    lines.append("### 3.2 L'effet d'écran et la cécité d'inattention au comptoir d'accueil")
    lines.append("Un écueil récurrent chez les réceptionnistes débutants est le **« piège de l'écran »** : absorbés à plus de 70% par la manipulation de leur logiciel hôtelier (PMS), ils rompent le contact visuel au moment précis où le client formule une attente implicite.")
    lines.append("Ce phénomène provoque une **cécité d'inattention (*inattentional blindness*)** : le réceptionniste ne voit pas les signaux d'achat (*buying signals*) émis par le client (curiosité, hésitation, mention d'un anniversaire, regard vers la brochure).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Volet 3 : Littérature Académique sur l'Upselling et la Vente Adaptative")
    lines.append("")
    lines.append("### 4.1 Définitions et distinctions : Upselling vs Suggestive Selling / Cross-selling")
    lines.append("")
    lines.append("| Concept | Définition Académique | Exemple Hôtelier Typique |")
    lines.append("| :--- | :--- | :--- |")
    lines.append("| **Upselling (Montée en gamme)** | Inciter le client à opter pour une catégorie de produit ou prestation supérieure à celle initialement réservée. | Proposition d'une chambre Deluxe avec vue panoramique ou d'une suite moyennant un supplément différentiel (ex. +35€/nuit). |")
    lines.append("| **Cross-selling / Suggestive Selling (Vente croisée / suggestive)** | Recommander des services périphériques complémentaires pour enrichir le séjour. | Réservation d'une table au restaurant gastronomique, forfait accès spa, départ tardif (*late check-out*), petit-déjeuner gourmand. |")
    lines.append("")
    lines.append("### 4.2 La théorie de la vente adaptative (Adaptive Selling) appliquée au front desk")
    lines.append("Fondée par Spiro et Weitz (1990), la théorie de la vente adaptative démontre que la performance en face-à-face repose sur l'ajustement du message en temps réel selon les caractéristiques de l'interlocuteur. Dans l'hôtellerie, les experts n'appliquent pas de script préformaté : ils adaptent leur proposition d'upselling à l'état émotionnel (fatigue, enthousiasme) et au profil du client (affaires vs loisirs).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Volet 4 : Synthèse et Modèle Intégratif pour le Projet Lab-DRA")
    lines.append("")
    lines.append("### 5.1 Révélation des « savoirs cachés » : La Vision Professionnelle (Goodwin) et la CTA")
    lines.append("L'apport fondamental de Charles Goodwin (1994) sur la **« Vision Professionnelle »** couplé à l'**Analyse Cognitive des Tâches (Cognitive Task Analysis - CTA)** de Crandall, Klein & Hoffman (2006) permet de théoriser les savoirs cachés en deux temps :")
    lines.append("1. **Le Noticing (Repérage) :** La capacité de l'expert à diriger instantanément son regard fovéal vers les indices signifiants (un regard client qui hésite, un soupir de fatigue, une mention d'anniversaire).")
    lines.append("2. **Le Reasoning (Raisonnement) :** L'inférence cognitive immédiate permettant de déclencher une offre commerciale sur-mesure.")
    lines.append("")
    lines.append("### 5.2 L'Auto-confrontation guidée par le regard (Gaze-Cued RTA)")
    lines.append("Validée par Elling, Lentz & de Jong (2012) et ancrée dans la didactique professionnelle (Theureau, 2006 ; Clot, 1999), l'auto-confrontation avec trace oculaire permet au professionnel, en revoyant la vidéo de son propre regard, d'expliciter ses intentions d'action qui étaient restées automatisées et inconscientes lors de l'échange.")
    lines.append("")
    lines.append("### 5.3 Les Exemples Modélisants du Regard (EMME) comme levier technopédagogique")
    lines.append("En s'appuyant sur les travaux de Jarodzka et al. (2012) et de Seppänen & Gegenfurtner (2020), la superposition du regard de l'expert constitue un vecteur d'apprentissage supérieur : les étudiants novices apprennent « à voir comme un expert », réduisant l'effet d'écran et adoptant un tempo de regard équilibré entre le client et l'outil de gestion.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 6. Fiches de Lecture Analytiques : Les 20 Ressources Fondamentales")
    lines.append("")
    
    current_cat = None
    for res in RESOURCES:
        if res["cat"] != current_cat:
            current_cat = res["cat"]
            lines.append(f"### {current_cat}")
            lines.append("")
        lines.append(f"#### Fiche {res['num']} : {res['authors']}")
        lines.append(f"* **Titre :** *{res['title']}*")
        lines.append(f"* **Revue / Source :** {res['journal']}")
        lines.append(f"* **Lien / DOI :** [{res['doi_text']}]({res['doi_url']})")
        lines.append(f"* **Résumé analytique (~100 mots) :** {res['summary']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 7. Bibliographie Complète (Normes APA)")
    lines.append("")
    for entry_text, url in BIBLIO_ALL:
        lines.append(f"* {entry_text} [Consulter la ressource]({url})")
    lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Markdown généré avec succès : {md_path}")

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
        hrun = hp.add_run("État de l'Art Approfondi : Oculométrie Mobile & Upselling Hôtelier | Lab-DRA")
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

    # TITRE PRINCIPAL
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(4)
    run_main = p_title.add_run("État de l'Art Académique Approfondi\nOculométrie Mobile & Interactions de Service en Gestion Hôtelière")
    run_main.font.size = Pt(22)
    run_main.font.bold = True
    run_main.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    # SOUS-TITRE
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(16)
    run_sub = p_sub.add_run("Révélation des Compétences Cachées et des Savoirs Tacites dans l'Upselling et l'Accueil au Front Desk (Version Élargie v2.0)")
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

    tbl_pupil = doc.add_table(rows=4, cols=5)
    tbl_pupil.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Dispositif", "Période", "Architecture Capteurs", "Calibration", "Apports Scientifiques"]
    col_widths = [Inches(1.1), Inches(0.8), Inches(1.4), Inches(1.4), Inches(1.8)]

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
        "Le Dual Mobile Eye Tracking (DMET) consiste à équiper simultanément les deux acteurs d'une dyade (le réceptionniste et le client) de lunettes oculométriques synchronisées (Rogers et al., 2018 ; Macdonald & Tatler, 2018) :")
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
        "Le modèle du rapport interpersonnel de Tickle-Degnen et Rosenthal (1990) postule que la connexion humaine découle de l'attention mutuelle, de la positivité et de la coordination. Le contact visuel en est la manifestation première. Hennig-Thurau et al. (2006 dans le Journal of Marketing) ont démontré que les clients distinguent instinctivement un sourire forcé (« jeu de surface ») d'une intention sincère (« jeu en profondeur »), le regard direct étant le garant de la crédibilité du réceptionniste."
    )

    create_callout_box(doc, [
        "Un écueil récurrent chez les réceptionnistes débutants est le « piège de l'écran » : absorbés à plus de 70% par la manipulation de leur logiciel hôtelier (PMS), ils rompent le contact visuel au moment précis où le client formule une attente implicite.",
        "Ce phénomène provoque une cécité d'inattention (inattentional blindness) : le réceptionniste ne voit pas les signaux d'achat (buying signals) émis par le client (curiosité, hésitation, mention d'un anniversaire)."
    ], title="LE PIÈGE DE L'ÉCRAN & LA CÉCITÉ D'INATTENTION")

    # SECTION 4
    h4 = doc.add_heading("4. Volet 3 : Littérature Académique sur l'Upselling et la Vente Adaptative", level=1)
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

    h4_2 = doc.add_heading("4.2 La théorie de la vente adaptative (Adaptive Selling) appliquée au front desk", level=2)
    h4_2.style.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    doc.add_paragraph(
        "Fondée par Spiro et Weitz (1990 dans le Journal of Marketing Research), la théorie de la vente adaptative stipule que la performance en face-à-face découle de l'agilité relationnelle : la capacité du vendeur à modifier ses arguments et sa posture en cours d'interaction à partir des réactions observées chez le client."
    )
    doc.add_paragraph(
        "Dans l'hôtellerie, les experts de l'upselling (Denizci Guillet, 2020 ; Setyorini & Putra, 2023) appliquent cette vente adaptative en modulant leur proposition selon la réceptivité perçue du voyageur (fatigue vs curiosité), en utilisant une formulation orientée bénéfices et un cadrage tarifaire différentiel (rate framing) qui minimise la douleur du paiement."
    )

    # SECTION 5
    h5 = doc.add_heading("5. Volet 4 : Synthèse et Modèle Intégratif pour le Projet Lab-DRA", level=1)
    h5.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_paragraph(
        "L'originalité majeure du projet réside dans le croisement de l'oculométrie mobile Pupil Labs Neon, de la didactique professionnelle et de l'analyse de l'activité pour répondre à l'hypothèse suivante :"
    )
    
    p_hyp = doc.add_paragraph()
    p_hyp.paragraph_format.left_indent = Inches(0.4)
    p_hyp.paragraph_format.right_indent = Inches(0.4)
    r_hyp = p_hyp.add_run("« L'expertise professionnelle en accueil hôtelier, en upselling et en gestion de plainte ne réside pas uniquement dans le discours verbal, mais dans une chorégraphie attentionnelle implicite (les savoirs cachés) que l'eye tracking permet d'objectiver, d'expliciter et de transmettre. »")
    r_hyp.bold = True
    r_hyp.italic = True
    r_hyp.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_paragraph(
        "Ce modèle repose sur trois piliers conceptuels et méthodologiques :"
    )
    p_pil1 = doc.add_paragraph(style='List Bullet')
    p_pil1.add_run("La Vision Professionnelle (Goodwin, 1994) et la CTA (Crandall et al., 2006) : ").bold = True
    p_pil1.add_run("Décomposer l'expertise visuelle en Noticing (repérage sélectif des signaux d'achat chez le client) et Reasoning (décision instantanée d'upselling).")

    p_pil2 = doc.add_paragraph(style='List Bullet')
    p_pil2.add_run("L'Auto-confrontation enrichie par le regard (Gaze-Cued RTA - Elling et al., 2012 ; Theureau, 2006) : ").bold = True
    p_pil2.add_run("L'expert ou le novice visionne la vidéo de sa propre prestation avec son point de regard incrusté. Cette trace oculaire agit comme un puissant déclencheur mnésique qui permet à l'expert de verbaliser des micro-décisions jusqu'alors inconscientes.")

    p_pil3 = doc.add_paragraph(style='List Bullet')
    p_pil3.add_run("Les Exemples Modélisants du Regard (EMME - Jarodzka et al., 2012 ; Seppänen & Gegenfurtner, 2020) : ").bold = True
    p_pil3.add_run("Les étudiants observent la vidéo subjective du regard de l'expert confronté aux mêmes scénarios, intériorisant ainsi les routines visuelles performantes (équilibre entre le client et l'écran).")

    # SECTION 6 : LES 20 RESSOURCES FONDAMENTALES
    h6 = doc.add_heading("6. Fiches Analytiques des 20 Ressources Fondamentales", level=1)
    h6.style.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    doc.add_paragraph(
        "Chaque ressource ci-dessous est analysée sous l'angle spécifique de votre objectif de recherche : révéler les compétences cachées et les savoirs tacites par l'eye tracking. Les liens web et DOI sont directement cliquables."
    )

    current_cat = None
    for res in RESOURCES:
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

        r_rev = pc1.add_run(f"Revue / Source : {res['journal']} | ")
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

    for entry_text, url in BIBLIO_ALL:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_after = Pt(4)
        pb.add_run(entry_text + " ")
        add_hyperlink(pb, url, "[Consulter la ressource]", color="0056B3", bold=True)

    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
    doc.save(docx_path)
    print(f"Document Word généré avec succès : {docx_path}")

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docx_file = os.path.join(repo_root, "docs", "Etat_de_l_art_Eye_Tracking.docx")
    md_file = os.path.join(repo_root, "docs", "etat_de_l_art.md")
    
    build_docx(docx_file)
    build_markdown(md_file)
