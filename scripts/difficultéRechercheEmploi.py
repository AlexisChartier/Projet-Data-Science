import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# Télécharger les stopwords
nltk.download('stopwords')
stop_words = stopwords.words('french')  # Convertir en liste

def load_and_preprocess_data(year):
    file_path = f'datav2/extraction_finale_enquete_{year}DS.' + ('xls' if year in [2018, 2020, 2023] else 'xlsx')
    df = pd.read_excel(file_path, engine='openpyxl' if year not in [2018, 2020, 2023] else None)

    # Supprimer les lignes avec des valeurs manquantes dans les commentaires
    df = df.dropna(subset=['Quelle(s) difficulté(s) rencontrez-vous dans votre recherche d\'emploi?'])

    # Appliquer le prétraitement
    df['Comments'] = df['Quelle(s) difficulté(s) rencontrez-vous dans votre recherche d\'emploi?'].str.lower()
    df['Comments'] = df['Comments'].str.replace(r'[^\w\s]', '')
    df['Comments'] = df['Comments'].fillna('')
    df['Comments'] = df['Comments'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word.lower() not in stop_words]))
  
    return df

# Charger et prétraiter les données pour chaque année
dataframes = [load_and_preprocess_data(year) for year in range(2018, 2024)]

# Concaténer les DataFrame
all_data = pd.concat(dataframes, ignore_index=True)  # Utiliser ignore_index pour réinitialiser l'index

# Prétraiter le texte pour la colonne 'Difficulté'
all_data['Difficulté'] = all_data['Quelle(s) difficulté(s) rencontrez-vous dans votre recherche d\'emploi?'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word.lower() not in stop_words]))

# Créer un modèle de sac de mots
vectorizer = CountVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(all_data['Difficulté'])

# Créer et ajuster le modèle LDA
lda = LatentDirichletAllocation(n_components=5)  # Le nombre de sujets est un hyperparamètre
lda.fit(X)

# Afficher les sujets
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic {topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

display_topics(lda, vectorizer.get_feature_names_out(), 10)
