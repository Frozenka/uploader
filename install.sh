#!/bin/bash

#Téléchargement du git et install des requirements
mkdir -p /opt/tools
git clone https://github.com/Frozenka/uploader.git /opt/tools/uploader
pip3 install -r /opt/tools/uploader/requirements.txt

#Géstion Xclip
if ! command -v xclip > /dev/null 2>&1; then
    sudo apt update
    sudo apt install xclip
fi
     
#Déclaration de l'emplacement
UPLOADER_FILE="/opt/tools/uploader/uploader.py"

#Formatage de l'alias
ALIAS_UPLOADER="alias uploader='python3 $UPLOADER_FILE'"

#Si exegol :
if [ -f "/.exegol/spwn.sh" ]; then
    echo "$ALIAS_UPLOADER" >> /root/.zshrc
    
else
    #Sinon
    CURRENT_SHELL="$SHELL"
        #recherche du Shell actif
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

fi


