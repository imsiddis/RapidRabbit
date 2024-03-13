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
from internal_library.asset_functions import beautify_string, clear_screen, sanitize_target_input, sanitize_port_input

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
#   Sanitize Input   # 
#====================#

#***************************************#
#> MOVED SANITATION TO ASSET FUNCTIONS <#
#***************************************#

## Port Input Sanitization
#def sanitize_port_input(port_input):
#    # This function will sanitize the input if and correct spelling mistakes done by the user.
#    dirty_input = str(port_input)
#    cleaned_ports = []
#    
#    # Split the input by comma.
#    port_parts = dirty_input.split(",")
#    
#    for part in port_parts:
#        # Remove spaces and handle ranges.
#        cleaned_part = part.replace(" ", "")
#        if "-" in cleaned_part:
#            # Correcting the input format.
#            range_parts = cleaned_part.split("-")
#            cleaned_range = f"{range_parts[0].strip()}-{range_parts[1].strip()}"
#            cleaned_ports.append(cleaned_range)
#        else:
#            # Append individual ports
#            cleaned_ports.append(cleaned_part)
#    return ",".join(cleaned_ports)
    
#def sanitize_target_input(target_input):
#    # This function will sanitize target_input (IP Address) to correct any errors or spelling mistakes done by the user.
#    dirty_input = str(target_input)
#    stripped_ip = []
#    
#    # Split the IP by puncuation marks.
#    ip_octets = dirty_input.split(".")
#    
#    for octet in ip_octets:
#        # Remove spaces
#        cleaned_octets = octet.replace(" ", "")
#        stripped_ip.append(cleaned_octets)
#    
#    # Reassemble IP
#    cleaned_ip = ".".join(stripped_ip)
#    
#    # Check if valid IPv4 Address
#    if len(stripped_ip) != 4:
#        # If IP has more or less than four octets, then raise ValueError. | Should add graceful exit here. <!!)
#        raise ValueError(f"\"{cleaned_ip}\" is not a valid IPv4 address.")
#    else:    
#        return cleaned_ip

#========[END]=======#
#   Sanitize Input   # 
#====================#


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

def main():
    while True:
        target = ""
        port_choice = ""
        print("Testing of port scanner:")
        target_choice = input("Enter Target IP: ")
        if target_choice.lower == "exit":
            break
        else:
            target = sanitize_target_input(target_choice)
            print(f"IP Chosen: {target}")
        try:
            # Get ports as a list
            port_choice = input("Enter port range or select individual ports.\nEnter here: ")
            if port_choice == "exit":
                break
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
            

if __name__ == "__main__":
    while True:
        clear_screen()
        main()
        

# class PortScanner:
#     def __init__(self):
#         self.timeout = 1  # Timeout for socket connection attempts

#     def is_port_open(self, target, port):
#         try:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                 s.settimeout(self.timeout)
#                 result = s.connect_ex((target, port))
#                 if result == 0:
#                     return True
#                 else:
#                     return False
#         except:
#             return False

#     def scan_ports(self, target, ports):
#         open_ports = []
#         for port in ports:
#             if self.is_port_open(target, port):
#                 print(f"Port {port} is [-> OPEN <-]")
#                 open_ports.append(port)
#             else:
#                 print(f"Port {port} is [CLOSED].")
#         return open_ports

# def parse_port_input(port_input):
#     ports = []
#     try:
#         if '-' in port_input:
#             start_port, end_port = map(int, port_input.split('-'))
#             ports = list(range(start_port, end_port + 1))
#         else:
#             ports = [int(port_input)]
#     except ValueError:
#         print("Invalid port input. Please enter a single port or a range (e.g., 80 or 20-80).")
#     return ports

# def get_target():
#     target = input("Enter Target IP or hostname: ")
#     return target

# def main():
#     scanner = PortScanner()
#     try:
#         target = get_target()
#         port_input = input("Enter port range or a single port (e.g., 80 or 20-80): ")
#         ports = parse_port_input(port_input)
#         if ports:
#             print("\n[SCANNING IN PROGRESS]")
#             open_ports = scanner.scan_ports(target, ports)
#             if open_ports:
#                 print("\nOpen Ports Discovered:")
#                 for port in open_ports:
#                     print(f"Port: {port}")
#                 input()
#             else:
#                 print("No open ports found.")
#     except KeyboardInterrupt:
#         print("\nScan cancelled by user.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()