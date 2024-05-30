#!/bin/bash

# Téléchargement du git et installation des requirements
mkdir -p /opt/tools
if [ -d "/opt/tools/uploader" ]; then
    echo "Mise à jour du dossier uploader."
    git -C /opt/tools/uploader pull
else
    echo "Clonage du dépôt."
    git clone https://github.com/Frozenka/uploader.git /opt/tools/uploader
fi
pip3 install -r /opt/tools/uploader/requirements.txt

# Gestion Xclip
if ! command -v xclip > /dev/null 2>&1; then
    sudo apt update
    sudo apt install xclip
fi

# Déclaration de l'emplacement
UPLOADER_FILE="/opt/tools/uploader/uploader.py"

# Formatage de l'alias
ALIAS_UPLOADER="alias uploader='python3 $UPLOADER_FILE'"

CURRENT_SHELL="$SHELL"
case $CURRENT_SHELL in
    */bash)
        CURRENT_SHELL="$HOME/.bashrc"
        ;;
    */spawn.sh) # Pour Exegol
        CURRENT_SHELL="$HOME/.zshrc"
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

# Rechargement du shell
"$SHELL"
