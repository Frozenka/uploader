#!/bin/bash

#Téléchargement du git et install des requirements
sudo mkdir -p /opt/tools
sudo git clone https://github.com/Frozenka/uploader.git /opt/tools/uploader
sudo pip3 install -r /opt/tools/uploader/requirements.txt

#Déclaration de l'emplacement
UPLOADER_FILE="/opt/tools/uploader/uploader.py"

#Formatage de l'alias
ALIAS_UPLOADER="alias uploader='python3 $UPLOADER_FILE'"

#Recherche du Shell actif
CURRENT_SHELL="$SHELL"
case $CURRENT_SHELL in
    */bash)
        CURRENT_SHELL="$HOME/.bashrc"
        ;;
    */zsh)
        CURRENT_SHELL="$HOME/.zshrc"
        ;;
    */sh)
        CURRENT_SHELL="$HOME/.profile"
        ;;
    *)
        echo "Shell non pris en charge : $CURRENT_SHELL"
        exit 1
        ;;
esac

# Vérification si l'alias existe déjà
if grep -q "$ALIAS_UPLOADER" "$CURRENT_SHELL"; then
    echo "Alias déjà présent!"
else
    echo "Rajout de l'alias"
    echo "$ALIAS_UPLOADER" >> "$CURRENT_SHELL"
fi

#Rechargement du shell
/"$SHELL"
