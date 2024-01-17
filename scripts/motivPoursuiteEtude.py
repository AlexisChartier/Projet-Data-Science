import pandas as pd
import spacy
import nltk as nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import seaborn as sns
from wordcloud import WordCloud
from bertopic import BERTopic
import matplotlib.pyplot as plt
import plotly.io as pio

# Initialisation
nlp = spacy.load('fr_core_news_sm')
stop_words = set(stopwords.words('french'))
sia = SentimentIntensityAnalyzer()

# Fonction de prétraitement
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', str(text).lower())
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if token.text not in stop_words and token.is_alpha]
    return ' '.join(lemmas)

# Fonction pour tracer le top des mots-clés TF-IDF
def plot_top_words(df_tfidf, top_n=10, title="Top TF-IDF Words"):
    # Somme des scores TF-IDF pour chaque mot
    word_sums = df_tfidf.sum(axis=0)
    top_words = word_sums.sort_values(ascending=False).head(top_n)
    
    # Création du graphique
    plt.figure(figsize=(10, 6))
    top_words.plot(kind='bar')
    plt.title(title)
    plt.ylabel('Sum of TF-IDF Scores')
    plt.xticks(rotation=45)
    plt.show()

# Charger et prétraiter les données
all_data = pd.DataFrame()
years = [2018, 2019, 2020, 2021, 2022, 2023]

for year in years:
    file_path = f'datav2/extraction_finale_enquete_{year}DS.' + ('xls' if year in [2018, 2020, 2023] else 'xlsx')
    df = pd.read_excel(file_path)
    df = df.dropna(subset=['Pour quelle raison avez-vous principalement choisi de poursuivre des études ?'])
    df['Texte_Traité'] = df['Pour quelle raison avez-vous principalement choisi de poursuivre des études ?'].apply(preprocess_text)
    df['Year'] = year
    all_data = all_data._append(df[['Texte_Traité', 'Year','Formation']], ignore_index=True)



# Analyze topics with BERTopic
bertopic_model = BERTopic(language='multilingual', n_gram_range=(1,3))
topics, _ = bertopic_model.fit_transform(all_data['Texte_Traité'])
bertopic_model.get_topic_info()

# Visualize topics
fig1 = bertopic_model.visualize_topics(width=600, height=600)
fig1.write_html("results/topicsPoursuiteEtude.html")
fig2 = bertopic_model.visualize_barchart(width=600, height=600)
fig2.write_html("results/barchartPoursuiteEtude.html")
