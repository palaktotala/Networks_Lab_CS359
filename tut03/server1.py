import socket		 	 # Import socket module
import sys

s = socket.socket() 	  		 # Create a socket object

while True:
	host = socket.gethostname()                    # Get local machine name
	port = int(sys.argv[1])


	s.bind((host, port)) 			 # Bind to the port
	s.listen(5) 			         # Now wait for client connection.

	print("Server has started yay!")
	c, addr = s.accept() 		# Establish connection with client.
	s.close()
	print('Got connection from', addr)

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