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

Une fois que cela est fait, vous pouvez télécharger les fichiers sur votre DC qui servira de machine d'administration. les fichiers doivent être dans le même dossier. Ce dossier doit être placé à la racine du dique C et s'appeler tfe.
Seul le fichier playbook.yml doit être mit à part dans le répertoire de votre choix sur votre contoller Ansible.

Veulliez aussi vérifier que le playbook Ansible a les configurations de votre choix et respecte la distribution Linux que vous aimeriez automatiser.

Il faut installer Ansible sur votre controller Ansible et Terraform sur votre machine d'administration. Vous devez aussi choisir vos Templates de machines virtuelles de manière à ce qu'ils soient compatibles avec Cloud-Init.

Il faut créer une OU où stocker vos utilisateurs et créer 2 groupes qu'il faut nommer etudiants et professeurs.

Il faut aussi placer une fichier excel vide appelé tfe.xlsx dans votre dossier.

Une fois que c'est fait vous devez remplir les fichiers global_config.json et credentials.auto.tfvars en conformité avec votre environnement de travail.

Le fichier credentials.auto.tfvars contient les informations de votre hyperviseur Proxmox et le login/mdp du compte administrateur de vos VM automatisées.

Le fichier global_config.json contient toutes les autres informations spécifiques que l'application a besoin pour faire fonctionner ce projet sur votre machine.

Ce fichier contient aussi des informations supplémentaires qui permettent de configurer ce projet selon vos désirs de manière plus avancée.

Ensuite il ne vous suffira plus que d'exécuter le fichier app.py pour configurer vos utilisateurs et vos VM.

## Utilisation du projet

Une fois l'installation terminée, vous pouvez commencer à utiliser l'application.

Pour ce faire, il faut exécuter le fichier app.py. Si tout fonctionne, vous devriez voir apparaitre une fenêtre comme ceci :

![Capture d'écran 2025-01-21 150351](https://github.com/user-attachments/assets/acf94f16-8c54-4dd3-b973-22dad69e3935)

Dans cette fenêtre se trouvent 6 boutons.

Le premier, celui nommé "Sélectionner un fichier" permet d'ajouter un fichier excel avec les champs Name, Surname et Group des utilisateurs.
les utilisateurs inscrits dans ce fichier seront automatiquement ajoutés à l'AD.

Le second, le bouton nommé "Lancer la création des VM", permet comme son nom l'indique de lancer la création des VM des utilisateurs.

Le troisième, nommé "Lancer la configuration des VM", permet de configurer les VM et de les ajouter à l'AD.

Enfin les boutons "Supprimer VM & utilisteurs" et "Supprimer certains utilisateurs" permettent de soit supprimer toutes les VM et tous les utilisateurs dans le premier cas, ou dans le second cas de donner un fichier excel semblable au premier fichier excel du bouton "Sélectionner un fichier" mais seulement avec les informations des utilisateurs que l'on veut supprimer. 


## Conseils d'utilisation du projet

Si vous désirez que vos utilisateurs aient accès à votre insfrastructure, il vous faut installer un serveur VPN sur votre router pour permettre aux utilisateurs de s'y connecter à distance.
