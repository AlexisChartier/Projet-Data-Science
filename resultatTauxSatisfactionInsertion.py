import matplotlib.pyplot as plt

# Données
annees = [2018, 2019, 2021, 2022, 2023]
proportion_satisfaction = [64.55, 63.35, 65.84, 57.00, 61.76]
proportion_neutre = [19.58, 21.47, 20.58, 22.71, 23.53]
proportion_non_satisfaction = [15.87, 15.18, 13.58, 20.29, 14.71]

# Tracer le graphique
plt.figure(figsize=(10, 6))
plt.plot(annees, proportion_satisfaction, marker='o', label='Satisfaction', linestyle='-', color='green')
plt.plot(annees, proportion_neutre, marker='o', label='Neutre', linestyle='-', color='orange')
plt.plot(annees, proportion_non_satisfaction, marker='o', label='Non satisfaction', linestyle='-', color='red')

# Ajouter des étiquettes et des titres
plt.title("Évolution de la satisfaction au fil du temps")
plt.xlabel("Année")
plt.ylabel("Proportion (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Afficher le graphique
plt.show()
