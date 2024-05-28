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
import argparse
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
    print('\nStopping the program ...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Géstion de la syntaxe
def Syntaxe(OS, IPHOST, selected_file, selected_port):
    style = ("bg_black", "fg_yellow", "bold")
    while True:  # Boucle pour réessayer avec un nouveau port en cas d'échec
        if OS == "Linux" or OS == "linux":  # Correction de la condition
            syntaxeFinal = f'wget http://{IPHOST}:{selected_port}/{os.path.basename(selected_file)}'
        elif OS == "Windows" or OS == "windows":  # Correction de la condition
            syntaxeFinal = f'iwr http://{IPHOST}:{selected_port}/{os.path.basename(selected_file)} -O {os.path.basename(selected_file)}'
        else:
            print("/!\ ERROR : unsupported operating system")
            return

        handler_object = HTTPserv(selected_file, selected_port)
        try:
            my_server = socketserver.TCPServer(("", int(selected_port)), handler_object)
            os.system(f"echo -n {syntaxeFinal} | xclip -selection clipboard | echo 'The command {syntaxeFinal} is in your clipboard'")
            my_server.serve_forever()
        except OSError as e:
            print(f"/!\ \033[91mERROR\033[0m : Unable to start the server on port {selected_port}. {e}")
            selected_port = IP_menu(IPHOST, style) 
        else:
            break  # Sortir de la boucle si le serveur démarre avec succès
        

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
    # Le port n'est pas accéssible sans plus de droits
    except PermissionError:
        print("Permission denied for port {}. Please enter a new port.".format(selected_port))
        return True
    sock.close()
    # Le port n'est pas utilisé
    return False

# Gestion du serveur
def HTTPserv(selected_file, selected_port):
    print("Starting server")

    class Requester(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' + os.path.basename(selected_file):
                print(f" Request for {selected_file} received, sending the file...")
                self.send_response(200)
                self.end_headers()
                with open(selected_file, 'rb') as file:
                    self.wfile.write(file.read())
                print(f"File {selected_file} sent, stopping the server...")
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
        print("You must run this script with root privileges or assign the necessary capabilities to the Python binary.")
        return False
    
def OS_menu(os_arg=None):
    # Menu système d'exploitation de la cible :
    if os_arg is not None:
        return os_arg
    else:
        # Menu système d'exploitation de la cible :
        style = ("bg_black", "fg_yellow", "bold")
        target_OS = ["Linux", "Windows"]
        terminal_menu = TerminalMenu(target_OS, menu_cursor="=>  ", menu_highlight_style=style, title="What is the target OS?")
        menu_entry_index = terminal_menu.show()
        return target_OS[menu_entry_index]
    

def IP_menu(IPHOST, style, port=None):
    if port is not None:
        return port
    
    while True:
        ChoixPort = ["80", "8080", "8000", "443", "1234", "666", "Another port"]
        Port_menu = TerminalMenu(ChoixPort, menu_cursor="=>  ", menu_highlight_style=style, title="Select a port : ")
        Port_entry_index = Port_menu.show()
        if ChoixPort[Port_entry_index] == "Another port":
            selected_port = int(input("Please enter the port : "))
            while check_port_in_use(IPHOST, selected_port):
                print(f"The port {selected_port} is already in use or you do not have the necessary capabilities to use it.")
                selected_port = int(input("Please enter another port : "))
        else:
            selected_port = int(ChoixPort[Port_entry_index])
            if selected_port < 1024:
                if not check_user_capabilities():
                    print(f"You do not have the necessary capabilities to use the port. {selected_port} !")
                selected_port = int(input("Please enter another port : "))
            while check_port_in_use(IPHOST, selected_port):
                print(f"The port {selected_port} is already in use!")
                selected_port = int(input("Please enter another port : "))
        return selected_port

def MenuGeneral(os_arg=None, dir_arg=None, port=None):
    style = ("bg_black", "fg_yellow", "bold")
    OS = OS_menu(os_arg)

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

        ip_menu = TerminalMenu(ip_mappings, menu_cursor="=>  ", menu_highlight_style=style, title="Select a network interface:")
        ip_entry_index = ip_menu.show()
        selected_ip = interfaces[ip_entry_index]
        IPHOST = ni.ifaddresses(selected_ip).get(ni.AF_INET)
        if not IPHOST:
            print("/!\ Error: No IP address found for the selected interface. \nPlease select another interface.")
            continue
        IPHOST = IPHOST[0]['addr']
        break

    # Menu choix du répertoire
    if dir_arg is None:
        while True:
            selected_directory = input("Enter the directory for file selection : ")
            if os.path.isdir(selected_directory):
                break
            else:
                print("The specified path is not a valid directory. Please try again.")
    else:
        selected_directory = dir_arg

    # Menu choix du fichier à uploader
    
    try:
        selected_file = subprocess.check_output(f"cd {selected_directory} && fzf", shell=True).decode().strip()
        selected_file = os.path.join(selected_directory, selected_file)
        print(f"You have selected the file : {selected_file}!")
    except subprocess.CalledProcessError as e:
        print("/!\  Error: Unable to select a file. try again.")
        sys.exit(1)

 
    selected_port = IP_menu(IPHOST, style, port)

    return OS, IPHOST, selected_file, selected_port

def main():
    parser = argparse.ArgumentParser(description="Tool for quickly downloading files to a remote machine based on the target operating system. Launch the program and follow the prompts.",
                                 epilog="Example:\n  python3 uploader.py --port 8081 --os linux --dir /tmp")
    parser.add_argument("--port","-p", type=int, help="Specify the port to use.")
    parser.add_argument("--os", type=str, help="Specify the target operating system. (Linux or Windows)")
    parser.add_argument("--dir","-d", type=str, help="Specify the directory of your file.")
    args = parser.parse_args()
   
   
    OS, IPHOST, selected_file, selected_port = MenuGeneral(args.os, args.dir, args.port)
    Syntaxe(OS, IPHOST, selected_file, selected_port)

if __name__ == "__main__":
    main()
