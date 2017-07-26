# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | port_scanner_udp
# 26.07.2017 Tomasz Wisniewski

"""
Simple UDP port scanner.
Notes:
    - initial code
"""

import socket
import sys, os
from IPv4_Header import IPv4_Header, ICMP
import random
from ctypes import *

port = random.randrange(20000) + 10000


def create_sender():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return s
    except:
        print("Error creating sender socket.")


def create_receiver():
    """ Raw sockets require admin privileges """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        # include headers in packets
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        # reuse address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind to localhost at port port
        s.bind(('', port))

        return s
    except:
        print("Error creating receiver socket.")


def run(target):
    sender = create_sender()
    receiver = create_receiver()

    sender.connect((target, port + 1))
    data, addr = receiver.recvfrom(2048)

    if data:
        print("got data")  # debug
        # extract data from packets using low level structures - ctypes
        packet_ip_header = IPv4_Header(data[:20])  # first 20 Bytes
        start_icmp = packet_ip_header.ihl * 4  # calculate start of ICMP , 20b
        packet_icmp_header = ICMP(data[start_icmp:start_icmp + sizeof(ICMP)])

        print("ICMP response from remote host:\ntype: {} code: {} result: {}".format(packet_icmp_header.type,
                                                          packet_icmp_header.code,
                                                          packet_icmp_header.show_results()))
    else:
        print("there is no data")

    sender.close()
    receiver.close()


def main():
    host = "10.0.0.64"
    run(host)


if __name__ == '__main__':
    main()
