# import needed libraries
import sys
import socket
import pyfiglet

# to test you can run an Echo Script that ill include to send communication through a port as long as the firewall rules allow it
# Create ASCII banner using "pyfiglet" library (This gives the script a bit of style)
ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Define the target IP address to be scanned
ip = '192.X.X.X'

# Create an empty dictionary to store open port numbers and banners
open_ports = {}
closed_ports = []
# Generate a list of port numbers to scan (from 1 to 65,534)
ports = range(430, 450)
banner_grab_ports = [80, 443, 21, 22, 25, 53, 110] # List of common ports with obtainable banners


# This function is to probe a specific port on the target IP address
def probe_port(ip, port, result=1):
    try:
        # create a socket object and set a timeout for connecting
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((ip, port))

        # If the connection was successful (port is open), set the result to 0
        if r == 0:
            if port in banner_grab_ports: # If the port is typically able to have a banner retrieval run the following code
                banner = sock.recv(1024)  # # Receive up to 1024 bytes of data from the service (This gets us the header/banner so we can understand the service used on this port)
                open_ports[port] = banner.decode('utf-8').strip() # store banner in the dictionary
                print(f"Port {port} is open - Service: {banner.decode('utf-8').strip()}") # Decodes the 1024 bytes of data into a service banner
            else: # if it's not normally obtainable then just check if the port is open, otherwise it wont print any status
                open_ports[port] = "Unable to retrieve banner"
                print(f"Port {port} is open - Service: Unable to retrieve banner")

        else:
            closed_ports.append(port)
            # banner = sock.recv(1024) # # Receive up to 1024 bytes of data from the service
            print(f"Port {port} is closed - Service:")
        #
        # close the socket
        sock.close()
    except Exception as e:
        pass

    # Return the result (0 if open, 1 if closed or error occurred)
    return result


# Iterate through the list of ports and probe each one on the target IP
for port in ports:
    sys.stdout.flush()
    probe_port(ip, port)

# Check if open ports were found and print the results
if open_ports:
    for port, banner in open_ports.items():
        if banner is not None:
            print(f"Port {port} is open - Service: {banner}")
        else:
            print(print(f"Port {port} is open"))
    # print("\nOpen Ports are: ")
    # print(sorted(open_ports))
else:
    print("\nLooks like no ports are open :(")
# if closed_ports:
#     print("\nClosed Ports are: ")
#     print(sorted(closed_ports))
# else:
#     print("\nNo ports are reported as closed.")
