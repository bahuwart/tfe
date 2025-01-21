import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import ansibleIntegration
import json
import time
import pandas as pd
from deleteFromXLSX import deleteUsers
from terraformDestroyVMs import terraform_cleanup
from terraformTemplate import terraformCreateTemplates
from importXLSX import importData

# Version 1.0

def load_config(config_file):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Le fichier de configuration '{config_file}' est introuvable.")
    
    with open(config_file, "r") as file:
        return json.load(file)

# Charger la configuration
CONFIG_FILE = "C:\\tfe\\global_config.json"
config = load_config(CONFIG_FILE)

# Chemins des scripts à exécuter
EXPORT_AD_SCRIPT = config["EXPORT_AD_SCRIPT"]
DELETE_FROM_AD_SCRIPT = config["DELETE_FROM_AD_SCRIPT"]
APP_DIRECTORY = config["APP_DIRECTORY"]
EXCEL_FILE_PATH = config["EXCEL_FILE_PATH"]
DELETE_USERS_FILE = config["DELETE_USERS_FILE"]
DELETE_SOME_FROM_AD_SCRIPT = config["DELETE_SOME_FROM_AD_SCRIPT"]
USER_DATA_FILE = config["USER_DATA_FILE"]

# Fonction pour exécuter un script et afficher les sorties en temps réel
def execute_script(command):
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        for line in process.stdout:
            update_console(line.strip())
        for error in process.stderr:
            update_console(error.strip(), error=True)

        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    return "Success"

# Fonction pour exécuter l'import du fichier Excel et l'export dans AD
def import_and_export_excel():
    update_status("Import des utilisateurs depuis le fichier Excel...")
    importData(pd.read_excel(EXCEL_FILE_PATH))
    update_status("Les utilisateurs ont été importés depuis le fichier Excel.")

    update_status("Import des utilisateurs dans l'AD...")
    result = execute_script(f"powershell -ExecutionPolicy Bypass -File {EXPORT_AD_SCRIPT}")
    if "Error" in result:
        update_status("Échec de l'import des utilisateurs dans l'AD.")
        messagebox.showerror("Erreur", f"Échec de exportAD.ps1 : {result}")
        return
    update_status("Les utilisateurs ont bien été importés dans l'AD.")
    messagebox.showinfo("Succès", "Les utilisateurs ont été importés dans l'AD avec succès !")

# Fonction pour exécuter le script deleteFromAD.ps1
def delete_from_ad():
    update_status("Suppression des utilisateurs depuis l'AD...")
    result = execute_script(f"powershell -ExecutionPolicy Bypass -File {DELETE_FROM_AD_SCRIPT}")
    if "Error" in result:
        update_status("Échec de la suppression des utilisateurs depuis l'AD.")
        messagebox.showerror("Erreur", f"Échec de deleteFromAD.ps1 : {result}")
        return
    update_status("Les utilisateurs ont été supprimés avec succès depuis l'AD.")
    messagebox.showinfo("Succès", "Les utilisateurs ont été supprimés avec succès depuis l'AD !")
    time.sleep(2)
    try:
        with open(USER_DATA_FILE, 'w') as f:
            f.write('[]')
        print(f"Le fichier {USER_DATA_FILE} a été vidé avec succès.")
    except Exception as e:
        print(f"Erreur lors du vidage du fichier JSON : {e}")
    terraform_destroy()

# Fonction pour appliquer Terraform
def terraform_apply():
    terraformCreateTemplates()
    update_status("Lancement de la création des VM...")
    command = f"terraform apply -auto-approve"
    result = execute_script(f"cd {APP_DIRECTORY} && {command}")
    if "Error" in result:
        update_status("Échec de la création des VM.")
        messagebox.showerror("Erreur", f"Échec de terraform apply : {result}")
        return
    update_status("Les VM ont été créées avec succès !")
    messagebox.showinfo("Succès", "Les VM ont été créées avec succès !")

# Fonction pour appliquer Terraform (destruction)
def terraform_destroy():
    update_status("Suppression des VM...")
    command = f"terraform destroy -auto-approve"
    result = execute_script(f"cd {APP_DIRECTORY} && {command}")
    if "Error" in result:
        update_status("Échec de la suppression des VM.")
        messagebox.showerror("Erreur", f"Échec de terraform destroy : {result}")
        return
    update_status("Les VM ont été supprimées avec succès !")
    messagebox.showinfo("Succès", "Les VM ont été supprimées avec succès !")

# Fonction pour exécuter Ansible (update_inventory et execute_playbook)
def run_ansible():
    update_status("Mise à jour de l'inventaire...")
    try:
        ansibleIntegration.update_inventory()  # Appel à la fonction depuis le module
        update_status("Inventaire mis à jour avec succès.")

        update_status("Exécution de la configuration des VM...")
        ansibleIntegration.execute_playbook(update_console)  # Appel à la fonction depuis le module
        update_status("Configuration des VM terminée avec succès !")
        messagebox.showinfo("Succès", "Configuration des VM terminée avec succès !")
    except Exception as e:
        update_status("Échec de la configuration des VM.")
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution d'Ansible : {e}")

# Fonction pour mettre à jour le statut dans l'interface graphique
def update_status(message):
    status_label.config(text=message)
    root.update_idletasks()

# Fonction pour afficher les sorties dans la console Tkinter
def update_console(message, error=False):
    message = message.encode("utf-8", "ignore").decode("utf-8")
    console_text.insert(tk.END, message + "\n")
    console_text.see(tk.END)
    if error:
        console_text.tag_add("error", "end-2l", "end-1l")
        console_text.tag_config("error", foreground="red")
    root.update_idletasks()

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            dest_path = EXCEL_FILE_PATH
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.replace(file_path, dest_path)
            update_status(f"Fichier {os.path.basename(file_path)} ajouté et renommé en tfe.xlsx avec succès.")
            # Exécuter uniquement les deux scripts IMPORT_XLSX_SCRIPT et EXPORT_AD_SCRIPT
            import_and_export_excel()
        except Exception as e:
            update_status("Erreur lors de l'ajout du fichier : " + str(e))
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du fichier : {str(e)}")

def delete_selected_users():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            dest_path = DELETE_USERS_FILE
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.replace(file_path, dest_path)
            update_status(f"Fichier {os.path.basename(file_path)} ajouté et renommé en delete.xlsx avec succès.")
            deleteUsers(dest_path, USER_DATA_FILE)
            update_status("Suppression des utilisateurs dans l'AD...")
            result = execute_script(f"powershell -ExecutionPolicy Bypass -File {DELETE_SOME_FROM_AD_SCRIPT}")
            if "Error" in result:
                update_status("Échec de la suppression des utilisateurs dans l'AD.")
                messagebox.showerror("Erreur", f"Échec de deleteSomeFromAD.ps1 : {result}")
                return
            update_status("Les utilisateurs ont bien été supprimés de l'AD.")
            messagebox.showinfo("Succès", "Les utilisateurs ont été supprimés de l'AD avec succès !")
            time.sleep(2)
            update_status("suppression des VMs...")
            commands = terraform_cleanup(USER_DATA_FILE)
            for command in commands :
                result = execute_script(f"cd {APP_DIRECTORY} && {command}")
                if "Error" in result:
                    update_status("Échec de la suppression des VM.")
                    messagebox.showerror("Erreur", f"Échec de terraform destroy : {result}")
                    return
                update_status("Les VM ont été supprimées avec succès !")
                messagebox.showinfo("Succès", "Les VM ont été supprimées avec succès !")
            
        except Exception as e:
            update_status("Erreur lors de l'ajout du fichier : " + str(e))
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du fichier : {str(e)}")

# Interface graphique principale
root = tk.Tk()
root.title("Gestion des Scripts")

# Dimensions de la fenêtre
root.geometry("750x700")

# Widgets
label = tk.Label(root, text="Sélectionnez un fichier Excel à traiter :", font=("Arial", 14))
label.pack(pady=10)

select_button = tk.Button(root, text="Sélectionner un fichier", command=select_file, font=("Arial", 12))
select_button.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
status_label.pack(pady=10)

console_label = tk.Label(root, text="Console :", font=("Arial", 12))
console_label.pack(pady=5)

console_text = tk.Text(root, wrap="word", height=10, font=("Courier", 10))
console_text.pack(fill="both", expand=True, padx=10, pady=5)

# Créer un conteneur pour les boutons principaux
frame_buttons = tk.Frame(root)
frame_buttons.pack(side="top", fill="x", padx=10, pady=10)

# Ajouter les boutons principaux
exit_button = tk.Button(frame_buttons, text="Quitter", command=root.quit, font=("Arial", 12), bg="red", fg="white")
exit_button.pack(side="left", padx=5)

terraform_button = tk.Button(frame_buttons, text="Lancer la création des VM", command=terraform_apply, font=("Arial", 12), bg="green", fg="white")
terraform_button.pack(side="left", padx=5)

ansible_button = tk.Button(frame_buttons, text="Lancer la configuration des VM", command=run_ansible, font=("Arial", 12), bg="orange", fg="white")
ansible_button.pack(side="left", padx=5)

delete_button = tk.Button(frame_buttons, text="Supprimer VM & utilisateurs", command=delete_from_ad, font=("Arial", 12), bg="blue", fg="white")
delete_button.pack(side="right", padx=5)

frame_delete_users = tk.Frame(root)
frame_delete_users.pack(side="bottom", fill="x")

# Ajouter le bouton "Supprimer certains utilisateurs"
delete_users_button = tk.Button(
    frame_delete_users,
    text="Supprimer certains utilisateurs & VM",
    command=delete_selected_users,
    font=("Arial", 12),
    bg="purple",
    fg="white"
)
delete_users_button.pack(side="bottom", pady=10)

# Lancer l'application
root.mainloop()
