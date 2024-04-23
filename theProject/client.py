import socket
import threading

IP = "127.0.0.1"
PORT = 8888
ENCODING = "UTF-8"
ADDR = (IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()
print("Listening")
has_controller = False
def handle_connection(conn, addr):
    unsorted = True
    while unsorted:
        msg = conn.recv(64).decode(ENCODING)
        if msg.startswith("type: "):
            if msg == "type: controller":
                if has_controller == False:


def handle_controller(conn, addr):
    raise NotImplementedError

def handle_client(conn, addr):
    raise NotImplementedError

running = True
while running:
    conn, addr = server.accept()
    c = threading.Thread(target=handle_connection, args=(conn, addr))
    c.start()
