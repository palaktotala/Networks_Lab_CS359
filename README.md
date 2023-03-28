# 2001CS84_CS359_Computer Networks Lab

TUTORIAL-1

In this tutorial, I learnt how to use wireshark to capture packets when I open any website. I tried on various websites like amazon, myntra, etc and used filters to save the specific packets that I wanted. It was fun!

TUTORIAL-2

NOTE - I have printed the IP address received by the function socket.gethostbyname
After you run the code, open a new browser in incognito mode and enter this IP address. Do not open the website using its name because one website can have multiple IP addresses so it is important that your browser uses the IP address received by the function to communicate and not some other one of the website.
Also don't browse anything else at the same time.
It totally depends on your internet connection, luckily I had a strong one so packets mostly got captured in one go.

References for writing the code - https://www.geeksforgeeks.org/packet-sniffing-using-scapy/

I started writing the code in this order:

TCP handshake start - 
1. Declared hostename and interface.
2. Made a sniffer function which gets and prints ip address and then runs the tcp_3_way_handshake_start function.
3. Made a tcp_3_way_handshake_start function which uses the filter "tcp and host " + ip_address and sniffs packets with this filter to send them to a save function. Also put a packet count of 03 so that we only get the 3 S,SA,A packets.
4. Made a save function that saves the packets in a pcap as and when the tcp start function sends it the sniffed packets
5. Ran the sniffer function
6. Committed and Pushed this code to repo