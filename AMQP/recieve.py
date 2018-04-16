#!/usr/bin/env python
import pika
import sys 
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()


channel.exchange_declare(exchange='topics',
                         exchange_type='topic')


result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

message_dict = {}
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topics',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    if method.routing_key in message_dict:
    	message_dict[method.routing_key].append(body.decode('utf-8'))
    else:
    	message_dict[method.routing_key] = [body.decode('utf-8')]

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    counts = []
    for key in list(message_dict.keys()):
    	counts.append(len(message_dict[key]))
    plt.figure(figsize=(10,10))
    plt.title('Number of Messages')
    freqdf = pd.DataFrame({'routing_key':list(message_dict.keys()),"counts":counts})
    sns.set_style("whitegrid")
    sns.set(font_scale = 0.7)
    ax = sns.barplot(x="routing_key", y="counts", data=freqdf)
    plt.show()
    print('\n' + "MESSAGES DICT: " + "\n")
    print(message_dict)


connection.close()

