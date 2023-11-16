from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob import TextBlob



#Fonctions

# Fonction pour obtenir le sentiment
def get_sentiment(text):
    # Créer un objet TextBlob avec le pos_tagger et l'analyseur Pattern pour le français
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

    # Déterminer le sentiment en fonction de la polarité
    if blob.sentiment.polarity > 0:
        return 'Positif'
    elif blob.sentiment.polarity < 0:
        return 'Négatif'
    else:
        return 'Neutre'

#Fonction qui définie le fichier utilisé comme source de données et qui formate et tokenize les données    
def df_setup(chemin):
    df = pd.read_excel(chemin)
    # Sélectionner uniquement les colonnes d'intérêt
    columns_of_interest = ['Vos remarques et commentaires relatifs à votre insertion professionnelle', 'Formation']
    df = df[columns_of_interest]    

    # Supprimer les lignes avec des valeurs manquantes dans les commentaires
    df = df.dropna(subset=['Vos remarques et commentaires relatifs à votre insertion professionnelle'])

    # Convertir le texte en minuscules
    df['Comments'] = df['Vos remarques et commentaires relatifs à votre insertion professionnelle'].str.lower()

    # Supprimer la ponctuation
    df['Comments'] = df['Comments'].str.replace(r'[^\w\s]', '')

    # Remplacer les valeurs NaN par des chaînes de caractères vides
    df['Comments'] = df['Comments'].fillna('')

    # Tokenization
    df['Tokens'] = df['Comments'].apply(word_tokenize)

    # Supprimer les stopwords
    stop_words = set(stopwords.words('french'))  # Utilisez 'english' si vos données sont en anglais
    df['Tokens'] = df['Tokens'].apply(lambda x: [word for word in x if word.lower() not in stop_words])
    
    return df

#Fonction qui affiche la satisfaction global
def printGlobalSatisfaction(df):
    # Calculer la proportion globale de satisfaction
    satisfaction_proportion = df['Sentiment'].value_counts(normalize=True)['Positive']
    neutral_proportion = df['Sentiment'].value_counts(normalize=True)['Neutral']
    # Afficher la proportion
    print(f'Proportion globale de satisfaction : {satisfaction_proportion:.2%}')
    print(f'Proportion globale neutre : {neutral_proportion:.2%}')



# 2018
# Charger les données depuis le fichier Excel
df2018 = df_setup('extraction_finale_enquete_2018DS.xls')
df2018['Sentiment'] = df2018['Tokens'].apply(get_sentiment)
printGlobalSatisfaction(df2018)

# 2019 
# Charger les données depuis le fichier Excel
df2019 = df_setup('extraction_finale_enquete_2019DS.xlsx')
df2019['Sentiment'] = df2019['Tokens'].apply(get_sentiment)
printGlobalSatisfaction(df2019)

# 2021
# Charger les données depuis le fichier Excel
df2021 = df_setup('extraction_finale_enquete_2021DS.xlsx')
df2021['Sentiment'] = df2021['Tokens'].apply(get_sentiment)
printGlobalSatisfaction(df2021)


# 2022
# Charger les données depuis le fichier Excel
df2022 = df_setup('extraction_finale_enquete_2022_DS.xlsx')
df2022['Sentiment'] = df2022['Tokens'].apply(get_sentiment)
printGlobalSatisfaction(df2022)

# 2023
# Charger les données depuis le fichier Excel
df2023 = df_setup('Extraction finale_enquete 2023DS.xls')
df2023['Sentiment'] = df2023['Tokens'].apply(get_sentiment)
printGlobalSatisfaction(df2023)