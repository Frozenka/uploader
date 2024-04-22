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
1. Clonez ce dépôt sur votre machine locale.
2. pip3 install -r requierements.txt
3. Assurez-vous d'avoir **Python 3 installé** sur votre système.
4. Exécutez le script `uploader.py`.
5. Suivez les instructions à l'écran pour sélectionner le système d'exploitation cible, choisir le fichier à télécharger et spécifier le port d'écoute.
6. Une fois que le serveur est démarré et que la commande de téléchargement est copiée dans votre presse-papiers, vous pouvez l'utiliser sur la machine distante.

## Prérequis
- Python 3.x
- Xclip (pour la copie dans le presse-papiers, uniquement pour Linux)
- requierements.txt

## Todo
- Améliorer le style graphique de l'interface utilisateur.
- Gérer les erreurs de manière plus efficace.
- ~Ajouter une fonctionnalité d'autocomplétion pour les fichiers en mode manuel.~


## Contribution
Les contributions sous forme de rapports de bugs, de suggestions ou de demandes de fonctionnalités sont les bienvenues ! 
N'hésitez pas à ouvrir une issue ou à soumettre une pull request.
