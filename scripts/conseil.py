import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords

# Initialisation
nlp = spacy.load('fr_core_news_sm')
nltk.download('stopwords')
french_stop_words = stopwords.words('french')
sia = SentimentIntensityAnalyzer()

# Fonction de prétraitement
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', str(text).lower())
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if token.text not in french_stop_words and token.is_alpha]
    return ' '.join(lemmas)

# Charger et prétraiter les données
all_data = pd.DataFrame()
years = [2018, 2019, 2020, 2021, 2022, 2023]

for year in years:
    file_path = f'datav2/extraction_finale_enquete_{year}DS.' + ('xls' if year in [2018, 2020, 2023] else 'xlsx')
    df = pd.read_excel(file_path)
    df = df.dropna(subset=['Quels conseils pourriez-vous donner aux étudiants actuellement en formation pour bien choisir leur stage de fin d\'étude ? réussir leur insertion professionnelle ?'])
    df['Texte_Traité'] = df['Quels conseils pourriez-vous donner aux étudiants actuellement en formation pour bien choisir leur stage de fin d\'étude ? réussir leur insertion professionnelle ?'].apply(preprocess_text)
    df['Year'] = year
    all_data = all_data._append(df[['Texte_Traité', 'Year']], ignore_index=True)

# Analyse de Sentiment
all_data['Sentiment'] = all_data['Texte_Traité'].apply(lambda x: sia.polarity_scores(x)['compound'])

# TF-IDF et NMF pour l'analyse thématique
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words=french_stop_words, ngram_range=(1, 3))
tfidf = vectorizer.fit_transform(all_data['Texte_Traité'])
nmf = NMF(n_components=5, random_state=1).fit(tfidf)

# Visualisation des thèmes avec Word Cloud
for topic_idx, topic in enumerate(nmf.components_):
    print(f"Topic {topic_idx}:")
    wordcloud = WordCloud(stopwords='french', background_color='white').generate_from_frequencies(dict(zip(vectorizer.get_feature_names_out(), topic)))
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"Topic {topic_idx}")
    plt.show()
