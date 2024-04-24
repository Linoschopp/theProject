import socket
import threading

IP = "127.0.0.1"
PORT = 8888
ENCODING = "UTF-8"
ADDR = (IP, PORT)

clients = set()
controller = ()
controller_active_client = ()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()
print("Listening")
has_controller = False
socket.get

def handle_connection(conn, addr):
	unsorted = True
	while unsorted:
		msg = conn.recv(64).decode(ENCODING)
		if msg.startswith("type: "):
			if msg == "type: controller":
				if has_controller == False:
					unsorted = False
					handle_controller(conn, addr)
			elif msg == "type: client":
				unsorted = False
				handle_client(conn, addr)
				
				
def handle_controller(conn, addr):
	global controller
	global controller_active_client
	global clients
	global running
	controller = (conn, addr)
	connected = True
	while connected:
		data = conn.recv(1024).decode(ENCODING)
		if controller_active_client != ():
			if data == "exit":
				controller_active_client = ()
				connected = False
				conn.close()
				controller = ()
			elif data == "shutdown":
				controller_active_client = ()
				connected = False
				conn.close()
				controller = ()
				for client in clients:
					client[0].send("shutdown")
					client[0].close()
					clients.remove(client)
				running = False
				server.close()
			elif data == "active exit":
				controller_active_client = ()
			elif data.startswith("command length "):
				try:
					cmd_length = int(data[15:])
				except ValueError as e:
					conn.send("error".encode(ENCODING))
					continue
				conn.send("OK")
				command = conn.recv(cmd_length).decode(ENCODING)
				controller_active_client[0].send(f"command length {str(cmd_length)}".encode(ENCODING))
				response = controller_active_client[0].recv(1024)
				if response == "OK":
					controller_active_client[0].send(command.encode(ENCODING))
		else:
			if data == "exit":
				connected = False
				conn.close()
				controller = ()
			elif data == "shutdown":
				connected = False
				conn.close()
				controller = ()
				for client in clients:
					client[0].send("shutdown")
					client[0].close()
					clients.remove(client)
				running = False
				server.close()
				
				

		
		
def handle_client(conn, addr):
	global clients
	clients.add((conn, addr))
	
	
running = True
while running:
	conn, addr = server.accept()
	c = threading.Thread(target=handle_connection, args=(conn, addr))
	c.start()
server.close()