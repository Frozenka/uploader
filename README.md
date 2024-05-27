# Uploader
Ce script Python vous permet de télécharger des fichiers sur une machine distante de manière rapide en fonction du système d'exploitation cible (Linux ou Windows). 
Il génère automatiquement la commande de téléchargement appropriée et ouvre un serveur Python local pour fournir le fichier à télécharger jusqu'à ce qu'une réponse HTTP 200 soit reçue, 
puis le serveur se ferme.

![uploader](https://github.com/Frozenka/uploader/assets/13807685/92b00363-2398-43bb-862e-08c3545ce8e4)


## Fonctionnalités
- **Sélection Automatique du Fichier :** Le script propose automatiquement les fichiers disponibles dans le répertoire courant pour le téléchargement, simplifiant ainsi le processus de téléchargement.
- **Gestion Intuitive du Système d'Exploitation :** Vous pouvez choisir le système d'exploitation cible (Linux ou Windows) pour obtenir la commande de téléchargement appropriée.
- **Gestion Facile du Serveur Local :** Le script ouvre un serveur Python local pour fournir le fichier à télécharger, ce qui facilite le processus et assure une transmission rapide.

## Utilisation
Lancez la commande suivante :
`curl -s https://raw.githubusercontent.com/Frozenka/uploader/main/install.sh | sudo bash`

## Prérequis
- Python 3.x
- Xclip (pour la copie dans le presse-papiers,En cas d'absence, le script l'installera)

## Todo
- Améliorer le style graphique de l'interface utilisateur.
- Gérer les erreurs de manière plus efficace.
- ~Passage a fzf pour la séléction du fichier~
- ~Ajouter une fonctionnalité d'autocomplétion pour les fichiers en mode manuel.~


## Contribution
Les contributions sous forme de rapports de bugs, de suggestions ou de demandes de fonctionnalités sont les bienvenues ! 
N'hésitez pas à ouvrir une issue ou à soumettre une pull request.
