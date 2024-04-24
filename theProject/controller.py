#! /usr/bin/python3
import socket


IP = "127.0.0.1"
PORT = 8888
ENCODING = "UTF-8"
ADDR = (IP, PORT)

controller= socket.socket(socket.AF_INET, socket.SOCK_STREAM)



while True:
    try:
        print("Trying to connect...")
        controller.connect(ADDR)
        break
    except ConnectionRefusedError as e:
        pass

print("Connected")

running = True
active = False
while running:
     print("")
