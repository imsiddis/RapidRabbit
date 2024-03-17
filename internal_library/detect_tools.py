import os
import json

# Assuming the internal_library modules work as expected. Otherwise, consider alternatives or validations.
from internal_library.asset_functions import clear_screen
from internal_library.tool_discovery import read_dir_content as ls_dir

# Global Variables
tool_folder_name = "tool_folder"  # Folder name where tools are located
json_file_name = "tools.json"  # Name of the JSON file to store the tool details

# Function to find the tool folder path
def get_script_paths():
    cwd = os.getcwd()
    tool_folder_path = os.path.join(cwd, tool_folder_name)
    if os.path.exists(tool_folder_path) and os.path.isdir(tool_folder_path):
        return tool_folder_path
    return None

# Function to read scripts from the tool folder and check for "tool_details"
def get_scripts(folder_path):
    script_paths = []
    ignore_list = []
    dir_content = os.listdir(folder_path)
    for file_name in dir_content:
        full_path = os.path.join(folder_path, file_name)
        if os.path.isfile(full_path) and file_name.endswith(".py"):
            with open(full_path, "r") as file:
                if "tool_details" in file.read():
                    script_paths.append(full_path)
                else:
                    ignore_list.append(file_name)
    return script_paths, ignore_list

# Function to extract tool details from python scripts safely
def get_tool_details(script_paths):
    detailed_tools = []
    ignore_list = []
    for tool_path in script_paths:
        with open(tool_path, "r") as file:
            content = file.read()
            local_env = {}
            try:
                exec(content, {}, local_env)  # Execute in an isolated environment
                if 'tool_details' in local_env:
                    tool_info = local_env['tool_details']
                    # Further validation to ensure everything in tool_info is serializable
                    if isinstance(tool_info, dict):
                        detailed_tools.append(tool_info)
                    else:
                        print(f"tool_details is not a dictionary in {tool_path}.")
                        ignore_list.append(tool_path)
                else:
                    ignore_list.append(tool_path)
            except Exception as e:
                print(f"Error processing {tool_path}: {e}")
                ignore_list.append(tool_path)
    return detailed_tools, ignore_list


# Function to serialize tool details to a JSON file
def tool_json_append(tool_folder_path, tools_info):
    json_path = os.path.join(tool_folder_path, json_file_name)
    try:
        with open(json_path, "w") as file:
            json.dump(tools_info, file, indent=4)
    except TypeError as e:
        print(f"Serialization error: {e}")
    except Exception as e:
        print(f"Error writing to {json_path}: {e}")
# Main function to coordinate the script execution
def main():
    clear_screen()
    tool_folder_path = get_script_paths()
    if tool_folder_path:
        script_paths, initial_ignore_list = get_scripts(tool_folder_path)
        detailed_tools, detailed_ignore_list = get_tool_details(script_paths)
        tool_json_append(tool_folder_path, detailed_tools)
        #print(json.dumps(detailed_tools, indent=4))
        #print("Ignored files:", initial_ignore_list + detailed_ignore_list)
        print("Updated tools.json with the tool details.")
    else:
        print("Tool folder not found. Please ensure it's in the current working directory.")

if __name__ == "__main__":
    main()
