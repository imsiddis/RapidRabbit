tool_details = {
    "name":"Port Scanner",
    "filename":"port_scanner.py",
    "Category":"Network", 
    "Version":"1.0",
    "Description":"This will scan a target to check if ports are open."
}


# This script will take a url/ip address and scan it for open ports.

# It will take a port range as input and scan the target for open ports in that range.

#=========#
# Imports #
#=========#
import socket
import random
import time
import argparse
from internal_library.asset_functions import beautify_string, beautify_title, clear_screen, sanitize_target_input, sanitize_port_input, splash_logo_no_indent, center_block_text, center_text

#=================#
# Argument Parser #
#=================#


def parse_args():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("-t", "--target", help="Target IP address to scan")
    parser.add_argument("-p", "--ports", help="Port range to scan, e.g., '20-80' or '80,443'")
    parser.add_argument("-r", "--random", action="store_true", help="Randomize the order of port scanning")
    parser.add_argument("--min-delay", type=float, default=0, help="Minimum delay between port scans in seconds")
    parser.add_argument("--max-delay", type=float, default=0, help="Maximum delay between port scans in seconds")
    args = parser.parse_args()

    # Sanitize inputs if they are provided
    if args.target:
        args.target = sanitize_target_input(args.target)
    if args.ports:
        args.ports = sanitize_port_input(args.ports)
    
    return args


def process_ports_arg(ports_str):
    """
    Processes the ports argument string and returns a list of port numbers.
    """
    ports = []
    if "-" in ports_str:
        ports = port_range(ports_str)
    elif "," in ports_str:
        ports = port_select(ports_str)
    elif ports_str.isdigit():
        ports = [int(ports_str)]
    else:
        raise ValueError("Invalid ports format. Use 'start-end' for range or 'port1,port2,...' for individual ports.")
    return ports


def is_port_open(target, port):
    # Creating the socket object.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    
    try:
        # Attempt to connect to target using specified port.
        s.connect((target, port))
        return True
    except:
        return False
    finally:
        s.close()


def scan_ports(target, port_range):
    # This function will be used to scan the target and port.
    open_ports = []
    
    for port in (port_range):
        if is_port_open(target, port):
            open_ports.append(port)
            print(f"Port {port} is [-> OPEN <-]")
        else:
            print(f"Port {port} is [CLOSED].")
    
    return open_ports

#========================#
# Stealth Scan Functions #
#========================#

def slow_scan(target, port_range, min_delay=1, max_delay=0):
    open_ports = []
    
    for port in port_range:
        
        time_delay = random.uniform(min_delay, max_delay) # Random delay between scans
        time.sleep(time_delay) # Sleep for random delay
        
        if is_port_open(target, port):
            open_ports.append(port)
            print(f"Port {port} is [-> OPEN <-]")
        else:
            print(f"Port {port} is [CLOSED].")
    
    return open_ports



def random_port_order(port_list):
    """
    Randomizes the order of a given list of port numbers.
    
    Parameters:
    - port_list: A list of port numbers.
    
    Returns:
    - A list of ports in a random order.
    """
    # Make a copy of the port list to avoid modifying the original list
    ports = list(port_list)
    
    # Shuffle the list of ports to randomize their order
    random.shuffle(ports)
    
    return ports


#==========================#
# Port Selection Functions #
#==========================#

def port_range(user_input):
    port_list = []
    try:
        # Split port range
        port_range = user_input.split("-")
        
        # Check that input is correctly submitted with a "start-end" format.
        if len(port_range) != 2:
            raise ValueError("Input must be a range in the format \"start-end\".")
        
        # Convert port range to integers
        port_range = range(int(port_range[0]), int(port_range[1]) + 1)
        for i in port_range:
            port_list.append(i)
    except ValueError as e:
        return f"Invalid input: {e}"
    
    return port_list
    
def port_select(user_input):
    # This function will used to select specific individual ports. 
    port_list = []
    
    # Error Handling if extra comma is in user input.
    if "," in user_input[-1]:
        user_input = user_input[:-1]
    else:
        pass
        
    # Splitting the chosen ports and then append to port_list.
    selected_ports = user_input.split(",")
    for i in selected_ports:
        port_list.append(int(i))    
    return port_list



#=======[START]======#
#    Get Functions   # 
#====================#

def get_ports():
    port_choice = input("Enter port range or select individual ports.\nEnter here: ")
    
    sanitized_choice = sanitize_port_input(port_choice)
    
    if "-" in sanitized_choice:
        # If "-" is used indicating a range of ports, then it will be handled here.
        print(port_range(sanitized_choice))
    elif "," in sanitized_choice:
        # If individual ports are selected, then it will be handled there.
        port_choice = sanitize_port_input(port_choice)
        print(port_select(sanitized_choice))
    elif sanitized_choice.isdigit():
        # Handle a single port
        return [int(sanitized_choice)]
    else:
        input("Error in deciding.")
        exit()

def get_target(target_choice):
    # Get the target IP from the user 
    target_choice = input("Enter Target IP: ")
    
    sanitized_choice = sanitize_target_input(target_choice)
    print(f"IP Chosen: {sanitized_choice}")
    verify_user_choice = input("Is this correct? [Y/n]\n")
    if verify_user_choice.lower() in [" ","","y","yes","yeah",]:
        print("Target acquired.")
        print(f"Target IP: {sanitized_choice}")
        return sanitized_choice
    else:
        input("Press ENTER to try again.")
        get_target()
        

#=======[ END ]======#
# Get Port Functions #
#====================#

port_scanner_options = """
1. Scan Ports
2. Exit
"""

help_section = """
This tool will scan a target to check if ports are open.

Shortcut commands:
    exit - Exit the program
    help - Display this message


You can enter a port range or select individual ports:

To chose a range you will use the following format:
    i.e. "20-80", "80-443", "1-65535" etc.
To chose individual ports you will use the following format:
    i.e. "80,443,8080,22,21" etc.
You can also enter a single port to scan.
    i.e. "80", "443", "8080", "22", "21" etc.

"""

menu_tip = """
This tool will scan a target to check if ports are open.
You can enter a port range or select individual ports.
You can write "exit" to return to the main menu or "help" to display the full help section.
"""


def main():
    while True:
        try:
            clear_screen()
            target = ""
            port_choice = ""
            logo = center_block_text(splash_logo_no_indent())
            print(logo)
            title = center_block_text(beautify_title("Port Scanner","~",5))
            tip = center_text(menu_tip)
            print(title)
            print(tip)
            print(port_scanner_options)
            
            user_choice = input(">> ")
            try:
                if user_choice == "1":
                    clear_screen()
                    print(logo)
                    print(title)
                    print("Testing of port scanner:")
                    target_choice = input("Enter Target IP: ")
                    if target_choice.lower == "exit":
                        break
                    elif target_choice.lower == "help":
                        print(help_section)
                        input("Press Enter to continue.")
                        break
                    else:
                        target = sanitize_target_input(target_choice)
                        print(f"IP Chosen: {target}")
                    try:
                        # Get ports as a list
                        port_choice = input("Enter port range or select individual ports.\nEnter here: ")
                        if port_choice == "exit":
                            exit()
                        else:
                            pass
                        sanitized_choice = sanitize_port_input(port_choice)
                        ports = []

                        # Display Status: In Progress
                        styled_in_progress = beautify_string("[SCANNING IN PROGRESS]", "=")

                        # Different Scanning Vectors
                        if "-" in sanitized_choice:
                            # Range
                            print(styled_in_progress) # Print Status: Progress
                            ports = port_range(sanitized_choice)
                        elif "," in sanitized_choice:
                            # Individual Range 
                            print(styled_in_progress) # Print Status: Progress
                            ports = port_select(sanitized_choice)
                        else:
                            # Specific
                            print(styled_in_progress) # Print Status: Progress
                            status = is_port_open(target, int(port_choice))
                            if status == False:
                                print(f"Port {port_choice} is [CLOSED].")
                            else:
                                #print(f"Port {port_choice} is [OPEN]")
                                ports.append(int(port_choice))

                        ports_open = scan_ports(target, ports)

                        # Reporting Findings in nice formatting.
                        num_open_ports = len(ports_open)
                        str_num_ports = f"Amount of open ports: {num_open_ports}"

                        print(beautify_string(str_num_ports, "-"))

                        if len(ports_open) != 0:
                            print("\nOpen Ports Discovered:")
                            print("----------------------")
                            for i in ports_open:
                                print(f"Port: {i}")
                            else:
                                pass
                            
                        end_of_scan = beautify_string("End of Scan", "~")
                        print(f"\n{end_of_scan}")
                        input("Press Enter to return to main menu.")
                        return
                    except KeyboardInterrupt:
                        print("\nScan cancelled by user.")
                        input("Press Enter to return to main menu.")
                        break
                    except ValueError as e:
                        print(f"An error occurred: {e}")
                        input("Press Enter to continue...")
                        return
                
                elif user_choice == "2" or "exit".lower():
                    print("Not exiting right")
                    print("Exiting the program...")
                    exit()
                    
            except KeyboardInterrupt:
                print("\nScan cancelled by user.")
                input("Press Enter to return to main menu.")
                break
        except KeyboardInterrupt:
            print("\nScan cancelled by user.")
            exit()
            
        except ValueError as e:
            print("Returning to main menu.")
            exit()
            

if __name__ == "__main__":
    
    # Parse command-line arguments
    args = parse_args()
    if args.target and args.ports:
        # Convert ports from string to list of integers
        ports_to_scan = process_ports_arg(args.ports)
        
        # Randomize the port order if the -r flag is set
        if args.random:
            ports_to_scan = random_port_order(ports_to_scan)
            
        if args.min_delay > 0 or args.max_delay > 0:
            # Perform the scan with delays
            slow_scan(args.target, ports_to_scan, args.min_delay, args.max_delay)
        
        else:
            # Perform the scan with potential delays
            scan_ports(args.target, ports_to_scan)
        
    else:
        # CLI Application
        while True:
            clear_screen()
            main()
        
# End of script