import socket
import sys
import select

read_socket=[]
write_socket=[]
socket_out={}

def get_input(c):
	# Receive the equation from the client
	equation=c.recv(1024).decode()

	# Check if the client has requested to quit
	if equation == "Q" or equation == "q" or equation == "Quit" or equation == "quit" or equation == "quit()":
		socket_out[c]="Quit"
	else:
		# Evaluate the equation 
		print("Client has given this equation:", equation)
		try:
			result = eval(equation)
			socket_out[c]=str(result)
		except (ZeroDivisionError):
			socket_out[c]="ZD"
		except (ArithmeticError):
			socket_out[c]="ME"
		except (SyntaxError):
			socket_out[c]="SE"
		except (NameError):
			socket_out[c]="NE"

	# Add the client socket to the list of sockets to be written to
	write_socket.append(c)

def send_output(c):
	# Send the result of the equation evaluation to the client
	c.send(socket_out[c].encode())

	# Remove the client socket from the list of sockets to be written to
	write_socket.remove(c)
	print("Sending reply:", socket_out[c])

	# If the client has requested to quit, close the socket and remove it from the list of sockets to be read from
	if(socket_out[c]=="Quit"):
		read_socket.remove(c)
		c.close()

	# Remove the client socket from the dictionary that stores the results of equation evaluations
	del socket_out[c]

def rec_conn(s):
	# Accept incoming client connections
	c, addr = s.accept()
	print('Connected to :', addr[0], ':', addr[1])

	# Add the client socket to the list of sockets to be read from
	read_socket.append(c)

def Main():
	# Get the host name and port number from command line arguments
	host = socket.gethostname()                    
	port = int(sys.argv[1])

	# Create a socket object and bind it to the host and port
	s = socket.socket() 	  		 
	s.bind((host, port)) 			 
	s.listen(5) 			         

	# Add the server socket to the list of sockets to be read from
	read_socket.append(s)

	# Print a message indicating that the server has started
	print("Server3 has started yay!")

	# A loop that listens for incoming client connections and evaluates equations sent by clients
	while True:
		# Wait for sockets to become readable or writable
		readable,writable,error=select.select(read_socket,write_socket,[])

		# Process readable sockets
		for x in readable:
			# If the socket is the server socket, accept the incoming connection
			if(x==s):
				rec_conn(s)
			# Otherwise, receive the equation from the client
			else:
				get_input(x)

		# Process writable sockets
		for x in writable:
			# Send the result of the equation evaluation to the client
			send_output(x)

if __name__ == '__main__':
	Main()
