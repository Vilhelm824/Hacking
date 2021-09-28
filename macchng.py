#! /usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify an new MAC address, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing mac address of " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not find MAC address")
        exit()


options = get_arguments()
initial_mac = get_current_mac(options.interface)
change_mac(options.interface, options.new_mac)
final_mac = get_current_mac(options.interface)

if final_mac == options.new_mac:
    print("[+] MAC address changed from " + initial_mac + " to " + final_mac)
    exit()
else:
    print("[-] Hmm, something went wrong, your MAC address wasn't changed")
    exit()