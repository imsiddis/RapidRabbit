import os
import json
import shutil
from pathlib import Path

# Define the tool folder and JSON file paths
TOOL_FOLDER = "tool_folder"
TOOLS_JSON_FILE = os.path.join(TOOL_FOLDER, "tools.json")

# Ensure the tool folder exists
os.makedirs(TOOL_FOLDER, exist_ok=True)

# Prompt the user for the JSON fields
name = input("Enter the tool name: ")
category = input("Enter the tool category: ")
version = input("Enter the tool version: ")
description = input("Enter the tool description: ")
location = input("Enter the path to the tool script file: ")

# Copy the tool script file to the tool folder
tool_script_filename = os.path.basename(location)
tool_script_path = os.path.join(TOOL_FOLDER, tool_script_filename)
shutil.copy(location, tool_script_path)

# Create the tool dictionary
tool_details = {
    "name": name,
    "filename": tool_script_filename,
    "category": category,
    "version": version,
    "description": description,
    "location": tool_script_path
}

# Load existing tools from the JSON file
if os.path.exists(TOOLS_JSON_FILE):
    with open(TOOLS_JSON_FILE, 'r') as file:
        tools = json.load(file)
else:
    tools = []

# Add the new tool data to the list
tools.append(tool_details)

# Save the updated tools list back to the JSON file
with open(TOOLS_JSON_FILE, 'w') as file:
    json.dump(tools, file, indent=4)

print(f"Tool '{name}' has been added successfully to {TOOLS_JSON_FILE}.")

# Read the existing script content
with open(tool_script_path, 'r') as file:
    script_content = file.readlines()

# Define the new dictionary content
new_dict_content = f"\ntool_details = {json.dumps(tool_details, indent=4)}\n"

# Find the insertion point (after imports and before the first function)
insert_point = 0
for i, line in enumerate(script_content):
    if line.strip().startswith("def "):
        insert_point = i
        break

# Insert the new dictionary content
updated_script_content = script_content[:insert_point] + [new_dict_content] + script_content[insert_point:]

# Write the updated content back to the script file
with open(tool_script_path, 'w') as file:
    file.writelines(updated_script_content)

print(f"The dictionary has been added to {tool_script_path} successfully.")
