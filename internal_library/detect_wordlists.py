# This function will load the wordlists from the wordlists folder.
# It will add them to a wordlist json file for use in the menu system if needed.
# If the wordlists folder does not exist, it will create it.
# If the wordlists.json file does not exist, it will create it.
# The content of the wordlists.json will be:
# [
#     {
#         "name": "name of the file",
#         "length": x (number of lines in the file)
#     },
#     {
#         "name": "name of the file",
#         "length": x (number of lines in the file)
#     }
# ]

# Imports
import os
import json

# Load wordlists from the wordlists folder

def detect_wordlists():
    """
    Load wordlists from the wordlists folder.

    Reads the wordlists from the wordlists folder and adds them to a wordlist json file for use in the menu system if needed.
    If the wordlists folder does not exist, it will create it.
    If the wordlists.json file does not exist, it will create it.
    The content of the wordlists.json will be:
    [
        {
            "name": "name of the file",
            "length": x (number of lines in the file)
        },
        {
            "name": "name of the file",
            "length": x (number of lines in the file)
        }
    ]

    Returns:
        list: A list of wordlists loaded from the wordlists folder.
    """
    wordlists_folder_path = "wordlists"
    json_file_name = "wordlists.json"
    json_path = os.path.join(wordlists_folder_path, json_file_name)

    # Create the wordlists folder if it does not exist
    if not os.path.exists(wordlists_folder_path):
        os.makedirs(wordlists_folder_path)

    # Create the wordlists.json file if it does not exist
    if not os.path.exists(json_path):
        with open(json_path, 'w') as file:
            json.dump([], file)

    # Load wordlists from the wordlists folder
    wordlists = []
    for file in os.listdir(wordlists_folder_path):
        if file.endswith(".txt"):
            file_path = os.path.join(wordlists_folder_path, file)
            with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                wordlists.append({"name": file, "length": len(lines)})

    # Save wordlists to the wordlists.json file
    with open(json_path, 'w') as file:
        json.dump(wordlists, file, indent=4)

    return wordlists

detect_wordlists()