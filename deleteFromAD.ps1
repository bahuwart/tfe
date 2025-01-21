# Import the Active Directory module
Import-Module ActiveDirectory

Import-Module ActiveDirectory

$configFile = "C:\tfe\global_config.json"

# Vérifier si le fichier JSON existe
if (-Not (Test-Path -Path $configFile)) {
    Write-Host "Le fichier de configuration JSON est introuvable : $configFile"
    exit 1
}

# Charger le fichier JSON
$config = Get-Content -Path $configFile | ConvertFrom-Json

# Extraire les valeurs nécessaires
$OUPath = $config.OU_USERS_PATH
$OUCPath = $config.OU_COMPUTERS_PATH

# Supprimer tous les utilisateurs dans l'OU "utilisateurs"
Write-Host "Suppression de tous les utilisateurs dans l'OU 'utilisateurs'..."
Get-ADUser -Filter * -SearchBase $OUPath | ForEach-Object {
    Write-Host "Suppression de l'utilisateur : $($_.SamAccountName)" -ForegroundColor Yellow
    Remove-ADUser -Identity $_.DistinguishedName -Confirm:$false
}

# Supprimer tous les objets dans Computers
Write-Host "Suppression des objets dans le conteneur Computers..."
Get-ADComputer -Filter * -SearchBase $OUCPath | ForEach-Object {
    Write-Host "Suppression de l'ordinateur : $($_.Name)" -ForegroundColor Yellow
    Remove-ADObject -Identity $_.DistinguishedName -Confirm:$false
}

Write-Host "Script terminé." -ForegroundColor Green
