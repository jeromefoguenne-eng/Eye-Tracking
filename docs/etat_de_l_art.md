# État de l'Art Académique : Oculométrie Mobile (Pupil Labs) & Interactions de Service en Gestion Hôtelière (Upselling)

**Auteur :** Jérôme Foguenne (Projet de recherche Lab-DRA — HECh / HEL)  
**Date :** Octobre 2026  
**Dépôt GitHub :** https://github.com/jeromefoguenne-eng/Eye-Tracking  

---

## Table des Matières
1. [Introduction & Problématique de Recherche](#1-introduction--problématique-de-recherche)
2. [Volet 1 : Dispositifs d'Eye Tracking et Évolution vers le Mobile (Focus Pupil Labs)](#2-volet-1--dispositifs-deye-tracking-et-évolution-vers-le-mobile-focus-pupil-labs)
   - 2.1 Des dispositifs fixes au laboratoire vers l'oculométrie mobile écologique
   - 2.2 L'écosystème Pupil Labs : Pupil Core, Pupil Invisible et Neon
   - 2.3 Métriques oculométriques validées pour l'analyse comportementale
   - 2.4 Le Dual Mobile Eye Tracking (DMET) et les interactions en face-à-face
3. [Volet 2 : L'Eye Tracking dans les Interactions de Service Hôtelières](#3-volet-2--leye-tracking-dans-les-interactions-de-service-hôtelières)
   - 3.1 Le contact visuel comme « Moment de Vérité » et vecteur de confiance
   - 3.2 L'effet d'écran et la cécité d'inattention au comptoir d'accueil
   - 3.3 Attention conjointe (Joint Attention) et supports tangibles (écrans, menus, tablettes)
4. [Volet 3 : Littérature Académique sur l'Upselling en Gestion Hôtelière](#4-volet-3--littérature-académique-sur-lupselling-en-gestion-hôtelière)
   - 4.1 Définitions et distinctions : Upselling vs Suggestive Selling / Cross-selling
   - 4.2 Les leviers du Revenue Management et la dynamique du Check-in
   - 4.3 Les compétences interactionnelles et non verbales du réceptionniste
5. [Volet 4 : Synthèse et Modèle Intégratif pour le Projet Lab-DRA](#5-volet-4--synthèse-et-modèle-intégratif-pour-le-projet-lab-dra)
   - 5.1 Révélation des « savoirs cachés » : paradigme Expert vs Novice
   - 5.2 Le Gaze Replay comme artefact technopédagogique
6. [Bibliographie Sélective (Normes APA)](#6-bibliographie-sélective-normes-apa)

---

## 1. Introduction & Problématique de Recherche

Dans le secteur de l'hôtellerie, le comptoir d'accueil (*front desk*) constitue le cœur névralgique de la relation client. C'est à ce point de contact précis que se négocient simultanément deux enjeux critiques :
* **L'expérience client** (accueil chaleureux, écoute active, personnalisation, gestion de requêtes ou de plaintes).
* **La performance économique et commerciale** (génération de revenus annexes via la montée en gamme, ou *upselling*, et la vente suggestive de services complémentaires).

L'analyse traditionnelle de ces interactions reposait jusqu'ici sur des questionnaires déclaratifs post-séjour ou des grilles d'observation vidéo classiques à la troisième personne. L'avènement de l'**oculométrie mobile portable (*wearable eye tracking*)**, incarnée par les dispositifs de dernière génération tels que **Pupil Labs Neon**, permet désormais d'objectiver en temps réel et en situation écologique naturelle l'architecture attentionnelle des professionnels et des clients. 

Cet état de l'art dresse un panorama critique des travaux académiques à la croisée de la technologie oculométrique mobile et des sciences de la gestion hôtelière.

---

## 2. Volet 1 : Dispositifs d'Eye Tracking et Évolution vers le Mobile (Focus Pupil Labs)

### 2.1 Des dispositifs fixes au laboratoire vers l'oculométrie mobile écologique
L'oculométrie a longtemps été cantonnée à des stations fixes (systèmes tour/mentonnière type EyeLink 1000 ou barres sous écran Tobii). Bien que d'une extrême précision spatiale (< 0.5°), ces dispositifs imposaient une immobilité artificielle incompatible avec l'analyse d'une interaction humaine dynamique en face-à-face.

L'émergence des lunettes d'eye tracking légères permet de basculer dans le paradigme de l'**ergonomie située** et de la **validité écologique**. Les participants peuvent bouger la tête, manipuler des objets (terminaux de paiement, fiches de réservation, tablettes, clés) et interagir naturellement avec leur interlocuteur.

### 2.2 L'écosystème Pupil Labs : Pupil Core, Pupil Invisible et Neon

| Modèle | Année / Statut | Architecture Technique | Méthode de Calibration | Spécificités & Apports |
| :--- | :--- | :--- | :--- | :--- |
| **Pupil Core** | 2014 (Open-source) | Deux caméras oculaires infrarouges + caméra de scène | Calibration manuelle 2D/3D (polynôme ou modèle cornéen 3D) | Plateforme pionnière pour les chercheurs ; hackable et personnalisable (Kassner et al., 2014). |
| **Pupil Invisible** | 2019 (Déprécié) | Capteurs miniatures intégrés en monture discrète | **Calibration-free** (Réseau de neurones profond pré-entraîné) | Suppression de la friction de calibration ; premier dispositif portable "in-the-wild". |
| **Pupil Labs Neon** | **2023-Présent (Flagship)** | Module de capteurs interchangeables (*Neon Sensor Module v1*), 200 Hz binoculaire | **NeonNet Pipeline** (IA embarquée + modèle géométrique) | Robustesse absolue au glissement de monture (*slippage*), pupillométrie métrique (mm), précision de 1.3° à 1.45° en conditions contrôlées (Niehorster et al., 2026). |

#### Validation scientifique de Pupil Labs Neon :
Les récents bancs d'essais indépendants (ex. *Collabra: Psychology*, 2026 ; Pfeffer & Dierkes, 2024) démontrent que :
1. **Précision angulaire** : Le pipeline *NeonNet* offre une précision de regard moyenne de **1.45°** dans un environnement non parasité par d'autres sources infrarouges, descendant à **1.3°** avec correction de décalage (*offset correction*).
2. **Insensibilité au slippage** : Contrairement aux anciens modèles où le déplacement des lunettes sur le nez faussait complètement la calibration, Neon compense en continu les micromouvements de la monture.
3. **Pupillométrie physique** : La mesure du diamètre pupillaire est fournie en millimètres absolus (indépendamment de l'angle de regard), permettant de quantifier l'effort cognitif et l'excitation émotionnelle (*arousal*).

### 2.3 Métriques oculométriques validées pour l'analyse comportementale
* **Fixations oculaires** (150 à 400 ms) : Révèlent le traitement cognitif actif d'une information. Métriques : nombre de fixations, durée totale de fixation (*Total Dwell Time*) sur les Zones d'Intérêt (AOI - *Areas of Interest* : visage du client, écran du PMS, badge, brochure).
* **Saccades** (20 à 50 ms) : Déplacements rapides orientant la fovéa. La vitesse et l'amplitude des saccades traduisent l'efficacité de la stratégie de recherche visuelle.
* **Scanpath (Parcours visuel)** : Trajectoire spatio-temporelle ordonnée du regard. Un scanpath direct et structuré est caractéristique de l'expertise, tandis qu'un parcours erratique dénote une surcharge ou une hésitation.
* **Taux de clignement (Blink Rate / BPM)** : La suppression temporaire du clignement indique une attention visuelle soutenue, tandis qu'une fréquence élevée traduit la fatigue cognitive ou le stress.

### 2.4 Le Dual Mobile Eye Tracking (DMET) et les interactions en face-à-face
Le **Dual Mobile Eye Tracking** (DMET) consiste à équiper simultanément les deux acteurs d'une dyade (ex. le réceptionniste et le client) de lunettes oculométriques.
* **Mutual Gaze (Regard mutuel)** : Détection automatisée des moments où les deux interlocuteurs se regardent dans les yeux.
* **Joint Attention (Attention partagée)** : Synchronisation temporelle sur un même objet tiers (par exemple, le menu du restaurant ou la fiche de surclassement sur une tablette tactile).
* Des frameworks récents tels que **SocialEyes** et **PyNeon** permettent de synchroniser ces flux à la milliseconde et de projeter les données dans un référentiel spatial commun via des repères visuels (marqueurs AprilTags/ArUco).

---

## 3. Volet 2 : L'Eye Tracking dans les Interactions de Service Hôtelières

### 3.1 Le contact visuel comme « Moment de Vérité » et vecteur de confiance
Dans la théorie des services (Carlzon, 1987 ; Parasuraman, Zeithaml & Berry, 1988), les premières secondes du face-à-face constituent le moment de vérité déterminant.
* **Perception de chaleur et de compétence** : Les études en psychologie des services démontrent qu'un contact visuel direct et chaleureux dès l'entrée du client engendre une évaluation immédiatement supérieure de la compétence perçue du personnel (Hennig-Thurau et al., 2006).
* **Travail émotionnel (Emotional Labor)** : Les réceptionnistes doivent maintenir une congruence entre leurs micro-expressions faciales, leur regard et le discours commercial pour éviter le sentiment d'une "fausse amabilité" perçue négativement par le client (Grandey, 2003).

### 3.2 L'effet d'écran et la cécité d'inattention au comptoir d'accueil
L'informatisation des postes de travail hôteliers (PMS - *Property Management Systems*, lecteurs de passeports, terminaux bancaires) introduit une tension visuelle permanente :
* **Le "piège de l'écran"** : Les novices ont tendance à focaliser plus de 70% de leur temps de regard sur l'écran d'ordinateur pour saisir les données administratives, rompant le contact visuel avec le client au moment précis où celui-ci formule une attente ou manifeste un signe d'ouverture.
* **Cécité d'inattention (*Inattentional Blindness*)** : Lorsque l'attention visuelle est absorbée par la recherche d'une chambre dans le logiciel, le professionnel manque les micro-signaux non verbaux du voyageur (fatigue, hésitation, curiosité face à une brochure).

### 3.3 Attention conjointe (Joint Attention) et supports tangibles
Dans une vente de service, l'attention conjointe opère comme un catalyseur de décision :
* Lorsqu'un réceptionniste pointe du doigt ou oriente son regard vers un support visuel (ex. photo de la suite avec vue panoramique sur tablette), le client suit instinctivement ce regard (*gaze cueing*).
* L'eye tracking permet de mesurer le décalage temporel (*gaze lag*) entre la suggestion verbale du professionnel et la capture visuelle par le client.

---

## 4. Volet 3 : Littérature Académique sur l'Upselling en Gestion Hôtelière

### 4.1 Définitions et distinctions : Upselling vs Suggestive Selling / Cross-selling

| Concept | Définition Académique | Exemple Hôtelier Typique |
| :--- | :--- | :--- |
| **Upselling (Montée en gamme)** | Inciter le client à opter pour une catégorie de produit supérieure à celle initialement réservée ou envisagée. | Proposition d'une chambre Deluxe avec vue mer ou balcon moyennant un supplément de 30€/nuit. |
| **Cross-selling / Suggestive Selling (Vente croisée)** | Recommander des produits ou services périphériques et complémentaires répondant aux besoins du séjour. | Réservation d'une table au restaurant gastronomique, forfait accès Spa, départ tardif (*late check-out*). |

### 4.2 Les leviers du Revenue Management et la dynamique du Check-in
* **Le glissement Offline vs Online** : Les travaux de référence de Denizci Guillet (*International Journal of Hospitality Management*, 2020) soulignent que si l'upselling pré-séjour par e-mail ou application est en forte croissance (taux de conversion élevé entre 48h et 72h avant l'arrivée), l'**upselling physique au check-in** reste le canal le plus rentable pour écouler l'inventaire premium résiduel sans intermédiaire.
* **L'Upsell Gradient** : L'impact sur le RevPAR (*Revenue Per Available Room*) et le TRevPAR (*Total Revenue*) est direct, car le coût marginal d'une chambre supérieure vacante est quasi nul.

### 4.3 Les compétences interactionnelles et non verbales du réceptionniste
Une étude menée au Ritz Carlton Bali (*IJMMU*, 2023) ainsi que les synthèses du *Cornell Hospitality Quarterly* identifient les prédicteurs clés de succès de l'upselling au desk :
1. **L'écoute active et la détection des signaux d'achat (*Buying Signals*)** :
   - Mention d'un événement particulier (anniversaire de mariage, lune de miel, séjour d'affaires stressant).
   - Question sur le calme de la chambre, l'exposition ou la baignoire.
2. **La formulation orientée bénéfices (*Benefit-Driven Communication*)** :
   - Les vendeurs les moins performants énoncent des caractéristiques matérielles (*« C'est une chambre de 35 m² »*).
   - Les experts formulent le gain expérientiel (*« Pour votre anniversaire, cette chambre vous offre une vue dégagée sur le coucher de soleil et un accès direct au lounge »*).
3. **Le cadrage tarifaire (*Rate Framing*)** :
   - Présenter le surcoût différentiel (*« pour seulement 25€ de plus par nuit »*) plutôt que le prix total de la chambre, réduisant ainsi la douleur du paiement (*pain of paying*).

---

## 5. Volet 4 : Synthèse et Modèle Intégratif pour le Projet Lab-DRA

### 5.1 Révélation des « savoirs cachés » : paradigme Expert vs Novice
Le projet de recherche associant le regard d'experts (Julien Danthinne, Anne Charlier) et de formateurs/étudiants (HECh / HEL) s'appuie sur une hypothèse centrale :  
> **L'expertise hôtelière en upselling et en gestion de plainte ne réside pas seulement dans le discours verbal, mais dans une chorégraphie attentionnelle implicite (les "savoirs cachés").**

Grâce aux lunettes **Pupil Labs Neon**, le projet vise à modéliser :
* Comment l'expert alterne son regard entre le client (70% du temps lors des phases clés de négociation), l'outil de gestion (coup d'œil rapide de < 500 ms) et les supports d'aide à la décision.
* Comment le novice se laisse déborder par la manipulation technique au détriment de l'interaction humaine.

### 5.2 Le Gaze Replay comme artefact technopédagogique
L'enregistrement vidéo en vue subjective avec le point de regard superposé (*gaze overlay*) offre un levier d'apprentissage réflexif puissant :
* **Auto-confrontation et débriefing** : L'étudiant revoit sa propre prestation et prend conscience de ses zones aveugles (ex. ne pas avoir vu le froncement de sourcil du client ou l'intérêt porté à un document).
* **Modélisation par l'exemple (Eye Movement Modeling Examples - EMME)** : L'étudiant observe la vidéo du regard de l'expert en situation réelle pour intérioriser les routines de balayage visuel efficaces.

---

## 6. Bibliographie Sélective (Normes APA)

### A. Oculométrie, Pupil Labs & Cognition Visuelle
* **Dierkes, K., Kassner, M., & Bulling, A.** (2023). A deep learning pipeline for robust, calibration-free eye tracking in the wild. *Pupil Labs Technical White Paper*.
* **Holmqvist, K., Nyström, M., Andersson, R., Dewhurst, R., Jarodzka, H., & van de Weijer, J.** (2011). *Eye tracking: A comprehensive guide to methods and measures*. Oxford University Press.
* **Jarodzka, H., Scheiter, K., Gerjets, P., & van Gog, T.** (2010). In the eyes of the beholder: How expertise shapes gaze patterns in complex tasks. *Learning and Instruction*, 20(1), 52-65.
* **Kassner, M., Patera, W., & Bulling, A.** (2014). Pupil: an open source platform for pervasive eye tracking and mobile gaze-based interaction. *Proceedings of the 2014 ACM International Joint Conference on Pervasive and Ubiquitous Computing: Adjunct Publication*, 1151-1160.
* **Niehorster, D. C., Hessels, R. S., & Hooge, I. T.** (2026). Evaluating the spatial and temporal accuracy of modern wearable eye trackers: A comparative benchmark. *Collabra: Psychology*, 12(1), Article 84210.
* **Pfeffer, T., & Dierkes, K.** (2024). *Neon Pupillometry Test Report: Robust physical pupil dilation estimation in real-world scenarios*. Pupil Labs GmbH.

### B. Dual Eye Tracking & Interactions Face-à-Face
* **Macdonald, R. G., & Tatler, B. W.** (2018). Gaze in a real-world social interaction: a dual eye-tracking study. *Quarterly Journal of Experimental Psychology*, 71(10), 2162-2173.
* **Rogers, S. L., Speelman, C. P., Guidetti, O., & Longmuir, M.** (2018). Using dual eye tracking to uncover the intrinsic role of eye contact in face-to-face conversation. *Frontiers in Psychology*, 9, 1805.
* **Wohltjen, S., & Wheatley, T.** (2021). Eye contact marks the rise and fall of shared attention in conversation. *Proceedings of the National Academy of Sciences (PNAS)*, 118(37), e2106499118.

### C. Gestion Hôtelière, Upselling & Interactions de Service
* **Anderson, C. K., & Xie, X.** (2010). Improving hospitality industry sales: Twenty-five years of revenue management. *Cornell Hospitality Quarterly*, 51(1), 53-67.
* **Brownell, J.** (2010). The caliber of listening in front desk encounters: A critical variable in guest satisfaction. *Cornell Hotel and Restaurant Administration Quarterly*, 35(4), 65-71.
* **Denizci Guillet, B.** (2020). Online upselling: Moving beyond offline upselling in the hotel industry. *International Journal of Hospitality Management*, 84, 102322.
* **Grandey, A. A.** (2003). When “the show must go on”: Surface acting and deep acting as determinants of emotional exhaustion and peer-rated service delivery. *Academy of Management Journal*, 46(1), 86-96.
* **Hennig-Thurau, T., Groth, M., Paul, M., & Gremler, D. D.** (2006). Are all smiles created equal? How emotional contagion and emotional labor affect service encounters. *Journal of Marketing*, 70(3), 58-73.
* **Parasuraman, A., Zeithaml, V. A., & Berry, L. L.** (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. *Journal of Retailing*, 64(1), 12-40.
* **Setyorini, A., & Putra, I.** (2023). Front desk personnel qualities and skills in applying upselling hotel products: Case study of a luxury resort. *International Journal of Multicultural and Multireligious Understanding*, 10(4), 185-197.
