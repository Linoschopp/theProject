#! /usr/bin/python3
import socket
import os
import math
from io import StringIO


IP = "127.0.0.1"
PORT = 8888
ENCODING = "UTF-8"
ADDR = (IP, PORT)

controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def display(text=None):
	if active:
		def print_line():
			print("\x1b[7m" + os.get_terminal_size().columns*" " + "\x1b[27m")
		print("\x1b[0;0H", end="")
		print("\x1b[1004l", end="")
		print("\x1b[2J", end="")
		print("\x1b[7m", end="")
		half = (os.get_terminal_size().columns-20)/2
		print(math.ceil(half)*" "+"Connected Controller"+math.floor(half)*" ")
		print("\x1b[27m", end="")
		height1 = math.floor((os.get_terminal_size().lines - 2)/ 5 * 4)
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
		if text:
			lines = text.split("\n")
			o_lines = out_lines[-height1:]
			for line in o_lines:
				print(line)
	else:
		def print_line():
			print("\x1b[7m" + os.get_terminal_size().columns*" " + "\x1b[27m")
		print("\x1b[0;0H", end="")
		print("\x1b[1004l", end="")
		print("\x1b[2J", end="")
		print("\x1b[7m", end="")
		half = (os.get_terminal_size().columns-24)/2
		print(math.ceil(half)*" "+"Not Connected Controller"+math.floor(half)*" ")
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

controller.send("type: controller".encode(ENCODING))
if controller.recv(64).decode(ENCODING) == "type ok":

	print("Connected")
	
	out_data = ""
	running = True
	active = False
	while running:
		try:
			if active:
				height = display()
				text = StringIO()
				send = False
				while True:
					inp = input()
					if len(text.getvalue().split("\n")) >= 1:
						if text.getvalue().split("\n")[-1].strip() == "" and inp == "":
							break
					text.write(inp+"\n")
					display(text)
				if text.getvalue() == ":active exit:":
					controller.send("active exit".encode(ENCODING))
					active = False
				elif not ":cancel:" in text.getvalue():
					controller.send(f"command length {len(text.getvalue().encode(ENCODING))}".encode(ENCODING))
					if controller.recv(1024).decode(ENCODING) == "command ok":
						controller.send(f"command content {text.getvalue()}".encode(ENCODING))
			else:
				display()
				inp = input("")			
				controller.send(f"activate {inp}".encode(ENCODING))	
				if controller.recv(1024).decode(ENCODING) == "activate ok":
					active = True
					
				
					
		except EOFError:
			controller.send("shutdown".encode(ENCODING))
			running = False
		except KeyboardInterrupt:
			controller.send("exit".encode(ENCODING))
			running = False
