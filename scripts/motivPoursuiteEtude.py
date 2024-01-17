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
import matplotlib.pyplot as plt
nltk.download('vader_lexicon')

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

# Créer une matrice TF-IDF avec ngram range 1-2
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_matrix = tfidf_vectorizer.fit_transform(all_data['Texte_Traité'])

# Obtenir les mots les plus fréquents par filière
top_n = 10
for formation in all_data['Formation'].unique():
    print(f"Top {top_n} mots les plus fréquents pour la filière '{formation}':")
    formation_data = all_data[all_data['Formation'] == formation]
    formation_tfidf_matrix = tfidf_matrix[formation_data.index]
    word_scores = pd.DataFrame(formation_tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out()).sum().sort_values(ascending=False)
    top_words = word_scores.head(top_n)
    print(top_words)
    print("\n")

    # Création du graphique à barres
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_words.index, y=top_words.values)
    plt.title(f"Top {top_n} mots les plus fréquents pour la filière '{formation}'")
    plt.xlabel('Mots')
    plt.ylabel('Somme des scores TF-IDF')
    plt.xticks(rotation=45)
    plt.show()

# Création du nuage de mots global
all_text = ' '.join(all_data['Texte_Traité'])
wordcloud = WordCloud(width=800, height=400).generate(all_text)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots global')
plt.show()


