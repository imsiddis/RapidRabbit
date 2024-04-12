# This will be the main file for the project.

# Imports
import os
import sys
import time
import datetime
import platform
from internal_library.asset_functions import loading_bar, exit_program, beautify_string, beautify_title, beautify
import socket
from internal_library.detect_tools import main as detect
from internal_library.auto_menu import main as auto_menu
from internal_library.asset_functions import splash_screen, splash_logo_no_indent, splash_screen_title, clear_screen, center_block_text, center_text



# Numerical Menu System
# This will be the main menu for the project.
# It will be a numerical menu system.

disclaimer_text = f'''
## Disclaimer ##
Disclaimer and Ethical Use Policy for The Rapid Rabbit Toolkit

Purpose and Intended Use
The Rapid Rabbit Toolkit is developed with the intent to support ethical hacking and cybersecurity defense activities. It is designed for educational purposes, security professionals, and technology enthusiasts to conduct responsible security assessments. Users of this toolkit are reminded to operate within all applicable legal and ethical boundaries and to ensure that its use aligns with the principles of constructive cybersecurity engagement.

Responsible Disclosure
Users who identify vulnerabilities with the aid of this toolkit are encouraged to engage in responsible disclosure practices. This includes notifying affected entities discreetly to allow for the rectification of vulnerabilities before any public disclosure, in accordance with established guidelines for responsible disclosure.

Prohibition of Malicious Use
The use of this toolkit for illegal or malicious activities is strictly prohibited. This includes, but is not limited to, deploying capabilities such as reverse shells or hash crackers without explicit authorization from the relevant authority. Engaging in unauthorized or harmful activities using this toolkit will lead to legal and ethical repercussions.

Ethical Awareness and Education
This toolkit includes resources designed to enhance the user’s understanding of cybersecurity ethics and legal compliance. Users are urged to secure necessary authorizations and understand the ethical implications before conducting any form of security assessments. We aim to promote an ethical hacking culture that respects privacy and the integrity of systems.

Community Involvement
Feedback and contributions from the cybersecurity community are highly valued. Users are invited to share their insights, suggestions, and concerns regarding both the ethical and security aspects of this toolkit to foster continuous improvement and ethical accountability in its development and use.

Commitment to Ethical Integrity
The development of The Rapid Rabbit Toolkit adheres to high standards of security and ethical integrity. Our goal is to provide a tool that not only advances cybersecurity techniques but also upholds the ethical principles that protect and enhance the digital landscape.

By using The Rapid Rabbit Toolkit, you acknowledge and agree to these terms, committing to uphold the highest standards of ethical conduct in your cybersecurity endeavors.

# End of Disclaimer #
    '''

info_box = f"This is the 'Rapid Rabbit Toolkit'.\n\nA lightweight toolkit for Cyber Professionals with the desire for a fast, easy to use set of tools in their profession.\nOne of the benefits of this toolkit is that it is easy to add your own tools or 'modules' as we call it, and the Rapid Rabbit will seamlessly integrate it to the toolkit.\nWe hope you will like it.\n\nBest Regards,\nSiddis"

# Centering output.
splash_logo = center_block_text(splash_logo_no_indent())
splash_title = center_block_text(splash_screen_title())
menu_title = center_text(beautify_title("The Rapid Rabbit Framework","~",5))
 
def main():
    detected = False
    try:
        # This will display the splash screen for the project.
        clear_screen()
        disclaimer = center_block_text(disclaimer_text)
        print(disclaimer_text)
        time.sleep(2)
        clear_screen()
        print(splash_logo)
        print(splash_title)
        #input("\n\n\t\t\t\t\t\t\tPress 'Enter' to continue... ")
        enter_to_continue = center_text("Press 'Enter' to continue...")
        input(f"\n\n{enter_to_continue}")
    except KeyboardInterrupt:
        return
    while True:
        try:
            clear_screen()
            if detected == False:
            #    loading_bar()
                detect()
                detected = True
                
            print(splash_logo) # Prints the splash logo centered
            print(menu_title) # Prints "The Rapid Rabbit Framework" *centered* with a line of ~ under it. !! See Centering output section above. !!
            auto_menu()
            input("\nPress 'Enter' to continue... ")
        except KeyboardInterrupt: # Catch the KeyboardInterrupt exception to prevent the program from crashing
            print("\nExiting the program...")
            sys.exit(0)
        except Exception as e: # Catch any other exceptions and display the error message
            print(f"An error occurred: {e}")
            time.sleep(2)
            main()
            
if __name__ == "__main__":
    main()