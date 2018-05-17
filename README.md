# Networking
Exploring and utilizing Computer Network architecture 
<br/>
## Projects Included:

### UDP-Dicovery-Chat
  - UDP discovery using ARP and a UDP broadcast packet scanner. <br/>
  - UDP Chat program with unicast and broadcast capabilities. Instructions are displayed on the screen as user traverse the program. The program follows this general sequence: <br/>
    1) Runs arp and puts information in a nice Dataframe <br/>
    2) Scans for peers, this may take some time <br/>
    3) Prompts the user to set the port of the socket(or use the default at 23432) <br/>
    4) prompts user to start a chat(either unicast or broadcast), listen for incoming messages, or just exit the program <br/>

### NetworkVisualization
  - Pipeline that uses wireshark's packet capture capabilities to visualize relationships between devices on a network.
  - Histogram of the frequency of packet types, (UDP,TCP,etc.)
  - Network graph with edges describing packets transmitted to other devices
 
### AMQP demonstration using pika: 
  - the Sender object can send messages over specific topic queues using different routing keys specified by the user. 
  - the Receiver object, saves the messages in its specific topic category and plots the frequency of each topic, as well as displaying all the messages when the user exits the program.
  - Usage: 
  - Sender: python Sender.py 
  - Receiver: python Receiver.py [binding_key] 

### MultiThreaded TCP Chat
  - requires python 3 
  - Allows for recieve/response communication 
  - Allows only for peer to peer communication, can't send messages to every client connected to the server simultaneously 

### Distributed Machine Learning
  - This project uses a multithreaded TCP socket server to create an emulated distributed platform, using the power of many machines connected to a central server to complete machine learning tasks. A user can send a text file with numerical and an algorithm like "kmeans". The file will be split into equal parts to be distributed to the clients, who will run the algorithm on their portion of the data, and send it back to the main server, which will then return it to the original user.



