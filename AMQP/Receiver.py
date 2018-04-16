#!/usr/bin/env python
import pika
import sys 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Receiver():

	def __init__(self,host,arg):
		self.host = host
		self.binding_keys = arg[1:]
		self.default = arg[0]
		self.message_dict = {}

	def start(self):
		binding_keys = self.binding_keys

		connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
		channel = connection.channel()


		channel.exchange_declare(exchange='topics',
		                         exchange_type='topic')


		result = channel.queue_declare(exclusive=True)
		queue_name = result.method.queue

		#if you dont include any keys
		if not binding_keys:
			binding_keys = ["#"]

		for binding_key in binding_keys:
		    channel.queue_bind(exchange='topics',
		                       queue=queue_name,
		                       routing_key=binding_key)

		print(' [*] Waiting for logs. To exit and view message counts, press CTRL+C')
		channel.basic_consume(self.callback,
	                      queue=queue_name,
	                      no_ack=True)

		try:
		    channel.start_consuming()
		except KeyboardInterrupt:
		    channel.stop_consuming()
		    counts = []
		    if len(list(self.message_dict.keys())) != 0:
			    for key in list(self.message_dict.keys()):
			    	counts.append(len(self.message_dict[key]))
			    plt.figure(figsize=(10,10))
			    plt.title('Number of Messages')
			    freqdf = pd.DataFrame({'routing_key':list(self.message_dict.keys()),"counts":counts})
			    sns.set_style("whitegrid")
			    sns.set(font_scale = 0.7)
			    ax = sns.barplot(x="routing_key", y="counts", data=freqdf)
			    plt.show()
			    print('\n' + "MESSAGES DICT: " + "\n")
			    print(self.message_dict)


		connection.close()

	def callback(self,ch, method, properties, body):
	    print(" [x] Received %r" % body)
	    if method.routing_key in self.message_dict:
	    	self.message_dict[method.routing_key].append(body.decode('utf-8'))
	    else:
	    	self.message_dict[method.routing_key] = [body.decode('utf-8')]


if __name__ == "__main__":
	print("WELCOME")
	recieve = Receiver('127.0.0.1',sys.argv)
	recieve.start()