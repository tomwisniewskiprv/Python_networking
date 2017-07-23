import socket
import os, platform
import struct
from ctypes import *

"""
    Simple packet sniffer, based on Black Hat Python.
"""

# host to listen on
host = "10.0.0.64"  # your IP goes here


class IP_header(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):

        # map protocol constants to their names
        self.protocol_map = {1: "ICMP", 2: "IGMP", 6: "TCP", 17: "UDP"}

        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


def run():
    op_sys = platform.system()
    if op_sys == "Windows":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    # create a raw socket and bind it to the public interface
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))

    # include IP headers in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # on Windows we need to send some ioctls to setup promiscuous mode
    if op_sys == "Windows":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65565)[0]  # read in a single packet

            # create an IP header from the first 20 bytes of the buffer
            ip_header = IP_header(raw_buffer[0:20])
            print("Protocol: {} {} -> {}".format(ip_header.protocol, ip_header.src_address, ip_header.dst_address))

    except KeyboardInterrupt:
        # on Windows turn off promiscuous mode
        if op_sys == "Windows":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

    finally:
        sniffer.close()


if __name__ == '__main__':
    run()
