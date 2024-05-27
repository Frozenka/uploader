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
CURRENT_SHELL=$(basename "$SHELL")
echo "Shell : $CURRENT_SHELL"
case $CURRENT_SHELL in
    bash)
        CURRENT_SHELL="$HOME/.bashrc"
        ;;
    zsh)
        CURRENT_SHELL="$HOME/.zshrc"
        ;;
    sh)
        CURRENT_SHELL="$HOME/.profile"
        ;;
    *)
        exit 1
        ;;
esac
#Vérif si l'alias éxiste déja
if ! grep -Fxq "$ALIAS_UPLOADER" "$UPLOADER_FILE"; then
    echo "$ALIAS_UPLOADER" >> "$CURRENT_SHELL"
fi
source "$CURRENT_SHELL"

