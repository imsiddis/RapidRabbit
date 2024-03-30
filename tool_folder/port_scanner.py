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
import struct
import select
import pathlib
import sys
# Append the parent directory of the current script to sys.path
current_dir = pathlib.Path(__file__).parent.absolute()  # Get the current directory of the script
parent_dir = current_dir.parent  # Navigate to the parent directory
sys.path.append(str(parent_dir))  # Append the parent directory to sys.path
from internal_library.asset_functions import beautify_string, beautify_title, clear_screen, sanitize_target_input, sanitize_port_input, splash_logo_no_indent, center_block_text, center_text

#=================#
# Argument Parser #
#=================#


def parse_args():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("--help", action="help", help="Show this help message and exit")
    parser.add_argument("-t", "--target", help="Target IP address to scan")
    parser.add_argument("-p", "--ports", help="Port range to scan, e.g., '20-80' or '80,443'")
    parser.add_argument("-r", "--random", action="store_true", help="Randomize the order of port scanning")
    parser.add_argument("--min-delay", type=float, default=0, help="Minimum delay between port scans in seconds")
    parser.add_argument("--max-delay", type=float, default=0, help="Maximum delay between port scans in seconds")
    parser.add_argument("-sS", "--stealth-scan", action="store_true", help="Perform a stealth scan using SYN packets")
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

#===================================#
# SYN Packet Construction Functions #
#===================================#

def checksum(data):
    """
    Calculates the TCP checksum for given data, ensuring data integrity over the network.

    The checksum is a critical part of the TCP/IP protocols, used to detect data corruption during transmission.
    This function implements the checksum calculation by dividing the data into 16-bit words,
    summing them together, and performing a bit-wise NOT operation on the result.

    Parameters:
    - data (bytes): The header and data for which the checksum is to be calculated.

    Returns:
    - The calculated checksum as an integer.
    """
    # Ensure the data is even-numbered in length by padding with a null byte if necessary.
    if len(data) % 2 != 0:
        data += b'\0'
        
    # Sum the 16-bit words in the data
    s = sum(array := struct.unpack('!'+str(len(data)//2)+'H', data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    
    # Add carry, if any, by shifting the right 16 bits and adding to the sum.
    # Then, perform a bit wise NOT operation to get the checksum.
    s = ~s & 0xffff
    return s

def create_tcp_header(source_port, dest_port, checksum):
    """
    Manually constructs a TCP header with the specified parameters.

    Parameters:
    - source_port (int): The source port number.
    - dest_port (int): The destination port number.
    - checksum (int): The pre-calculated checksum for the header and data.

    The TCP header includes fields like sequence numbers and flags. Here, we're particularly setting the SYN flag to initiate a connection.

    The struct module is used to pack the header fields into a byte string, following the network byte order (!),
    which is Big-Endian. This is crucial for ensuring that the packet is correctly interpreted by network devices.

    Returns:
    - A byte string representing the TCP header.
    """
    # TCP header are packed using the struct module to ensure correct byte order.
    # This includes the source port, destination port, sequence number, acknowledgment number, and data offset,
    # flags (with SYN flag set), window size, checksum, and urgent pointer.
    seq = 0
    ack_seq = 0
    doff = 5
    syn_flag = 2
    window = socket.htons(5840)
    urg_ptr = 0
    offset_res = (doff << 4) + 0
    tcp_flags = syn_flag
    tcp_header = struct.pack('!HHLLBBHHH', source_port, dest_port, seq, ack_seq, offset_res, tcp_flags, window, checksum, urg_ptr)
    return tcp_header

def get_source_ip(target_ip):
    """ Get the source IP address of the machine """
    try:
        # Temporary socket to determine the source IP
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect((target_ip, 80))  # 80 is arbitrary, no data is sent
        source_ip = temp_sock.getsockname()[0]
        temp_sock.close()
        return source_ip
    except Exception as e:
        print(f"Could not determine source IP: {e}")
        return None
#==========================================#
# End of SYN Packet Construction Functions #
#==========================================#

#===================#
# Syn Scan Function #
#===================#

def syn_scan(target_ip, target_port):
    """
    Performs a TCP SYN scan on the specified port of the target IP.

    This function crafts a TCP packet with the SYN flag set and sends it to the target port.
    It listens for a SYN-ACK response, which indicates the port is open, or a RST (reset),
    indicating the port is closed.

    The SYN scan is a type of stealth scanning technique as it does not complete the TCP handshake,
    making the scan less detectable by some firewalls and intrusion detection systems.

    Parameters:
    - target_ip (str): The IP address of the target system.
    - target_port (int): The port number to scan.

    Note: This function requires raw socket permissions, typically requiring administrative privileges.
    """
    # Craft the SYN packet using raw sockets, setting the SYN flag.
    # Listen for responses to determine if the port is open or closed.
    try:
        source_ip = get_source_ip(target_ip)
        if not source_ip:
            print("Source IP could not be determined.")
            return

        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

        s.settimeout(5)
        source_port = 12345

        placeholder_tcp_header = create_tcp_header(source_port, target_port, 0) # Checksum is 0 for now
        pseudo_header = struct.pack('!4s4sBBH', socket.inet_aton(source_ip), socket.inet_aton(target_ip), 0, socket.IPPROTO_TCP, len(placeholder_tcp_header)) # 0 is the placeholder for checksum
        psh = pseudo_header + placeholder_tcp_header
        tcp_checksum = checksum(psh) 
        tcp_header = create_tcp_header(source_port, target_port, tcp_checksum)
        s.sendto(tcp_header, (target_ip, target_port))

        ready = select.select([s], [], [], 5) # Wait for <x> seconds for a response (x=5)
        if ready[0]:
            data, addr = s.recvfrom(1024)
            tcp_header_len = (data[32] >> 4) * 4
            tcp_header = data[20:20+tcp_header_len]
            if len(tcp_header) > 13:
                flags = tcp_header[13]
                if flags & 0x12:  # SYN-ACK
                    print(f"Port {target_port} is open (SYN-ACK received).")
                elif flags & 0x04:  # RST
                    print(f"Port {target_port} is closed (RST received).")
        else:
            print(f"No response received for port {target_port}, it might be filtered or the scan timed out.")
    except KeyboardInterrupt:
        print("\nScan cancelled by user.")
    except UnboundLocalError:
        print("! This feature is currently only supported on Linux systems. !")
    #except PermissionError:
    #    print("Permission denied. Please run the script as a superuser.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        try:
            s.close()
        except UnboundLocalError:
            print("! This feature is currently only supported on Linux systems. !")
            return 
#==========================#   
# End of Syn Scan Function #
#==========================#

             
#===============================#
# End of Stealth Scan Functions #
#===============================#


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
    args = parse_args()
    if args.target and args.ports:
        # Convert ports from string to list of integers
        ports_to_scan = process_ports_arg(args.ports)
        
        # Randomize the port order if the -r flag is set
        if args.random:
            ports_to_scan = random_port_order(ports_to_scan)
            
        # Determine which scan function to use based on the delay arguments
        if args.min_delay > 0 or args.max_delay > 0:
            # Perform the scan with delays
            open_ports = slow_scan(args.target, ports_to_scan, args.min_delay, args.max_delay)
            
        if args.stealth_scan:
            # Perform a stealth scan using SYN packets
            for port in ports_to_scan:
                syn_scan(args.target, port)
        else:
            # Perform the regular scan without delays
            open_ports = scan_ports(args.target, ports_to_scan)
        if args.help:
            print(help_section)   
        # Reporting Findings in nice formatting.
        try:
            num_open_ports = len(open_ports)
            str_num_ports = f"Amount of open ports: {num_open_ports}"
            print(beautify_string(str_num_ports, "-"))

            if num_open_ports != 0:
                print("\nOpen Ports Discovered:")
                print("----------------------")
                for port in open_ports:
                    print(f"Port: {port}")
        except NameError:
            pass
        
        print(beautify_string("End of Scan", "~"))
        
    else:
        # CLI Application
        while True:
            clear_screen()
            main()
        
# End of script