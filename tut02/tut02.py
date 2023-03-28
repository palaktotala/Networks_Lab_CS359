import scapy.all as scapy
import socket

def save_tcp_3_way_handshake_start(packet):
    print(packet)
    #print("I am here 3!") -> error detecting line
    scapy.wrpcap("TCP_3_Way_Handshake_Start_2001CS84.pcap", packet, append=True)

def tcp_3_way_handshake_start(ip_address, interface):
    filter = "tcp and host " + ip_address
    #print("I am here 1!") -> error detecting line
    scapy.sniff(iface=interface, store=False, filter=filter, count=3, prn=save_tcp_3_way_handshake_start)
    #print("I am here 2!") -> error detecting line

def sniffer(interface, hostname):
    ip_address = socket.gethostbyname(hostname)
    print(ip_address)
    tcp_3_way_handshake_start(ip_address, interface)


hostname = "codeforces.com"
interface = "Wi-Fi"
sniffer(interface, hostname)

