#!/usr/bin/env python

import subprocess
import re
from optparse import OptionParser

def get_arguments():
    parser = OptionParser()
    parser.add_option('-i', '--interface', dest="interface", help="interface name")
    parser.add_option('-a', '--mac', dest="mac_address", help="new MAC address")
    (options, args) = parser.parse_args()

    if not options.interface:
        parser.error("Please provide network interface name")
    elif not options.mac_address: 
        parser.error("Please provide a new MAC address")
    else:
        return (options, args)
    
def change_mac_address(interface_name, new_mac):
    print("[+] Changing MAC address for " + options.interface + " to " + options.mac_address)
    subprocess.call(["ifconfig", options.interface, "down"])
    subprocess.call(["ifconfig", options.interface, "hw", "ether", options.mac_address])
    subprocess.call(["ifconfig", options.interface, "up"])

def get_mac_address(interface_name):
    ifconfig_output = subprocess.check_output(["ifconfig", interface_name])
    mac_address_search_results = re.search(r"(\w\w:){5}\w\w", str(ifconfig_output))

    if mac_address_search_results:
        return mac_address_search_results.group(0)
    else:
        print("Could not read MAC address")
    
(options, args) = get_arguments()

current_mac_address = get_mac_address(options.interface)
print("Current MAC => " + str(current_mac_address))

change_mac_address(options.interface, options.mac_address)

current_mac_address = get_mac_address(options.interface)

if current_mac_address == options.mac_address:
    print("MAC address was successfully changed to " + current_mac_address)
else:
    print("MAC address was NOT changed")