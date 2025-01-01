import pandas as pd
import json

# Charger les utilisateurs depuis le fichier XLSX
def load_xlsx_users(xlsx_file):
    """
    Charge les utilisateurs depuis un fichier Excel et retourne un ensemble de tuples (Name, Surname).
    """
    try:
        df = pd.read_excel(xlsx_file)
        if 'Name' not in df.columns or 'Surname' not in df.columns:
            raise ValueError("Les colonnes 'Name' et 'Surname' sont manquantes dans le fichier XLSX.")
        # Retourner un ensemble de tuples (Name, Surname)
        return set(zip(df['Name'], df['Surname']))  # Création de tuples pour chaque utilisateur
    except Exception as e:
        print(f"Erreur lors du chargement du fichier XLSX : {e}")
        return set()

# Charger les utilisateurs depuis le fichier JSON
def load_json_users(users_data_file):
    """
    Charge les utilisateurs depuis un fichier JSON et retourne une liste d'utilisateurs.
    """
    try:
        with open(users_data_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier JSON : {e}")
        return []

# Supprimer les utilisateurs en fonction des Name et Surname
def delete_users(users, users_to_delete):
    """
    Supprime les utilisateurs de la liste 'users' si leur (Name, Surname) est dans 'users_to_delete'.
    Retourne la liste des utilisateurs après suppression.
    """
    users_after_deletion = []
    for user in users:
        user_name_surname = (user['Name'], user['Surname'])
        if user_name_surname not in users_to_delete:
            users_after_deletion.append(user)
        else:
            print(f"Utilisateur {user['Name']} {user['Surname']} supprimé.")
    return users_after_deletion

# Sauvegarder les utilisateurs après suppression dans un fichier JSON
def save_users_to_json(users, users_data_file):
    """
    Sauvegarde les utilisateurs dans le fichier JSON après modification.
    """
    try:
        with open(users_data_file, 'w') as f:
            json.dump(users, f, indent=4)
        print(f"Les utilisateurs ont été mis à jour et enregistrés dans {users_data_file}.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier JSON : {e}")



def deleteUsers(delete_file, users_data_file):

    users_to_delete = load_xlsx_users(delete_file)
    users = load_json_users(users_data_file)
    updated_users = delete_users(users, users_to_delete)
    save_users_to_json(updated_users, users_data_file)