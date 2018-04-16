#!/usr/bin/env python
import pika

class Sender():

	def __init__(self,host):
		self.host = host

	def start(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
		channel = connection.channel()


		channel.exchange_declare(exchange='topics',
		                         exchange_type='topic')

		exit = True
		while exit:
			try:
				message = input("SEND A MESSAGE: " + '\n')
				routing_key = input("enter a routing key: " + '\n')
				if len(routing_key) < 3:
					routing_key = "default"

				channel.basic_publish(exchange='topics',
			                      routing_key=routing_key,
			                      body=message)
				print(" [x] Sent %r:%r" % (routing_key, message))
			except KeyboardInterrupt:
				print("EXITED")
				break
		connection.close()

if __name__ == "__main__":
	sender = Sender('127.0.0.1')
	sender.start()