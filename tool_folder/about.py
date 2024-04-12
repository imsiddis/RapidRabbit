from internal_library.asset_functions import clear_screen, beautify, beautify_string, beautify_title

tool_details = {
    "name":"about",
    "filename":"about.py",
    "Category":"Information",
    "version":"1.0",
    "Description":"This will be the about section for the project."
}

def disclaimer():
    print(f'''
# Disclaimer #
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
    ''')
def about():
    print('''
Creator: @imSiddis

Description:
The Rapid Rabbit Toolkit is a collection of scripts and tools designed to streamline the process of running and managing various cybersecurity tools. 
It provides a user-friendly interface for accessing and executing tools, as well as a modular structure for adding your own scripts and tools to the toolkit. 
The toolkit is designed to be easy to use and customizable, allowing you to tailor it to your specific needs and preferences.
It was developed as part of a cybersecurity dissertation project, and is intended to be a useful resource for cybersecurity professionals, students, and enthusiasts.
The toolkit is designed to run on any platform that supports Python, and is intended to be easy to install and use. It includes built-in functions for handling assets, such as creating and managing directories and files, and provides a clear and structured command-line interface for interacting with the toolkit.        
    ''')

def main():
    clear_screen()
    about()
    input("Press Enter to continue...")
    clear_screen()
    disclaimer()

if __name__ == "__main__":
    main()