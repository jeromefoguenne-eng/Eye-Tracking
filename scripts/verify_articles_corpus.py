# -*- coding: utf-8 -*-
"""
Script de génération de l'État de l'Art - Projet SIMACCUEIL (Lab-DRA / HECh / HEL)
Basé exclusivement sur le document de référence :
"Constats Etats de l'art.docx" (Jérôme Foguenne)
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/1fkIBcrCzPRb5vu38I-Tx5bAdVap7IFEn?usp=sharing"

# 22 Références strictement issues de Constats Etats de l'art.docx (Texte 9 exclu comme indiqué par l'auteur)
ARTICLES = [
    {
        "num": "Texte 01",
        "pilier": "Pilier 1 : Fondements Cognitifs, Expertise & Vision Professionnelle",
        "auteurs": "Beckmann, J. F.",
        "annee": "2010",
        "titre": "Taming a beast of burden – On some issues with the conceptualisation and operationalisation of cognitive load",
        "revue": "Learning and Instruction, 20(3), 250–264",
        "doi": "https://doi.org/10.1016/j.learninstruc.2010.02.006",
        "drive_file": "01 - Taming a beast of burden – On some issues with the conceptualisation and operationalisation of cognitive load.docx",
        "resume": (
            "L’article de Jens Beckmann analyse les limites conceptuelles et méthodologiques de la théorie de la charge cognitive (CLT). "
            "L’auteur souligne l’incapacité des mesures traditionnelles à isoler les charges intrinsèque, extrinsèque et germane, "
            "celles-ci ne mesurant que l’effort global perçu. Pour surmonter cet obstacle, Beckmann développe le Cadre de Complexité "
            "(Complexity Framework), distinguant rigoureusement les exigences objectives de la tâche, les conditions de la situation "
            "et les capacités de mémoire de travail du sujet. Une validation empirique auprès de trois populations démontre que l’analyse "
            "a priori des actes cognitifs requis prédit bien plus fidèlement la charge mentale et les performances d’apprentissage."
        ),
        "contribution": (
            "Pour SIMACCUEIL, cet article éclaire le lien critique entre maîtrise logicielle et disponibilité attentionnelle. En accueil "
            "hôtelier, la manipulation du PMS génère une charge cognitive majeure chez le réceptionniste novice. L’automatisation des "
            "procédures de saisie informatique et des requêtes tarifaires libère des ressources en mémoire de travail, permettant au "
            "professionnel de reporter son attention visuelle vers le client. Cette disponibilité cognitive est la condition sine qua non "
            "pour observer les indices comportementaux non verbaux de l’interlocuteur, diagnostiquer ses attentes implicites et saisir les "
            "opportunités propices à l’upselling ou à la désescalade lors d’une réclamation."
        )
    },
    {
        "num": "Texte 02",
        "pilier": "Pilier 1 : Fondements Cognitifs, Expertise & Vision Professionnelle",
        "auteurs": "Gegenfurtner, A., Lehtinen, E., & Säljö, R.",
        "annee": "2011",
        "titre": "Expertise Differences in the Comprehension of Visualizations: A Meta-Analysis of Eye-Tracking Research",
        "revue": "Educational Psychology Review, 23(4), 523–552",
        "doi": "https://doi.org/10.1007/s10648-011-9174-7",
        "drive_file": "02 - Expertise Differences in the Comprehension of Visualizations a Meta-Analysis of Eye-Tracking.pdf",
        "resume": (
            "Cette méta-analyse pionnière synthétise 73 études empiriques en oculométrie (819 experts et 893 novices) afin d’éprouver "
            "les lois régissant la perception experte. Les résultats confirment trois théories majeures : la mémoire de travail à long terme "
            "(durées moyennes de fixation plus brèves), la réduction de l’information (davantage de fixations sélectives sur les zones "
            "pertinentes et rejet des distracteurs redondants) et le modèle holistique (saccades plus amples et accès parafovéal accéléré "
            "vers l’information critique). Ces mécanismes oculomoteurs universels expliquent la rapidité d’interprétation et la supériorité "
            "décisionnelle constante des experts à travers de multiples domaines professionnels."
        ),
        "contribution": (
            "Cette méta-analyse fournit à SIMACCUEIL ses postulats directeurs : l’expertise en réception ne se caractérise pas par un regard "
            "fixe ou omniscient, mais par une allocation sélective de l’attention. L’opérateur expérimenté identifie instantanément les "
            "zones signifiantes de son environnement (champs clés du PMS, micro-expressions du client). Les critères d’opérationnalisation "
            "de l’expertise (heures d’entraînement, simulations accumulées) permettent de structurer le protocole expérimental. L’objectif "
            "pédagogique consiste à mesurer comment la familiarisation logicielle progressive amène les étudiants à délaisser les champs "
            "secondaires de l’écran pour focaliser leur regard sur les variables décisives de la relation de service."
        )
    },
    {
        "num": "Texte 03",
        "pilier": "Pilier 3 : Didactique Professionnelle & Modélisation du Regard (EMME)",
        "auteurs": "Van Gog, T., Paas, F., Marcus, N., Ayres, P., & Sweller, J.",
        "annee": "2009",
        "titre": "Examining the effect of eye-movement modelling examples on learning",
        "revue": "Computers in Human Behavior, 25(3), 785–789",
        "doi": "https://doi.org/10.1016/j.chb.2009.02.005",
        "drive_file": "03 - VanGogetal_CiHB_2009.pdf",
        "resume": (
            "Cet article évalue l’intérêt pédagogique de superposer les mouvements oculaires d’un expert sur des exemples de résolution "
            "de problèmes pour guider l’attention des apprenants. Contrairement aux attentes initiales, la visualisation brute du tracé "
            "oculaire combinée à des explications verbales peut s’avérer contre-productive en introduisant une redondance attentionnelle "
            "et une surcharge cognitive extrinsèque. Les auteurs concluent que rendre visible le regard expert ne suffit pas à transmettre "
            "son raisonnement. L’efficacité du guidage visuel dépend étroitement de la complexité dynamique de la tâche et nécessite une "
            "scénarisation didactique rigoureuse pour éviter toute interférence attentionnelle."
        ),
        "contribution": (
            "Pour SIMACCUEIL, cette recherche prévient un écueil majeur : projeter le flux vidéo brut de l’eye tracker Neon aux étudiants "
            "ne constitue pas un outil didactique magique. En débriefing post-simulation, le tracé oculaire ne prend sens que s’il est "
            "confronté aux verbalisations du réceptionniste et aux micro-situations professionnelles (co-attention sur tablette, bascule "
            "vers l’écran). Cette étude invite à construire une grille d’observation articulant fixations et intentions réelles, tout en "
            "réservant l’analyse visuelle à des moments critiques bien délimités (annonce d’un supplément tarifaire ou formulation d’une "
            "objection par le client) pour garantir un apprentissage réflexif optimal."
        )
    },
    {
        "num": "Texte 04",
        "pilier": "Pilier 1 : Fondements Cognitifs, Expertise & Vision Professionnelle",
        "auteurs": "Goodwin, C.",
        "annee": "1994",
        "titre": "Professional Vision",
        "revue": "American Anthropologist, 96(3), 606–633",
        "doi": "https://doi.org/10.1525/aa.1994.96.3.02a00100",
        "drive_file": "04 - Goodwin - Professional vision.pdf",
        "resume": (
            "Dans son texte fondateur, Charles Goodwin démontre que la perception n’est pas un processus purement physiologique individuel, "
            "mais une pratique sociale et située forgée par l’appartenance à une communauté de pratique : la vision professionnelle. "
            "À travers l’analyse ethnographique de fouilles archéologiques et du procès Rodney King, Goodwin identifie trois pratiques "
            "discursives constitutives de l’expertise : les schémas de codage (catégorisation du réel), la mise en évidence visuelle "
            "(highlighting de traits saillants) et la production de représentations graphiques partagées. La vision experte transforme ainsi "
            "un flux perceptif brut en objets signifiants pour l’action collective."
        ),
        "contribution": (
            "Goodwin offre à SIMACCUEIL son cadre épistémologique fondamental : regarder un comptoir de réception ou un écran PMS n’est pas "
            "un acte neutre, mais une compétence professionnelle située. Les étudiants doivent apprendre à voir comme des réceptionnistes "
            "chevronnés. Cela implique de maîtriser le codage des informations hôtelières (disponibilités, profils clients VIP), de repérer "
            "immédiatement les signaux d’insatisfaction ou d’ouverture commerciale, et d’utiliser la tablette comme représentation partagée "
            "avec le client. Goodwin justifie une grille d’analyse articulant données oculométriques, interactions verbales et manipulations "
            "d’artefacts dans la construction d’une posture d’accueil experte."
        )
    },
    {
        "num": "Texte 05",
        "pilier": "Pilier 1 : Fondements Cognitifs, Expertise & Vision Professionnelle",
        "auteurs": "Crandall, B., Klein, G. A., & Hoffman, R. R.",
        "annee": "2006",
        "titre": "Working Minds: A Practitioner's Guide to Cognitive Task Analysis",
        "revue": "MIT Press, Cambridge, MA",
        "doi": "https://doi.org/10.7551/mitpress/7304.001.0001",
        "drive_file": "05 - Crandall, Klein & Hoffman - Working Minds - A Practitioner's Guide to Cognitive Task Analysis (Synthese).docx",
        "resume": (
            "Cet ouvrage de référence opérationnalise l’Analyse Cognitive des Tâches (Cognitive Task Analysis - CTA) dans le paradigme "
            "du Naturalistic Decision Making. Les auteurs démontrent que l’expertise repose massivement sur des connaissances tacites et "
            "une reconnaissance automatique de configurations (pattern recognition) difficilement verbalisables spontanément. La méthode "
            "de décision critique (CDM) déploie un protocole d’entretien en quatre étapes (cadrage, recueil approfondi des incidents "
            "critiques, analyse des exigences décisionnelles et modélisation didactique) permettant d’expliciter les indices perceptifs "
            "subtils guidant les décisions expertes sous forte pression temporelle."
        ),
        "contribution": (
            "Pour SIMACCUEIL, la CTA fournit la méthode idéale pour construire les scénarios de simulation et exploiter les données de "
            "l’eye tracking Neon. Les arbitrages d’un réceptionniste (refuser un surclassement gratuit, proposer une suite, gérer un "
            "client furieux) reposent sur des indices discrets. En utilisant le tracé oculaire comme support d’un entretien de rappel "
            "stimulé post-simulation, le chercheur amène l’étudiant ou l’expert à verbaliser les raisons exactes pour lesquelles son "
            "regard s’est posé sur une case tarifaire ou sur le visage du client à une seconde précise, explicitant ainsi l’intuition "
            "décisionnelle hôtelière."
        )
    },
    {
        "num": "Texte 06",
        "pilier": "Pilier 3 : Didactique Professionnelle & Modélisation du Regard (EMME)",
        "auteurs": "Elling, S., Lentz, L., & de Jong, M.",
        "annee": "2012",
        "titre": "Combining Concurrent Think-Aloud Protocols and Eye-Tracking Observations: An Analysis of Verbalizations and Silences",
        "revue": "IEEE Transactions on Professional Communication, 55(3), 206–220",
        "doi": "https://doi.org/10.1109/TPC.2012.2206190",
        "drive_file": "06- Combining Concurrent Think-Aloud Protocols and Eye-Tracking Observations.pdf",
        "resume": (
            "Les auteurs examinent la validité méthodologique de l’articulation entre le protocole de verbalisation concomitante "
            "(think-aloud) et l’oculométrie. En analysant la nature des verbalisations et des silences (qui représentent 27 % du temps "
            "d’interaction), l’étude démontre que les deux techniques se complètent idéalement. L’oculométrie révèle précisément ce que "
            "les participants traitent visuellement durant leurs phases de mutisme, souvent causées par une surcharge cognitive intense "
            "ou l’exécution d’une routine procédurale automatisée, levant ainsi l’opacité inhérente aux seuls rapports verbaux."
        ),
        "contribution": (
            "Dans SIMACCUEIL, où le réceptionniste interagit verbalement avec un client simulé, le think-aloud concomitant est inapplicable "
            "sans détruire le réalisme écologique de l’accueil. L’apport d’Elling et al. réside dans la valorisation des silences : lorsqu’un "
            "étudiant s’interrompt de parler face au client, l’eye tracker Pupil Labs Neon capture exactement ce qui accapare son regard "
            "(hésitation sur le PMS, recherche désespérée d’un tarif, blocage technique). L’entretien d’explicitation rétrospectif s’appuie "
            "sur ces épisodes de silence oculairement documentés pour comprendre l’origine des ruptures de communication en front desk."
        )
    },
    {
        "num": "Texte 07",
        "pilier": "Pilier 1 : Fondements Cognitifs, Expertise & Vision Professionnelle",
        "auteurs": "Theureau, J. (recension par Marc Durand)",
        "annee": "2016",
        "titre": "Le cours d’action. L’enaction et l’expérience (Recension de l’ouvrage de 2015)",
        "revue": "Activités, 13(2)",
        "doi": "https://doi.org/10.4000/activites.2847",
        "drive_file": "07 - « L'analyse de l'activité, le cours d'action et l'entreti.pdf",
        "resume": (
            "La recension par Marc Durand de l’œuvre majeure de Jacques Theureau expose le programme de recherche du cours d’action, "
            "ancré dans l’épistémologie de l’enaction et de la cognition située. Ce cadre postule que l’activité humaine constitue un "
            "processus dynamique de construction de sens, accessible par l’analyse de ce qui est montrable, racontable et mimable "
            "par l’acteur. L’ouvrage propose des outils méthodologiques rigoureux (entretiens d’autoconfrontation, décomposition en "
            "unités élémentaires d’action-signe) pour reconstruire la dynamique temporelle de l’expérience vécue en contexte professionnel "
            "naturel ou simulé."
        ),
        "contribution": (
            "Le cours d’action offre à SIMACCUEIL un cadre théorique solide pour articuler les métriques oculaires objectives et la "
            "signification subjective vécue par le réceptionniste. Le regard ne peut être réduit à des coordonnées cartésiennes : il est "
            "une unité d’action qui actualise les préoccupations de l’acteur à l’instant t. L’enregistrement Pupil Labs Neon sert de trace "
            "matérielle pour mener des entretiens d’autoconfrontation post-simulation. L’étudiant explicite comment la perception visuelle "
            "d’une réclamation ou d’un écran PMS a façonné son cours d’expérience, facilitant une transformation réflexive de ses pratiques."
        )
    },
    {
        "num": "Texte 08",
        "pilier": "Pilier 2 : Métrologie Oculométrique Mobile & Zones d'Intérêt (AOI)",
        "auteurs": "Hooge, I. T. C., Nyström, M., Niehorster, D. C., Andersson, R., et al.",
        "annee": "2024",
        "titre": "The fundamentals of eye tracking part 6: Working with areas of interest",
        "revue": "Behavior Research Methods, 56(6), 5780–5800",
        "doi": "https://doi.org/10.3758/s13428-023-02264-5",
        "drive_file": "08 - The fundamentals of eye tracking part 6.docx",
        "resume": (
            "Ce guide méthodologique fondamental clarifie la conception, l’opérationnalisation et les limites de l’usage des zones d’intérêt "
            "(Areas of Interest - AOI). Les auteurs avertissent qu’une fixation dans une AOI ne prouve ni le traitement cognitif ni la "
            "compréhension du stimulus. Ils détaillent les exigences métrologiques : calibrage de la taille des AOI selon la précision réelle "
            "du matériel, distinction entre AOI statiques (écrans fixes) et AOI dynamiques (cibles mobiles dans l’espace réel), et risques de "
            "biais d’agrégation temporelle. Le texte insiste sur la transparence des choix d’échantillonnage et de découpage des zones."
        ),
        "contribution": (
            "Cet article est le manuel de référence pour la conception des protocoles d’analyse dans SIMACCUEIL. Dans un accueil hôtelier, "
            "les cibles visuelles sont mixtes : le PMS sur ordinateur fixe requiert des AOI d’interface statiques (tarifs, chambre, boutons), "
            "tandis que le visage du client, ses gestes et la tablette d’upselling nécessitent des AOI dynamiques tridimensionnelles. "
            "L’étude prescrit de dimensionner les marges de tolérance des AOI en tenant compte de la parallaxe et de la précision angulaire "
            "des lunettes Pupil Labs Neon, garantissant une interprétation reproductible et scientifiquement irréprochable des temps de fixation."
        )
    },
    {
        "num": "Texte 10",
        "pilier": "Pilier 3 : Didactique Professionnelle & Modélisation du Regard (EMME)",
        "auteurs": "Jarodzka, H., Balslev, T., Holmqvist, K., Nyström, M., Scheiter, K., Gerjets, P., & Eika, B.",
        "annee": "2012",
        "titre": "Conveying clinical reasoning based on visual observation via eye-movement modelling examples",
        "revue": "Instructional Science, 40(5), 813–827",
        "doi": "https://doi.org/10.1007/s11251-012-9218-1",
        "drive_file": "10 - Conveying clinical reasoning based on visual observation.pdf",
        "resume": (
            "Cette étude quasi-expérimentale examine comment la forme de visualisation du regard expert influence l’apprentissage clinique. "
            "Des étudiants en médecine visionnent des cas pédiatriques selon trois conditions : verbalisation seule (contrôle), cercle "
            "oculaire ou mise en évidence de type spotlight (zone fixée nette, environnement flouté). Les résultats révèlent la supériorité "
            "du spotlight, qui guide sélectivement l’attention sans détruire la perception de la scène globale. Les étudiants de cette "
            "condition obtiennent des performances diagnostiques significativement supérieures sur de nouveaux cas sans guidage visuel."
        ),
        "contribution": (
            "Jarodzka et al. démontrent que l’oculométrie peut modéliser l’expertise pour l’enseignement sans tomber dans l’écueil du "
            "cercle rouge distrayant. Pour la formation hôtelière à l’HECh, la transposition est immédiate : pour concevoir des capsules "
            "vidéo d’apprentissage de l’accueil, un effet spotlight guidant le regard des étudiants vers les zones décisives (un détail du "
            "PMS, une crispation de la cliente mécontente) transmettra les heuristiques de décision bien plus efficacement qu’un simple "
            "cours magistral, renforçant la vision professionnelle avant les mises en situation réelles."
        )
    },
    {
        "num": "Texte 11",
        "pilier": "Pilier 3 : Didactique Professionnelle & Modélisation du Regard (EMME)",
        "auteurs": "Seppänen, M., & Gegenfurtner, A.",
        "annee": "2012",
        "titre": "Seeing through a teacher's eyes improves students' imaging interpretation",
        "revue": "Medical Education, 46(11), 1113–1114",
        "doi": "https://doi.org/10.1111/medu.12028",
        "drive_file": "11 - Seppanen_Gegenfurtner_2012_MedicalEducation.pdf",
        "resume": (
            "Dans cette publication synthétique, les auteurs testent l’efficacité de l’apprentissage par modélisation du regard de l’enseignant "
            "(EMME) lors de l’interprétation d’imageries diagnostiques complexes. Les apprenants exposés au cheminement visuel dynamique "
            "de l’expert développent des stratégies d’inspection méthodique et découvrent plus rapidement les anomalies structurelles. "
            "L’article démontre que le guidage visuel explicite structure l’organisation perceptive des novices, accélérant leur transition "
            "vers un traitement holistique de l’image et prévenant les erreurs d’inattention ou de recherche aléatoire."
        ),
        "contribution": (
            "Cet apport confirme la faisabilité didactique d’un transfert de compétences basé sur le regard dans SIMACCUEIL. Dans la "
            "manipulation des interfaces complexes de gestion hôtelière (Opera, PMS), les étudiants passent souvent de longues secondes "
            "à chercher une fonction. En modélisant les saccades expertes d’un réceptionniste confirmé (qui va droit à l’information "
            "d’upselling tout en maintenant le contact oculaire), l’enseignant fournit un modèle perceptivo-moteur facilitant la routinisation "
            "des contrôles visuels et fluidifiant l’interaction commerciale de l’apprenant face au client."
        )
    },
    {
        "num": "Texte 12",
        "pilier": "Pilier 4 : Dynamiques Interactionnelles, Synchronisation & Rapport",
        "auteurs": "Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M.",
        "annee": "2018",
        "titre": "Using dual eye tracking to uncover personal gaze patterns during social interaction",
        "revue": "Scientific Reports, 8, Article 4271",
        "doi": "https://doi.org/10.1038/s41598-018-22726-7",
        "drive_file": "12 - Using_dual_eye_tracking_to_uncover_personal_gaze_p.pdf",
        "resume": (
            "Cette étude utilise un dispositif de double oculométrie mobile (dual eye tracking) pour enregistrer simultanément le regard "
            "de deux interlocuteurs lors d’une interaction sociale face-à-face non contrainte. Les auteurs mettent au jour une signature "
            "visuelle personnelle très stable, mais révèlent que le contact visuel direct mutuel est beaucoup plus rare que supposé, ne "
            "représentant qu’une faible fraction du temps. Les participants détournent systématiquement leur regard pendant la formulation "
            "de leurs propos afin de moduler leur charge cognitive, le contact oculaire intervenant principalement lors de l’écoute passive."
        ),
        "contribution": (
            "Cette recherche est méthodologiquement fondatrice pour SIMACCUEIL, qui envisage d’équiper simultanément le réceptionniste "
            "et le client avec des lunettes Neon. Elle empêche d’adopter une vision naïve de l’accueil hôtelier : un bon réceptionniste ne "
            "regarde pas le client en continu dans les yeux. L’aversion du regard vers l’écran ou le comptoir est normale lors de la réflexion "
            "ou du chiffrage de l’upselling. L’enjeu évaluatif sera de mesurer la synchronisation des regards et d’identifier les moments où "
            "le décrochage visuel devient nuisible au sentiment d’écoute et à la gestion bienveillante de la plainte."
        )
    },
    {
        "num": "Texte 13",
        "pilier": "Pilier 4 : Dynamiques Interactionnelles, Synchronisation & Rapport",
        "auteurs": "Wohltjen, S., & Wheatley, T.",
        "annee": "2021",
        "titre": "Eye contact marks the rise and fall of shared attention in conversation",
        "revue": "Proceedings of the National Academy of Sciences (PNAS), 118(37), e2106490118",
        "doi": "https://doi.org/10.1073/pnas.2106490118",
        "drive_file": "13 - wohltjen_wheatley_PNAS_2021.pdf",
        "resume": (
            "Publié dans PNAS, cet article majeur explore les liens dynamiques entre le contact visuel, la synchronisation pupillaire "
            "et l’attention partagée lors de conversations naturelles spontanées. À l’aide de lunettes oculométriques et de l’analyse "
            "de synchronie croisée, les chercheuses démontrent que le contact oculaire marque le point culminant (apogée) de l’attention "
            "partagée, mais qu’il entraîne immédiatement après une désynchronisation attentionnelle. La rupture du contact visuel apparaît "
            "ainsi nécessaire pour permettre aux interlocuteurs de réinitialiser leur pensée individuelle et d’injecter de nouvelles idées "
            "dans le dialogue."
        ),
        "contribution": (
            "Cet article apporte une clé d’analyse théorique d’une valeur inestimable pour le projet : le contact visuel en réception "
            "hôtelière opère comme un signal de coordination interactionnelle cyclique. Pour SIMACCUEIL, l’alternance entre regards mutuels "
            "intenses et regards vers le logiciel ou la tablette ne traduit pas une faute professionnelle, mais une respiration cognitive "
            "naturelle. L’analyse des données Neon permettra de vérifier si les étudiants experts savent synchroniser leur regard au moment "
            "précis de l’accord client (clôture de l’upselling ou acceptation d’une compensation) avant de replonger dans la saisie logicielle."
        )
    },
    {
        "num": "Texte 14",
        "pilier": "Pilier 4 : Dynamiques Interactionnelles, Synchronisation & Rapport",
        "auteurs": "Tickle-Degnen, L., & Rosenthal, R.",
        "annee": "1990",
        "titre": "The Nature of Rapport and Its Nonverbal Correlates",
        "revue": "Psychological Inquiry, 1(4), 285–293",
        "doi": "https://doi.org/10.1207/s15327965pli0104_1",
        "drive_file": "14 - The_Nature_of_Rapport_and_Its_Nonverbal_Correlates.pdf",
        "resume": (
            "Dans ce modèle théorique fondateur, Tickle-Degnen et Rosenthal conceptualisent le « rapport » interpersonnel comme l’expérience "
            "partagée d’une relation harmonieuse et empathique, reposant sur trois composantes non verbales interconnectées : l’attention "
            "mutuelle (regard dirigé, posture orientée), la positivité (sourires, hochements de tête) et la coordination interactionnelle "
            "(posture en miroir, synchronie temporelle des mouvements). Les auteurs montrent que l’importance relative de ces dimensions "
            "évolue au fil de l’échange, la coordination devenant prépondérante à mesure que la relation se consolide."
        ),
        "contribution": (
            "Le modèle du rapport fournit la grille de lecture psychosociale indispensable pour évaluer la qualité de l’accueil dans "
            "SIMACCUEIL. Les mesures brutes d’eye tracking (fixations) ne prennent de la valeur que si elles sont corrélées aux indices de "
            "l’attention mutuelle et de la synchronie non verbale. Lors d’une réclamation client, le rétablissement de la confiance repose "
            "sur la coordination du réceptionniste face à la détresse du voyageur. Cette référence permet de construire une grille externe "
            "multidimensionnelle articulant l’orientation corporelle, le regard et le verbatim pour valider la réussite relationnelle de la simulation."
        )
    },
    {
        "num": "Texte 15",
        "pilier": "Pilier 4 : Dynamiques Interactionnelles, Synchronisation & Rapport",
        "auteurs": "Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D.",
        "annee": "2006",
        "titre": "Are All Smiles Created Equal? How Emotional Contagion and Emotional Labor Affect Service Relationships",
        "revue": "Journal of Marketing, 70(3), 58–73",
        "doi": "https://doi.org/10.1509/jmkg.70.3.058",
        "drive_file": "15.a. - Are_All_Smiles_Created_Equal_How_Emotional_Contagi.pdf",
        "resume": (
            "Cet article fondamental du Journal of Marketing étudie l’impact des sourires des employés sur la satisfaction client à travers "
            "le prisme du travail émotionnel (emotional labor) et de la contagion émotionnelle primitive. En comparant les sourires authentiques "
            "(Duchenne, impliquant les muscles périorbitaires) et les sourires de façade (surface acting imposé par les standards de service), "
            "les auteurs démontrent que seuls les sourires authentiques déclenchent une contagion émotionnelle positive chez le client. Les sourires "
            "feints sont immédiatement détectés et dégradent l’évaluation globale de l’interaction de service."
        ),
        "contribution": (
            "Cette étude apporte à SIMACCUEIL un avertissement majeur : la relation client en hôtellerie ne se résume pas à l’application "
            "mécanique de standards comportementaux. Pour le volet réclamation et upselling, un réceptionniste affichant un sourire forcé "
            "pendant qu’il consulte son PMS risque d’exacerber l’agacement du client. L’analyse conjointe des vidéos de scène de l’eye tracker "
            "Neon et des codages faciaux permettra de mesurer la congruence émotionnelle des étudiants et d’évaluer si l’attention visuelle "
            "portée au client reflète une écoute empathique sincère ou une simple posture professionnelle stéréotypée."
        )
    },
    {
        "num": "Texte 16",
        "pilier": "Pilier 6 : Upselling & Pratiques Métier en Réception Hôtelière",
        "auteurs": "Ruki, M.",
        "annee": "2023",
        "titre": "Front Desk Personnel Qualities and Skills in Applying Upselling Hotel Products: Case Study of The Ritz-Carlton Bali",
        "revue": "Journal of Applied Sciences in Travel and Hospitality, 6(1), 32–41",
        "doi": "https://doi.org/10.31940/jasth.v6i1.32-41",
        "drive_file": "16 - Front Desk Personnel Qualities and Skills in Applying Upselling Hotel Products.pdf",
        "resume": (
            "Cette recherche appliquée analyse les compétences et qualités requises pour réussir l’upselling au front desk d’un établissement "
            "de luxe international (The Ritz-Carlton Bali). L’auteur démontre que l’efficacité commerciale des réceptionnistes repose sur "
            "un triptyque indissociable : la maîtrise rigoureuse des procédures opérationnelles et des standards de marque, l’aisance linguistique "
            "en anglais professionnel combinée à une communication persuasive non agressive, et une connaissance encyclopédique des produits "
            "hôteliers (différences précises entre suites, forfaits, options exclusives). L’upselling est conçu comme un service d’optimisation "
            "du séjour du voyageur."
        ),
        "contribution": (
            "Cet article ancre le projet SIMACCUEIL dans les réalités professionnelles de l’hôtellerie haut de gamme enseignée à la Haute École. "
            "Il définit les variables concrètes que le scénario simulé doit solliciter : la maîtrise des catégories de chambres, l’argumentation "
            "des suppléments et la fluidité linguistique. Les données de l’eye tracker permettront de corréler la maîtrise de ce référentiel "
            "métier avec l’organisation du regard : un réceptionniste hésitant sur les détails d’une suite passera trop de temps les yeux "
            "rivés sur son écran de réservation, manquant les indices d’hésitation ou d’accord sur le visage de son client."
        )
    },
    {
        "num": "Texte 17",
        "pilier": "Pilier 5 : Applications de l'Eye Tracking en Tourisme & Évaluation",
        "auteurs": "Scott, N., Zhang, R., Le, D., & Gao, J.",
        "annee": "2019",
        "titre": "A Review of Eye-Tracking Research in Tourism",
        "revue": "Annals of Tourism Research, 77, 102–114",
        "doi": "https://doi.org/10.1016/j.annals.2019.05.007",
        "drive_file": "17 - Scott_2017_Areviewofeyetrackingresearch.pdf",
        "resume": (
            "Cette revue systématique parue dans les Annals of Tourism Research dresse le bilan exhaustif de l’usage de l’oculométrie dans "
            "la recherche touristique et hôtelière. Les auteurs recensent les applications dominantes : perception des publicités, navigation "
            "sur les sites web de réservation hôtelière, choix de destinations et attention portée aux supports marketing physiques et "
            "digitaux. L’article relève toutefois un déséquilibre marquant : l’immense majorité des travaux s’est concentrée sur des écrans "
            "fixes en laboratoire, laissant quasi inexplorées les interactions humaines directes en milieu d’accueil réel."
        ),
        "contribution": (
            "Cette revue offre à SIMACCUEIL sa justification académique majeure : en déployant des lunettes d’eye tracking mobile de "
            "dernière génération (Pupil Labs Neon) pour étudier une interaction en face-à-face au comptoir d’accueil, le projet comble "
            "un manque empirique flagrant de la littérature touristique internationale. Scott et al. alertent en outre sur les précautions "
            "d’interprétation : une fixation longue n’est pas synonyme d’agrément. SIMACCUEIL s’inspire de ces recommandations pour trianguler "
            "systématiquement les données attentionnelles avec des entretiens rétrospectifs et des indicateurs de performance commerciale."
        )
    },
    {
        "num": "Texte 19",
        "pilier": "Pilier 5 : Applications de l'Eye Tracking en Tourisme & Évaluation",
        "auteurs": "Wolff, C. E., Jarodzka, H., van den Bogert, N., & Boshuizen, H. P.",
        "annee": "2016",
        "titre": "Teacher vision: Expert and novice teachers' perception of problematic classroom management scenes",
        "revue": "Instructional Science, 44(3), 243–265",
        "doi": "https://doi.org/10.1007/s11251-016-9367-z",
        "drive_file": "21 - Teacher vision expert and novice teachers’ perception.pdf",
        "resume": (
            "Cette recherche étudie comment l’expertise professionnelle façonne la vision et l’interprétation de situations incidentes "
            "complexes. En confrontant des enseignants experts et novices à des vidéos de classe perturbées, les auteurs démontrent "
            "que les experts effectuent un traitement holistique et contextualisé des événements : leurs fixations sont réparties "
            "stratégiquement sur l’ensemble du groupe, leurs verbalisations portent sur la signification sous-jacente des comportements, "
            "tandis que les novices restent piégés par des détails isolés et superficiels sans saisir la dynamique globale de la scène."
        ),
        "contribution": (
            "L’étude de Wolff et al. est directement transposable à l’interaction d’accueil hôtelier lors d’une gestion de réclamation ou "
            "d’un surclassement. Le réceptionniste expert surveille simultanément l’état de son PMS, le temps d’attente des autres voyageurs "
            "dans le lobby et les micro-attitudes de son interlocuteur. L’utilisation de l’oculométrie dans SIMACCUEIL permettra de vérifier "
            "si les étudiants expérimentés développent cette conscience périphérique globale ou s’ils souffrent d’une cécité attentionnelle "
            "focalisée sur leur écran d’ordinateur, guidant la conception d’exercices de simulation ciblés."
        )
    },
    {
        "num": "Texte 20",
        "pilier": "Pilier 5 : Applications de l'Eye Tracking en Tourisme & Évaluation",
        "auteurs": "Cortina, K. S., Miller, K. F., McKenzie, R., & Epstein, A.",
        "annee": "2015",
        "titre": "Where Low and High Inference Data Converge: Validation of CLASS Assessment of Mathematics Instruction Using Mobile Eye Tracking with Expert and Novice Teachers",
        "revue": "International Journal of Science and Mathematics Education, 13(2), 389–403",
        "doi": "https://doi.org/10.1007/s10763-014-9610-5",
        "drive_file": "20 - Where Low and High Inference Data Converge.pdf",
        "resume": (
            "Cette étude pionnière établit la passerelle méthodologique entre les mesures oculométriques mobiles (données à faible inférence, "
            "low-inference data, telles que la fréquence du regard vers les visages) et les grilles standardisées d’évaluation de la qualité "
            "pédagogique par des observateurs externes (données à forte inférence, high-inference data, via le protocole CLASS). Les résultats "
            "démontrent une convergence statistique étroite : les professionnels les mieux notés sur le plan qualitatif sont précisément ceux "
            "dont le regard alloue un temps supérieur aux élèves, validant l’oculométrie comme indicateur objectif d’engagement professionnel."
        ),
        "contribution": (
            "Pour SIMACCUEIL, Cortina et al. apportent la preuve méthodologique que des données biométriques objectives (temps de regard "
            "sur le client via les lunettes Neon) peuvent valider une grille d’évaluation qualitative de l’accueil hôtelier. Le projet pourra "
            "corréler les scores d’accueil attribués par les professeurs évaluateurs avec les indicateurs oculométriques réels. Cette triangulation "
            "évite tout biais de subjectivité dans l’appréciation des simulations et fournit aux étudiants des rétroactions chiffrées "
            "incontestables sur leur capacité réelle à maintenir le contact relationnel pendant la saisie d’une transaction d’upselling."
        )
    },
    {
        "num": "Texte 22",
        "pilier": "Pilier 5 : Applications de l'Eye Tracking en Tourisme & Évaluation",
        "auteurs": "Vickers, J. N.",
        "annee": "2016",
        "titre": "Origins and current issues in Quiet Eye research",
        "revue": "Current Issues in Sport Science (CISS), 1, 101",
        "doi": "https://doi.org/10.15203/CISS_2016.101",
        "drive_file": "22 - Origins and current issues in Quiet Eye research.pdf",
        "resume": (
            "Joan Vickers synthétise 25 années de recherche sur le Quiet Eye (QE), défini comme la dernière fixation ou le dernier suivi visuel "
            "stabilisé sur une zone critique avant le déclenchement d’une action motrice ou décisionnelle complexe. La méta-analyse montre "
            "que la durée du QE est en moyenne 62 % plus longue chez les experts que chez les novices. Cette stabilisation visuelle "
            "reflète le temps nécessaire aux circuits cérébraux pour organiser et programmer la réponse neuromotrice optimale, un entraînement "
            "ciblé au QE produisant des gains de performance spectaculaires."
        ),
        "contribution": (
            "Bien qu’issu du sport d’élite, le concept de Quiet Eye offre une hypothèse heuristique fascinante pour SIMACCUEIL : avant de "
            "formuler verbalement une offre d’upselling ou d’annoncer une solution à un client furieux, le réceptionniste expert stabilise-t-il "
            "son regard sur une zone clé (le total tarifaire ou le regard du client) pour finaliser son arbitrage ? L’analyse fine de la "
            "dernière fixation précédant la prise de parole critique permettra d’examiner si une pause attentionnelle stabilisée est associée "
            "à une persuasion accrue et à un meilleur contrôle émotionnel."
        )
    },
    {
        "num": "Texte 23",
        "pilier": "Pilier 5 : Applications de l'Eye Tracking en Tourisme & Évaluation",
        "auteurs": "Otterbring, T., Wästlund, E., Gustafsson, A., & Shams, P.",
        "annee": "2014",
        "titre": "Vision (im)possible? The effects of in-store signage on customers' visual attention",
        "revue": "Journal of Retailing and Consumer Services, 21(5), 676–684",
        "doi": "https://doi.org/10.1016/j.jretconser.2014.05.002",
        "drive_file": "23 - Vision (im)possible.pdf",
        "resume": (
            "Menée en conditions d’achat réelles au moyen d’eye trackers mobiles dans un supermarché, cette étude analyse l’impact de la "
            "signalétique commerciale sur l’attention visuelle des clients. Les résultats révèlent une profonde dépendance temporelle : "
            "l’attention portée aux panneaux promotionnels s’effondre dès que le client bascule dans une phase de recherche finalisée ou "
            "de décision d’achat ciblée. De plus, la familiarité avec l’environnement commercial réduit drastiquement l’exploration visuelle, "
            "les clients routiniers naviguant en pilotage automatique et ignorant les incitations visuelles non essentielles."
        ),
        "contribution": (
            "Cette étude de terrain offre un éclairage précieux pour la présentation des offres d’upselling dans SIMACCUEIL. Si un client "
            "arrive à la réception épuisé ou préoccupé par une réclamation (chambre sale), toute signalétique ou brochure posée sur le comptoir "
            "devient visuellement invisible. L’efficacité commerciale de l’upselling ne repose pas sur des supports passifs, mais sur la "
            "capacité du réceptionniste à introduire activement la tablette dans le champ visuel du client au moment opportun, synchronisant "
            "son regard avec l’argumentation orale pour capter son attention partagée."
        )
    },
    {
        "num": "Texte 24.b",
        "pilier": "Pilier 2 : Métrologie Oculométrique Mobile & Zones d'Intérêt (AOI)",
        "auteurs": "De Beugher, S., Brône, G., & Goedemé, T.",
        "annee": "2014",
        "titre": "Automatic Analysis of In-the-Wild Mobile Eye-Tracking Experiments using Object, Face and Person Detection",
        "revue": "VISAPP 2014 - Proceedings of the 9th International Conference on Computer Vision Theory and Applications, 725–732",
        "doi": "https://doi.org/10.5220/0004738507250732",
        "drive_file": "24.b - Automatic Analysis of In-the-Wild Mobile Eye-tracking Experiments.pdf",
        "resume": (
            "Cet article d’ingénierie logicielle propose un pipeline algorithmique d’automatisation du codage des données d’eye tracking "
            "mobile en environnement écologique non contrôlé. En combinant la vision par ordinateur, la détection de visages, d’objets "
            "spécifiques et de silhouettes humaines avec un lissage temporel probabiliste, les auteurs parviennent à convertir automatiquement "
            "les coordonnées de regard brutes en métriques sémantiques par zones d’intérêt dynamiques. Cette méthode réduit drastiquement "
            "le temps prohibitif requis par l’annotation manuelle image par image des vidéos oculométriques mobiles."
        ),
        "contribution": (
            "Ce texte résout le goulot d’étranglement méthodologique majeur auquel fait face le projet SIMACCUEIL. Dans une simulation "
            "d’accueil hôtelier mobile, l’annotation manuelle des vidéos Pupil Labs Neon (identifier si le regard se porte sur le client, "
            "l’écran ou la tablette) exigerait des centaines d’heures de codage. L’implémentation d’un pipeline de détection automatique "
            "des visages et des écrans, inspiré de De Beugher et al., permettra d’extraire automatiquement les temps de fixation et les "
            "transitions visuelles, rendant possible l’analyse à grande échelle des cohortes d’étudiants de l’HECh."
        )
    },
    {
        "num": "Texte 25",
        "pilier": "Pilier 6 : Upselling & Pratiques Métier en Réception Hôtelière",
        "auteurs": "Denizci Guillet, B.",
        "annee": "2020",
        "titre": "Online upselling: Moving beyond offline upselling in the hotel industry",
        "revue": "International Journal of Hospitality Management, 88, 102522",
        "doi": "https://doi.org/10.1016/j.ijhm.2020.102522",
        "drive_file": "25 - Online upselling Moving beyond offline upselling in the hotel industry.docx",
        "resume": (
            "Dans cette étude mixte parue dans l'IJHM, Bilgihan Denizci Guillet analyse l’articulation entre les programmes d’upselling en ligne "
            "(e-mails automatisés, pré-séjour) et les pratiques physiques d’upselling au front desk. L’auteure met en évidence une fragmentation "
            "nuisible des stratégies de revenue management : les réceptionnistes ignorent souvent les offres préalablement reçues ou refusées "
            "par le voyageur en ligne. L’article plaide pour un modèle omnicanal unifié, où les outils numériques de la réception complètent "
            "harmonieusement le parcours d’achat en personnalisant la proposition tarifaire selon les besoins immédiats du client."
        ),
        "contribution": (
            "Cet article fournit à SIMACCUEIL le scénario professionnel idéal pour concevoir les simulations d’upselling. Il invite à construire "
            "une situation d’accueil réaliste où le réceptionniste doit vérifier dans le PMS l’historique des propositions en ligne du client "
            "avant d’engager la négociation de surclassement en face-à-face. L’oculométrie permettra d’observer comment l’étudiant gère ce double "
            "défi : consulter les informations numériques en temps opportun tout en développant une posture commerciale persuasive et "
            "accueillante, sans rompre le lien de confiance lors du check-in."
        )
    }
]

def check_word_counts():
    print("=== VÉRIFICATION DU NOMBRE DE MOTS (OBJECTIF ~100 MOTS) ===")
    for a in ARTICLES:
        wc_res = len(a["resume"].split())
        wc_con = len(a["contribution"].split())
        print(f"{a['num']}: Résumé={wc_res} mots | Contribution={wc_con} mots")

if __name__ == "__main__":
    check_word_counts()
