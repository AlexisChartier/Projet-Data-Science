# Projet Data Science

## Présentation du Projet

### Sujet
Le projet de Data Science porte sur l'insertion professionnelle des ingénieurs de Polytech Montpellier. L'étude couvre les enquêtes réalisées à 6, 18, et 30 mois après l'obtention du diplôme. Les données, fournies par l'équipe enseignante, sont diverses, hétérogènes, et parfois incomplètes. Les enquêtes s'étendent de la promotion 2022 à 6 mois après l'obtention du diplôme jusqu'à la promotion 2014 à 30 mois.

**Contacts :**
- Jérémy Vacquié (jeremy.vacquie@umontpellier.fr)
- Marie-José Samy (marie-jose.samy@umontpellier.fr)

### Objectif
Le projet se concentre sur l'analyse des retours textuels des diplômés sur leur formation à Polytech Montpellier, données jusqu'à présent peu étudiées.

### Problématiques
1. Comment évaluer la satisfaction des diplômés de Polytech Montpellier en se basant sur les retours textuels des enquêtes à 6, 18 et 30 mois après l'obtention de leur diplôme?
2. Quelles sont les tendances générales ou les évolutions observables dans les retours textuels sur la formation, et existe-t-il des différences significatives entre les différentes promotions?
3. Comment catégoriser les retours textuels en thèmes spécifiques pour mieux comprendre les points forts et les points faibles de la formation à Polytech Montpellier?
4. Existe-t-il des corrélations entre la satisfaction exprimée dans les retours textuels et d'autres indicateurs tels que le taux d'insertion professionnelle ou la spécialisation des diplômés?
5. Quels UE approfondir, ajouter, supprimer?

### Méthodes Possibles
1. Utilisation de techniques de traitement du langage naturel (NLP) pour extraire des thèmes récurrents ou des sentiments positifs/négatifs dans les retours textuels.
2. Analyse de texte fréquentielle pour identifier les mots clés et les expressions les plus utilisés par les diplômés.
3. Application de techniques de clustering pour regrouper les retours textuels similaires et identifier des tendances communes.
4. Réalisation d'analyses longitudinales pour observer l'évolution des opinions au fil du temps.
5. Utilisation de méthodes statistiques pour évaluer la significativité des différences entre les promotions ou pour identifier des corrélations avec d'autres variables.

### Axes à Développer
- Choix des technologies
  - Justification et explication du fonctionnement des librairies utilisées
- Liste des librairies Python à installer
  - NLTK (pour le traitement du langage naturel)
  - Matplotlib (pour la visualisation des données)
  - Pandas (pour la manipulation de données)
  - Scikit-learn (pour les outils de machine learning)
  - Wordcloud (pour la création de nuages de mots)
  - Seaborn (pour des visualisations statistiques)
  - TfidfVectorizer (de scikit-learn, pour la vectorisation du texte)
  - TextBlob (pour l'analyse des sentiments)
  - Gensim (pour le traitement des thèmes à partir de l'analyse textuelle)
  - Librairies additionnelles: xlrd, openpyxl
- Méthode pour les scripts sous Python
  - Importation du fichier Excel
  - Choix des colonnes pertinentes
  - Formatage des données
  - Application d'algorithmes d'analyse textuelle
  - Affichage et interprétation des résultats
- Structure du code
  - Un fichier pour chaque problématique recherchée pour rendre le code plus lisible

### Résultats & Interprétation
Les résultats seront présentés sous forme de graphiques, nuages de mots, et statistiques. L'évaluation de la pertinence des résultats se fera en comparant les résultats obtenus avec l'analyse textuelle avec d'autres résultats d'analyses de données binaires pour voir si des conclusions différentes peuvent être tirées.

### Structure du Projet

- **data**: Contient les données au format Excel.
- **examples**: Contient des exemples de scripts Python pour analyser les données.
- **results**: Contient les graphiques obtenus à partir de l'analyse des données.
- **script**: Contient les scripts utilisés pour l'analyse de données.
