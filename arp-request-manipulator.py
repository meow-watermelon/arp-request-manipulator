#!/usr/bin/env python3

import argparse
import os
from scapy.all import Ether,ARP,raw,sendp
import sys

def build_arp_request_packet(eth_hw_src, eth_hw_dst, arp_hw_src, arp_hw_dst, arp_ip_src, arp_ip_dst):
    # scapy uses decimal to define fields
    ether_type = 2054 # 0x0806
    arp_hw_type = 1
    arp_proto_type = 2048 # 0x0800
    hw_addr_length = 6
    proto_length = 4
    op = 1 # ARP request

    try:
        arp_request_packet = Ether(dst=eth_hw_dst, src=eth_hw_src, type=ether_type)/ARP(hwtype=arp_hw_type, ptype=arp_proto_type, hwlen=hw_addr_length, plen=proto_length, op=op, hwsrc=arp_hw_src, psrc=arp_ip_src, hwdst=arp_hw_dst, pdst=arp_ip_dst)
    except Exception as e:
        return False
    else:
        return arp_request_packet

def display_packet_info(packet):
    print('##### Raw Packet Bytes #####')
    print(raw(packet))
    print()
    packet.show()

if __name__ == '__main__':
    # set up command arguments
    parser = argparse.ArgumentParser(description='ARP Request Packet Manipulator')
    parser.add_argument('--ethersrc', type=str, required=True, help='Ethernet source hardware address')
    parser.add_argument('--etherdst', type=str, required=False, default='ff:ff:ff:ff:ff:ff', help='Ethernet destination hardware address (default: ff:ff:ff:ff:ff:ff)')
    parser.add_argument('--arphwsrc', type=str, required=True, help='ARP sender hardware address')
    parser.add_argument('--arphwdst', type=str, required=False, default='00:00:00:00:00:00', help='ARP destination hardware address (default: 00:00:00:00:00:00)')
    parser.add_argument('--arpipsrc', type=str, required=True, help='ARP source IP address')
    parser.add_argument('--arpipdst', type=str, required=True, help='ARP destination IP address')
    parser.add_argument('--count', type=int, required=False, default=1, help='Number of APR requests will be sent (default: 1)')
    args = parser.parse_args()

    # scapy needs superuser permission to send packets. check EUID and exit if it's not root user
    euid = os.geteuid()
    if euid != 0:
        print('Please run this utility under root user permission.')
        sys.exit(2)

    # build the ARP request packet
    arp_request = build_arp_request_packet(args.ethersrc, args.etherdst, args.arphwsrc, args.arphwdst, args.arpipsrc, args.arpipdst)

    if not arp_request:
        # failed to build the ARP request packet, exit
        print('Failed to build the ARP request.')
        sys.exit(3)
    else:
        # display packet information
        display_packet_info(arp_request)

        # send ARP request every 1 second
        sendp(arp_request, count=args.count, inter=1)
