#!/usr/bin/env python3
# Auteur : Frozenk / Christopher SIMON

'''
Description :
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


# Géstion de la syntaxe
def Syntaxe(OS,IPHOST,selected_file,selected_port):
    if OS == "Linux":
        syntaxeFinal = f'wget http://{IPHOST}:{selected_port}/{selected_file}'
        handler_object = HTTPserv(selected_file, selected_port)
        my_server = socketserver.TCPServer(("", int(selected_port)), handler_object)
        os.system(f"echo -n {syntaxeFinal} | xclip -selection clipboard | echo 'La commande {syntaxeFinal} est dans votre presse-papier' ")
        my_server.serve_forever()

    elif OS == "Windows":
        syntaxeFinal = f'iwr http://{IPHOST}:{selected_port}/{selected_file} -O {selected_file}'
        handler_object = HTTPserv(selected_file, selected_port)
        my_server = socketserver.TCPServer(("", int(selected_port)), handler_object)
        os.system(f"echo -n {syntaxeFinal} | xclip -selection clipboard | echo 'La commande {syntaxeFinal} est dans votre presse-papier' ")
        my_server.serve_forever()  
    else:
        print('Erreur')
        
#Gestion droits sur le Port
def check_user_capabilities():
    getcap_output = os.popen('getcap $(which python3)').read()

    if 'cap_net_bind_service' in getcap_output:
        return True
    else:
        return False

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


# Gestion du server       
def HTTPserv(selected_file,selected_port):
    print("Lancement serveur")

    class Requester(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' + selected_file:
                print(f"Requête pour {selected_file} reçue, envoi du fichier...")
                self.send_response(200)
                self.end_headers()
                with open(selected_file, 'rb') as file:
                    self.wfile.write(file.read())
                print(f"Fichier {selected_file} envoyé, arrêt du serveur...")
                os._exit(0)  # Arrête le serveur
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

            server_address = ("", selected_port)
            httpd = http.server.HTTPServer(server_address, RequestHandler)
            httpd.serve_forever()
    return Requester


# Gestion du menu
def MenuGeneral():
    # Menu syteme d'exploitation de la cible :
    style = ("bg_black", "fg_yellow", "bold")
    ChoixCible = ["Linux", "Windows"]
    terminal_menu = TerminalMenu(ChoixCible,menu_cursor="=>  ", menu_highlight_style=style, title="Quelle est la cible du téléchargement ?" )
    menu_entry_index = terminal_menu.show()
    OS = ChoixCible[menu_entry_index]     
    
    # Menu choix de l'interface réseaux
    interfaces = ni.interfaces()
    ips = [ni.ifaddresses(interface).get(ni.AF_INET) for interface in interfaces]
    ips = [ip[0]['addr'] for ip in ips if ip]
    ChoixIP = interfaces
    ip_menu = TerminalMenu(ChoixIP, menu_cursor="=>  ", menu_highlight_style=style, title="Choisissez une adresse IP :")
    ip_entry_index = ip_menu.show()
    selected_ip = ChoixIP[ip_entry_index]
    IPHOST = ni.ifaddresses(selected_ip).get(ni.AF_INET)[0]['addr']

  # Menu Choix du fichier a upload
    current_directory = os.getcwd()
    selected_file = subprocess.check_output("fzf", shell=True).decode().strip()
    selected_file = os.path.relpath(selected_file, current_directory) 
    print(f"Vous avez sélectionné le fichier {selected_file}!")


    #Menu Port downlaod
    ChoixPort = ["80","8080","8000","443","1234","666","Autre Port"]
    Port_menu = TerminalMenu(ChoixPort, menu_cursor="=>  ", menu_highlight_style=style, title="Choisissez un PORT :")
    Port_entry_index = Port_menu.show()
    if ChoixPort[Port_entry_index] == "Autre Port":
        selected_port = input("Veuillez entrer le port :")
        while check_port_in_use(IPHOST, int(selected_port)) or not check_user_capabilities():
            print("Le port est déja utilisé ou vous n'avez pas les capacités nécessaires!Veuillez entrer un autre port")
            selected_port = input("Veuillez entrer le port :")
    else:
        selected_port = ChoixPort[Port_entry_index]

    return (OS, IPHOST, selected_file,selected_port)



def main():
    OS, IPHOST, selected_file, selected_port = MenuGeneral()
    Syntaxe(OS, IPHOST, selected_file,selected_port)

if __name__ == "__main__":
    main()
