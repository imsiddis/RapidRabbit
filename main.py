# This will be the main file for the project.

# Imports
import os
import sys
import time
import datetime
import platform
from internal_library.asset_functions import clear_screen, loading_bar, exit_program, beautify_string, beautify_title, beautify
import Network.port_scanner as portscan
import start_SQLite
import socket
from internal_library.detect_tools import main as detect
from internal_library.test_auto_menu import main as auto_menu
from internal_library.asset_functions import splash_screen, splash_logo_no_indent



# Numerical Menu System
# This will be the main menu for the project.
# It will be a numerical menu system.


info_box = f"This is the 'Rapid Rabbit Toolkit'.\n\nA lightweight toolkit for Cyber Professionals with the desire for a fast, easy to use set of tools in their profession.\nOne of the benefits of this toolkit is that it is easy to add your own tools or 'modules' as we call it, and the Rapid Rabbit will seamlessly integrate it to the toolkit.\nWe hope you will like it.\n\nBest Regards,\nSiddis"


 
def main():
    try:
        clear_screen()
        welcome_screen = splash_screen()
        print(welcome_screen)
        input("\n\n\t\t\t\t\t\t\tPress 'Enter' to continue... ")
    except KeyboardInterrupt:
        return
    while True:
        try:
            clear_screen()
            detect()
            logo = splash_logo_no_indent()
            print(beautify("The Rapid Rabbit Framework","~",is_title=False))

            print(logo)
            auto_menu()
        except KeyboardInterrupt: # Catch the KeyboardInterrupt exception to prevent the program from crashing
            print("\nExiting the program...")
            sys.exit(0)
        except Exception as e: # Catch any other exceptions and display the error message
            print(f"An error occurred: {e}")
            time.sleep(2)
            main()
            
if __name__ == "__main__":
    main()