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

    # Dictionnaire pour stocker les taux de satisfaction par filière
    satisfaction_rates = {'Satisfaction': [], 'Neutral': [], 'Negative': []}
    years = []

    for year in range(2018, 2024):
        print(f'{year} :')
        # Charger les données depuis le fichier Excel
        df = df_setup(f'datav2/extraction_finale_enquete_{year}DS.xls' if year == 2018 or year == 2023 or year == 2020 else f'datav2/extraction_finale_enquete_{year}DS.xlsx')
        df['Formation'] = df['Formation'].str.strip()  

        satisfaction_rate = {'Satisfaction': [], 'Neutral': [], 'Negative': []}

        for formation in formations:
            # Filtrer les données pour la formation actuelle
            df_formation = df[df['Formation'] == formation]

            # Calculer le taux de satisfaction pour la filière
            satisfaction, neutral, negative = calculate_satisfaction_rate(df_formation)

            # Ajouter les taux au dictionnaire
            satisfaction_rate['Satisfaction'].append(satisfaction)
            satisfaction_rate['Neutral'].append(neutral)
            satisfaction_rate['Negative'].append(negative)

            print(f"Taux de satisfaction pour la formation {formation} : {satisfaction:.2%}")
            print(f"Taux neutre pour la formation {formation} : {neutral:.2%}")
            print(f"Taux non satisfaction pour la formation {formation} : {negative:.2%}")


        # Ajouter les taux au dictionnaire principal
        satisfaction_rates['Satisfaction'].append(satisfaction_rate['Satisfaction'])
        satisfaction_rates['Neutral'].append(satisfaction_rate['Neutral'])
        satisfaction_rates['Negative'].append(satisfaction_rate['Negative'])
        years.append(year)

    # Tracer le graphique
    plt.figure(figsize=(10, 6))
    
    for i, formation in enumerate(formations):
        plt.plot(years, [rate[i] for rate in satisfaction_rates['Satisfaction']], marker='o', label=f'{formation}', linestyle='-')

    # Ajouter des étiquettes et des titres
    plt.title("Évolution du taux de satisfaction par filière au fil du temps")
    plt.xlabel("Année")
    plt.ylabel("Taux de Satisfaction (%)")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()

    # Afficher le graphique
    plt.show()


if __name__ == "__main__":
    main()
