from socket import * #sockets
from threading import Thread
from socket import *
import numpy as np
import pandas as pd
import argparse
import pickle
import time

class DistributedML(Thread):

	def __init__(self,port,response):

		self.port = port
		self.response = response
		self.addresses = []
		self.threadlist = set()
		self.clients = {}
		self.s = socket(AF_INET, SOCK_STREAM)
		self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.s.bind(('', self.port))
		self.array = np.array([])
		self.arrsize = 0
		self.mainclient = 0
		self.counter = 0
		self.progress = 0
		print("Listening on ip and port: " + str(self.s.getsockname()))

	def start(self):
		self.s.listen(5)
		while True:
			try:
				client, addr = self.s.accept()
				client.settimeout(120)
				self.clients[str(client)] = client
				self.addresses.append(addr)
				t = Thread(target = self.listento, args=(client,addr,(len(self.addresses)-1)))
				t.start()
				self.threadlist.add(t)
			except KeyboardInterrupt:
				print("Shutting Down Server!")
				break


	def distribute(self, mainclient,array,algo):

		self.arrsize = array.shape[0]
		length  = len(list(self.clients.values())) - 1
		indices = np.arange(array.shape[0])
		if length <= 0:

			sendmsg = "distributed".encode('utf-8')
			sendmsg = [sendmsg,pickle.dumps(array),algo.encode('utf-8')]
			self.mainclient.send(pickle.dumps(sendmsg))

		clientvals = list(self.clients.values())
		for c in range(len(clientvals)):
			time.sleep(2.5)
			if clientvals[c] != self.mainclient:
				distr = np.random.choice(indices,int(array.shape[0]/length),replace=False)
				newarray = pickle.dumps(array[distr])
				sendmsg = "distributed".encode('utf-8')
				sendmsg = [sendmsg,newarray,algo.encode('utf-8')]
				clientvals[c].send(pickle.dumps(sendmsg))
				indices = indices[np.where(np.isin(indices,distr)== False)[0]]
				self.counter += 1

	def piecetogether(self,array):

		self.progress += 1
		if self.array.shape[0] == 0:
			self.array = array
			self.arrsize = array.shape[0]

		else:
			if len(self.array.shape) > 1:
				self.array = np.vstack((self.array,array))
			else:
				self.array = np.concatenate((self.array,array))

		if self.counter == (len(list(self.clients.values()))-1):
			print("Finished Job")
			fin = ["finished".encode('utf-8'),pickle.dumps(self.array)]
			self.mainclient.send(pickle.dumps(fin))
			self.mainclient = 0
			self.arrsize = 0
			self.array = np.array([])
			self.counter = 0
			del self.clients[str(self.mainclient)]	


	def listento(self, client, addr,usernumber):
		size = 4000
		count = 0
		print(str(client) + " ADDED")
		while True:
			try:
				data = client.recv(size)
				data = pickle.loads(data)
				if data[0].decode('utf-8') == "Connected":

					if self.mainclient == 0:
						client.send(pickle.dumps(["initialize".encode('utf-8')]))
				else:

					if data[0].decode('utf-8') == "send_payload":

						if self.mainclient == 0:
							print("Started job of " + data[2].decode('utf-8') + " for client: " + str(client))
							self.mainclient = client
							self.distribute(client,pickle.loads(data[1]),data[2].decode('utf-8'))

						else:
							print("Wait for your turn!")

					elif data[0].decode('utf-8') == "finished_task":
						print("Client: " + str(client) + " Finished Task!")
						self.piecetogether(pickle.loads(data[1]))
						print("Progress: ")
						print(str(100*self.progress/(len(list(self.clients.values())) - 1)) + "%")

			except:
				print("Client: " + str(client) + " disconnected!")
				del self.clients[str(client)]
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
	dml = DistributedML(port,"Hey, you've connected!")
	dml.start()
	#closes threads
	for threads in dml.threadlist:
		print("Closing Threads!")
		threads.join()

    





