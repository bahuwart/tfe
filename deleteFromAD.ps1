# Import the Active Directory module
Import-Module ActiveDirectory

# Variables
$adminUser = "admin"  # Nom de l'utilisateur à exclure

# Supprimer les utilisateurs sauf l'utilisateur admin
Write-Host "Suppression des utilisateurs sauf '$adminUser'..."
Get-ADUser -Filter * -SearchBase "OU=utilisateurs,DC=tfe,DC=lab" | ForEach-Object {
    if ($_.SamAccountName -ne $adminUser) {
        Write-Host "Suppression de l'utilisateur : $($_.SamAccountName)" -ForegroundColor Yellow
        Remove-ADUser -Identity $_.DistinguishedName -Confirm:$false
    } else {
        Write-Host "Utilisateur exclu : $adminUser" -ForegroundColor Green
    }
}

# Supprimer tous les objets dans Computers
Write-Host "Suppression des objets dans le conteneur Computers..."
Get-ADComputer -Filter * -SearchBase "CN=Computers,DC=tfe,DC=lab" | ForEach-Object {
    Write-Host "Suppression de l'ordinateur : $($_.Name)" -ForegroundColor Yellow
    Remove-ADComputer -Identity $_.DistinguishedName -Confirm:$false
}

Write-Host "Script terminé." -ForegroundColor Green
