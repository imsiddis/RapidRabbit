# This will be functions that can be used by any file in the project.
#
# Imports
import os
import sys
import time
import datetime
import platform
import socket

# Clear the screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
# Animated loading bar
def loading_bar():
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write("\r")
        sys.stdout.write("[%-10s] %d%%" % ("="*i, 10*i))
        sys.stdout.flush()
    print("")
    
# Exit the program
def exit_program():
    clear_screen()
    print("Thank you for using the program.")
    time.sleep(2)
    sys.exit()
    
# Get the current date and time
# The format will be DD-MM-YYYY HH:MM:SS
def get_date_time():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")

# Get the current operating system
def get_os():
    return platform.system()

# Get the current working directory
def get_cwd():
    return os.getcwd()

# Get the current user
def get_user():
    return os.getlogin()

# Get the current platform
def get_platform():
    return platform.platform()

# Get current python version
def get_python_version():
    return platform.python_version()

#=============================#
#   Beautify CLI Functions    #
# Make menus look nice here:  #
#=============================#

def beautify_string(string, border):
    """Beautifies A string with borders above and below.

    Args:
        string (_type_): A string that will be parsed.
        x (_type_): Char you want to beatify the results.
    """
    string_length = len(string) * border
    return f"\n{string_length}\n{string}\n{string_length}\n"

def beautify_title(string, border_char, padding=0):
    """ Beautifies a title with padding and borders. """
    # Original string length
    title_length = len(string)
    
    # Capitalize Title
    string = string.upper()
    
    # Padding Start-End.
    title_padding_start = border_char + (padding * " ")
    title_padding_end = (padding * " ") + border_char
    
    # Title Length After Padding
    title_length_after_padding = len(title_padding_start) + title_length + len(title_padding_end)
    
    # Title with padding
    title_with_padding = f"{title_padding_start}{string}{title_padding_end}"
    
    # Adding Borders
    border_char = title_length_after_padding * border_char
    
    # Beautified Title Result
    beautified_title = f"{border_char}\n{title_with_padding}\n{border_char}"
    
    return beautified_title

def beautify(text, border_char, padding=2, is_title=False, is_heading=False): # NB: This code might take over for each instance needed for beauitfying text.
    if is_title:
        text = text.upper()
    elif is_heading:
        text = text.title()
    else:
        pass
    
    
    # Split the text into lines.
    lines = text.split("\n")
    
    # Get dimensions of the lines.
    max_line_length = max(len(line) for line in lines) # Get the maximum length of the provided string.
    box_width = max_line_length + (padding * 2)
    
    # Top Border.
    box = [border_char * box_width]
    
    # Add each line with padding.
    for line in lines:
        line_with_padding = line.center(max_line_length) # This will align the text to the center.
        box.append(f"{border_char} {line_with_padding} {border_char}".ljust(box_width - 1))
        
    # Bottom border.
    box.append(border_char * box_width)
    
    return "\n".join(box)


# ASCII Logo and Title
def splash_screen(logo=True,title=True):
    return f"""
                                                            (%%%%%%%%%%%%%%%%                               
                                                      .%%%%%%%%%&.     .&%%%%%%%%%                          
                                                   &&&&%&           %  %%       &&&&&&                      
                                                &&&&&       &&&&&&.        &(  ,    &&&&&                   
                                              &&&&/           &&&&&&&&&    &&&&&&&    %&&&&                 
                                            &&&&,   @@@@@.      @&&&&&@@@     &          &&&&               
                                           @&&&&&&&   @@@@@@@@@@    @@@@@@@      @@@@&&&&&&&&@              
                                          @@@@@&&&&&&&  @@@@@@@@@@@@@  @@@@@@         @&@  @@@@             
                                         (######@@          @@@@@@@@@@@@  @@@@@@@        @@ @@@@            
                                        @@@@.   @@         @         @@@@@@@@@@@@@@@@@       @@@@           
                                        @@@@@@&&&&&%%%%%%%&&%%%%%@@      @@@@@@@/    @@@     @@@@           
                                                                          @@@@@@@@@@@@@@@@   @@@@           
                                        @@@@@@@@@@@@                    @@@@@@@@@@@@@@@@@#   @@@@           
                                        @@@@@@@@      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     ,  @@@&           
                                                  %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      & @  @@@@            
                                             @  @@@@@@@@,@@@@@@@@@@@@@@@@@@@@@@            @@@@             
                                           **/////**//(@@@  @@@@@@@@@@@@@@@@@@            @@@@              
                                                       ,@  /@@@@@@@@@@@@@@@@@      .(   @@@@@               
                                              @@@@@@@@@@@@@@@@@@    @@@@@@@@   (@     @@@@@                 
                                                                @@@@  @@@@         @@@@@@                   
                                                   @@@@@@@@@@@  @@@@           @@@@@@@                      
                                                       @@@@@@@@@@     .@@@@@@@@@@@                          
                                                             @@@@@@@@@@@@@@@                                
                                                                                  """
def splash_logo_no_indent():
    print("""
          
                        (%%%%%%%%%%%%%%%%                               
                  .%%%%%%%%%&.     .&%%%%%%%%%                          
               &&&&%&           %  %%       &&&&&&                      
            &&&&&       &&&&&&.        &(  ,    &&&&&                   
          &&&&/           &&&&&&&&&    &&&&&&&    %&&&&                 
        &&&&,   @@@@@.      @&&&&&@@@     &          &&&&               
       @&&&&&&&   @@@@@@@@@@    @@@@@@@      @@@@&&&&&&&&@              
      @@@@@&&&&&&&  @@@@@@@@@@@@@  @@@@@@         @&@  @@@@             
     (######@@          @@@@@@@@@@@@  @@@@@@@        @@ @@@@            
    @@@@.   @@         @         @@@@@@@@@@@@@@@@@       @@@@           
    @@@@@@&&&&&%%%%%%%&&%%%%%@@      @@@@@@@/    @@@     @@@@           
                                      @@@@@@@@@@@@@@@@   @@@@           
    @@@@@@@@@@@@                    @@@@@@@@@@@@@@@@@#   @@@@           
    @@@@@@@@      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     ,  @@@&           
              %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      & @  @@@@            
         @  @@@@@@@@,@@@@@@@@@@@@@@@@@@@@@@            @@@@             
       **/////**//(@@@  @@@@@@@@@@@@@@@@@@            @@@@              
                   ,@  /@@@@@@@@@@@@@@@@@      .(   @@@@@               
          @@@@@@@@@@@@@@@@@@    @@@@@@@@   (@     @@@@@                 
                            @@@@  @@@@         @@@@@@                   
               @@@@@@@@@@@  @@@@           @@@@@@@                      
                   @@@@@@@@@@     .@@@@@@@@@@@                          
                         @@@@@@@@@@@@@@@
          """)
    splash_screen_title = """

     _______ _              ______              _     _    ______        _     _     _          _______          _  _     _       
    (_______) |            (_____ \            (_)   | |  (_____ \      | |   | |   (_)  _     (_______)        | || |   (_)  _   
        _   | |__  _____    _____) )_____ ____  _  __| |   _____) )_____| |__ | |__  _ _| |_       _  ___   ___ | || |  _ _ _| |_ 
       | |  |  _ \| ___ |  |  __  /(____ |  _ \| |/ _  |  |  __  /(____ |  _ \|  _ \| (_   _)     | |/ _ \ / _ \| || |_/ ) (_   _)
       | |  | | | | ____|  | |  \ \/ ___ | |_| | ( (_| |  | |  \ \/ ___ | |_) ) |_) ) | | |_      | | |_| | |_| | ||  _ (| | | |_ 
       |_|  |_| |_|_____)  |_|   |_\_____|  __/|_|\____|  |_|   |_\_____|____/|____/|_|  \__)     |_|\___/ \___/ \_)_| \_)_|  \__)
                                         |_|                                                                                      
    """

#===================================#
# Automatic Menu Integration System #
#===================================#

def menu_option(option_number, option_name, style=1):
    # This function will present the menu as specified by its input variables.
    option_style_1 = f"[{option_number}] - {option_name}\n"
    option_style_2 = f"[{option_number}] ~ {option_name}\n"
    option_style_3 = f"{option_number}. {option_name}\n"
    
    if style == 1:
        return option_style_1
    elif style == 2:
        return option_style_2
    elif style == 3:
        return option_style_3
    else:
        return "No valid style was selected."


#======================#
# NETWORKING FUNCTIONS #
#======================#

def resolve_hostname(hostname):
    """ Resolves a hostname to an IP address. """
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        raise ValueError(f"Could not resolve hostname: {hostname}")
    