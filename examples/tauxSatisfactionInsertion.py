import pandas as pd
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob import TextBlob
import matplotlib.pyplot as plt

def get_sentiment(text):
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    polarite, subjectivite = blob.sentiment

    if polarite > 0:
        return 'Positive'
    elif polarite < 0:
        return 'Negative'
    else:
        return 'Neutral'

def df_setup(chemin):
    df = pd.read_excel(chemin)
    
    # Supprimer les lignes avec des valeurs manquantes dans les commentaires
    df = df.dropna(subset=['Vos remarques et commentaires relatifs à votre insertion professionnelle'])

    # Convertir le texte en minuscules
    df['Comments'] = df['Vos remarques et commentaires relatifs à votre insertion professionnelle'].str.lower()

    # Supprimer la ponctuation
    df['Comments'] = df['Comments'].str.replace(r'[^\w\s]', '')

    # Remplacer les valeurs NaN par des chaînes de caractères vides
    df['Comments'] = df['Comments'].fillna('')

    # Ajouter une colonne 'Sentiment' avec le sentiment pour chaque commentaire
    df['Sentiment'] = df['Comments'].apply(get_sentiment)
    
    return df

def calculate_satisfaction_rate(df):
    satisfaction_proportion = df['Sentiment'].value_counts(normalize=True).get('Positive', 0)
    neutral_proportion = df['Sentiment'].value_counts(normalize=True).get('Neutral', 0)
    negative_proportion = df['Sentiment'].value_counts(normalize=True).get('Negative', 0)
    return satisfaction_proportion, neutral_proportion, negative_proportion

def main():
    # Liste des formations
    formations = [
        'Mécanique et Interactions (MI)',
        'Microélectronique Et Automatique (MEA)',
        'Matériaux (MAT)',
        'Génie Biologique et Agroalimentaires (GBA)',
        'Mécanique Structures Industrielles (MSI - apprentissage)',
        'Eau et Génie Civil (EGC - apprentissage)',
        'Sciences et Technologies de l\'Eau (STE)',
        'Informatique et Gestion (IG)',
        'Systèmes Embarqués (SE - apprentissage)'
    ]

    # Dictionnaire pour stocker les taux de satisfaction par année
    satisfaction_rates = {'Satisfaction': [], 'Neutral': [], 'Negative': []}
    years = []

    # Charger les données depuis le fichier Excel
    dfs = []
    for year in range(2018, 2024):
        df = df_setup(f'datav2/extraction_finale_enquete_{year}DS.xls' if year == 2018 or year == 2023 or year == 2020 else f'datav2/extraction_finale_enquete_{year}DS.xlsx')
        df['Formation'] = df['Formation'].str.strip()
        df['Année d\'obtention du diplôme'] = year
        dfs.append(df)

    # Concaténer les données de toutes les années
    df_concat = pd.concat(dfs)

    # Trier par année d'obtention du diplôme
    df_concat.sort_values(by='Année d\'obtention du diplôme', inplace=True)

    for year in range(2018, 2024):
        print(f'{year} :')
        # Filtrer les données pour l'année actuelle
        df_year = df_concat[df_concat['Année d\'obtention du diplôme'] == year]

        # Calculer le taux de satisfaction pour l'année
        satisfaction, neutral, negative = calculate_satisfaction_rate(df_year)

        # Ajouter les taux au dictionnaire
        satisfaction_rates['Satisfaction'].append(satisfaction)
        satisfaction_rates['Neutral'].append(neutral)
        satisfaction_rates['Negative'].append(negative)

        print(f"Taux de satisfaction pour l'année {year} : {satisfaction:.2%}")
        print(f"Taux neutre pour l'année {year} : {neutral:.2%}")
        print(f"Taux non satisfaction pour l'année {year} : {negative:.2%}")

        years.append(year)

    # Tracer le graphique
    plt.figure(figsize=(10, 6))
    
    plt.plot(years, satisfaction_rates['Satisfaction'], marker='o', label='Satisfaction', linestyle='-')
    plt.plot(years, satisfaction_rates['Neutral'], marker='o', label='Neutral', linestyle='-')
    plt.plot(years, satisfaction_rates['Negative'], marker='o', label='Negative', linestyle='-')

    # Ajouter des étiquettes et des titres
    plt.title("Évolution du taux de satisfaction global au fil du temps")
    plt.xlabel("Année")
    plt.ylabel("Taux de Satisfaction (%)")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()

    # Afficher le graphique
    plt.show()


if __name__ == "__main__":
    main()
