import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import ansibleIntegration  # Import du module contenant les fonctions Ansible

# Chemins des scripts à exécuter
IMPORT_XLSX_SCRIPT = "C:\\tfe\\importXLSX.py"
EXPORT_AD_SCRIPT = "C:\\tfe\\exportAD.ps1"
DELETE_FROM_AD_SCRIPT = "C:\\tfe\\deleteFromAD.ps1"
TERRAFORM_TEMPLATE_SCRIPT = "C:\\tfe\\terraformTemplate.py"
TERRAFORM_DIRECTORY = "C:\\tfe"  # Répertoire contenant les fichiers Terraform

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
    terraform_destroy()

# Fonction pour appliquer Terraform
def terraform_apply():
    update_status("Lancement de la création des VM...")
    command = f"terraform apply -auto-approve"
    result = execute_script(f"cd {TERRAFORM_DIRECTORY} && {command}")
    if "Error" in result:
        update_status("Échec de la création des VM.")
        messagebox.showerror("Erreur", f"Échec de terraform apply : {result}")
        return
    update_status("Les VM ont été créées avec succès !")
    messagebox.showinfo("Succès", "Les VM ont été créées avec succès !")
    show_ansible_button()  # Afficher le bouton pour Ansible

# Fonction pour appliquer Terraform
def terraform_destroy():
    update_status("Suppression des VM...")
    command = f"terraform destroy -auto-approve"
    result = execute_script(f"cd {TERRAFORM_DIRECTORY} && {command}")
    if "Error" in result:
        update_status("Échec de la suppression des VM.")
        messagebox.showerror("Erreur", f"Échec de terraform destroy : {result}")
        return
    update_status("Les VM ont été supprimées avec succès !")
    messagebox.showinfo("Succès", "Les VM ont été supprimées avec succès !")

# Fonction principale pour gérer le workflow
def process_workflow():
    console_text.delete(1.0, tk.END)  # Réinitialiser la console

    update_status("Import des utilisateurs depuis le fichier Excel...")
    result = execute_script(f"python {IMPORT_XLSX_SCRIPT}")
    if "Error" in result:
        update_status("Échec de l'import des utilisateurs du fichier Excel.")
        messagebox.showerror("Erreur", f"Échec de importXLSX.py : {result}")
        return
    update_status("Les utilisateurs ont été importés depuis le fichier Excel.")

    update_status("Import des utilisateurs dans l'AD...")
    result = execute_script(f"powershell -ExecutionPolicy Bypass -File {EXPORT_AD_SCRIPT}")
    if "Error" in result:
        update_status("Échec de l'import des utilisateurs dans l'AD.")
        messagebox.showerror("Erreur", f"Échec de exportAD.ps1 : {result}")
        return
    update_status("Les utilisateurs ont bien été importés dans l'AD.")

    update_status("Création des templates des VM des utilisateurs...")
    result = execute_script(f"python {TERRAFORM_TEMPLATE_SCRIPT}")
    if "Error" in result:
        update_status("Échec de la création des templates.")
        messagebox.showerror("Erreur", f"Échec de terraformTemplate.py : {result}")
        return
    update_status("Les templates ont été créés avec succès.")

    update_status("Tous les scripts ont été exécutés avec succès.")
    show_terraform_button()

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

def show_terraform_button():
    terraform_button.pack(side="left", padx=5)

def show_ansible_button():
    ansible_button.pack(side="left", padx=5)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            # Définir le nouveau chemin avec le nom de fichier tfe.xlsx
            dest_path = os.path.join("C:\\tfe", "tfe.xlsx")
            
            # Vérifier si le fichier existe déjà à cet emplacement et le supprimer si nécessaire
            if os.path.exists(dest_path):
                os.remove(dest_path)
            
            # Déplacer et renommer le fichier
            os.replace(file_path, dest_path)
            
            update_status(f"Fichier {os.path.basename(file_path)} ajouté et renommé en tfe.xlsx avec succès.")
            process_workflow()
        except Exception as e:
            update_status("Erreur lors de l'ajout du fichier : " + str(e))
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du fichier : {str(e)}")

            
# Interface graphique principale
root = tk.Tk()
root.title("Gestion des Scripts")

# Dimensions de la fenêtre
root.geometry("750x600")

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

# Créer un conteneur pour les boutons
frame_buttons = tk.Frame(root)
frame_buttons.pack(side="bottom", fill="x", padx=10, pady=10)

# Bouton Quitter (toujours visible, à gauche)
exit_button = tk.Button(frame_buttons, text="Quitter", command=root.quit, font=("Arial", 12), bg="red", fg="white")
exit_button.pack(side="left", padx=5)

# Boutons Terraform et Ansible (qui apparaîtront progressivement)
terraform_button = tk.Button(frame_buttons, text="Lancer la création des VM", command=terraform_apply, font=("Arial", 12), bg="green", fg="white")
terraform_button.pack_forget()  # Masqué au départ

ansible_button = tk.Button(frame_buttons, text="Lancer la configuration des VM", command=run_ansible, font=("Arial", 12), bg="orange", fg="white")
ansible_button.pack_forget()  # Masqué au départ

delete_button = tk.Button(frame_buttons, text="Supprimer VM & utilisateurs", command=delete_from_ad, font=("Arial", 12), bg="blue", fg="white")
delete_button.pack(side="right", padx=5)

# Lancer l'application
root.mainloop()
