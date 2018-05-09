from socket import *
import numpy as np
import pickle
import sklearn
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA

class Client():

	def __init__(self,ip,port):

		self.ip = ip
		self.port = port
		self.socket = socket(AF_INET,SOCK_STREAM)
		self.array = np.random.uniform(size=(40,5))
		self.algo_choices = ["kmeans","agglomerative","pca"]

	def check_send(self):

		filename = input("Enter a textfile of data or press any button to continue without it: ")
		try:
			self.array = np.loadtxt(filename, delimiter=',')
			print("file read")
			print("First 10 rows: ")
			print(self.array[:10])
		except Exception as e:
			print("File omitted!")
			self.array = np.random.uniform(size=(40,4))
		print("Algorithm options: kmeans, agglomerative, pca\n")
		response = input("send an algorithm or press any key to continue: ")
		matrix = pickle.dumps(self.array)
		if np.isin(response,self.algo_choices) == False:
			print("Waiting for jobs...")
			pass
		else:
			responsearr = ["send_payload".encode('utf-8'),matrix,response.encode('utf-8')]
			self.socket.send(pickle.dumps(responsearr))



	def run_algo(self,data):

		prediction = []
		matrix = pickle.loads(data[1])
		algo = data[2].decode('utf-8')

		if algo == "kmeans":
			k = KMeans(n_clusters=3)	
			k.fit(matrix)
			prediction = k.predict(matrix)

		elif algo == "agglomerative":
			clustering = AgglomerativeClustering(linkage="average", n_clusters=3)
			clustering.fit(matrix)
			prediction = clustering.labels_

		elif algo == "pca":
			pca = PCA(n_components=2)
			pca.fit(matrix)
			prediction = pca.transform(matrix)

		responsearr = ["finished_task".encode('utf-8'),pickle.dumps(prediction)]
		print("Finished Portion")
		self.socket.send(pickle.dumps(responsearr))

	def connect(self):

		self.socket.connect((self.ip,self.port))
		response = "Connected"
		self.socket.send(pickle.dumps([response.encode('utf-8')]))

		while True:
			data = self.socket.recv(2048)
			if data:
				data = pickle.loads(data)
				if data[0].decode('utf-8') == "initialize":
					
					self.check_send()

				elif data[0].decode('utf-8') == "finished":

					print("FINISHED")
					return pickle.loads(data[1])

				elif data[0].decode('utf-8') == "distributed":
					self.run_algo(data)
					# break
			else:
				print("Server closed!")
				break
				



ip = input("Enter an IP: ")
port = int(input("Enter a port: "))
# ip = "127.0.0.1"
# port = 1337
c = Client(ip,port)
kmeans_array = c.connect()
print(kmeans_array)

