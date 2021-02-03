#!/usr/bin/env python

import scapy.all as scapy
from argparse import ArgumentParser

def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="IP target to search")
    args = parser.parse_args()

    if not args.target:
        parser.error("Please provide target IP")
    else:
        return args

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose = False)[0]
    
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac_address": element[1].hwsrc}
        clients_list.append(client_dict)
    
    return clients_list

def print_results(result_list):
    print("IP\t\t\tMAC Address\n--------------------------------------------")
    for element in result_list:
        print(element["ip"] + "\t\t" + element["mac_address"])

args = get_arguments()
results = scan(args.target)
print_results(results)