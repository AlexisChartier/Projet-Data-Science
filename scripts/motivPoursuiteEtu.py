import pandas as pd
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import matplotlib.pyplot as plt


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
    all_data = all_data._append(df[['Texte_Traité', 'Year']], ignore_index=True)

# Analyse de Sentiment
all_data['Sentiment'] = all_data['Texte_Traité'].apply(lambda x: sia.polarity_scores(x)['compound'])

# TF-IDF avec Bigrammes et Trigrammes
vectorizer = TfidfVectorizer(ngram_range=(1, 3))
tfidf_matrix = vectorizer.fit_transform(all_data['Texte_Traité'])
feature_names = vectorizer.get_feature_names_out()
dense = tfidf_matrix.todense()
denselist = dense.tolist()
df_tfidf = pd.DataFrame(denselist, columns=feature_names)
# Appel de la fonction pour afficher le graphique
plot_top_words(df_tfidf, top_n=10, title="Top 10 TF-IDF Words")

# Afficher les résultats
top_n = 10
for col in df_tfidf.columns:
    print(f"Top {top_n} mots-clés pour '{col}':")
    top_keywords = df_tfidf[col].sort_values(ascending=False).head(top_n)
    print(top_keywords)
    print("\n")



