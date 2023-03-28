#I have explained the code and my thought process in readme

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

def save_tcp_handshake_close(packet):
    print(packet)
    #print("I am here 3!") -> error detecting line
    scapy.wrpcap("TCP_Handshake_Close_2001CS84.pcap", packet, append=True)

def tcp_handshake_close(ip_address, interface):
    filter = "tcp and host " + ip_address + " and tcp[tcpflags] & tcp-fin != 0"
    scapy.sniff(iface=interface, store=False, filter=filter, count=2, prn=save_tcp_handshake_close)

var=0

def save_arp(packet):
    global var
    if(var==0 and packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==1):
        print(packet)
        scapy.wrpcap("ARP_2001CS84.pcap", packet, append=True)
        var=1
    if(var==1 and packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==2):
        print(packet)
        scapy.wrpcap("ARP_2001CS84.pcap", packet, append=True)
        var=2

def arp(interface):
    filter = "arp"
    scapy.sniff(iface=interface, store=False, filter=filter, count=10, prn=save_arp)

def save_arp_request_response(packet):
    print(packet)
    scapy.wrpcap("ARP_Request_Response_2001CS84.pcap", packet, append=True)

def arp_request_response(interface):
    filter = "arp"
    scapy.sniff(iface=interface, store=False, filter=filter, count=2, prn=save_arp_request_response)

def save_dns_request_response(packet):
    global var
    if(var<2 and packet.haslayer(scapy.DNSQR) and packet[scapy.DNSQR].qtype==1 and ("codeforces" in str(packet[scapy.DNSQR].qname))):
        print(packet)
        scapy.wrpcap("DNS_Request_Response_2001CS84.pcap", packet, append=True)
        var=var+1

def dns_request_response(interface):
    filter = "port 53"
    scapy.sniff(iface=interface, store=False, filter=filter, count=200, prn=save_dns_request_response)

def save_ping_request_response(packet):
    print(packet)
    scapy.wrpcap("PING_Request_Response_2001CS84.pcap", packet, append=True)

def ping_request_response(ip_address, interface):
    filter = "icmp and host " + "8.8.8.8"
    scapy.sniff(iface=interface, store=False, filter=filter, count=2, prn=save_ping_request_response)

def sniffer(interface, hostname):
    ip_address = socket.gethostbyname(hostname)
    print(ip_address)
    #tcp_3_way_handshake_start(ip_address, interface)
    #tcp_handshake_close(ip_address, interface)
    #arp(interface)
    #arp_request_response(interface)
    var=0 #restore the value of var after it becomes 1
    #dns_request_response(interface)
    ping_request_response(ip_address, interface)

hostname = "codeforces.com"
interface = "Wi-Fi"
sniffer(interface, hostname)

