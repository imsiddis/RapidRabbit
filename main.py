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


def main_menu(): # OUTDATED
    # Clear the screen
    clear_screen()

    # Print the menu
    print(beautify("The Rapid Rabbit Toolkit","~", 2,is_heading=True))
    print(beautify_title("Main Menu","~",1))
    print("1. Network (Currently port scanner - NB: Need to create a Network Menu)")
    print("2. Option 2")
    print("3. Option 3")
    print("4. Option 4")
    print("0. Exit")
    print("")

    # Get the user's choice
    choice = input("Enter your choice: ")

    # Decide what to do
    if choice == "1":
        # Network - Currently set to the port scanner. Will be its own category eventually.
        clear_screen()
        portscan.scan_menu()
        
        
    elif choice == "2":
        # option_2()
        clear_screen()
        print(beautify(info_box, "#"))
    elif choice == "3":
        #dev_menu()
        pass
    elif choice == "4":
        clear_screen()
        network_menu()
    elif choice == "5":
        pass
    elif choice == "6":
        pass
    elif choice == "0":
        exit_program()
    else:
        print("Invalid choice. Please try again.")
        time.sleep(1)
        main_menu()
        
        
def network_menu(): # OUTDATED
    # This section will contain all the network modules in the toolkit. 
    print(beautify("Network Tools","~",is_title=True))
    print(beautify_string("1. Port Scanner\n2. LAN Discovery\n3. About", "~"))
    
    user_choice = input(">> ")
    
    if user_choice == "1":
        clear_screen()
        portscan.scan_menu()

def hash_menu(): # OUTDATED
    # This section will contain all the hashing modules in the toolkit.
    pass

def dev_menu(): # OUTDATED
    # Clear the screen
    clear_screen()
    print("Dev Menu")
    print("1. Populate the database")
    print("2. Reset the database")
    print("3. Option 3")
    print("0. Back")
    
    # Get the user's choice
    choice = input("Enter your choice: ")
    
    # Decide what to do
    if choice == "1":
        start_SQLite.fill_dummy_users()
    elif choice == "2":
        # option_2()
        pass
    elif choice == "3":
        # option_3()
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        pass
    elif choice == "0":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        time.sleep(1)
        dev_menu()


 
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