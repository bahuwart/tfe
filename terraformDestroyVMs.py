import json
import subprocess

# Charger les utilisateurs depuis le fichier JSON
def load_json_users(json_file):
    """
    Charge les utilisateurs depuis un fichier JSON et retourne un ensemble des usernames.
    """
    try:
        with open(json_file, 'r') as f:
            users = json.load(f)
            # Retourner un ensemble de usernames actifs
            return {user['Username'] for user in users}
    except Exception as e:
        print(f"Erreur lors du chargement du fichier JSON : {e}")
        return set()

# Lister les ressources Terraform
def list_terraform_resources():
    """
    Liste toutes les ressources Terraform et retourne les noms des ressources.
    """
    try:
        result = subprocess.run(["terraform", "state", "list"], capture_output=True, text=True, check=True)
        resources = result.stdout.splitlines()
        return resources
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande Terraform : {e}")
        return []

# Supprimer une ressource via Terraform
def destroy_terraform_resource(resource_name):
    """
    Supprime une ressource spécifique via Terraform destroy.
    """
    try:
        subprocess.run(["terraform", "destroy", "-target", resource_name, "-auto-approve"], check=True)
        print(f"Ressource {resource_name} supprimée avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la suppression de la ressource {resource_name} : {e}")

# Extraire le nom d'utilisateur de la ressource Terraform
def extract_username_from_resource(resource_name):
    """
    Extrait le nom d'utilisateur du nom de la ressource Terraform (par exemple proxmox_vm_qemu.mlavoine-VM1087 -> mlavoine).
    """
    parts = resource_name.split('.')
    if len(parts) >= 2:
        username_vm = parts[1]  # Après "proxmox_vm_qemu."
        username = username_vm.split('-')[0]  # Extraire la partie avant le "-"
        return username
    return None

# Vérifier les ressources à supprimer
def check_and_destroy_unused_resources(users, resources):
    """
    Vérifie les ressources et supprime celles qui correspondent à des utilisateurs qui ne sont plus actifs.
    """
    for resource in resources:
        username = extract_username_from_resource(resource)
        if username and username not in users:
            # Si l'utilisateur n'est plus dans le fichier JSON, on détruit la ressource
            print(f"L'utilisateur {username} n'est plus actif. Suppression de la ressource {resource}.")
            destroy_terraform_resource(resource)
        else:
            print(f"La ressource {resource} appartient à un utilisateur actif ({username}). Aucun changement effectué.")

def terraform_cleanup(json_file):
    """
    Génère une liste de commandes Terraform pour supprimer les ressources inutiles.
    """
    # Charger les utilisateurs actifs depuis le fichier JSON
    active_users = load_json_users(json_file)
    
    # Lister toutes les ressources Terraform
    resources = list_terraform_resources()
    
    # Créer une liste de commandes Terraform pour supprimer les ressources inutilisées
    commands = []
    
    for resource in resources:
        username = extract_username_from_resource(resource)
        if username and username not in active_users:
            # Si l'utilisateur n'est plus dans le fichier JSON, ajouter la commande de suppression
            commands.append(f"terraform destroy -target {resource} -auto-approve")
        else:
            # Sinon, on peut éventuellement ajouter un message pour un log
            print(f"La ressource {resource} appartient à un utilisateur actif ({username}). Aucun changement effectué.")
    
    # Retourner la liste de commandes à exécuter
    return commands