
"""
# This function will take input from the json file called "tools.json" in the folder "tool_folder".
# It will extract the tools by name corresponding to the "Category" section provided by the request.
# For each entry in the json file the following template is used:
{
    "name": "Hash Identify",
    "category": "Hash Cracking",
    "version": "1.0",
    "description": "This tool will identify a given hash.",
    "location" : PATH
}
"""
import os
import json
import subprocess
from internal_library.asset_functions import clear_screen, beautify_title, center_text
from internal_library.detect_tools import main as detect

tool_list = []

def normalize_tool_data(tool):
    # Normalize the keys to lowercase
    normalized_tool = {key.lower(): value for key, value in tool.items()}
    return normalized_tool

def get_tools_by_category(category):
    """
    Retrieves a list of tools from a JSON file based on the specified category.

    Args:
        category (str): The category of tools to retrieve.

    Returns:
        list: A list of tools that belong to the specified category.

    Raises:
        FileNotFoundError: If the tools.json file does not exist in the specified folder.
        json.JSONDecodeError: If there is an error decoding JSON from the file.
        Exception: If any other error occurs during the process.
    """
    tool_folder_path = "tool_folder"
    json_file_name = "tools.json"
    json_path = os.path.join(tool_folder_path, json_file_name)
    
    if not os.path.exists(json_path):
        print("The tools.json file does not exist in the specified folder.")
        return []
    
    try:
        with open(json_path, 'r') as file:
            tools = json.load(file)
        
        filtered_tools = []
        for tool in tools:
            normalized_tool = normalize_tool_data(tool)  # Normalize the tool data
            if normalized_tool.get('category', '').lower() == category.lower():
                filtered_tools.append(normalized_tool)  # Use the normalized tool for further operations

        if not filtered_tools: # If no tools are found in the category
            print(f"No tools found in the category '{category}'.")
            return []
        
        for tool in filtered_tools: # Print the tools found in the category
            tool_list.append(tool)
            print(f"Name: {tool['name']}, Version: {tool['version']}, Description: {tool['description']}")

        return filtered_tools
        
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return []


def load_tools_from_json():
    """
    Load tools from a JSON file.

    Reads the tools.json file located in the specified tool_folder_path and returns the loaded tools as a list.

    Returns:
        list: A list of tools loaded from the JSON file.

    Raises:
        FileNotFoundError: If the tools.json file does not exist in the specified folder.
        json.JSONDecodeError: If there is an error decoding JSON from the file.
        Exception: If any other error occurs during the loading process.
    """
    tool_folder_path = "tool_folder"
    json_file_name = "tools.json"
    json_path = os.path.join(tool_folder_path, json_file_name)
    
    if not os.path.exists(json_path):
        print("The tools.json file does not exist in the specified folder.")
        return []
    
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return []

def get_unique_categories(tools):
    """
    Get the unique categories of tools.

    Args:
        tools (list): A list of tools.

    Returns:
        set: A set containing the unique categories of the tools.
    """
    categories = set()
    for tool in tools:
        normalized_tool = normalize_tool_data(tool)
        categories.add(normalized_tool.get('category', 'Uncategorized').lower())
    return categories

def display_tools_by_category(tools, category):
    """
    Display tools by category.

    Args:
        tools (list): List of tools.
        category (str): Category to filter the tools by.

    Returns:
        None
    """
    filtered_tools = [tool for tool in tools if tool.get('category', '').lower() == category.lower()]
    if not filtered_tools:
        print(f"No tools found in the category '{category}'.")
    else:
        for tool in filtered_tools:
            print(f"Name: {tool['name']}, Version: {tool['version']}, Description: {tool['description']}")

def main():
    """
    This function is the entry point of the program. It allows the user to select a category and a tool,
    and then executes the chosen tool script.
    """
    
    # Validate the tool_folder path
    tools = load_tools_from_json() # Load tools from the JSON file
    normalized_tools = [normalize_tool_data(tool) for tool in tools] # Normalize the tools for further operations
    
    categories = get_unique_categories(normalized_tools) # Get the unique categories of the tools
    if not categories:
        print("No categories found.")
        return # Exit the program if no categories are found
    else:
        pass
    
    
    print("Select a category:") 
    
    # Display the categories with their index numbers
    for i, category in enumerate(sorted(categories), 1):
        print(f"{i}. {category.title()}")
        
    
    try: 
        # Prompt the user to select a category
        category_choice = input("\nEnter your choice (number) for category: \n>> ")
        
        # Quick Commands
        if category_choice == "exit":
            print("Exiting the program...")
            exit()
        elif category_choice == "cls":
            clear_screen()
            return
        elif category_choice == "help":
            print("Type 'exit' to exit the program, 'cls' to clear the screen, or 'help' to display this message.")
            return
        elif category_choice == "crack":
            pass
        elif category_choice == "network":
            pass
        elif category_choice == "list":
            # This will list all tools in all categories. All Categories will be in upper case.
            for category in categories:
                category_title = beautify_title(f"{category}","~", 1)
                print(category_title)
                display_tools_by_category(normalized_tools, category)
            return
        elif category_choice == "update":
            detect()
            return
        
        chosen_category = list(sorted(categories))[int(category_choice) - 1]
        
        clear_screen()
        #print(f"\nTools in category '{chosen_category.capitalize()}':\n")
        category_title = beautify_title(f"{chosen_category}","~", 1)
        print(category_title)
        
        
        category_tools = [tool for tool in normalized_tools if tool['category'].lower() == chosen_category]
        for i, tool in enumerate(category_tools, 1):
            print(f"{i}. {tool['name']}")
        
        #######################
        # SELECT TOOL SECTION #
        #######################
        
        # Prompt the user to select a tool
        tool_choice = int(input("\nEnter your choice (number) for tool: \n>> ")) - 1
        chosen_tool = category_tools[tool_choice] # Get the chosen tool from the list of tools
        
        # Assuming the tool's name corresponds to a script filename in the tool_folder | WARNING: This is a security risk!
        tool_script_path = os.path.join("tool_folder", chosen_tool['filename'].replace(" ", "_"))
        print(f"Running {chosen_tool['name']} from {tool_script_path}...") # Note to self: Hide this from output?
        
        # Execute the tool script
        subprocess.run(["python", tool_script_path], check=True)
        
    except (ValueError, IndexError):
        print("Invalid selection. Please enter a valid number.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute the tool script: {e}")

if __name__ == "__main__":
    main()
