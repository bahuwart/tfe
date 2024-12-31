import pandas as pd
import os

# Charger le fichier Excel
def load_excel(file_path):
    return pd.read_excel(file_path)

# Générer le fichier Terraform pour chaque utilisateur
def generate_terraform_resources(data, output_file):
    with open(output_file, "w") as tf_file:

        tf_file.write(
"""
variable "admin_login" {
type = string
}

variable "admin_password" {
type = string
}
"""
            )

        for _, row in data.iterrows():
            username = row["Username"]
            first_name = row["Name"]
            last_name = row["Surname"]
            mac_address = row["MAC_Address"]
            group = row["Group"]

            # Extraire les deux derniers chiffres de l'adresse MAC
            mac_suffix = mac_address.split(":")[-1]

            if group.lower() == "etudiants":
                tag = 10
                vmid = f"10{mac_suffix}"
            elif group.lower() == "professeurs":
                tag = 20
                vmid = f"20{mac_suffix}"
            else:
                continue  # Ignorer les groupes non pris en charge

            resource = f"""
resource "proxmox_vm_qemu" "{username}" {{
    name        = "{username}-VM"
    desc        = "Ubuntu virtual machine of {first_name} {last_name}"
    vmid        = "{vmid}"
    target_node = "pve"

    agent   = 0
    clone   = "linux-cloud"
    cores   = 1
    sockets = 1
    cpu     = "host"
    memory  = 1024

    os_type  = "cloud-init"
    scsihw   = "virtio-scsi-pci"
    bootdisk = "scsi0"

    disk {{
        type         = "disk"
        storage      = "local-lvm"
        size         = "4G"
        iothread     = true
        slot = "scsi0"
    }}

    disk {{
        type    = "cloudinit"
        storage = "local-lvm"
        slot = "ide2"
        size = "4M"
    }}

    network {{
        model  = "virtio"
        bridge = "vmbr3"
        tag    = {tag}
        macaddr = "{mac_address}"
    }}

    serial {{
        type = "socket"
        id = 0
    }}
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip=dhcp"
    vm_state = "running"
}}
"""
            tf_file.write(resource)
            tf_file.write("\n")  # Séparation entre les ressources

# Chemin vers le fichier Excel
excel_file = "tfe.xlsx"
output_tf_file = "deployement.tf"

# Charger les données
try:
    data = load_excel(excel_file)
    # Filtrer uniquement les colonnes nécessaires
    filtered_data = data[["Username", "Name", "Surname", "Group", "MAC_Address"]]
    # Générer le fichier Terraform
    generate_terraform_resources(filtered_data, output_tf_file)
    print(f"Les ressources Terraform ont été générées dans le fichier {output_tf_file}")
except Exception as e:
    print(f"Erreur : {e}")
