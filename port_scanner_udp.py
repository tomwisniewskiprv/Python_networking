# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | port_scanner_udp
# 26.07.2017 Tomasz Wisniewski

"""
    Simple UDP port scanner.
    Notes:
        - add timeout
        - complete type:code pairs in IPv4 header
"""

import socket
import argparse
from IPv4_Header import IPv4_Header, ICMP
import binascii
import random
from ctypes import *

port = random.randrange(20000) + 20000


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
        # allow to reuse address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind to localhost at port
        s.bind(('', port))

        return s
    except:
        print("Error creating receiver socket.")


def run(target):
    sender = create_sender()
    receiver = create_receiver()

    sender.sendto(b'', (target, port + 1))
    sender.close()
    print("Request sent. Waiting for response.")

    raw_data = receiver.recvfrom(512)[0]  # that's more than enough data
    receiver.close()

    if raw_data:
        # extract raw_data from packets using low level structures - ctypes
        packet_ip_header = IPv4_Header(raw_data[:20])  # first 20 Bytes
        start_icmp = packet_ip_header.ihl * 4  # calculate start of ICMP
        packet_icmp_header = ICMP(raw_data[start_icmp:start_icmp + sizeof(ICMP)])

        print("Remote host ({}) responded:".format(target))
        icmp_data = "{}".format(binascii.hexlify(raw_data).decode("utf-8"))

        print("Raw data: {}\nType: {}\nCode: {}\nDescription: {}".format(icmp_data, packet_icmp_header.type,
                                                                         packet_icmp_header.code,
                                                                         packet_icmp_header.get_description()))
    else:
        print("There was no answer. Probably host is down or is set up to not give a response.")


def main(host):
    run(host)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="IP address of remote host to scan.", type=str)
    args = parser.parse_args()
    main(args.host)
