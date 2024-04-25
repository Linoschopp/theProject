#! /usr/bin/python3
import socket
import os


IP = "127.0.0.1"
PORT = 8888
ENCODING = "UTF-8"
ADDR = (IP, PORT)

controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def out(data):
    raise NotImplementedError

def recieve_output():
    global running
    while running:
        data = controller.recv(1024).decode(ENCODING)
        if data.startswith("tell length "):
            try:
                length = int(data[12:])
            except ValueError as e:
                controller.send("tell error".encode(ENCODING))
                continue
            controller.send("tell ok".encode(ENCODING))
            message = controller.recv(length + 13).decode(ENCODING)
            if message.startswith("tell content "):
                message = message[13:]
                out(message)

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
