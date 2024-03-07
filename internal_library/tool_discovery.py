# This script will search the toolkits folder for all the tools.


# Imports #
import os


# Ignore list
# Should contain script necessary scripts so as not to list them to the user.
ignore_list = []


#======================#
# Directory Navigation #
#======================#



def working_directory():
    # Get current directory. -> Returns as a string.
    current_dir = os.getcwd()
    return current_dir

#========================#
# Directory Manipulation # 
#========================#

def read_dir_content(path):
    # Get directory of given path. -> Returning as a list.
    ls_dir = os.listdir(path)
    return ls_dir

def dir_content_full_path(path, content_list):
    # This function will iterate through the given directory, 
    # and return the full path for each object for use in other functions.
    
    dir_objects = []
    for content in content_list:
        path_plus_content = f"{path}\\{content}"
        dir_objects.append(path_plus_content)
    return dir_objects

def is_folder_result(dir_objects):
    # This will print out whether an object is a file or a folder/directory.
    folders = []
    files = []
    for object in dir_objects:
        if os.path.isdir(object):
            print(f"{object} <- (Folder)")
            folders.append(object)
        else:
            print(f"{object} <- (File)")
            files.append(object)
            
    return folders, files

# Testing Area
path = working_directory()
cwr_content = read_dir_content(working_directory())

# dir_content_paths = dir_iterate_objects(path,cwr_content)


            
#result = is_folder_result(dir_content_full_path(path,cwr_content))


print(path)

