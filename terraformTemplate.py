import json

# Charger le fichier JSON
def load_json(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)

# Extraire les informations nécessaires d'un utilisateur
def get_user_details(user):
    username = user["Username"]
    first_name = user["Name"]
    last_name = user["Surname"]
    group = user["Group"]
    ip_addresses = [value for key, value in user.items() if key.startswith("IP_Address")]
    return username, first_name, last_name, group, ip_addresses

# Générer la ressource Terraform pour une adresse IP spécifique
def generate_terraform_resource(username, first_name, last_name, group, ip_address, ip_suffix):
    ip_gateway = ".".join(ip_address.split(".")[:-1]) + ".1"

    # Déterminer le groupe (et le tag correspondant)
    if group.lower() == "etudiants":
        tag = 10
        vmid = f"10{ip_suffix}"
    elif group.lower() == "professeurs":
        tag = 20
        vmid = f"20{ip_suffix}"
    else:
        return ""  # Ignorer les groupes non pris en charge

    # Nom de la ressource avec un suffixe basé sur l'IP
    resource_name = f"{username}-VM{vmid}"

    resource = f"""
resource "proxmox_vm_qemu" "{resource_name}" {{
    name        = "{username}-VM{vmid}"
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
    }}

    serial {{
        type = "socket"
        id = 0
    }}
    ciuser = var.admin_login
    cipassword = var.admin_password
    ipconfig0   = "ip={ip_address}/24,gw={ip_gateway}"
    vm_state = "running"
}}
"""
    return resource

# Générer les ressources Terraform pour tous les utilisateurs
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

        # Pour chaque utilisateur
        for user in data:
            username, first_name, last_name, group, ip_addresses = get_user_details(user)

            # Traiter chaque adresse IP
            for ip_address in ip_addresses:
                if ip_address:  # Si l'adresse IP est valide
                    ip_suffix = ip_address.split(".")[-1]
                    resource = generate_terraform_resource(username, first_name, last_name, group, ip_address, ip_suffix)
                    tf_file.write(resource)
                    tf_file.write("\n")  # Séparation entre les ressources

# Chemin vers le fichier JSON
json_file = "users_data.json"
output_tf_file = "deployement.tf"

# Charger les données
try:
    data = load_json(json_file)
    # Générer le fichier Terraform
    generate_terraform_resources(data, output_tf_file)
    print(f"Les ressources Terraform ont été générées dans le fichier {output_tf_file}")
except Exception as e:
    print(f"Erreur : {e}")
