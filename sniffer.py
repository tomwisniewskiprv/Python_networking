# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | sniffer
# 23.07.2017 Tomasz Wisniewski

import socket
import os, sys, platform
import struct
from ctypes import *
import binascii

from IPv4_Header import IPv4_Header
from IPv4_Header import ICMP

"""
    Simple packet sniffer, based on Black Hat Python.
"""

# host to listen on
host = "10.0.0.64"  # your IP goes here


def run():
    op_sys = platform.system()
    if op_sys == "Windows":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    # create a raw socket and bind it to the public interface
    sniffer = None
    try:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))
    except:
        print("Script requires higher privileges to run.")
        sys.exit(1)

    # include IP headers in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # on Windows we need to send some ioctls to setup promiscuous mode
    if op_sys == "Windows":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65565)[0]  # read in a single packet

            # create an IP header from the first 20 bytes of the buffer
            # 20 Bytes == 160 bites == IP header
            # 96b  12B   source address
            # 128b 16B   destination address
            ip_header = IPv4_Header(raw_buffer[0:20])

            print("Protocol: {:4} {:15} -> {:15} TTL: {}".format(ip_header.protocol, ip_header.src_address,
                                                                 ip_header.dst_address, ip_header.ttl))
            if ip_header.protocol == "ICMP":
                start_icmp = ip_header.ihl * 4  # 20b
                raw_icmp = raw_buffer[start_icmp:start_icmp + sizeof(ICMP)]
                icmp_header = ICMP(raw_icmp)
                print("{:10}ICMP: type: {} code: {} result: {}".format(" ",icmp_header.type, icmp_header.code,
                                                               icmp_header.show_results()))

    except KeyboardInterrupt:
        # on Windows turn off promiscuous mode
        if op_sys == "Windows":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

    finally:
        sniffer.close()
        sys.exit()


if __name__ == '__main__':
    run()
