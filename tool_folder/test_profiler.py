# This script will handle the dealings with profiling a target.
# As the saying goes "Knowledge is power", especially when you are targeting someone specific.
# The data stored in the profiles, should then be able to be used by other scripts.

#tool_details = {
#    "name":"Profiler",
#    "filename":"test_profiler.py",
#    "Category":"Profiles", 
#    "Version":"a0.1",
#    "Description":"The profiler lets you manage target profiles."
#}

# Imports
import json
import os
from internal_library.asset_functions import clear_screen, beautify, beautify_string, beautify_title
import time


# Name of the json file where profiles are stored.
profiles_file = "profiles.json"

# Ensure the profiles file exists
def init_profiles_file():
    if not os.path.exists(profiles_file):
        with open(profiles_file, 'w') as file:
            json.dump([], file)

# Load profiles from JSON
def load_profiles():
    with open(profiles_file, 'r') as file:
        return json.load(file)

# Save profiles to JSON
def save_profiles(profiles):
    with open(profiles_file, 'w') as file:
        json.dump(profiles, file, indent=4)

# Add a new profile
def add_profile():
    profiles = load_profiles()
    name = input("Enter the profile name (required): ").strip()
    # Ensure name is provided
    if not name:
        print("Profile name is required.")
        return
    # Check if the profile already exists
    if any(profile['profile_name'] == name for profile in profiles):
        print("A profile with this name already exists.")
        return
    new_profile = {"name": name}
    # Dynamically add other details
    while True:
        key = input("Enter detail to add (or press enter to finish): ").strip()
        if key == "":
            break
        value = input(f"Enter {key} value: ").strip()
        new_profile[key] = value
    profiles.append(new_profile)
    save_profiles(profiles)
    print("Profile added successfully.")
    
# List existing profiles
def list_profiles_name():
    profile_list = []
    profiles = load_profiles()
    if not profiles:
        raise TypeError("NoneType")
    for profile in profiles:
        profile_list.append(profile['name'])
        print(f"Profile: {profile['name']}")
    return profile_list




# Main function to run the CLI application
def main():
    list_of_profiles = []
    init_profiles_file()
    while True:
        try:
            clear_screen()
            title = beautify_title("Profiler","~",1)
            print(f"\n{title}\n")
            print("1. Add Profile")
            print("2. Edit Profile (To be implemented)")
            print("3. View Profiles")
            print("4. Exit")
            choice = input("\nEnter your choice: \n>> ").strip()
            if choice == '1':
                add_profile()
            elif choice == '2':
                # Placeholder for edit_profile function
                print("Edit profile feature coming soon.")
            elif choice == '3':
                clear_screen()
                print(beautify_title("Profiles","~",1))
                profile_list = list_profiles_name()
                for i in profile_list:
                    list_of_profiles.append(i)
                input("\nPress ENTER to continue...")

            elif choice == '4':
                print("Exiting...")
                return
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("Operation cancelled.")
            break
        except TypeError as e:
            if "NoneType" in str(e): # If no profiles are found
                error_message = beautify_string("| Error: No profiles found. |","-")
                print(f"{error_message}\nPlease add a profile to continue.")
                input("Press ENTER to continue...")
            else:
                print(f"An error occurred: {e}")
                input("Press ENTER to continue...")
        except Exception as e:
            print(f"An error occurred: {e} 120")
            input("Press ENTER to continue...")
    #input("Press ENTER to continue...") # Wait for user input before exiting

if __name__ == "__main__":
    main()
