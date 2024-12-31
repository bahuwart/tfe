import pandas as pd
import json
import numpy as np

# Chemin du fichier Excel
file_path = "tfe.xlsx"

# Lire le fichier Excel
data = pd.read_excel(file_path)

# Convertir les données en une liste de dictionnaires
user_data = data.to_dict(orient="records")

# Sauvegarder les données dans un fichier JSON
with open("users_data.json", "w") as json_file:
    json.dump(user_data, json_file, indent=4)

print("Données extraites et sauvegardées dans users_data.json")
