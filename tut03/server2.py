import socket
import sys

# import thread module
from _thread import *
import threading

# thread function
def threaded(c):

     while True:
          try:
               equation=c.recv(1024).decode()
               if equation == "Q" or equation == "q" or equation == "Quit" or equation == "quit" or equation == "quit()":
                    c.send("Quit".encode())
                    break
               else:
                    print("Client has given this equation:", equation)
                    result = eval(equation)
                    c.send(str(result).encode())
                    print("Sending reply:", result)
          except (ZeroDivisionError):
               c.send("ZD".encode())
          except (ArithmeticError):
               c.send("ME".encode())
          except (SyntaxError):
               c.send("SE".encode())
          except (NameError):
               c.send("NE".encode())

     c.close() 			# Close the connection.


def Main():

	host = socket.gethostname()                    # Get local machine name
	port = int(sys.argv[1])
	s = socket.socket() 	  		 # Create a socket object
	s.bind((host, port)) 			 # Bind to the port
	s.listen(5) 			         # Now wait for client connection.

	print("Server has started yay!")

	# a forever loop until client wants to exit
	while True:

		# establish connection with client
		c, addr = s.accept()
		print('Connected to :', addr[0], ':', addr[1])

		# Start a new thread and return its identifier
		start_new_thread(threaded, (c,))
	s.close()


if __name__ == '__main__':
	Main()
