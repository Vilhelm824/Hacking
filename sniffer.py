#! /usr/bin/python

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
	# set store to false so memory isn't overwhelmed, prn calls given function every time this is executed
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) 


def process_sniffed_packet(packet):
	if packet.haslayer(http.HTTPRequest):
		print(packet.show)


sniff("eth0")