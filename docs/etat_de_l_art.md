# État de l'Art Académique Approfondi : Oculométrie Mobile (Pupil Labs), Révélation des Savoirs Tacites et Dynamiques Attentionnelles en Situation Professionnelle

**Auteur :** Jérôme Foguenne (Projet de recherche Lab-DRA — Haute École Charlemagne [HECh] / Haute École de la Ville de Liège [HEL])  
**Date :** Octobre 2026 (Version Corpus Intégral — Dossier Ressources HECh)  
**Dépôt GitHub :** https://github.com/jeromefoguenne-eng/Eye-Tracking  

---

> [!IMPORTANT]
> **Règle de Rigueur Méthodologique :**  
> Conformément aux impératifs scientifiques du projet de recherche, cet état de l'art s'appuie **strictement et exclusivement** sur les **17 documents scientifiques** archivés dans le dossier des ressources de recherche (`C:\Google Drive\Prépas light\HECh\Projet recherche\Ressources`). Aucune référence bibliographique extérieure non validée dans ce corpus n'a été introduite.

---

## Table des Matières
1. [Introduction & Problématique de Recherche](#1-introduction--problématique-de-recherche)
2. [Volet 1 : Fondements Cognitifs, Expertise & Savoirs Tacites](#2-volet-1--fondements-cognitifs-expertise--savoirs-tacites)
   - 2.1 Charge cognitive et limites de traitement de l'information (Beckmann, 2010 - Ressource 01)
   - 2.2 Lois universelles du regard expert : la méta-analyse de Gegenfurtner et al. (2011 - Ressource 02)
   - 2.3 La « Vision Professionnelle » comme pratique située (Goodwin, 1994 - Ressource 04)
   - 2.4 L'Analyse Cognitive des Tâches (CTA) et le modèle NDM (Crandall, Klein & Hoffman, 2006 - Ressource 05)
   - 2.5 L'auto-confrontation enrichie par les traces dans le cours d'action (Theureau / Durand, 2016 - Ressource 07)
3. [Volet 2 : Méthodologie Oculométrique Mobile & Analyse Spatio-Temporelle](#3-volet-2--méthodologie-oculométrique-mobile--analyse-spatio-temporelle)
   - 3.1 Rigueur d'analyse des Zones d'Intérêt (AOI) : Hooge et al. (2026 - Ressource 08)
   - 3.2 Meilleures pratiques de l'oculométrie mobile écologique : Nolte et al. (2026 - Ressource 09.b)
   - 3.3 Évaluation technique de Pupil Labs Neon et pupillométrie physique : Pfeffer & Dierkes (2024 - Ressource 09.a)
4. [Volet 3 : Technopédagogie du Regard, Modélisation (EMME) & Protocoles Verbaux](#4-volet-3--technopédagogie-du-regard-modélisation-emme--protocoles-verbaux)
   - 4.1 Guidage attentionnel par la trace oculaire (EMME) : Van Gog et al. (2009 - Ressource 03)
   - 4.2 Transmission du raisonnement visuel professionnel : Jarodzka et al. (2012 - Ressource 10)
   - 4.3 Preuve expérimentale du transfert d'expertise : Seppänen & Gegenfurtner (2012 - Ressource 11)
   - 4.4 Supériorité de l'explicitation rétrospective guidée par le regard : Elling et al. (2012 - Ressource 06)
5. [Volet 4 : Dynamiques Sociales du Regard, Dual Eye Tracking & Interactions de Service / Upselling](#5-volet-4--dynamiques-sociales-du-regard-dual-eye-tracking--interactions-de-service--upselling)
   - 5.1 Analyse dyadique en face-à-face via le Dual Eye Tracking : Rogers et al. (2018 - Ressource 12)
   - 5.2 Montée et déclin de l'attention partagée en conversation : Wohltjen & Wheatley (2021 - Ressource 13)
   - 5.3 Établissement du rapport interpersonnel et corrélats non verbaux : Tickle-Degnen & Rosenthal (1990 - Ressource 14)
   - 5.4 Travail émotionnel, authenticité du sourire et contagion affective : Hennig-Thurau et al. (2006 - Ressources 15.a & 15.b)
   - 5.5 Compétences terrain et qualités des réceptionnistes dans l'upselling hôtelier : Setyorini & Putra (2023 - Ressource 16)
   - 5.6 État de l'art de l'oculométrie dans l'hôtellerie et le tourisme : Scott et al. (2017/2019 - Ressource 17)
6. [Fiches de Lecture Analytiques : Les 17 Ressources Fondamentales](#6-fiches-de-lecture-analytiques--les-17-ressources-fondamentales)
7. [Bibliographie Complète (Normes APA 7 - Corpus Exclusif)](#7-bibliographie-complète-normes-apa-7---corpus-exclusif)

---

## 1. Introduction & Problématique de Recherche

Dans le secteur de l'accueil, de la gestion hôtelière et du tourisme, le comptoir d'enregistrement (*front desk*) représente le point névralgique de la rencontre de service. C'est à ce carrefour relationnel que le personnel doit synchroniser deux impératifs hautement exigeants :
1. **L'excellence relationnelle et l'hospitalité :** accueillir le client avec bienveillance, capter ses attentes implicites, instaurer un climat de confiance et traiter les demandes spécifiques.
2. **La performance commerciale et le Revenue Management :** saisir les opportunités de valorisation du séjour via la montée en gamme (*upselling* de chambre, vue, suite) ou la recommandation de prestations périphériques (*cross-selling* de restauration, spa, départs tardifs) (Setyorini & Putra, 2023 ; Scott et al., 2017/2019).

L'analyse traditionnelle de ces interactions a longtemps été limitée par des dispositifs méthodologiques déclaratifs (questionnaires post-séjour) ou des enregistrements vidéo externes à la troisième personne. Ces démarches ne permettent pas d'accéder au flux attentionnel direct de l'opérateur ni d'objectiver comment le regard oscille en temps réel entre le visage du client, l'écran de gestion hôtelière (PMS) et les supports d'aide à la vente.

L'introduction de l'**oculométrie mobile portable (*wearable mobile eye tracking*)**, incarnée par les lunettes **Pupil Labs Neon** (Pfeffer & Dierkes, 2024 ; Nolte et al., 2026), apporte une rupture méthodologique décisive. En échantillonnant le regard à 200 Hz dans un cadre écologique non contraignant, le système permet de révéler les « savoirs cachés » de l'expertise (Crandall, Klein & Hoffman, 2006 ; Goodwin, 1994) et de comprendre l'architecture cognitive des praticiens de l'accueil.

---

## 2. Volet 1 : Fondements Cognitifs, Expertise & Savoirs Tacites

### 2.1 Charge cognitive et limites de traitement de l'information (Beckmann, 2010 - Ressource 01)
Dans son analyse critique de la théorie de la charge cognitive (CLT), Jens F. Beckmann (2010) réexamine les postulats traditionnels sur les charges intrinsèque, extrinsèque et essentielle. Il démontre que la charge cognitive ne peut se résumer à la simple interactivité d'éléments abstraits : elle résulte d'une dialectique étroite entre la complexité structurale de la tâche et les capacités de traitement de l'individu.
* **Transposition à l'accueil hôtelier :** La tâche de check-in impose une double charge : traiter des données alphanumériques complexes sur le logiciel PMS (charge liée à l'outil) tout en maintenant une communication fluide et empathique avec le client (charge relationnelle). Chez le novice, cette complexité sature la mémoire de travail, induisant le « piège de l'écran » (regard fixé à plus de 70% sur le moniteur). L'expert, grâce à l'automatisation de ses routines cognitives, comprime cette charge mentale et préserve ses capacités attentionnelles pour l'interaction humaine.

### 2.2 Lois universelles du regard expert : la méta-analyse de Gegenfurtner et al. (2011 - Ressource 02)
La méta-analyse pionnière conduite par Gegenfurtner, Lehtinen et Säljö (2011) synthétise les données oculométriques comparant experts et novices dans divers domaines professionnels. Les auteurs établissent trois invariants de l'expertise visuelle :
* **Filtrage des redondances :** Les experts consacrent significativement moins de fixations et un temps de séjour réduit aux zones non informatives ou redondantes.
* **Rapidité de détection des indices critiques :** Le délai précédant la première fixation sur les éléments pertinents est drastiquement plus court chez les experts.
* **Encodage approfondi :** Leurs fixations sur les zones cibles sont plus stables, reflétant une interprétation sémantique immédiate conforme à leurs schémas de connaissances.

### 2.3 La « Vision Professionnelle » comme pratique située (Goodwin, 1994 - Ressource 04)
Charles Goodwin (1994) théorise la « vision professionnelle » (*Professional Vision*) comme une compétence culturellement construite et socialement située au sein d'une communauté de pratique. Goodwin démontre que voir n'est pas un acte biologique passif, mais une pratique active articulée en trois processus :
1. **Le codage perceptuel (*Coding*) :** Transformer le flux continu du réel en catégories professionnelles signifiantes.
2. **La mise en relief (*Highlighting*) :** Orienter délibérément l'attention sur des détails spécifiques pour les rendre saillants.
3. **La production et l'usage de représentations matérielles (*Graphic representations*) :** Intégrer des artefacts tangibles dans l'activité.
Dans notre contexte, le réceptionniste expert mobilise sa vision professionnelle pour décoder en une fraction de seconde la posture, la fatigue ou la réceptivité du client et synchroniser sa présentation des options de surclassement.

### 2.4 L'Analyse Cognitive des Tâches (CTA) et le modèle NDM (Crandall, Klein & Hoffman, 2006 - Ressource 05)
L'ouvrage fondamental de Crandall, Klein et Hoffman (2006) formalise la méthodologie de l'Analyse Cognitive des Tâches (CTA) ancrée dans le courant du *Naturalistic Decision Making* (NDM). Les auteurs démontrent que dans les environnements dynamiques, les experts ne comparent pas exhaustivement des listes d'options, mais reconnaissent des situations typiques (*Recognition-Primed Decision* - RPD) et appliquent intuitivement des lignes d'action plausibles.
* **Le paradoxe de l'expertise :** Plus un individu développe son expertise, plus ses connaissances deviennent tacites et inaccessibles à l'auto-évaluation verbale classique. L'enregistrement oculométrique résout ce verrou méthodologique : la vidéo du regard sert d'ancrage mnésique objectif (*cued-recall*) pour guider l'entretien de décision critique (CDM) et expliciter les modèles mentaux sous-jacents.

### 2.5 L'auto-confrontation enrichie par les traces dans le cours d'action (Theureau / Durand, 2016 - Ressource 07)
Issu de l'ergonomie cognitive francophone, le cadre théorique du cours d'action (Theureau, 2016 ; Durand, 2016) appréhende l'activité comme une én-action, indissociable du sens vécu par l'acteur en situation réelle. Pour documenter la part pré-réflexive de l'action, l'entretien d'auto-confrontation place le professionnel devant les traces extrinsèques de son activité. Le flux vidéo oculaire mobile constitue la trace extrinsèque par excellence : le praticien ne peut rationaliser artificiellement son comportement a posteriori ; il est amené à expliciter pourquoi son regard a bifurqué vers un indice précis, révélant la dynamique temporelle de ses préoccupations.

---

## 3. Volet 2 : Méthodologie Oculométrique Mobile & Analyse Spatio-Temporelle

### 3.1 Rigueur d'analyse des Zones d'Intérêt (AOI) : Hooge et al. (2026 - Ressource 08)
L'analyse scientifique des enregistrements oculométriques requiert une rigueur statistique absolue dans la segmentation des Zones d'Intérêt (AOI). Hooge et al. (2026) mettent en évidence les écueils récurrents dans la littérature : frontières d'AOI trop étroites ignorant l'imprécision du signal, mauvaise gestion des cibles mobiles et dérives d'échantillonnage.
* **Standardisation au Lab-DRA :** En suivant les préconisations de Hooge et al. (2026), quatre AOI dynamiques majeures sont délimitées avec marges de tolérance adaptées :
  1. *AOI_Client_Face* : Visage et regard de l'interlocuteur.
  2. *AOI_PMS_Screen* : Écran du logiciel hôtelier.
  3. *AOI_Physical_Collateral* : Dépliant, brochure ou support visuel de présentation des chambres supérieures.
  4. *AOI_Terminal_Keys* : Clavier, terminal de paiement ou clé de chambre.

### 3.2 Meilleures pratiques de l'oculométrie mobile écologique : Nolte et al. (2026 - Ressource 09.b)
Le déploiement de lunettes d'eye tracking dans des environnements naturels (« in the wild ») impose des contraintes méthodologiques strictes documentées par Nolte et al. (2026) :
* **Contrôle de la parallaxe :** Ajustement de la distance de travail entre l'opérateur et le comptoir pour compenser le décalage optique entre la caméra de scène et les capteurs oculaires.
* **Gestion du slippage :** Vérification de la stabilité mécanique de la monture lors des mouvements de tête spontanés.
* **Éclairage ambiant :** Maîtrise de la luminosité pour éviter les reflets parasites sur les cornées et garantir une segmentation pupillaire optimale.

### 3.3 Évaluation technique de Pupil Labs Neon et pupillométrie physique : Pfeffer & Dierkes (2024 - Ressource 09.a)
Le rapport technique de Pfeffer et Dierkes (2024) documente la validité du système Pupil Labs Neon :
* **Architecture NeonNet :** Grâce à un réseau de neurones convolutif embarqué, Neon supprime l'étape fastidieuse de calibration manuelle utilisateur tout en échantillonnant à 200 Hz. L'appareil est robuste aux mouvements et déplacements de monture.
* **Pupillométrie absolue (mm) :** Neon calcule en continu le diamètre physique de la pupille en millimètres, débarrassé des artefacts d'angle oculaire. Cette mesure objective permet de suivre en temps réel la dilatation pupillaire, indice physiologique direct de l'intensité de la charge cognitive et de l'activation émotionnelle lors des moments de négociation commerciale.

---

## 4. Volet 3 : Technopédagogie du Regard, Modélisation (EMME) & Protocoles Verbaux

### 4.1 Guidage attentionnel par la trace oculaire (EMME) : Van Gog et al. (2009 - Ressource 03)
Les travaux fondateurs de Tamara Van Gog, Halszka Jarodzka et leurs collègues (2009) démontrent l'efficacité des Exemples Modélisants du Regard (*Eye Movement Modeling Examples* - EMME). En superposant le point de regard mobile d'un expert sur un enregistrement vidéo, le dispositif guide directement le faisceau attentionnel des étudiants vers les zones pertinentes. Cette focalisation visuelle réduit les tâtonnements perceptifs des novices et accélère l'acquisition des compétences procédurales.

### 4.2 Transmission du raisonnement visuel professionnel : Jarodzka et al. (2012 - Ressource 10)
Jarodzka et ses collaborateurs (2012) appliquent les EMME à la transmission du raisonnement visuel complexe. Les auteurs prouvent que combiner la trace oculaire experte avec des explications verbales adaptées permet aux apprenants de comprendre non seulement *où* regarder, mais également *pourquoi* regarder à cet endroit précis. Les apprenants s'approprient ainsi les heuristiques d'investigation de l'expert, développant un modèle mental supérieur de la tâche.

### 4.3 Preuve expérimentale du transfert d'expertise : Seppänen & Gegenfurtner (2012 - Ressource 11)
Dans leur étude expérimentale « Seeing through a teacher's eyes », Seppänen et Gegenfurtner (2012 dans *Medical Education*) apportent la preuve du transfert : les étudiants ayant visionné les mouvements oculaires enregistrés d'un tuteur obtiennent des scores de précision significativement plus élevés que le groupe contrôle. Leurs propres trajectoires oculaires enregistrées par eye tracking révèlent une augmentation massive des fixations sur les zones cibles et une quasi-disparition des fixations sur les zones redondantes.

### 4.4 Supériorité de l'explicitation rétrospective guidée par le regard : Elling et al. (2012 - Ressource 06)
Sanne Elling, Leo Lentz et Menno de Jong (2012) démontrent la supériorité méthodologique du protocole de verbalisation rétrospective guidée par la trace oculaire (*Gaze-Cued Retrospective Think-Aloud* - RTA) sur la verbalisation simultanée (*concurrent think-aloud*). Demander à un participant de commenter ses actions en direct lors d'une interaction de service crée une surcharge cognitive artificielle et modifie son comportement relationnel. Le protocole Gaze-Cued RTA, en confrontant le sujet à son enregistrement silencieux enrichi de son tracé oculaire, permet une explicitation métacognitive approfondie sans altérer la fidélité de la tâche initiale.

---

## 5. Volet 4 : Dynamiques Sociales du Regard, Dual Eye Tracking & Interactions de Service / Upselling

### 5.1 Analyse dyadique en face-à-face via le Dual Eye Tracking : Rogers et al. (2018 - Ressource 12)
L'article pionnier de Shane L. Rogers et al. (2018 dans *Scientific Reports*) pose les bases du *Dual Eye Tracking* en situation d'échange social en face-à-face. Les auteurs démontrent que le contact visuel direct mutuel (*mutual gaze*) n'occupe qu'une fraction ciblée du temps de communication globale, mais joue un rôle fondamental de synchronisation sociale et de distribution des tours de parole (*turn-taking*). Cette approche permet de cartographier la coordination visuelle entre le réceptionniste et le client au comptoir.

### 5.2 Montée et déclin de l'attention partagée en conversation : Wohltjen & Wheatley (2021 - Ressource 13)
Publiée dans les *Proceedings of the National Academy of Sciences* (PNAS), l'étude de Sophie Wohltjen et Thalia Wheatley (2021) met en évidence le cycle naturel de l'attention partagée (*shared attention*) :
* Le contact visuel mutuel monte en puissance jusqu'à marquer l'acmé de la connexion interpersonnelle.
* Une fois ce pic de synchronie atteint, les partenaires détournent spontanément le regard pour traiter cognitivement les informations reçues et désaturer leur mémoire de travail.
* **Application directe à l'upselling :** Le réceptionniste expert capte le regard du client pour affirmer la valeur d'une chambre supérieure, puis détourne délibérément son regard vers la documentation ou le comptoir pour accorder au voyageur le temps cognitif nécessaire à son choix sans instaurer de pression anxiogène.

### 5.3 Établissement du rapport interpersonnel et corrélats non verbaux : Tickle-Degnen & Rosenthal (1990 - Ressource 14)
Tickle-Degnen et Rosenthal (1990) modélisent le rapport interpersonnel autour de trois piliers non verbaux :
1. **L'attention mutuelle (*Mutual Attentiveness*) :** Soutenue prioritairement par l'orientation du regard et du corps.
2. **La positivité (*Positivity*) :** Chaleur de l'expression faciale et du ton.
3. **La coordination (*Coordination*) :** Synchronisation rythmique des échanges.
Dans le parcours client, l'attention mutuelle doit être consolidée dès les premières secondes de l'accueil ; sans cet ancrage visuel initial, toute offre commerciale ultérieure (surclassement) est perçue comme intrusive et subit un taux de rejet massif.

### 5.4 Travail émotionnel, authenticité du sourire et contagion affective : Hennig-Thurau et al. (2006 - Ressources 15.a & 15.b)
Dans le *Journal of Marketing*, Thorsten Hennig-Thurau et ses co-auteurs (2006) analysent la contagion émotionnelle dans les relations de service. Ils démontrent que les consommateurs distinguent sans ambiguïté :
* Le **« jeu de surface » (*Surface Acting*) :** Sourire de façade forcé, où le regard reste fuyant ou absorbé par les outils administratifs.
* Le **« jeu en profondeur » (*Deep Acting*) :** Empathie sincère, où le contact visuel est engagé et congruent avec l'expression faciale.
Seul le jeu en profondeur déclenche une contagion émotionnelle positive, maximisant la satisfaction globale, renforçant la fidélisation et augmentant la propension du client à accepter une montée en gamme.

### 5.5 Compétences terrain et qualités des réceptionnistes dans l'upselling hôtelier : Setyorini & Putra (2023 - Ressource 16)
L'étude qualitative de Setyorini et Putra (2023) menée au sein d'un complexe hôtelier de luxe analyse les qualités des réceptionnistes performants lors de l'upselling :
* Maîtrise parfaite des caractéristiques produit de chaque catégorie de chambre.
* Capacité à cadrer l'offre en termes de bénéfices expérientiels (confort, vue panoramique, calme) plutôt qu'en supplément financier arithmétique.
* Intelligence de situation et aisance relationnelle non verbale pour surmonter l'appréhension du rejet commercial. L'expert n'impose pas, il conseille opportunément.

### 5.6 État de l'art de l'oculométrie dans l'hôtellerie et le tourisme : Scott et al. (2017/2019 - Ressource 17)
Dans leur revue systématique parue dans *Current Issues in Tourism*, Noel Scott et ses co-auteurs (2017/2019) synthétisent l'apport de l'eye tracking dans le tourisme. Les auteurs constatent que la majorité des travaux s'est concentrée sur des écrans d'ordinateurs fixes (publicités, sites de réservation) et appellent la communauté scientifique à investir les interactions physiques en présentiel grâce à l'oculométrie portable. Notre projet Lab-DRA répond à cette invitation en déployant Pupil Labs Neon directement dans l'interaction de comptoir.

---

## 6. Fiches de Lecture Analytiques : Les 17 Ressources Fondamentales

### ■ Pilier 1 : Fondements Cognitifs, Expertise, Vision Professionnelle & Savoirs Tacites

#### FICHE RESSOURCE 01 : Beckmann, J. F. (2010)
* **Titre :** *Taming a beast of burden – On some issues with the conceptualisation and operationalisation of cognitive load*
* **Revue / Source :** Learning and Instruction, 20(3), 250–264 | [DOI: 10.1016/j.learninstruc.2009.02.024](https://doi.org/10.1016/j.learninstruc.2009.02.024)
* **Résumé analytique & Portée pour le projet :** Cet article fondamental réexamine les postulats de la Cognitive Load Theory (CLT) et la distinction tripartite entre charge cognitive intrinsèque, extrinsèque et essentielle. L'auteur propose un cadre fondé sur la complexité pour dépasser la simple notion d'interactivité des éléments et dériver des estimations a priori de la charge mentale. L'étude empirique montre que la capacité individuelle de traitement détermine la mesure dans laquelle la complexité d'une tâche se traduit en surcharge cognitive. Dans le cadre de notre projet, cette recherche éclaire comment le multitâche au comptoir d'accueil (gérer le client tout en consultant le logiciel hôtelier) sature les ressources attentionnelles des novices, tandis que l'expertise permet de comprimer cette charge.

#### FICHE RESSOURCE 02 : Gegenfurtner, A., Lehtinen, E., & Säljö, R. (2011)
* **Titre :** *Expertise differences in the comprehension of visualizations: A meta-analysis of eye-tracking research in professional domains*
* **Revue / Source :** Educational Psychology Review, 23(4), 523–552 | [DOI: 10.1007/s10648-011-9174-7](https://doi.org/10.1007/s10648-011-9174-7)
* **Résumé analytique & Portée pour le projet :** Cette méta-analyse majeure synthétise des dizaines d'études comparant experts et novices à travers l'oculométrie dans divers contextes professionnels. Les résultats confirment trois lois universelles de l'expertise visuelle : les experts effectuent des fixations significativement plus courtes sur les zones redondantes, identifient les informations critiques beaucoup plus rapidement (temps de première fixation réduit), et présentent une plus grande flexibilité attentionnelle face aux imprévus. L'article démontre que les compétences incorporées d'un métier reposent sur des schémas perceptifs automatisés que l'eye tracking permet d'objectiver mathématiquement.

#### FICHE RESSOURCE 04 : Goodwin, C. (1994)
* **Titre :** *Professional Vision*
* **Revue / Source :** American Anthropologist, 96(3), 606–633 | [DOI: 10.1525/aa.1994.96.3.02a00100](https://doi.org/10.1525/aa.1994.96.3.02a00100)
* **Résumé analytique & Portée pour le projet :** Théorie séminale de la « vision professionnelle », cet article d'anthropologie cognitive démontre comment les membres d'une communauté de pratique apprennent à percevoir le monde selon des schémas socialement situés. Goodwin décompose l'expertise visuelle en trois pratiques : le codage (catégorisation perceptuelle), la mise en relief (highlighting, focalisation sur les indices saillants) et l'usage de représentations matérielles. Appliqué à l'accueil hôtelier, ce cadre explique comment le professionnel expert « lit » instantanément les indices non verbaux du client et les opportunités de surclassement, là où le novice ne perçoit qu'une situation administrative d'enregistrement standard.

#### FICHE RESSOURCE 05 : Crandall, B., Klein, G. A., & Hoffman, R. R. (2006)
* **Titre :** *Working Minds: A Practitioner's Guide to Cognitive Task Analysis*
* **Revue / Source :** The MIT Press, Cambridge, MA | [DOI: 10.7551/mitpress/7304.001.0001](https://doi.org/10.7551/mitpress/7304.001.0001)
* **Résumé analytique & Portée pour le projet :** Ouvrage de référence internationale sur l'Analyse Cognitive des Tâches (Cognitive Task Analysis - CTA) et le Naturalistic Decision Making (NDM). Les auteurs fournissent les protocoles rigoureux (Critical Decision Method - CDM, Knowledge Audit, Concept Mapping) permettant d'extraire les connaissances tacites d'experts confrontés à des situations critiques et dynamiques. Couplée à l'oculométrie mobile moderne, la démarche CTA permet de surmonter le paradoxe de l'expertise (plus un professionnel est compétent, plus ses schémas sont automatisés et moins il est capable de les expliquer). L'enregistrement oculaire sert de support de remémoration (cued-recall) pour documenter la détection de micro-indices, les modèles mentaux et les décisions adaptatives.

#### FICHE RESSOURCE 07 : Theureau, J. (2016) / Durand, M. (2016)
* **Titre :** *Le cours d'action. L'enaction et l'expérience / L'analyse de l'activité et l'entretien d'auto-confrontation enrichi par les traces*
* **Revue / Source :** Activités, 13(1), Recension et prolongements théoriques | [DOI: 10.4000/activites.2769](https://doi.org/10.4000/activites.2769)
* **Résumé analytique & Portée pour le projet :** Issu de l'ergonomie cognitive et de l'approche du cours d'action, ce cadre théorise l'entretien d'auto-confrontation. Un professionnel est confronté aux traces extrinsèques audiovisuelles de sa propre pratique pour documenter la dynamique de son expérience vécue et faire émerger les savoirs incorporés pré-réflexifs. Couplée à l'oculométrie mobile de dernière génération, la trace du regard agit comme un déclencheur mnésique exceptionnel : l'acteur est invité à expliciter le sens de ses réorientations visuelles au cours de l'interaction de service, révélant la rationalité sous-jacente de ses arbitrages relationnels.

---

### ■ Pilier 2 : Méthodologie Oculométrique, Métriques & Dispositifs Mobiles

#### FICHE RESSOURCE 08 : Hooge, I. T. C., Nyström, M., Niehorster, D. C., Andersson, R., Foulsham, T., Nuthmann, A., & Hessels, R. S. (2026)
* **Titre :** *The fundamentals of eye tracking part 6: Working with areas of interest*
* **Revue / Source :** Behavior Research Methods, 58(3) | [DOI: 10.3758/s13428-025-02598-6](https://doi.org/10.3758/s13428-025-02598-6)
* **Résumé analytique & Portée pour le projet :** Cet article méthodologique fondamental de la série internationale sur l'oculométrie établit les règles d'or et les standards méthodologiques pour l'utilisation des Zones d'Intérêt (Areas of Interest - AOI). Les auteurs examinent les pièges de délimitation spatiale, l'impact des imprécisions de pointage et la gestion des AOI dynamiques dans les environnements réels. Dans notre projet de simulation d'accueil, cette publication fournit la rigueur statistique indispensable pour découper et analyser les AOI clés : visage du client, écran du logiciel PMS, terminal de paiement et documents promotionnels de surclassement.

#### FICHE RESSOURCE 09.a : Pfeffer, T., & Dierkes, K. (2024)
* **Titre :** *Neon Pupillometry Test Report: An evaluation of Neon's pupillometry feature*
* **Revue / Source :** Pupil Labs GmbH Technical Report | [Rapport Technique Pupil Labs](https://pupil-labs.com/products/neon/)
* **Résumé analytique & Portée pour le projet :** Rapport technique d'évaluation du système d'oculométrie mobile Pupil Labs Neon. Les auteurs documentent les performances de l'architecture NeonNet (réseau de neurones profond embarqué fonctionnant sans calibration utilisateur manuelle à 200 Hz). Ils démontrent la fiabilité de la pupillométrie physique (mesure absolue du diamètre pupillaire en millimètres, corrigée des distorsions d'angle). Cet outil permet de sonder en temps réel non seulement l'orientation spatiale du regard, mais également les variations physiologiques de la charge mentale et de l'éveil émotionnel lors des phases sensibles de négociation.

#### FICHE RESSOURCE 09.b : Nolte, D., Walter, J. L., von Bassewitz, L., et al. (2026)
* **Titre :** *Mobile eye tracking in the real world: Best practices*
* **Revue / Source :** Journal of Vision, 26(2):6, 1–22 | [DOI: 10.1167/jov.26.2.6](https://doi.org/10.1167/jov.26.2.6)
* **Résumé analytique & Portée pour le projet :** Ce guide international de référence détaille les meilleures pratiques pour conduire des recherches en oculométrie mobile dans des contextes réels non contraints (« in the wild »). Les auteurs abordent la gestion des variations de luminosité, les mouvements de tête, les glissements mécaniques de la monture et l'alignement des flux de données avec les vidéos de scène. Ce texte constitue le socle procédural garantissant la validité écologique et la reproductibilité des enregistrements réalisés au comptoir d'accueil hôtelier du Lab-DRA.

---

### ■ Pilier 3 : Didactique de l'Expertise Visuelle, EMME & Protocoles Verbaux

#### FICHE RESSOURCE 03 : Van Gog, T., Jarodzka, H., Scheiter, K., Gerjets, P., & Paas, F. (2009)
* **Titre :** *Attention guidance during example study via the model's eye movements*
* **Revue / Source :** Computers in Human Behavior, 25(3), 785–794 | [DOI: 10.1016/j.chb.2009.02.002](https://doi.org/10.1016/j.chb.2009.02.002)
* **Résumé analytique & Portée pour le projet :** Les auteurs introduisent la méthodologie pionnière des EMME (Eye Movement Modeling Examples). En enregistrant le parcours oculaire d'un modèle expert et en le superposant sur la vidéo visionnée par les apprenants, on guide directement leur attention sur les zones stratégiques de la tâche. Combinée au protocole de verbalisation rétrospective guidée par le regard, cette technique permet d'accélérer l'apprentissage en matérialisant visuellement les prises de décision implicites qui échappent aux explications verbales traditionnelles.

#### FICHE RESSOURCE 06 : Elling, S., Lentz, L., & de Jong, M. (2012)
* **Titre :** *Combining concurrent think-aloud protocols and eye-tracking observations: An analysis of verbalizations and silences*
* **Revue / Source :** IEEE Transactions on Professional Communication, 55(3), 206–218 | [DOI: 10.1109/TPC.2012.2206190](https://doi.org/10.1109/TPC.2012.2206190)
* **Résumé analytique & Portée pour le projet :** Cette étude méthodologique rigoureuse compare l'impact de la réflexion à voix haute simultanée (concurrent think-aloud) et des protocoles rétrospectifs couplés à l'eye tracking. Les auteurs démontrent que verbaliser en temps réel pendant une tâche interactive induit une surcharge cognitive et modifie artificiellement le comportement naturel de l'opérateur. En revanche, le protocole rétrospectif guidé par la trace oculaire (gaze-cued RTA) préserve l'authenticité de l'interaction et génère des verbalisations réflexives d'une grande profondeur sur les silences et les fixations clés.

#### FICHE RESSOURCE 10 : Jarodzka, H., Balslev, T., Holmqvist, K., Nyström, M., Scheiter, K., Gerjets, P., & Eika, B. (2012)
* **Titre :** *Conveying clinical reasoning based on visual observation via eye-movement modelling examples*
* **Revue / Source :** Teaching and Learning in Medicine / Instructional Science | [DOI: 10.1080/10401334.2012.692283](https://doi.org/10.1080/10401334.2012.692283)
* **Résumé analytique & Portée pour le projet :** Cette recherche empirique démontre l'efficacité des exemples modélisants du regard (EMME) pour transmettre des compétences de raisonnement complexes fondées sur l'observation visuelle. En visionnant la trajectoire oculaire de l'expert synchronisée avec ses commentaires pédagogiques, les apprenants améliorent considérablement leur précision diagnostique et adoptent des stratégies de balayage visuel calquées sur celles de l'expert. Ce dispositif valide le modèle de transfert pour l'hôtellerie : visionner la trajectoire du regard d'un réceptionniste expert permet aux étudiants d'intérioriser le tempo attentionnel nécessaire à la relation client.

#### FICHE RESSOURCE 11 : Seppänen, M., & Gegenfurtner, A. (2012)
* **Titre :** *Seeing through a teacher's eyes improves students' imaging interpretation*
* **Revue / Source :** Medical Education, 46(11), 1113–1114 | [DOI: 10.1111/medu.12041](https://doi.org/10.1111/medu.12041)
* **Résumé analytique & Portée pour le projet :** Publiée dans Medical Education, cette étude quasi-expérimentale teste l'impact du visionnage des mouvements oculaires d'un enseignant (« seeing through a teacher's eyes »). Les résultats démontrent que les apprenants du groupe expérimental améliorent significativement leur exactitude et leur sensibilité de diagnostic par rapport au groupe témoin. Leurs propres trajectoires oculaires montrent une augmentation marquée des fixations sur les zones pertinentes de la tâche et une diminution des fixations sur les zones redondantes. Cela confirme la puissance pédagogique du rejeu oculaire pour restructurer la perception des apprenants.

---

### ■ Pilier 4 : Dynamique Sociale du Regard, Dual Eye Tracking & Interactions de Service / Upselling

#### FICHE RESSOURCE 12 : Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M. (2018)
* **Titre :** *Using dual eye tracking to uncover personal gaze patterns during social interaction*
* **Revue / Source :** Scientific Reports, 8, Article 4271 | [DOI: 10.1038/s41598-018-22726-7](https://doi.org/10.1038/s41598-018-22726-7)
* **Résumé analytique & Portée pour le projet :** Cet article pionnier explore le Dual Eye Tracking (enregistrement simultané et synchronisé de deux participants lors d'une interaction face-à-face). Les auteurs quantifient les schémas de regard individuel et montrent que le contact visuel mutuel direct ne représente qu'une fraction ciblée du temps de parole, servant de régulateur clé des prises de tour (turn-taking) et de la coordination dyadique. Cette méthodologie fournit la matrice analytique pour mesurer comment un réceptionniste et un client synchronisent leurs regards autour des offres commerciales.

#### FICHE RESSOURCE 13 : Wohltjen, S., & Wheatley, T. (2021)
* **Titre :** *Eye contact marks the rise and fall of shared attention in conversation*
* **Revue / Source :** Proceedings of the National Academy of Sciences (PNAS), 118(37), e2106499118 | [DOI: 10.1073/pnas.2106499118](https://doi.org/10.1073/pnas.2106499118)
* **Résumé analytique & Portée pour le projet :** Publiée dans PNAS, cette recherche démontre que le contact oculaire agit comme un interrupteur dynamique de l'attention partagée (shared attention). Le contact visuel mutuel s'intensifie jusqu'à ce que la synchronie conversationnelle atteigne son pic, après quoi les interlocuteurs détournent spontanément le regard pour traiter cognitivement les informations et réguler leur charge mentale. Ce mécanisme neurocognitif est crucial pour l'upselling : le réceptionniste expert sait exactement quand capter le regard du client pour soutenir sa proposition, puis quand le détourner vers un support matériel pour lui laisser l'espace de délibération.

#### FICHE RESSOURCE 14 : Tickle-Degnen, L., & Rosenthal, R. (1990)
* **Titre :** *The Nature of Rapport and Its Nonverbal Correlates*
* **Revue / Source :** Psychological Inquiry, 1(4), 285–293 | [DOI: 10.1207/s15327965pli0104_1](https://doi.org/10.1207/s15327965pli0104_1)
* **Résumé analytique & Portée pour le projet :** Théorie majeure du « rapport interpersonnel », cet article postule que la connexion relationnelle réussie repose sur trois composantes non verbales dynamiques : l'attention mutuelle (mutual attentiveness), la positivité (positivity) et la coordination posturale/rythmique (coordination). Le regard y est identifié comme le levier central de l'attention mutuelle. Au comptoir d'accueil, l'établissement précoce de ce rapport est la condition préalable indispensable pour qu'une proposition de surclassement soit perçue comme un conseil personnalisé plutôt que comme une intrusion commerciale.

#### FICHE RESSOURCE 15 : Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D. (2006)
* **Titre :** *Are All Smiles Created Equal? How Emotional Contagion and Emotional Labor Affect Service Encounters*
* **Revue / Source :** Journal of Marketing, 70(3), 58–73 | [DOI: 10.1509/jmkg.70.3.058](https://doi.org/10.1509/jmkg.70.3.058)
* **Résumé analytique & Portée pour le projet :** Étude fondamentale en marketing des services sur la contagion émotionnelle et le travail émotionnel. Les auteurs démontrent que les clients perçoivent avec acuité la différence entre un sourire forcé (« jeu de surface » / surface acting) et un engagement relationnel authentique (« jeu en profondeur » / deep acting). La congruence du regard et la stabilité attentionnelle sont des marqueurs cruciaux d'authenticité. Un professionnel dont le regard reste rivé à son écran informatique trahit un manque d'engagement, ce qui dégrade la confiance et réduit drastiquement les chances de succès des initiatives d'upselling.

#### FICHE RESSOURCE 16 : Setyorini, A., & Putra, I. (2023)
* **Titre :** *Front Desk Personnel Qualities and Skills in Applying Upselling Hotel Products: Case Study of the Ritz Carlton Bali*
* **Revue / Source :** International Journal of Multicultural and Multireligious Understanding, 10(4), 550–558 | [DOI: 10.18415/ijmmu.v10i4.4646](https://doi.org/10.18415/ijmmu.v10i4.4646)
* **Résumé analytique & Portée pour le projet :** Cette étude de terrain qualitative analyse les compétences requises pour réussir l'upselling hôtelier en situation réelle de check-in. Les auteurs identifient trois facteurs de réussite : la parfaite maîtrise de l'inventaire des chambres, le cadrage tarifaire axé sur la valeur de l'expérience plutôt que sur le surcoût brut, et l'intelligence de situation (communication non verbale, observation de la fatigue ou des besoins implicites du voyageur). L'étude montre que les praticiens experts abordent l'upselling comme un service d'excellence, adaptant leur posture et leur tempo visuel au rythme du client.

#### FICHE RESSOURCE 17 : Scott, N., Zhang, R., Le, D., & Gao, J. (2017/2019)
* **Titre :** *A review of eye-tracking research in tourism*
* **Revue / Source :** Current Issues in Tourism, 22(10), 1244–1261 | [DOI: 10.1080/13683500.2017.1367367](https://doi.org/10.1080/13683500.2017.1367367)
* **Résumé analytique & Portée pour le projet :** Revue systématique de référence sur l'application de l'oculométrie dans les secteurs du tourisme et de l'hôtellerie. Les auteurs recensent les recherches menées sur l'attention visuelle appliquée aux interfaces numériques, aux supports promotionnels et aux environnements de service. L'article met en exergue l'impératif méthodologique de dépasser les mesures déclaratives classiques par des données biométriques directes et souligne le potentiel des technologies oculométriques portables pour investiguer les interactions de service en direct.

---

## 7. Bibliographie Complète (Normes APA 7 - Corpus Exclusif)

* **Ressource 01 :** Beckmann, J. F. (2010). Taming a beast of burden – On some issues with the conceptualisation and operationalisation of cognitive load. *Learning and Instruction*, 20(3), 250–264. [DOI: 10.1016/j.learninstruc.2009.02.024](https://doi.org/10.1016/j.learninstruc.2009.02.024)
* **Ressource 02 :** Gegenfurtner, A., Lehtinen, E., & Säljö, R. (2011). Expertise differences in the comprehension of visualizations: A meta-analysis of eye-tracking research in professional domains. *Educational Psychology Review*, 23(4), 523–552. [DOI: 10.1007/s10648-011-9174-7](https://doi.org/10.1007/s10648-011-9174-7)
* **Ressource 03 :** Van Gog, T., Jarodzka, H., Scheiter, K., Gerjets, P., & Paas, F. (2009). Attention guidance during example study via the model's eye movements. *Computers in Human Behavior*, 25(3), 785–794. [DOI: 10.1016/j.chb.2009.02.002](https://doi.org/10.1016/j.chb.2009.02.002)
* **Ressource 04 :** Goodwin, C. (1994). Professional Vision. *American Anthropologist*, 96(3), 606–633. [DOI: 10.1525/aa.1994.96.3.02a00100](https://doi.org/10.1525/aa.1994.96.3.02a00100)
* **Ressource 05 :** Crandall, B., Klein, G. A., & Hoffman, R. R. (2006). *Working Minds: A Practitioner's Guide to Cognitive Task Analysis*. The MIT Press, Cambridge, MA. [DOI: 10.7551/mitpress/7304.001.0001](https://doi.org/10.7551/mitpress/7304.001.0001)
* **Ressource 06 :** Elling, S., Lentz, L., & de Jong, M. (2012). Combining concurrent think-aloud protocols and eye-tracking observations: An analysis of verbalizations and silences. *IEEE Transactions on Professional Communication*, 55(3), 206–218. [DOI: 10.1109/TPC.2012.2206190](https://doi.org/10.1109/TPC.2012.2206190)
* **Ressource 07 :** Theureau, J. (2016) / Durand, M. (2016). Le cours d'action. L'enaction et l'expérience / L'analyse de l'activité et l'entretien d'auto-confrontation enrichi par les traces. *Activités*, 13(1). [DOI: 10.4000/activites.2769](https://doi.org/10.4000/activites.2769)
* **Ressource 08 :** Hooge, I. T. C., Nyström, M., Niehorster, D. C., Andersson, R., Foulsham, T., Nuthmann, A., & Hessels, R. S. (2026). The fundamentals of eye tracking part 6: Working with areas of interest. *Behavior Research Methods*, 58(3). [DOI: 10.3758/s13428-025-02598-6](https://doi.org/10.3758/s13428-025-02598-6)
* **Ressource 09.a :** Pfeffer, T., & Dierkes, K. (2024). *Neon Pupillometry Test Report: An evaluation of Neon's pupillometry feature*. Pupil Labs GmbH Technical Report. [Rapport Technique Pupil Labs](https://pupil-labs.com/products/neon/)
* **Ressource 09.b :** Nolte, D., Walter, J. L., von Bassewitz, L., et al. (2026). Mobile eye tracking in the real world: Best practices. *Journal of Vision*, 26(2):6, 1–22. [DOI: 10.1167/jov.26.2.6](https://doi.org/10.1167/jov.26.2.6)
* **Ressource 10 :** Jarodzka, H., Balslev, T., Holmqvist, K., Nyström, M., Scheiter, K., Gerjets, P., & Eika, B. (2012). Conveying clinical reasoning based on visual observation via eye-movement modelling examples. *Teaching and Learning in Medicine / Instructional Science*. [DOI: 10.1080/10401334.2012.692283](https://doi.org/10.1080/10401334.2012.692283)
* **Ressource 11 :** Seppänen, M., & Gegenfurtner, A. (2012). Seeing through a teacher's eyes improves students' imaging interpretation. *Medical Education*, 46(11), 1113–1114. [DOI: 10.1111/medu.12041](https://doi.org/10.1111/medu.12041)
* **Ressource 12 :** Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M. (2018). Using dual eye tracking to uncover personal gaze patterns during social interaction. *Scientific Reports*, 8, Article 4271. [DOI: 10.1038/s41598-018-22726-7](https://doi.org/10.1038/s41598-018-22726-7)
* **Ressource 13 :** Wohltjen, S., & Wheatley, T. (2021). Eye contact marks the rise and fall of shared attention in conversation. *Proceedings of the National Academy of Sciences (PNAS)*, 118(37), e2106499118. [DOI: 10.1073/pnas.2106499118](https://doi.org/10.1073/pnas.2106499118)
* **Ressource 14 :** Tickle-Degnen, L., & Rosenthal, R. (1990). The Nature of Rapport and Its Nonverbal Correlates. *Psychological Inquiry*, 1(4), 285–293. [DOI: 10.1207/s15327965pli0104_1](https://doi.org/10.1207/s15327965pli0104_1)
* **Ressource 15 :** Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D. (2006). Are All Smiles Created Equal? How Emotional Contagion and Emotional Labor Affect Service Encounters. *Journal of Marketing*, 70(3), 58–73. [DOI: 10.1509/jmkg.70.3.058](https://doi.org/10.1509/jmkg.70.3.058)
* **Ressource 16 :** Setyorini, A., & Putra, I. (2023). Front Desk Personnel Qualities and Skills in Applying Upselling Hotel Products: Case Study of the Ritz Carlton Bali. *International Journal of Multicultural and Multireligious Understanding*, 10(4), 550–558. [DOI: 10.18415/ijmmu.v10i4.4646](https://doi.org/10.18415/ijmmu.v10i4.4646)
* **Ressource 17 :** Scott, N., Zhang, R., Le, D., & Gao, J. (2017/2019). A review of eye-tracking research in tourism. *Current Issues in Tourism*, 22(10), 1244–1261. [DOI: 10.1080/13683500.2017.1367367](https://doi.org/10.1080/13683500.2017.1367367)
