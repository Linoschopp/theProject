#! /usr/bin/python3
import socket
import os
import math


IP = "127.0.0.1"
PORT = 8888
ENCODING = "UTF-8"
ADDR = (IP, PORT)

controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def display():
    if active:
        def print_line():
            print("\x1b[7m" + os.get_terminal_size().columns*" " + "\x1b[27m")
        print("\x1b[0;0H", end="")
        print("\x1b[1004l", end="")
        print("\x1b[2J", end="")
        print("\x1b[7m", end="")
        half = (os.get_terminal_size().columns-18)/2
        print(math.ceil(half)*" "+"Active  Controller"+math.floor(half)*" ")
        print("\x1b[27m", end="")
        height1 = math.floor((os.get_terminal_size().lines - 2)/ 8 * 7)
        height2 = os.get_terminal_size().lines - 2 - height1
        out_lines = out_data.split("\n")
        out_out_lines = out_lines[-height1:]
        extra_lines1 = 0
        while len(out_out_lines)+extra_lines1 < height1:
            extra_lines1 += 1
        for line in out_out_lines:
            print(line)
        for x in range(extra_lines1):
            print()
        print_line()
    else:
        def print_line():
            print("\x1b[7m" + os.get_terminal_size().columns*" " + "\x1b[27m")
        print("\x1b[0;0H", end="")
        print("\x1b[1004l", end="")
        print("\x1b[2J", end="")
        print("\x1b[7m", end="")
        half = (os.get_terminal_size().columns-20)/2
        print(math.ceil(half)*" "+"Inactive  Controller"+math.floor(half)*" ")
        print("\x1b[27m", end="")

def recieve_output():
    global out_data
    while running:
        data = controller.recv(1024).decode(ENCODING)
        if data.startswith("tell len out "):
            try:
                out_length = int(data[13:])
            except ValueError as e:
                controller.send("tell error".encode(ENCODING))
                continue
            controller.send("tell ok".encode(ENCODING))
            out_data = controller.recv(out_length + 9).decode(ENCODING)


while True:
    try:
        print("Trying to connect...")
        controller.connect(ADDR)
        break
    except ConnectionRefusedError as e:
        pass

print("Connected")

out_data = ""
running = True
active = False
while running:
    if not active:
        try:
            display()
            inp = input(">>> ")
            if inp == "exit":
                controller.send("exit".encode(ENCODING))
            elif inp == "shutdown":
                controller.send("shutdown".encode(ENCODING))
            elif inp.startswith("activate "):
                controller.send(inp.encode(ENCODING))
            
        except EOFError:
            controller.send("exit".encode(ENCODING))
        except KeyboardInterrupt:
            controller.send("exit".encode(ENCODING))
        


