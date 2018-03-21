# Networking
Exploring and utilizing Computer Network architecture 
<br/>
## Projects Included:

### UDP-Dicovery-Chat
Requires python3 <br>
-UDP discovery using ARP and a UDP broadcast packet scanner. <br/>
-UDP Chat program with unicast and broadcast capabilities. Instructions are displayed on the screen as user traverse the program. The program follows this general sequence: <br/>
    1) Runs arp and puts information in a nice Dataframe <br/>
    2) Scans for peers, this may take some time <br/>
    3) Prompts the user to set the port of the socket(or use the default at 23432) <br/>
    4) prompts user to start a chat(either unicast or broadcast), listen for incoming messages, or just exit the program <br/>

### NetworkVisualization
Requires python3 <br>
-Pipeline that uses wireshark's packet capture capabilities to visualize relationships between devices on a network.
-Histogram of the frequency of packet types, (UDP,TCP,etc.)
-Network graph with edges describing packets transmitted to other devices
