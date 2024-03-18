# This script will be a hash generator tool.
# You will give it a string and it will then generate a hash of the string in several different formats.


# Imports
import hashlib
from internal_library.asset_functions import clear_screen, beautify, beautify_string, beautify_title

tool_details = {
    "name": "Hash Generator",
    "filename": "hash_generator.py",
    "category": "Hash Cracking",
    "version": "1.0",
    "description": "This will generate hashes using an input."
}


#==================#
# Global Variables #
#==================#

string = ""
hashes = {}

#==================#
#  Hash Functions  #
#==================#

def generate_hash(string):
    """Function to generate a hash of the given string in several different formats."""
    global hashes
    hashes = {
        "md5": hashlib.md5(string.encode()).hexdigest(),
        "sha1": hashlib.sha1(string.encode()).hexdigest(),
        "sha224": hashlib.sha224(string.encode()).hexdigest(),
        "sha256": hashlib.sha256(string.encode()).hexdigest(),
        "sha384": hashlib.sha384(string.encode()).hexdigest(),
        "sha512": hashlib.sha512(string.encode()).hexdigest(),
        "ntlm": hashlib.new('md4', string.encode('utf-16le')).hexdigest()
    }
    
    return hashes

def main():
    while True:
        clear_screen()
        print(beautify_title("Hash Generator","~",5))
        print("\nThis tool will generate a hash of the given string in several different formats.")
        print("\nPlease enter the string to generate the hash: ")
        string = input("\nString: ")
        
        if string == "exit":
            break
        
        hashes = generate_hash(string)
        print("\nHashes generated successfully.")
        print("\nHashes:")
        for hash_type, hash_value in hashes.items():
            print(f"{hash_type.upper()}: {hash_value}")
        input("\nPress 'Enter' to continue... ")
    
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            input("\nPress 'Enter' to continue... ")