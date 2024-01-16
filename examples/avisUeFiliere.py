#Méthode d'analyse : Fréauence des mots

import pandas as pd
from collections import Counter

def process_enseignements(dataframe,annee):
    # Dictionnaire pour stocker les enseignements par filière
    enseignements_par_filiere = {
        'Mécanique et Interactions (MI)': {'utileinsertion':[], 'merite': [], 'utile': [], 'inutile': []},
        'Microélectronique Et Automatique (MEA)': {'utileinsertion':[],'merite': [], 'utile': [], 'inutile': []},
        'Matériaux (MAT)': {'utileinsertion':[],'merite': [], 'utile': [], 'inutile': []},
        'Génie Biologique et Agroalimentaires (GBA)': {'utileinsertion':[],'merite': [], 'utile': [], 'inutile': []},
        'Mécanique Structures Industrielles (MSI - apprentissage)': {'utileinsertion':[],'merite': [], 'utile': [], 'inutile': []},
        'Eau et Génie Civil (EGC - apprentissage)': {'utileinsertion':[],'merite': [], 'utile': [], 'inutile': []},
        'Sciences et Technologies de l\'Eau (STE)': {'utileinsertion':[],'merite': [], 'utile': [], 'inutile': []},
        'Informatique et Gestion (IG)': {'utileinsertion':[],'merite': [], 'utile': [], 'inutile': []},
        'Systèmes Embarqués (SE - apprentissage)': {'utileinsertion':[],'merite': [], 'utile': [], 'inutile': []},
    }

    # Itérer sur chaque ligne du dataframe
    for index, row in dataframe.iterrows():
        # Filtrer les données pour les enseignements par filière
        filiere = row['Formation']

        # Ajouter les enseignements correspondants à chaque catégorie
        utile_inser = row['Quels enseignements vous semblent les plus utiles pour l\'exercice de votre métier et votre insertion professionnelle ?']
        merite_value = row['Parmi les enseignements fournis par l\'école, quels sont ceux qui mériteraient d\'être approfondis ou renforcés ?']
        utile_value = row['Quels enseignements, absents de votre formation, vous auraient été utiles ?']
        inutile_value = row['Quels enseignements, présents dans votre formation, vous paraissent inutiles ?']

        
        # Vérifier si les valeurs ne sont pas nulles (NaN) avant d'appliquer split()
        if isinstance(merite_value, str) and isinstance(utile_value, str) and isinstance(inutile_value, str) and isinstance(utile_inser, str):
            # Normalisation des données
            utile_inser = utile_inser.lower().strip()
            merite_value = merite_value.lower().strip()
            utile_value = utile_value.lower().strip()
            inutile_value = inutile_value.lower().strip()

            # Ajout des enseignements dans le dictionnaire
            enseignements_par_filiere[filiere]['utileinsertion'].extend(utile_inser.split(','))
            enseignements_par_filiere[filiere]['merite'].extend(merite_value.split(','))
            enseignements_par_filiere[filiere]['utile'].extend(utile_value.split(','))
            enseignements_par_filiere[filiere]['inutile'].extend(inutile_value.split(','))

    # Afficher les trois résultats les plus fréquents pour chaque catégorie
    for filiere, enseignements in enseignements_par_filiere.items():
        for categorie, liste_enseignements in enseignements.items():
            # Utiliser Counter pour compter les occurrences
            counter = Counter(liste_enseignements)
            # Sélectionner les trois résultats les plus fréquents
            top_3 = counter.most_common(3)
            # Afficher les résultats
            print(f"\nFilière {filiere}, Catégorie {categorie}, Année {annee}  :")
            for enseignement, count in top_3:
                print(f"{enseignement}: {count} fois")

def main():
    # Liste des années à analyser
    annees = [2020,2021, 2022, 2023]

    # Boucle sur les années
    for annee in annees:
        if annee == 2023:
            fichier_excel = f'datav2/extraction_finale_enquete_{annee}DS.xls'
            df = pd.read_excel(fichier_excel)
        elif annee == 2020:
            fichier_excel = f'datav2/extraction_finale_enquete_2020DS.xls'
            df = pd.read_excel(fichier_excel)
        else:
        # Charger les données depuis le fichier Excel
            fichier_excel = f'datav2/extraction_finale_enquete_{annee}DS.xlsx'
            df = pd.read_excel(fichier_excel)
        
        # Appeler la fonction pour traiter les enseignements
        process_enseignements(df, annee)

if __name__ == "__main__":
    main()