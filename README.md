# Uploader
## English :
This Python script allows you to quickly upload files to a remote machine based on the target operating system (Linux or Windows). It automatically generates the appropriate download command based on the request (Curl, Wget, Certutil, Powershell, etc.) and opens a local Python server to provide the file for download until an HTTP 200 response is received, after which the server shuts down.

![uploader](https://github.com/Frozenka/uploader/assets/13807685/b0bc7142-8a30-4cc7-8162-8c9145047973)

## Functionality
- **OS Selection Menu**: Select the target operating system.
- **Network Interface Selection Menu**: Choose the network interface to use.
- **File Selection**: Select the file to upload.
- **Port Selection**: Choose the port for the HTTP server.
- **Download Command Generation**: The script generates and copies the appropriate command to download the file on the target machine.
- **HTTP Server Startup**: The integrated HTTP server starts serving the selected file.

## Installation:
Run the following command:
`curl -s https://raw.githubusercontent.com/Frozenka/uploader/main/install.sh | sudo bash`

## Arguments
```
--port, -p : Specify the port to use.
--os, -os : Specify the target operating system (Linux or Windows).
--file, -f : Specify the file to upload.
--output, -o : Specify the output file on the target machine.
--payload, -py : Specify the type of payload (wget, curl, etc.).
```

Example:
`uploader --port 8080 --os Linux --file /path/to/file --output output_file --payload Curl`

## Prerequisites
- Python 3.x
- Xclip (for clipboard copying, the script will install it if missing)

## Acknowledgements
This script was combined with a similar script (Uberfile) by Charlie BROMBERG (Shutdown - @_nwodtuhs) available on [this GitHub repository](https://github.com/ShutdownRepo/uberfile). Thanks to Charlie BROMBERG (Shutdown - @_nwodtuhs) for allowing us to use his script, and to 'ֆŋσσƥყ' for development and debugging assistance.

## Contribution
Contributions in the form of bug reports, suggestions, or feature requests are welcome! Feel free to open an issue or submit a pull request.

---------------------------------------------------------------------
## French :
Ce script Python vous permet de télécharger des fichiers sur une machine distante de manière rapide en fonction du système d'exploitation cible (Linux ou Windows). 
Il génère automatiquement la commande de téléchargement appropriée en fonction de la demande ( Curl, Wget, Certutil,Powershel ect..) et ouvre un serveur Python local pour fournir le fichier à télécharger jusqu'à ce qu'une réponse HTTP 200 soit reçue, 
puis le serveur se ferme.

![uploader](https://github.com/Frozenka/uploader/assets/13807685/b0bc7142-8a30-4cc7-8162-8c9145047973)

## Fonctionnement
- Menu de sélection du système d'exploitation : Sélectionnez le système d'exploitation cible.
- Menu de sélection de l'interface réseau : Choisissez l'interface réseau à utiliser.
- Sélection du fichier : Sélectionnez le fichier à télécharger.
- Sélection du port : Choisissez le port pour le serveur HTTP.
- Génération de la commande de téléchargement : Le script génère et copie la commande appropriée pour télécharger le fichier sur la machine cible.
- Démarrage du serveur HTTP : Le serveur HTTP intégré commence à servir le fichier sélectionné.

## Installation :
Lancez la commande suivante :
`curl -s https://raw.githubusercontent.com/Frozenka/uploader/main/install.sh | sudo bash`

## Arguments
```
--port, -p      : Spécifiez le port à utiliser.
--os, -os       : Spécifiez le système d'exploitation cible (Linux ou Windows).
--file, -f      : Spécifiez le fichier à télécharger.
--output, -o    : Spécifiez le fichier de sortie sur la machine cible.
--payload, -py  : Spécifiez le type de payload (wget, curl, etc.).
```

Exemple:
`uploader --port 8080 --os Linux --file /path/to/file --output output_file --payload Curl`

## Prérequis
- Python 3.x
- Xclip (pour la copie dans le presse-papiers,En cas d'absence, le script l'installera)


## Remerciements :
Ce script a été combiné avec un script similaire (Uberfile) de Charlie BROMBERG (Shutdown - @_nwodtuhs) disponible sur [ce repository GitHub](https://github.com/ShutdownRepo/uberfile)
Remerciements à Charlie BROMBERG (Shutdown - @_nwodtuhs) pour l'autorisation de reprendre son script, et à 'ֆŋσσƥყ' pour l'aide au développement et au débogage.

## Contribution
Les contributions sous forme de rapports de bugs, de suggestions ou de demandes de fonctionnalités sont les bienvenues ! 
N'hésitez pas à ouvrir une issue ou à soumettre une pull request.
