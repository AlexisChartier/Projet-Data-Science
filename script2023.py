from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd



# Charger les données depuis le fichier Excel
df = pd.read_excel('Extraction finale_enquete 2023DS.xls')

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

from textblob_fr import PatternTagger, PatternAnalyzer
from textblob import TextBlob
# Exemple de fonction pour obtenir le sentiment
def get_sentiment(text):
    # Créer un objet TextBlob avec le pos_tagger et l'analyseur Pattern pour le français
    blob = TextBlob(texte, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

    # Déterminer le sentiment en fonction de la polarité
    if blob.sentiment.polarity > 0:
        return 'Positif'
    elif blob.sentiment.polarity < 0:
        return 'Négatif'
    else:
        return 'Neutre'
    

# Appliquer la fonction à la colonne 'Comments'
df['Sentiment'] = df['Comments'].apply(get_sentiment)

# Calculer la proportion globale de satisfaction
satisfaction_proportion = df['Sentiment'].value_counts(normalize=True)['Positive']
neutral_proportion = df['Sentiment'].value_counts(normalize=True)['Neutral']
# Afficher la proportion
print(f'Proportion globale de satisfaction : {satisfaction_proportion:.2%}')
print(f'Proportion globale neutre : {neutral_proportion:.2%}')
from sklearn.feature_extraction.text import TfidfVectorizer

# Convertir les tokens en texte pour la vectorisation
df['Processed_Comments'] = df['Tokens'].apply(lambda x: ' '.join(x))

# Utiliser TfidfVectorizer pour créer une représentation vectorielle
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['Processed_Comments'])

from sklearn.cluster import KMeans

num_clusters = 5  # Nombre de thèmes à détecter (à ajuster selon votre besoin)
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

# Afficher les résultats
for cluster_num in range(num_clusters):
    print(f"Cluster {cluster_num + 1}:")
    cluster_comments = df[df['Cluster'] == cluster_num]['Comments']
    print(cluster_comments)
    print("\n")

import matplotlib.pyplot as plt
import seaborn as sns

# Supposons que vous ayez une colonne 'Sentiment' avec des valeurs comme 'Positif', 'Négatif', 'Neutre'
plt.figure(figsize=(8, 5))
sns.countplot(x='Formation', data=df)
plt.title('Distribution des sentiments dans les commentaires')
plt.show()