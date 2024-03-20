'''
This will be a cracking software that will use a wordlist to crack a given hash.
It will first use the hash_identifier script to identify the hash type and then it will use the appropriate algorithm to crack it.

If the hash is MD5 or NTLM, it will ask the user if they know which one it is.
If they do, it will use the appropriate algorithm.
If they don't, it will use both algorithms.

If the hash is SHA1, SHA224, SHA256, SHA384 or SHA512, it will use the appropriate algorithm.
'''
tool_details = {
    "name": "Hash Cracker",
    "filename": "hash_cracker.py",
    "category": "Hash Cracking",
    "version": "1.0",
    "description": "This will crack a given hash using a wordlist."
}

import hashlib
import threading
import os
from multiprocessing import Queue
from internal_library.asset_functions import beautify, beautify_string, loading_bar, clear_screen, beautify_title, menu_option, center_text, center_block_text
from internal_library.detect_wordlists import detect_wordlists
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import time


# Assume other necessary imports and function definitions remain as before

def identify_hash(hash):
    """
    Identifies the type of hash based on its length.

    Args:
        hash (str): The hash to be identified.

    Returns:
        str: The type of hash if identified, otherwise "Unknown".
    """
    hash_type = {
        32: 'MD5 or NTLM',
        40: 'SHA1',
        56: 'SHA224',
        64: 'SHA256',
        96: 'SHA384',
        128: 'SHA512'
    }
    if len(hash) == 32:
        print("The hash is either MD5 or NTLM.")
        print("Do you know which one it is? (Y/n)")
        answer = input(">> ")
        if answer.lower() in ('y', 'yes', ''):
            print("Enter 1 for MD5 or 2 for NTLM: ")
            answer = input(">> ")
            if answer == '1':
                clear_screen()
                print("Cracking MD5 hash...")
                return 'MD5'
            elif answer == '2':
                clear_screen()
                print("Cracking NTLM hash...")
                return 'NTLM'
            else:
                print("Invalid input.")
        else:
            return hash_type.get(len(hash), "Unknown")
    else:
        print("Cracking hash...")
        return hash_type.get(len(hash), "Unknown")


class HashCracker:
    """
    A class for cracking hashes using a wordlist.

    Attributes:
        wordlist_path (str): The path to the wordlist file.
        lock (threading.Lock): A lock for thread synchronization.
        found (bool): A flag indicating if the hash has been cracked.
        total_words (int): The total number of words in the wordlist.
        processed_words (int): The number of words processed so far.

    Methods:
        wordlist_length(): Returns the length of the wordlist.
        update_progress(processed): Updates the progress of the hash cracking process.
        crack_batch(words, hash_to_crack, hash_function): Cracks a batch of words.
        load_and_crack(hash_to_crack, hash_function): Loads the wordlist and cracks the hash in batches.
        crack_hash(hash_to_crack): Cracks the given hash using the wordlist.
    """

    def __init__(self, wordlist_path):
        self.wordlist_path = wordlist_path
        self.lock = threading.Lock()
        self.found = False
        self.total_words = self.wordlist_length()
        self.processed_words = 0

    def wordlist_length(self):
        """
        Returns the length of the wordlist.

        Returns:
            int: The length of the wordlist.
        """
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
                return sum(1 for _ in wordlist)
        except FileNotFoundError:
            print("The wordlist file was not found.")
            return 0

    def update_progress(self, processed):
        """
        Updates the progress of the hash cracking process.

        Args:
            processed (int): The number of words processed in the current batch.
        """
        with self.lock:
            self.processed_words += processed
            progress = (self.processed_words / self.total_words) * 100
            print(f"\rProgress: {progress:.2f}%", end='')

    def crack_batch(self, words, hash_to_crack, hash_function):
        """
        Cracks a batch of words.

        Args:
            words (list): A list of words to be checked against the hash.
            hash_to_crack (str): The hash to be cracked.
            hash_function (function): The hash function to be used for hashing the words.

        Returns:
            None
        """
        for word in words:
            if self.found:
                return
            if hash_function(word) == hash_to_crack:
                with self.lock:
                    if not self.found:
                        cracked_message = beautify(f"Cracked: {hash_to_crack} = {word}", "#", 2)
                        print(f"\n{cracked_message}")
                        self.found = True
                        return
        self.update_progress(len(words))

    def load_and_crack(self, hash_to_crack, hash_function):
        """
        Loads the wordlist and cracks the hash in batches.

        Args:
            hash_to_crack (str): The hash to be cracked.
            hash_function (function): The hash function to be used for hashing the words.

        Yields:
            list: A batch of words from the wordlist.
        """
        batch_size = 10000  # Adjust based on optimal testing
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
                words_batch = []
                for word in wordlist:
                    words_batch.append(word.strip("\n"))
                    if len(words_batch) >= batch_size:
                        if self.found:
                            break
                        yield words_batch
                        words_batch = []
                if words_batch and not self.found:  # Process any remaining words
                    yield words_batch
        except FileNotFoundError:
            print("The wordlist file was not found.")
            return

    def crack_hash(self, hash_to_crack):
        """
        Cracks the given hash using the wordlist.

        Args:
            hash_to_crack (str): The hash to be cracked.

        Returns:
            None
        """
        start_time = time.time() # Start time for performance measurement
        
        hash_type = identify_hash(hash_to_crack)
        if hash_type not in ['MD5', 'NTLM', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512']:
            print("Unknown hash type.")
            return

        hash_function = { # Select the appropriate hash function based on the hash type
            'MD5': lambda word: hashlib.md5(word.encode()).hexdigest(),
            'NTLM': lambda word: hashlib.new('md4', word.encode('utf-16le')).hexdigest(),
            'SHA1': lambda word: hashlib.sha1(word.encode()).hexdigest(),
            'SHA224': lambda word: hashlib.sha224(word.encode()).hexdigest(),
            'SHA256': lambda word: hashlib.sha256(word.encode()).hexdigest(),
            'SHA384': lambda word: hashlib.sha384(word.encode()).hexdigest(),
            'SHA512': lambda word: hashlib.sha512(word.encode()).hexdigest()
        }.get(hash_type, lambda word: None)

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor: # Use all available CPU cores
            futures = [executor.submit(self.crack_batch, batch, hash_to_crack, hash_function) for batch in self.load_and_crack(hash_to_crack, hash_function)]
            concurrent.futures.wait(futures)

        end_time = time.time()
        elapsed_time = end_time - start_time # Calculate elapsed time
        if self.found:
            print(f"\nHash cracked in {elapsed_time:.2f} seconds.")
        else:
            print(f"\nFailed to crack the hash in {elapsed_time:.2f} seconds.")
        if not self.found:
            print("\nFailed to crack the hash.")

def menu_options():
    select_wordlist = menu_option(1, "Select Wordlist")
    enter_hash = menu_option(2, "Enter Hash to Crack")
    exit = menu_option(3, "Exit")
    return f"{select_wordlist}{enter_hash}{exit}"

def main_menu(chosen_wordlist=None, hash_to_crack=None):
    clear_screen()
    print(beautify_title("Hash Cracker", "=", 5))
    
    if chosen_wordlist == None:
        print("Selected Wordlist: N/A")
    else:
        print(f"Selected Wordlist: {chosen_wordlist}")

    print("\nSelect an option:")
    options = menu_options()
    print(f"{options}")
    choice = input(">> ").strip()
    return choice

def select_wordlist(wordlists):
    clear_screen()
    print(beautify_title("Select Wordlist", "=", 2))
    for i, wordlist in enumerate(wordlists, start=1):
        print(menu_option(i, f"{wordlist['name']} - {wordlist['length']} words"))
    print(menu_option(len(wordlists) + 1, "Go Back"))
    choice = int(input("> ").strip())
    if choice <= len(wordlists):
        return wordlists[choice - 1]['name']
    return None

# Usage example with menu integration
if __name__ == "__main__":
    wordlists = detect_wordlists()
    wordlist_path = None # Initialize the wordlist path
    hash_to_crack = None # Initialize the hash to crack
    select_wordlist_name = None # Initialize the selected wordlist name

    while True: # Main menu loop
        choice = main_menu(select_wordlist_name)
        if choice == '1': # Select wordlist
            selected_wordlist = select_wordlist(wordlists) # Select a wordlist
            if selected_wordlist:
                wordlist_path = os.path.join("wordlists", selected_wordlist)
                select_wordlist_name = selected_wordlist # Update the selected wordlist name
                print(f"Selected wordlist: {selected_wordlist}")
                time.sleep(1)
        elif choice == '2': # Enter hash to crack
            if wordlist_path:
                hash_to_crack = input("Enter the hash to crack: ").strip()
                hash_cracker = HashCracker(wordlist_path)
                hash_cracker.crack_hash(hash_to_crack)
                input("Press ENTER to continue...")
            else:
                print("Please select a wordlist first.")
                time.sleep(1)
        elif choice == '3' or "exit" in choice.lower():
            print("Exiting the program...")
            break
        elif "hash:" in choice: # For testing purposes
            hash_to_crack = choice.split(":")[1].strip()
            hash_cracker = HashCracker(wordlist_path)
            hash_cracker.crack_hash(hash_to_crack)
            input("Press ENTER to continue...")
        clear_screen()
        