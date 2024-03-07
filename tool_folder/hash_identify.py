# This script will identify a given hash type. 
# Because MD5 and NTLMS have the same length, we will need to use a different method to identify them or at least to differentiate them.

# Imports
from internal_library.asset_functions import beautify, beautify_string, clear_screen

tool_details = {
    "name":"Hash Identify",
    "filename":"hash_identify.py",
    "category":"Hash Cracking",
    "version":"1.0",
    "description":"This tool will identify a given hash."
}


def hash_identifier(hash):
    """2
    Identifies the type of a given hash based on its length.

    Parameters:
        hash (str): The hash string whose type needs to be identified.

    Returns:
        str: The identified hash type or a string indicating possible types.
    """
    # Mapping hash length to their respective types
    hash_type = {
        32: 'MD5 or NTLM',
        40: 'SHA1',
        56: 'SHA224',
        64: 'SHA256',
        96: 'SHA384',
        128: 'SHA512'
    }

    hash_length = len(hash)

    # Return the hash type based on length
    return hash_type.get(hash_length, "Unknown")

def main():
    """
    Main function to run the hash identifier.
    Asks user for a hash string and displays the identified hash type.
    """
    while True:
        clear_screen()
        try:
            title = beautify_string("Hash Identifier", "~")
            print(f"\n{title}")
            hash = input("Enter a hash to identify its type:\n>> ")
            if hash == "":
                input("No hash provided.")
                break
            hash_type = hash_identifier(hash)

            print(f"The hash type is: {hash_type}")

            # Additional logic for MD5 or NTLM can be handled here if needed
            if hash_type == 'MD5 or NTLM':
                print("The hash is either MD5 or NTLM. \nDo you know which one it is? (Y/n)")
                answer = input(">> ")
                if answer.lower() in ('y', 'yes', ''):
                    print("Enter 1 for MD5 or 2 for NTLM: ")
                    answer = input(">> ")
                    if answer == '1': # MD5
                        print("The hash type is: MD5")
                        break
                    elif answer == '2': # NTLM
                        print("The hash type is: NTLM")
                        return "ntlm"
                    else:
                        print("Invalid input.")
                        break
                else:
                    print("The hash type is: MD5 or NTLM")
                    break
            else:
                break
        except KeyboardInterrupt:
            print("Operation cancelled.")
            break
    input("Press ENTER to continue...") # Wait for user input before exiting

if __name__ == "__main__":
    main()