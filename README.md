# TFE Basil Huwart Automatisation d'un VDI

## Comment mettre en place ce projet ?
Avant de télécharger les fichiers, il faut d'abord mettre en place l'infrastructure. Pour cela il faut 
* un serveur Proxmox
* un router avec 3 sous-réseaux
    - le sous-réseau 172.16.1.0/24 pour le management
    - le sous-réseau 10.0.10.0/24 pour les étudiants
    - le sous-réseau 10.0.20.0/24 pour les professeurs
* un Active Directory
* un contoller Ansible

## Mise en place du projet

Une fois que cela est fait, vous pouvez télécharger les fichiers sur votre DC qui servira de machine d'administration. les fichiers doivent être dans le même dossier.
Seul le fichier playbook.yml doit être mit à part dans le répertoire de votre choix sur votre contoller Ansible.

Veulliez aussi vérifier que le playbook Ansible a les configurations de votre choix et respecte la distribution Linux que vous aimeriez automatiser.

Il faut installer Ansible sur votre machine Ansible controller et Terraform sur votre machine d'administration. Vous devez aussi choisir vos Templates de machines virtuelles de manière à ce qu'ils soient compatibles avec Cloud-Init.

Une fois que c'est fait vous devez remplir les fichiers global_config.json et credentials.auto.tfvars en conformité avec votre environnement de travail.

Le fichier credentials.auto.tfvars contient les informations de votre hyperviseur Proxmox et le login/mdp du compte administrateur de vos VM automatisées.

Le fichier global_config.json contient toutes les autres informations spécifiques que l'application a besoin pour faire fonctionner ce projet sur votre machine.

Ce fichier contient aussi des informations supplémentaires qui permettent de configurer ce projet selon vos désirs de manière plus avancée.

Ensuite il ne vous suffira plus que d'exécuter le fichier app.py pour configurer vos utilisateurs et vos VM :)

## Conseils d'utilisation du projet

Si vous désirez que vos utilisateurs aient accès à votre insfrastructure à distance, il vous faut installer un serveur VPN sur votre router pour permettre aux utilisateurs de s'y connecter à distance.
