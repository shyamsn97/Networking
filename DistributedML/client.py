from socket import *
import numpy as np
import pickle
import sklearn
from sklearn.cluster import KMeans

class Client():

	def __init__(self,ip,port):

		self.ip = ip
		self.port = port
		self.socket = socket(AF_INET,SOCK_STREAM)
		self.array = np.random.uniform(size=(40,5))

	def connect(self):

		self.socket.connect((self.ip,self.port))
		response = "Connected"
		self.socket.send(pickle.dumps([response.encode('utf-8')]))

		while True:
			data = self.socket.recv(2048)
			if data:
				data = pickle.loads(data)
				if data[0].decode('utf-8') == "initialize":
					response = input("send an array and algorithm or wait to be served by entering wait: ")
					if response == "wait":
						pass
					if response == "kmeans":
						matrix = pickle.dumps(self.array)
						responsearr = ["send_payload".encode('utf-8'),matrix,response.encode('utf-8')]
						self.socket.send(pickle.dumps(responsearr))
				elif data[0].decode('utf-8') == "finished":

					print("FINISHED")
					return pickle.loads(data[1])

				elif data[0].decode('utf-8') == "distributed":

					matrix = pickle.loads(data[1])
					k = KMeans(n_clusters=3)
					k.fit(matrix)
					prediction = k.predict(matrix)
					responsearr = ["finished_task".encode('utf-8'),pickle.dumps(prediction)]
					self.socket.send(pickle.dumps(responsearr))
			else:
				print("Server closed!")
				break
				



ip = input("Enter an IP: ")
port = int(input("Enter a port: "))
c = Client(ip,port)
kmeans_array = c.connect()
print(kmeans_array)

