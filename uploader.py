#!/usr/bin/env python3
   
'''
Description :
# Auteur : Frozenk / Christopher SIMON        
Ce programme permet d'obtenir directement la commande de téléchargement en fonction du système d'exploitation (Windows ou Linux),
et d'ouvrir automatiquement le serveur Python jusqu'à ce qu'un code 200 soit obtenu
À ce moment, le serveur Python se fermera.

Todo :
- Améliorer le style graphique
- Gérer les erreurs de manière plus efficace
'''

import os
import socket
import readline
import http.server
import socketserver
import subprocess
import netifaces as ni
from simple_term_menu import TerminalMenu
import signal
import sys

# Gérer l'interruption Ctrl+C
def signal_handler(sig, frame):
    print('\nArret du programme ...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Géstion de la syntaxe
def Syntaxe(OS, IPHOST, selected_file, selected_port):
    if OS == "Linux":
        syntaxeFinal = f'wget http://{IPHOST}:{selected_port}/{os.path.basename(selected_file)}'
    elif OS == "Windows":
        syntaxeFinal = f'iwr http://{IPHOST}:{selected_port}/{os.path.basename(selected_file)} -O {os.path.basename(selected_file)}'
    else:
        print("/!\ Erreur : système d'exploitation non supporté")
        return

    handler_object = HTTPserv(selected_file, selected_port)
    try:
        my_server = socketserver.TCPServer(("", int(selected_port)), handler_object)
        os.system(f"echo -n {syntaxeFinal} | xclip -selection clipboard | echo 'La commande {syntaxeFinal} est dans votre presse-papier'")
        my_server.serve_forever()
    except OSError as e:
        print(f"/!\ Erreur : Impossible de démarrer le serveur sur le port {selected_port}. {e}")

# Gestion des ports
def check_port_in_use(IPHOST, selected_port):
    # Créer un socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((IPHOST, selected_port))
    except OSError:
        # Le port est déjà utilisé
        return True
    # Le port est pas accéssible sans plus de droits
    except PermissionError:
        print("Permission denied for port {}. Please enter a new port.".format(selected_port))
        return True
    sock.close()
    # Le port n'est pas utilisé
    return False

# Gestion du serveur
def HTTPserv(selected_file, selected_port):
    print("Lancement serveur")

    class Requester(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' + os.path.basename(selected_file):
                print(f"Requête pour {selected_file} reçue, envoi du fichier...")
                self.send_response(200)
                self.end_headers()
                with open(selected_file, 'rb') as file:
                    self.wfile.write(file.read())
                print(f"Fichier {selected_file} envoyé, arrêt du serveur...")
                os._exit(0)  # Arrête le serveur
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

            server_address = ("", selected_port)
            httpd = http.server.HTTPServer(server_address, Requester)
            httpd.serve_forever()
    return Requester

# Vérifier si le script est exécuté en tant que root
def check_user_capabilities():
    if os.geteuid() == 0:
        return True
    else:
        print("Vous devez exécuter ce script avec des privilèges root ou attribuer les capacités nécessaires au binaire Python.")
        return False

def MenuGeneral():
    # Menu système d'exploitation de la cible :
    style = ("bg_black", "fg_yellow", "bold")
    ChoixCible = ["Linux", "Windows"]
    terminal_menu = TerminalMenu(ChoixCible, menu_cursor="=>  ", menu_highlight_style=style, title="Quelle est la cible du téléchargement ?")
    menu_entry_index = terminal_menu.show()
    OS = ChoixCible[menu_entry_index]

    # Menu choix de l'interface réseau
    while True:
        interfaces = ni.interfaces()
        ip_mappings = []
        for interface in interfaces:
            ip_info = ni.ifaddresses(interface).get(ni.AF_INET)
            if ip_info:
                ip_address = ip_info[0]['addr']
                ip_mappings.append(f"{interface} == {ip_address}")
            else:
                ip_mappings.append(f"{interface} == No IP")

        ip_menu = TerminalMenu(ip_mappings, menu_cursor="=>  ", menu_highlight_style=style, title="Choisissez une interface reseau :")
        ip_entry_index = ip_menu.show()
        selected_ip = interfaces[ip_entry_index]
        IPHOST = ni.ifaddresses(selected_ip).get(ni.AF_INET)
        if not IPHOST:
            print("/!\ Erreur : Aucune adresse IP trouvée pour l'interface sélectionnée. \nVeuillez sélectionner une autre interface.")
            continue
        IPHOST = IPHOST[0]['addr']
        break

    # Menu choix du répertoire
    while True:
        selected_directory = input("Entrez le répertoire pour la sélection de fichier : ")
        if os.path.isdir(selected_directory):
            break
        else:
            print("Le chemin spécifié n'est pas un répertoire valide. Veuillez réessayer.")

    # Menu choix du fichier à uploader
    try:
        selected_file = subprocess.check_output(f"cd {selected_directory} && fzf", shell=True).decode().strip()
        selected_file = os.path.join(selected_directory, selected_file)
        print(f"Vous avez sélectionné le fichier {selected_file}!")
    except subprocess.CalledProcessError as e:
        print("/!\ Erreur : Impossible de sélectionner un fichier. Assurez-vous que fzf est installé et réessayez.")
        sys.exit(1)

    # Menu choix du port de téléchargement
    ChoixPort = ["80", "8080", "8000", "443", "1234", "666", "Autre Port"]
    Port_menu = TerminalMenu(ChoixPort, menu_cursor="=>  ", menu_highlight_style=style, title="Choisissez un PORT :")
    Port_entry_index = Port_menu.show()
    if ChoixPort[Port_entry_index] == "Autre Port":
        selected_port = int(input("Veuillez entrer le port :"))
        while check_port_in_use(IPHOST, selected_port):
            print(f"Le port {selected_port} est déjà utilisé ou vous n'avez pas les capacités nécessaires pour l'utiliser.")
            selected_port = int(input("Veuillez entrer un autre PORT :"))
    else:
        selected_port = int(ChoixPort[Port_entry_index])
        if selected_port < 1024:
            if not check_user_capabilities():
                print(f"Vous n'avez pas les capacités nécessaires pour utiliser le port {selected_port} !")
                sys.exit(1)
        while check_port_in_use(IPHOST, selected_port):
            print(f"Le port {selected_port} est déjà utilisé !")
            selected_port = int(input("Veuillez entrer un autre PORT :"))

    return OS, IPHOST, selected_file, selected_port

def main():
    OS, IPHOST, selected_file, selected_port = MenuGeneral()
    Syntaxe(OS, IPHOST, selected_file, selected_port)

if __name__ == "__main__":
    main()
