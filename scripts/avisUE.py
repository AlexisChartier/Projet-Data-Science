import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def load_and_preprocess(year):
    file_path = f'datav2/extraction_finale_enquete_{year}DS.' + ('xls' if year in [2018, 2020, 2023] else 'xlsx')
    df = pd.read_excel(file_path)
    df = df.dropna(subset=['Quels enseignements vous semblent les plus utiles pour l\'exercice de votre métier et votre insertion professionnelle ?'])
    df = df.dropna(subset=['Parmi les enseignements fournis par l\'école, quels sont ceux qui mériteraient d\'être approfondis ou renforcés ?'])
    df = df.dropna(subset=['Quels enseignements, absents de votre formation, vous auraient été utiles ?'])
    df = df.dropna(subset=['Quels enseignements, présents dans votre formation, vous paraissent inutiles ?'])
    df['Quels enseignements vous semblent les plus utiles pour l\'exercice de votre métier et votre insertion professionnelle ?'] = df['Quels enseignements vous semblent les plus utiles pour l\'exercice de votre métier et votre insertion professionnelle ?'].str.lower().str.replace(r'[^\w\s]', '')
    df['Parmi les enseignements fournis par l\'école, quels sont ceux qui mériteraient d\'être approfondis ou renforcés ?'] = df['Parmi les enseignements fournis par l\'école, quels sont ceux qui mériteraient d\'être approfondis ou renforcés ?'].str.lower().str.replace(r'[^\w\s]', '')
    df['Quels enseignements, absents de votre formation, vous auraient été utiles ?'] = df['Quels enseignements, absents de votre formation, vous auraient été utiles ?'].str.lower().str.replace(r'[^\w\s]', '')
    df['Quels enseignements, présents dans votre formation, vous paraissent inutiles ?'] = df['Quels enseignements, présents dans votre formation, vous paraissent inutiles ?'].str.lower().str.replace(r'[^\w\s]', '')
    return df


def plot_results(enseignements_par_filiere):
    for filiere, enseignements in enseignements_par_filiere.items():
        for categorie, liste_enseignements in enseignements.items():
            # Utiliser Counter pour compter les occurrences
            counter = Counter(liste_enseignements)
            # Sélectionner les trois résultats les plus fréquents
            top_3 = counter.most_common(3)
            # Extraire les enseignements et les occurrences
            enseignements, occurrences = zip(*top_3)
            # Créer un graphique à barres
            plt.bar(enseignements, occurrences)
            # Ajouter des étiquettes aux barres
            for i, v in enumerate(occurrences):
                plt.text(i, v, str(v), ha='center', va='bottom')
            # Ajouter un titre et des étiquettes d'axe
            plt.title(f"Résultats des enseignements pour la filière {filiere}, catégorie {categorie}")
            plt.xlabel("Enseignements")
            plt.ylabel("Occurrences")
            # Afficher le graphique
            plt.savefig(f"results/Avis sur les UE/avisUE_{filiere}_{categorie}.png")
            plt.show()

def process_enseignements(dataframe):
    # Dictionnaire pour stocker les enseignements par filière
    enseignements_par_filiere = {
        'Mécanique et Interactions (MI)': {'utileinsertion':[], 'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
        'Microélectronique Et Automatique (MEA)': {'utileinsertion':[],'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
        'Matériaux (MAT)': {'utileinsertion':[],'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
        'Génie Biologique et Agroalimentaires (GBA)': {'utileinsertion':[],'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
        'Mécanique Structures Industrielles (MSI - apprentissage)': {'utileinsertion':[],'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
        'Eau et Génie Civil (EGC - apprentissage)': {'utileinsertion':[],'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
        'Sciences et Technologies de l\'Eau (STE)': {'utileinsertion':[],'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
        'Informatique et Gestion (IG)': {'utileinsertion':[],'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
        'Systèmes Embarqués (SE - apprentissage)': {'utileinsertion':[],'meriteapprondis': [], 'auraitutile': [], 'inutile': []},
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
            enseignements_par_filiere[filiere]['meriteapprondis'].extend(merite_value.split(','))
            enseignements_par_filiere[filiere]['auraitutile'].extend(utile_value.split(','))
            enseignements_par_filiere[filiere]['inutile'].extend(inutile_value.split(','))

    plot_results(enseignements_par_filiere)
    # Afficher les trois résultats les plus fréquents pour chaque catégorie
    for filiere, enseignements in enseignements_par_filiere.items():
        for categorie, liste_enseignements in enseignements.items():
            # Utiliser Counter pour compter les occurrences
            counter = Counter(liste_enseignements)
            # Sélectionner les trois résultats les plus fréquents
            top_3 = counter.most_common(3)
            # Afficher les résultats
            print(f"\nFilière {filiere}, Catégorie {categorie} :")
            for enseignement, count in top_3:
                print(f"{enseignement}: {count} fois")


def main():
    years = range(2020, 2024)
    all_data = pd.DataFrame()

    for year in years:
        df_year = load_and_preprocess(year)
        all_data = pd.concat([all_data, df_year])

    process_enseignements(all_data)

if __name__ == '__main__':
    main()
