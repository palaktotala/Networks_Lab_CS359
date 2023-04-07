import socket		 	 
import sys
import ipaddress

s = socket.socket() # Create a socket object

try:
    #host = socket.gethostname()
    host = str(ipaddress.ip_address(sys.argv[1]))    # Reading IP Address
    port = int(sys.argv[2])                           # Reading port number
    try:
        s.connect((host, port))                           # Connecting to server
    except:
        print("Error: Another client is already connected to server1")
        quit()

    print("Connected to server")

    
    while(True):
        equ=input("Please enter an arithmetic equation to the server or type out Q to quit: ")
        s.send(equ.encode())
        result = s.recv(1024).decode()

        if result == "Quit":
            print("Closing client connection!")
            break
        elif result == "ZD":
            print("Zero division")
        elif result == "ME":
            print("Math error")
        elif result == "SE":
            print("Syntax error")
        elif result == "NE":
            print("Name error")
        else:
            print("The answer is:", result)
            

    s.close 				 # Close the socket when done
#except (IndexError, ValueError):
except (IndexError, ValueError):
    print("You did not specify an IP address and port number")