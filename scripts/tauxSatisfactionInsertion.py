from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob import TextBlob
import matplotlib.pyplot as plt

#Variables
stop_words = set(stopwords.words('french'))  # Utilisez 'english' si vos données sont en anglais
annees = [0]*5
proportionSatisfaction = [0]*5
proportionNeutre = [0]*5
proportionNegatif= [0]*5
#Fonctions

# Fonction pour obtenir le sentiment
def get_sentiment(text):
    # Créer un objet TextBlob avec le pos_tagger et l'analyseur Pattern pour le français
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

    polarite, subjectivite = blob.sentiment

    # Déterminer le sentiment en fonction de la polarité
    if polarite > 0:
        return 'Positive'
    elif polarite < 0:
        return 'Negative'
    else:
        return 'Neutral'

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

    # Supprimer les stopwords
    df['Comments'] = df['Comments'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word.lower() not in stop_words]))
  
    return df

#Fonction qui affiche la satisfaction global
def printGlobalSatisfaction(df, annee):
    # Calculer la proportion globale de satisfaction
    satisfaction_proportion = df['Sentiment'].value_counts(normalize=True)['Positive']
    neutral_proportion = df['Sentiment'].value_counts(normalize=True)['Neutral']
    negative_proportion = df['Sentiment'].value_counts(normalize=True)['Negative']
    # Afficher la proportion
    print(f'Proportion globale de satisfaction : {satisfaction_proportion:.2%}')
    print(f'Proportion globale neutre : {neutral_proportion:.2%}')
    print(f'Proportion globale non satisfaction : {negative_proportion:.2%}')
    return satisfaction_proportion, neutral_proportion, negative_proportion, annee



# 2018
print('2018 :')
# Charger les données depuis le fichier Excel
df2018 = df_setup('datav2/extraction_finale_enquete_2018DS.xls')
df2018['Sentiment'] = df2018['Comments'].apply(get_sentiment)
proportionSatisfaction[0],proportionNeutre[0],proportionNegatif[0],annees[0] = printGlobalSatisfaction(df2018, 2018)

# 2019 
print('2019 :')
# Charger les données depuis le fichier Excel
df2019 = df_setup('datav2/extraction_finale_enquete_2019DS.xlsx')
df2019['Sentiment'] = df2019['Comments'].apply(get_sentiment)
proportionSatisfaction[1],proportionNeutre[1],proportionNegatif[1],annees[1] =printGlobalSatisfaction(df2019, 2019)

# 2020 
print('2020 :')
# Charger les données depuis le fichier Excel
df2020 = df_setup('datav2/extraction_finale_enquete_2020DS.xls')
df2020['Sentiment'] = df2019['Comments'].apply(get_sentiment)
proportionSatisfaction[1],proportionNeutre[1],proportionNegatif[1],annees[1] =printGlobalSatisfaction(df2020, 2020)


# 2021
print('2021 :')
# Charger les données depuis le fichier Excel
df2021 = df_setup('datav2/extraction_finale_enquete_2021DS.xlsx')
df2021['Sentiment'] = df2021['Comments'].apply(get_sentiment)
proportionSatisfaction[2],proportionNeutre[2],proportionNegatif[2],annees[2] =printGlobalSatisfaction(df2021, 2021)


# 2022
print('2022 :')
# Charger les données depuis le fichier Excel
df2022 = df_setup('datav2/extraction_finale_enquete_2022DS.xlsx')
df2022['Sentiment'] = df2022['Comments'].apply(get_sentiment)
proportionSatisfaction[3],proportionNeutre[3],proportionNegatif[3],annees[3] = printGlobalSatisfaction(df2022, 2022)

# 2023
print('2023 :')
# Charger les données depuis le fichier Excel
df2023 = df_setup('datav2/extraction_finale_enquete_2023DS.xls')
df2023['Sentiment'] = df2023['Comments'].apply(get_sentiment)
proportionSatisfaction[4],proportionNeutre[4],proportionNegatif[4],annees[4] =printGlobalSatisfaction(df2023, 2023)

# Tracer le graphique
plt.figure(figsize=(10, 6))
plt.plot(annees, proportionSatisfaction, marker='o', label='Satisfaction', linestyle='-', color='green')
plt.plot(annees, proportionNeutre, marker='o', label='Neutre', linestyle='-', color='orange')
plt.plot(annees, proportionNegatif, marker='o', label='Non satisfaction', linestyle='-', color='red')

# Ajouter des étiquettes et des titres
plt.title("Évolution de la satisfaction au fil du temps")
plt.xlabel("Année")
plt.ylabel("Proportion (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Afficher le graphique
plt.show()
