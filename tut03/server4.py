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
		print("Client has given this equation:", equation)
        # Result will be the same equation, since we are supposed to echo whatever is sent by client
		result = equation
		socket_out[c]=str(result)
	write_socket.append(c)

#Below code is same as that of server 3

def send_output(c):
	c.send(socket_out[c].encode())
	write_socket.remove(c)
	print("Sending reply:", socket_out[c])
	if(socket_out[c]=="Quit"):
		read_socket.remove(c)
		c.close()
	del socket_out[c]

def rec_conn(s):
	# establish connection with client
	c, addr = s.accept()
	print('Connected to :', addr[0], ':', addr[1])
	read_socket.append(c)

def Main():

	host = socket.gethostname()      # Get local machine name
	port = int(sys.argv[1])
	s = socket.socket() 	  		 # Create a socket object
	s.bind((host, port)) 			 # Bind to the port
	s.listen(5) 			         # Now wait for client connection.
	read_socket.append(s)
	print("Server4 has started yay!")

	while True:
		readable,writable,error=select.select(read_socket,write_socket,[])

		for x in readable:
			if(x==s):
				rec_conn(s)
			else:
				get_input(x)
		for x in writable:
			send_output(x)

	


if __name__ == '__main__':
	Main()
