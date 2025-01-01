# Charger le module Active Directory
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
$UsersDataPath = $config.USER_DATA_FILE
$OUPath = $config.OU_PATH

# Lire le fichier JSON généré par Python
$usersDataFile = $UsersDataPath
$jsonData = Get-Content -Path $usersDataFile | ConvertFrom-Json

# Obtenir la liste des utilisateurs dans l'OU spécifiée de l'Active Directory
$adUsers = Get-ADUser -Filter * -SearchBase $OUPath | Select-Object SamAccountName

# Convertir les utilisateurs dans le fichier JSON en liste de SamAccountName
$jsonUsernames = $jsonData | ForEach-Object { $_.Username }

# Comparer les utilisateurs présents dans AD et ceux du fichier JSON
foreach ($adUser in $adUsers) {
    if ($adUser.SamAccountName -notin $jsonUsernames) {
        # Si l'utilisateur AD n'est pas dans le fichier JSON, supprimer l'utilisateur de l'OU spécifiée
        try {
            Remove-ADUser -Identity $adUser.SamAccountName -Confirm:$false
            Write-Host "Utilisateur $($adUser.SamAccountName) supprimé de l'Active Directory (OU: $OUPath)." -ForegroundColor Red
        } catch {
            Write-Host "Erreur lors de la suppression de l'utilisateur $($adUser.SamAccountName) : $_" -ForegroundColor Red
        }
    } else {
        Write-Host "L'utilisateur $($adUser.SamAccountName) est présent dans le fichier JSON. Aucun changement effectué." -ForegroundColor Green
    }
}