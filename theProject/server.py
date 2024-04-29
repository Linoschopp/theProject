#! /usr/bin/python3
import socket
import threading
import errno

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


def handle_connection(conn, addr):
	unsorted = True
	while unsorted:
		msg = conn.recv(64).decode(ENCODING)
		if msg.startswith("type: "):
			if msg == "type: controller":
				if controller == ():
					unsorted = False
					conn.send("type ok".encode(ENCODING))
					handle_controller(conn, addr)
				else:
					conn.send("type not ok".encode(ENCODING))
			elif msg == "type: client":
				unsorted = False
				conn.send("type ok".encode(ENCODING))
				handle_client(conn, addr)
			else:
				conn.send("type not ok".encode(ENCODING))
				
				
def handle_controller(conn, addr):
	global controller
	global controller_active_client
	global clients
	global running
	controller = (conn, addr)
	connected = True
	while connected:
		try:
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
					cls = clients.copy()
					for client in cls:
						client[0].send("shutdown".encode(ENCODING))
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
						conn.send("comand error".encode(ENCODING))
						continue
					conn.send("command ok".encode(ENCODING))
					command = conn.recv(cmd_length + 16).decode(ENCODING)
					if command.startswith("command content "):
						command = command[16:]
						controller_active_client[0].send(f"command length {str(cmd_length)}".encode(ENCODING))
						response = controller_active_client[0].recv(1024).decode(ENCODING)
						if response == "command ok":
							controller_active_client[0].send("command content " + command.encode(ENCODING))
		except OSError:
			pass
		else:
			if data == "exit":
				connected = False
				conn.close()
				controller = ()
			elif data == "shutdown":
				connected = False
				conn.close()
				controller = ()
				cls = clients.copy()
				for client in cls:
					client[0].send("shutdown".encode(ENCODING))
					client[0].close()
					clients.remove(client)
				running = False
				server.close()
			elif data.startswith("activate "):
				print(data)
				ad = socket.gethostbyname(data[9:])
				for client in clients:
					if client[1][0] == ad:
						controller_active_client = client
						break
				if controller_active_client != ():
					conn.send("activate ok".encode(ENCODING))
				else:
					conn.send("activate error".encode(ENCODING))
					
					
def handle_client(conn, addr):
	global clients
	clients.add((conn, addr))
	while (conn, addr) in clients:
		try:
			data = conn.recv(1024).decode(ENCODING)
			if data == "exit":
				connected = False
				conn.close()
				clients.remove((conn, addr))
			if data.startswith("tell len out "):
				try:
					out_length = int(data[13:])
				except ValueError as e:
					conn.send("tell error".encode(ENCODING))
					continue
				conn.send("tell ok".encode(ENCODING))
				out_data = conn.recv(out_length+9).decode(ENCODING)
				if out_data.startswith("tell out "):
					out_data = out_data[9:]
					err_data = err_data[9:]
					controller[0].send(f"tell len out {len(out_data.getvalue().encode(ENCODING))}".encode(ENCODING))
					response = controller[0].recv(1024).decode(ENCODING)
					if response == "tell ok":
						controller[0].send(("tell out " + out_data.getvalue()).encode(ENCODING))
		except OSError:
			pass			
					
running = True
while running:
	try:
		conn, addr = server.accept()
		c = threading.Thread(target=handle_connection, args=(conn, addr))
		c.start()
	except ConnectionAbortedError:
		pass

try:
	server.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
except OSError as e:
	if e.errno != errno.ENOTCONN:
		server.close()