import pandas as pd
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
#from bertopic import BERTopic
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Initialiser spacy pour la lemmatisation
nlp = spacy.load('fr_core_news_sm')

# Télécharger les stopwords
nltk.download('stopwords')
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
vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words=stop_words)
X = vectorizer.fit_transform(all_data['Comments'])

# Analyse de thèmes avec NMF
nmf = NMF(n_components=5, random_state=42)
nmf.fit(X)

feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(nmf.components_):
    print(f"Topic {topic_idx}:")
    print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))

#bertopic_model = BERTopic(language='french')
#topics, _ = bertopic_model.fit_transform(all_data['Comments'])

for topic_idx in range(nmf.n_components):
    words = dict(zip(feature_names, nmf.components_[topic_idx]))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(words)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Topic {topic_idx}")
    plt.show()

#bertopic_model.visualize_topics()



