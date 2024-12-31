import pandas as pd
import json
import random
import string
import os

# Variable de configuration pour déterminer le nombre d'adresses IP par groupe
IP_CONFIG = {
    "etudiants": 2,  # 2 adresses IP pour les étudiants
    "professeurs": 1,  # 1 adresse IP pour les professeurs
    # Ajoutez d'autres groupes si nécessaire
}

# Fonction pour générer un mot de passe aléatoire de 12 caractères
def generate_password(length=12):
    if length < 4:
        raise ValueError("La longueur du mot de passe doit être d'au moins 4 caractères.")

    password = [random.choice(string.ascii_uppercase),  # Une majuscule
                random.choice(string.ascii_lowercase),  # Une minuscule
                random.choice(string.digits),          # Un chiffre
                '?']                                   # Le caractère spécial

    # Compléter le reste des caractères avec des chiffres, des majuscules et des minuscules
    password += random.choices(string.ascii_letters + string.digits, k=length - 4)

    # Mélanger les caractères pour éviter un ordre prévisible
    random.shuffle(password)

    return ''.join(password)

# Fonction pour générer une adresse IP unique
def generate_ip_address(group, used_ips):
    while True:
        if group.lower() == "etudiants":
            ip_start = 10
            ip_middle = 0
            ip_third = 10
            ip_last = random.randint(10, 250)
        elif group.lower() == "professeurs":
            ip_start = 10
            ip_middle = 0
            ip_third = 20
            ip_last = random.randint(10, 250)
        else:
            raise ValueError("Groupe inconnu : ", group)
        
        ip_address = f"{ip_start}.{ip_middle}.{ip_third}.{ip_last}"
        
        # Vérifier si l'IP est déjà utilisée
        if ip_address not in used_ips:
            used_ips.add(ip_address)
            return ip_address

# Charger les données JSON existantes
def load_existing_data(json_path):
    if os.path.exists(json_path):
        with open(json_path, "r") as json_file:
            return json.load(json_file)
    return []

# Vérifier et ajuster les usernames pour éviter les doublons et identifier les mêmes utilisateurs
def ensure_unique_username(name, surname, existing_usernames):
    base_username = f"{name[0].lower()}{surname.lower()}"
    if base_username not in existing_usernames:
        existing_usernames.add(base_username)
        return base_username

    # Si le username existe déjà, ajouter la deuxième lettre du prénom
    modified_username = f"{name[:2].lower()}{surname.lower()}"
    while modified_username in existing_usernames:
        name_prefix_length = len(modified_username) - len(surname) + 1
        modified_username = f"{name[:name_prefix_length].lower()}{surname.lower()}"

    existing_usernames.add(modified_username)
    return modified_username

# Chemin du fichier Excel
file_path = "tfe.xlsx"
json_file_path = "users_data.json"

# Lire le fichier Excel
data = pd.read_excel(file_path)

# Charger les données JSON existantes
existing_data = load_existing_data(json_file_path)
existing_usernames = {user["Username"] for user in existing_data}
existing_full_names = {(user["Name"], user["Surname"]) for user in existing_data}
used_ips = {user["IP_Address"] for user in existing_data}

# Ajouter les deuxièmes IP si elles existent
used_ips.update(user.get("IP_Address2", "") for user in existing_data if "IP_Address2" in user)

# Transformer les données
transformed_data = existing_data.copy()

def transform_row(row):
    name = row["Name"]
    surname = row["Surname"]
    group = row["Group"]

    # Si l'utilisateur existe déjà (même prénom et nom), on le saute
    if (name, surname) in existing_full_names:
        return None

    username = ensure_unique_username(name, surname, existing_usernames)
    
    # Générer l'adresse IP principale
    ip_address = generate_ip_address(group, used_ips)

    # Nombre d'adresses IP à attribuer en fonction du groupe
    num_ips = IP_CONFIG.get(group.lower(), 1)  # Par défaut, 1 adresse IP pour les groupes non spécifiés

    # Générer des adresses IP supplémentaires si nécessaire
    ip_addresses = [ip_address]
    for _ in range(num_ips - 1):
        ip_addresses.append(generate_ip_address(group, used_ips))

    # Créer le dictionnaire de données pour l'utilisateur
    user_data = {
        "Name": name,
        "Surname": surname,
        "Group": group,
        "Username": username,
        "Password": generate_password(),
        "IP_Address": ip_addresses[0]  # Toujours inclure la première IP
    }

    # Ajouter les adresses IP supplémentaires si nécessaire
    if num_ips > 1:
        for i, ip in enumerate(ip_addresses[1:], start=2):
            user_data[f"IP_Address{i}"] = ip

    return user_data

# Appliquer la transformation ligne par ligne
for _, row in data.iterrows():
    new_user = transform_row(row)
    if new_user:  # Ajouter uniquement les nouveaux utilisateurs
        transformed_data.append(new_user)
        existing_full_names.add((new_user["Name"], new_user["Surname"]))

# Sauvegarder les données dans un fichier JSON
with open(json_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=4)

print("Données extraites et ajoutées dans users_data.json")
