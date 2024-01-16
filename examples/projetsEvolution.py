import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy
from collections import Counter
import re

# Charger le modèle spaCy pour le traitement du texte en français
nlp = spacy.load("fr_core_news_sm")

def extract_themes(text):
    # Utiliser spaCy pour le traitement du texte
    doc = nlp(text)

    # Extraire les entités nommées (NER) et compter leur fréquence
    themes = [ent.text.lower() for ent in doc.ents if ent.label_ == "MISC" or ent.label_ == "ORG"]
    theme_counter = Counter(themes)

    # Retourner les thèmes les plus fréquents
    return theme_counter

def generate_wordcloud(text_counter, title):
    if len(text_counter) != 0:
        # Générer le nuage de mot
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(text_counter)

        # Afficher le nuage de mots
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(title)
        plt.show()

def clean_text(text):
    if pd.isna(text):
        return ''
    # Supprimer les caractères indésirables, y compris les retours chariot et les espaces en fin de mot
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', str(text))
    # Remplacer les sauts de ligne par des espaces
    cleaned_text = cleaned_text.replace('\n', ' ').replace('\r', '')
    return cleaned_text.strip()

def main():
    # Liste des années à analyser
    annees = [2018,2019,2020,2021, 2022, 2023]

    # Dictionnaire pour stocker les thèmes globaux par filière
    themes_globaux_par_filiere = {}


    for annee in annees:
        if annee == 2023 or annee == 2018 or annee  == 2020:
            fichier_excel = f'datav2/extraction_finale_enquete_{annee}DS.xls'
            df = pd.read_excel(fichier_excel)
        else:
            # Charger les données depuis le fichier Excel
            fichier_excel = f'datav2/extraction_finale_enquete_{annee}DS.xlsx'
            df = pd.read_excel(fichier_excel, engine='openpyxl')


        df["Quels sont vos projets d'évolution de carrière ?"] = df["Quels sont vos projets d'évolution de carrière ?"].apply(clean_text)
        
        # Extraire les données textuelles
        textes_projets_evolution = df["Quels sont vos projets d'évolution de carrière ?"].dropna()

        # Concaténer tous les textes en une seule chaîne
        texte_global = " ".join(textes_projets_evolution)

        # Extraire les thèmes
        themes_counter = extract_themes(texte_global)

        # Générer et afficher le nuage de mots
        generate_wordcloud(themes_counter, f"Nuage de mots des thèmes en {annee}")

    for annee in annees:
        if annee == 2023 or annee == 2018 or annee  == 2020:
            fichier_excel = f'datav2/extraction_finale_enquete_{annee}DS.xls'
            df = pd.read_excel(fichier_excel)
        else:
            # Charger les données depuis le fichier Excel
            fichier_excel = f'datav2/extraction_finale_enquete_{annee}DS.xlsx'
            df = pd.read_excel(fichier_excel, engine='openpyxl')

        # Liste des filières dans le DataFrame
        filieres = df['Formation'].unique()

        for filiere in filieres:
            if filiere not in themes_globaux_par_filiere:
                themes_globaux_par_filiere[filiere] = themes_counter.copy()
            else:
                themes_globaux_par_filiere[filiere] += themes_counter

        for filiere in filieres:
            # Filtrer le DataFrame par filière
            df_filiere = df[df['Formation'] == filiere]

            # Nettoyer la colonne des projets d'évolution de carrière
            df_filiere.loc[:, "Quels sont vos projets d'évolution de carrière ?"] = df_filiere["Quels sont vos projets d'évolution de carrière ?"].apply(clean_text)

            # Extraire les données textuelles
            textes_projets_evolution = df_filiere["Quels sont vos projets d'évolution de carrière ?"].dropna()

            # Concaténer tous les textes en une seule chaîne
            texte_global = " ".join(textes_projets_evolution)

            # Extraire les thèmes
            themes_counter = extract_themes(texte_global)

            # Générer et afficher le nuage de mots pour chaque filière et année
            generate_wordcloud(themes_counter, f"Nuage de mots des thèmes en {filiere} - {annee}")
                # Générer et afficher le nuage de mots global pour chaque filière
    for filiere, themes_counter in themes_globaux_par_filiere.items():
        generate_wordcloud(themes_counter, f"Nuage de mots des thèmes en {filiere} - Global")

if __name__ == "__main__":
    main()
