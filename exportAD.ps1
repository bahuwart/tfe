# Charger le module Active Directory
Import-Module ActiveDirectory

# Lire le fichier JSON généré par Python
$jsonPath = "C:\tfe\users_data.json"
$jsonData = Get-Content -Path $jsonPath | ConvertFrom-Json

# Fonction pour vérifier si un utilisateur existe dans AD
function Test-UserExists {
    param (
        [string]$SamAccountName
    )
    try {
        $user = Get-ADUser -Filter {SamAccountName -eq $SamAccountName} -ErrorAction SilentlyContinue
        return $null -ne $user
    } catch {
        Write-Host "Erreur lors de la vérification de l'utilisateur $SamAccountName : $_" -ForegroundColor Red
        return $false
    }
}

# Parcourir chaque utilisateur extrait du fichier JSON
foreach ($user in $jsonData) {
    $username = $user.Username
    $name = $user.Name
    $surname = $user.Surname
    $password = $user.Password
    $group = $user.Group

    # Vérifier que toutes les données nécessaires sont présentes
    if (-not $username -or -not $name -or -not $surname -or -not $password -or -not $group) {
        Write-Host "Données manquantes pour l'utilisateur $username. Passer à l'utilisateur suivant." -ForegroundColor Yellow
        continue
    }

    # Vérifier si l'utilisateur existe déjà dans AD
    if (Test-UserExists -SamAccountName $username) {
        Write-Host "L'utilisateur $username existe déjà. Aucun changement effectué." -ForegroundColor Yellow
    } else {
        # Créer un nouvel utilisateur dans Active Directory sans spécifier l'OU
        try {
            $newUser = New-ADUser -SamAccountName $username `
                                   -UserPrincipalName "$username@tfe.lab" `
                                   -DisplayName "$name $surname" `
                                   -GivenName $name `
                                   -Surname $surname `
                                   -Name "$name $surname" `
                                   -AccountPassword (ConvertTo-SecureString $password -AsPlainText -Force) `
                                   -Enabled $true `
                                   -PasswordNeverExpires $true `
                                   -PassThru 

            Write-Host "Utilisateur $username créé avec succès." -ForegroundColor Green

            # Déplacer l'utilisateur vers l'OU souhaitée
            $ouPath = "OU=utilisateurs,DC=TFE,DC=lab"
            Move-ADObject -Identity $newUser.DistinguishedName -TargetPath $ouPath
            Write-Host "Utilisateur $username déplacé vers l'OU utilisateur." -ForegroundColor Green

            # Ajouter l'utilisateur au groupe spécifié
            Add-ADGroupMember -Identity $group -Members $newUser.SamAccountName
            Write-Host "Utilisateur $username ajouté au groupe $group." -ForegroundColor Green

        } catch {
            Write-Host "Erreur lors de la création de l'utilisateur $username : $_" -ForegroundColor Red
        }
    }
}
