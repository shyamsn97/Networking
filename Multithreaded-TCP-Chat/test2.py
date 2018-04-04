from socket import *

TCP_IP = '127.0.0.1'

TCP_PORT = 1337

s = socket(AF_INET, SOCK_STREAM) 
s.connect((TCP_IP, TCP_PORT))

s.send("sup bro".encode('utf-8'))

while True:
	data = s.recv(1024)
	if data:
		print("Sent: " + str(data.decode('utf-8')))
		response = input("Send a response: ")
		s.send(response.encode('utf-8'))
	else:
		print("Server closed!")
		break

