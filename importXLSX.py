import pandas as pd
import json
import random
import string
import os

def load_config(config_file):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Le fichier de configuration '{config_file}' est introuvable.")
    
    with open(config_file, "r") as file:
        return json.load(file)

# Charger la configuration
CONFIG_FILE = "C:\\tfe\\global_config.json"
config = load_config(CONFIG_FILE)

VM_NUMBERS = config["VM_NUMBERS"]
EXCEL_FILE_PATH = config["EXCEL_FILE_PATH"]
USERS_DATA_FILE = config["USER_DATA_FILE"]

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


# Lire le fichier Excel
data = pd.read_excel(EXCEL_FILE_PATH)

existing_data = load_existing_data(USERS_DATA_FILE)

# Extraire tous les usernames existants
existing_usernames = {user["Username"] for user in existing_data}

# Extraire toutes les combinaisons "Name" et "Surname" existantes
existing_full_names = {(user["Name"], user["Surname"]) for user in existing_data}

# Extraire toutes les adresses IP utilisées
used_ips = set()
for user in existing_data:
    # Parcourir toutes les clés et ajouter les adresses IP trouvées
    used_ips.update(value for key, value in user.items() if key.startswith("IP_Address") and value)


# Transformer les données
transformed_data = existing_data.copy()

# Vérifier et compléter les adresses IP si nécessaire
def ensure_correct_ip_count(user, group, used_ips):
    """Vérifie et ajoute les adresses IP manquantes pour un utilisateur."""
    # Récupérer les adresses IP existantes
    ip_addresses = [user[key] for key in user if key.startswith("IP_Address") and user[key]]
    num_existing_ips = len(ip_addresses)

    # Nombre d'adresses IP requis pour le groupe
    num_required_ips = VM_NUMBERS.get(group.lower(), 1)

    # Si le nombre d'IP existantes est inférieur à ce qui est requis, en ajouter
    if num_existing_ips < num_required_ips:
        for _ in range(num_required_ips - num_existing_ips):
            new_ip = generate_ip_address(group, used_ips)
            ip_addresses.append(new_ip)

    # Mettre à jour les clés dans le dictionnaire utilisateur
    for i, ip in enumerate(ip_addresses):
        if i == 0:
            user["IP_Address"] = ip  # La première IP reste sous la clé "IP_Address"
        else:
            user[f"IP_Address{i+1}"] = ip  # Les autres IP utilisent des clés IP_Address2, IP_Address3, etc.

    return user

# Vérifier les utilisateurs existants pour compléter leurs adresses IP
for user in existing_data:
    group = user["Group"]
    ensure_correct_ip_count(user, group, used_ips)

# Transformer les nouvelles données
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
    num_ips = VM_NUMBERS.get(group.lower(), 1)  # Par défaut, 1 adresse IP pour les groupes non spécifiés

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
        "IP_Address": ip_addresses[0]  # Toujours inclure la première IP sous "IP_Address"
    }

    # Ajouter les adresses IP supplémentaires si nécessaire
    if num_ips > 1:
        for i, ip in enumerate(ip_addresses[1:], start=2):
            user_data[f"IP_Address{i}"] = ip

    return user_data

def importData() : 
    for _, row in data.iterrows():
        new_user = transform_row(row)
        if new_user:  # Ajouter uniquement les nouveaux utilisateurs
            transformed_data.append(new_user)
            existing_full_names.add((new_user["Name"], new_user["Surname"]))

    # Sauvegarder les données dans un fichier JSON
    with open(USERS_DATA_FILE, "w") as json_file:
        json.dump(transformed_data, json_file, indent=4)

    print("Données extraites et ajoutées dans users_data.json")
