import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Charger les données depuis le fichier Excel
# years = range(2018, 2024)
#dfs = []
#Test
#for year in years:
#    df = pd.read_excel('chemin/vers/votre/fichier/Data_{}.xlsx'.format(year))
#    dfs.append(df)

# Concaténer les données de toutes les années
#df = pd.concat(dfs, ignore_index=True)

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

df['Comments'] = df['Comments'].fillna('')


# Tokenization
df['Tokens'] = df['Comments'].apply(word_tokenize)

# Supprimer les stopwords
stop_words = set(stopwords.words('french'))  # Utilisez 'english' si vos données sont en anglais
df['Tokens'] = df['Tokens'].apply(lambda x: [word for word in x if word.lower() not in stop_words])

text_data = df['Comments'].astype(str)





stop_words_french = [
    'à', 'à demi', 'à peine', 'à peu près', 'absolument', 'actuellement', 'ainsi', 'alors', 'apparemment', 'approximativement',
    'après', 'après-demain', 'assez', 'assurément', 'au', 'aucun', 'aucunement', 'aucuns', "aujourd'hui", 'auparavant', 'aussi',
    'aussitôt', 'autant', 'autre', 'autrefois', 'autrement', 'avant', 'avant-hier', 'avec', 'avoir',
    'beaucoup', 'bien', 'bientôt', 'bon',
    'c', 'ça', 'car', 'carrément', 'ce', 'cela', 'cependant', 'certainement', 'certes', 'ces', 'ceux', 'chaque', 'ci', 'comme',
    'comment', 'complètement',
    'd', "d'abord", 'dans', 'davantage', 'de', 'début', 'dedans', 'dehors', 'déjà', 'demain', 'depuis', 'derechef', 'des',
    'désormais', 'deux', 'devrait', 'diablement', 'divinement', 'doit', 'donc', 'dorénavant', 'dos', 'droite', 'drôlement', 'du',
    'elle', 'elles', 'en', 'en vérité', 'encore', 'enfin', 'ensuite', 'entièrement', 'entre-temps', 'environ', 'essai', 'est',
    'et', 'étaient', 'état', 'été', 'étions', 'être', 'eu', 'extrêmement',
    'fait', 'faites', 'fois', 'font', 'force',
    'grandement', 'guère',
    'habituellement', 'haut', 'hier', 'hors',
    'ici', 'il', 'ils', 'infiniment', 'insuffisamment',
    'jadis', 'jamais', 'je', 'joliment',
    'ka',
    'la', 'là', 'le', 'les', 'leur', 'leurs', 'lol', 'longtemps', 'lors',
    'ma', 'maintenant', 'mais', 'mdr', 'même', 'mes', 'moins', 'mon', 'mot',
    'naguère', 'ne', 'ni', 'nommés', 'non', 'notre', 'nous', 'nouveaux', 'nullement',
    'ou', 'où', 'oui',
    'par', 'parce', 'parfois', 'parole', 'pas', 'pas mal', 'passablement', 'personne', 'personnes', 'peu', 'peut', 'peut-être',
    'pièce', 'plupart', 'plus', 'plutôt', 'point', 'pour', 'pourquoi', 'précisément', 'premièrement', 'presque', 'probablement',
    'prou', 'puis',
    'quand', 'quasi', 'quasiment', 'que', 'quel', 'quelle', 'quelles', 'quelque', 'quelquefois', 'quels', 'qui', 'quoi', 'quotidiennement',
    'rien', 'rudement',
    's', 'sa', 'sans', 'sans doute', 'ses', 'seulement', 'si', 'sien', 'sitôt', 'soit', 'son', 'sont', 'soudain', 'sous', 'souvent',
    'soyez', 'subitement', 'suffisamment', 'sur',
    't', "t'", 'ta', 'tandis', 'tant', 'tantôt', 'tard', 'tellement', 'tellement', 'tels', 'terriblement', 'tes', 'ton', 'tôt',
    'totalement', 'toujours', 'tous', 'tout', 'tout à fait', 'toutefois', 'très', 'trop', 'tu',
    'un', 'une',
    'valeur', 'vers', 'voie', 'voient', 'volontiers', 'vont', 'votre', 'vous', 'vraiment', 'vraisemblablement'
]


# Vectorisation du texte avec TF-IDF
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words=stop_words_french)
tfidf_matrix = vectorizer.fit_transform(text_data)

# Modèle LDA (Latent Dirichlet Allocation)
num_topics = 3  # Choisir le nombre de thèmes souhaité
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(tfidf_matrix)

# Afficher les mots clés par thème
feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    print(f"Thème #{topic_idx + 1} : {', '.join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]])}")
    print()

# Ajouter une colonne au dataframe pour stocker les thèmes attribués à chaque texte
df['Theme'] = lda.transform(tfidf_matrix).argmax(axis=1)

# Visualisation de la distribution des thèmes
plt.figure(figsize=(10, 6))
sns.countplot(x='Theme', data=df)
plt.title('Distribution des thèmes')
plt.show()
