import json
import paramiko

# Informations de connexion SSH
ANSIBLE_HOST = "172.16.1.30"  # Adresse IP ou hostname du serveur Ansible
ANSIBLE_USER = "root"  # Utilisateur SSH
ANSIBLE_PASSWORD = "password"  # Mot de passe SSH (ou utiliser une clé privée pour plus de sécurité)
ANSIBLE_PATH = "/root/ansible-controller/inventory.ini"  # Chemin cible sur la machine distante

# Chemin du fichier JSON avec les données des utilisateurs
USER_DATA_FILE = "C:\\tfe\\users_data.json"  # Chemin du fichier JSON avec les données des utilisateurs

import json

def generate_inventory(USER_DATA_FILE):
    # Charger les données des utilisateurs depuis le fichier JSON
    try:
        with open(USER_DATA_FILE, 'r') as f:
            users_data = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
        return

    # Liste pour stocker les lignes du fichier inventory
    inventory_lines = ["[VMs]"]

    for user in users_data:
        username = user['Username']
        group = user['Group']

        # Extraire toutes les adresses IP en recherchant les clés qui commencent par "IP_Address"
        ip_addresses = [value for key, value in user.items() if key.startswith("IP_Address")]

        # Ajouter une ligne pour chaque adresse IP
        for ip_address in ip_addresses:
            # On peut ici ajouter des traitements supplémentaires pour gérer différentes plages d'IP
            # Pour cet exemple, je vais simplement créer des noms de VM avec les suffixes des adresses IP
            if group.lower() == 'etudiants':
                inventory_lines.append(f"{username}-VM{ip_address.split('.')[-2]}{ip_address.split('.')[-1]} ansible_host={ip_address} ansible_user=tfe ansible_password=password username={username}")
            elif group.lower() == 'professeurs':
                inventory_lines.append(f"{username}-VM{ip_address.split('.')[-2]}{ip_address.split('.')[-1]} ansible_host={ip_address} ansible_user=tfe ansible_password=password username={username}")

    # Sauvegarder le fichier inventory.ini
    inventory_content = "\n".join(inventory_lines)
    
    # Écrire dans le fichier inventory.ini localement avant de le transférer
    with open("inventory.ini", 'w') as f:
        f.write(inventory_content)
    
    print(f"Le fichier inventory.ini a été généré localement.")
    return "inventory.ini"


def update_inventory():
    # Générer le fichier inventory.ini
    inventory_file = generate_inventory(USER_DATA_FILE)
    
    if inventory_file:
        try:
            # Créer un objet SSHClient pour établir la connexion
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accepter les clés d'hôte non connues
            ssh.connect(ANSIBLE_HOST, username=ANSIBLE_USER, password=ANSIBLE_PASSWORD)


            # Ouvrir une session SFTP pour transférer le fichier
            sftp = ssh.open_sftp()
            sftp.put(inventory_file, ANSIBLE_PATH)  # Transférer le fichier
            sftp.close()  # Fermer la connexion SFTP

            print(f"Le fichier {inventory_file} a été mis à jour sur {ANSIBLE_HOST} à l'emplacement {ANSIBLE_PATH}.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'inventaire : {e}")
        finally:
            ssh.close()  # Toujours fermer la connexion SSH

def execute_playbook(update_console):
    """
    Exécute le playbook Ansible via SSH et redirige la sortie vers une console Tkinter.
    :param update_console: Fonction Tkinter pour mettre à jour la console.
    """
    # Commande à exécuter sur le contrôleur Ansible
    playbook_command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i /root/ansible-controller/inventory.ini /root/ansible-controller/playbook.yml"

    try:
        # Créer un objet SSHClient pour établir la connexion
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accepter les clés d'hôte non connues
        ssh.connect(ANSIBLE_HOST, username=ANSIBLE_USER, password=ANSIBLE_PASSWORD)

        # Supprimer le fichier known_hosts pour éviter les conflits
        update_console("Suppression du fichier known_hosts...")
        ssh.exec_command("rm -f ~/.ssh/known_hosts")

        # Exécuter la commande sur la machine distante
        update_console("Exécution de la commande ansible-playbook...")
        stdin, stdout, stderr = ssh.exec_command(playbook_command)

        # Lire la sortie et les erreurs en temps réel
        for line in iter(stdout.readline, ""):
            update_console(line.strip())

        for line in iter(stderr.readline, ""):
            update_console(line.strip(), error=True)

        update_console("La commande ansible-playbook a été exécutée avec succès.")

    except Exception as e:
        update_console(f"Erreur lors de l'exécution du playbook : {e}", error=True)

    finally:
        ssh.close()  # Toujours fermer la connexion SSH

update_inventory()