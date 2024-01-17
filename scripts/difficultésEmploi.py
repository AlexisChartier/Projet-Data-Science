import pandas as pd
from pytest import console_main
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
from bertopic import BERTopic
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.io as pio

# Initialiser spacy pour la lemmatisation
nlp = spacy.load('fr_core_news_sm')

# Télécharger les stopwords
#nltk.download('stopwords')
stop_words = stopwords.words('french')

def preprocess_text(text):
    # Lemmatisation et suppression des stopwords
    doc = nlp(text)
    lemmatized = " ".join([token.lemma_ for token in doc if token.text.lower() not in stop_words])
    return lemmatized

def load_and_preprocess_data(year):
    file_path = f'datav2/extraction_finale_enquete_{year}DS.' + ('xls' if year in [2018, 2020, 2023] else 'xlsx')
    df = pd.read_excel(file_path, engine='openpyxl' if year not in [2018, 2020, 2023] else None)

    # Supprimer les lignes avec des valeurs manquantes dans les commentaires
    df = df.dropna(subset=['Quelle(s) difficulté(s) rencontrez-vous dans votre recherche d\'emploi?'])

    # Appliquer le prétraitement avancé
    df['Comments'] = df['Quelle(s) difficulté(s) rencontrez-vous dans votre recherche d\'emploi?'].apply(preprocess_text)
    return df

# Charger et prétraiter les données pour chaque année
dataframes = [load_and_preprocess_data(year) for year in range(2018, 2024)]

# Concaténer les DataFrame
all_data = pd.concat(dataframes, ignore_index=True)

# Vectorisation avec Bigrammes et Trigrammes
#vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words=stop_words)
#X = vectorizer.fit_transform(all_data['Comments'])

# Sort 'Comments' column of all_data by 'Formation' column
all_data_sorted = all_data.sort_values(by='Formation')
pio.renderers.default='iframe'
# Analyze topics with BERTopic
bertopic_model = BERTopic(language='multilingual', n_gram_range=(1,3))
topics, _ = bertopic_model.fit_transform(all_data_sorted['Comments'])
bertopic_model.get_topic_info()
# Visualize topics
fig1 = bertopic_model.visualize_topics(width=600, height=600)
fig1.write_html("results/difficultésEmploiTopics.html")
fig2 = bertopic_model.visualize_barchart(width=600, height=600)
fig2.write_html("results/difficultésEmploiBarchart.html")



