from socket import * #sockets
from threading import Thread
from socket import *
import argparse

parser=argparse.ArgumentParser( #help
    description='''Multithreaded TCP socket Chat Server.\n
    Give a port number and wait for clients to connect, then have a recieve/respond type communication with them.\n
    Can have up to 5 clients to listen for in the queue.\n
    Right now there is trouble cancelling all the threads, be careful!\n
    requires python 3
     ''', 
    )

args=parser.parse_args()


class MTCP_Server(Thread):
	"""
	Multithreaded TCP Chat Client that has the ability to communicate with multiple clients
	Parameters:
		port: integer, port number
		response: String response as a default message sent when initial connection is made
	"""
	#TODO: Fix global message to send
	def __init__(self,port,response):
		self.port = port
		self.response = response
		self.addresses = []
		self.threadlist = set()
		self.clients = set()
		self.s = socket(AF_INET, SOCK_STREAM)
		self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.s.bind(('', self.port))
		print("Listening on port: " + str(port))

	def start(self):
		self.s.listen(5)
		while True:
			try:
				client, addr = self.s.accept()
				client.settimeout(120)
				self.clients.add(client)
				self.addresses.append(addr)
				t = Thread(target = self.listento, args=(client,addr,(len(self.addresses)-1)))
				t.start()
				self.threadlist.add(t)
			except KeyboardInterrupt:
				print("Shutting Down Server!")
				break

	def listento(self, client, addr,usernumber):
		size = 1024
		count = 0
		while True:
			try:
				data = client.recv(size)
				print("ip,port)" + str(addr) + " user# " + str(usernumber) + " sent: " + data.decode('utf-8'))
				if data:
					response = "Respond to (ip,port) " + str(addr) + " user# " + str(usernumber) + " :\n"
					response = input("Send to all users:\n ")
					for c in self.clients:
						print(c)
						c.send(response.encode('utf-8'))
					# client.send(response.encode('utf-8'))
				else:
					raise error('Client disconnected')
			except:
				client.close()
				return False

if __name__ == "__main__":
	print("Welcome!")
	while True:
		port = input("Enter a port number above 1024: ")
		try:
			port = int(port)
			break
		except ValueError:
			pass
	mtcp = MTCP_Server(port,"Hey, you've connected!")
	mtcp.start()
	#closes threads
	for threads in mtcp.threadlist:
		print("Closing Threads!")
		threads.join()

    





