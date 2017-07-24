# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | IPv4_Header
# 23.07.2017 Tomasz Wisniewski

from ctypes import *
import socket
import struct


class IPv4_Header(Structure):
    """ Raw IPv4 header structure """
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

    def __init__(self, socket_buffer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # map protocol constants to their names
        self.protocol_map = {1: "ICMP", 2: "IGMP", 6: "TCP", 17: "UDP"}

        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map.get(self.protocol_num)
        except:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    """ Raw Internet Control Message Protocol structure """
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.types = {0: "Echo Reply", 8: "Echo Request", 3: "Destination Unreachable", 11: "Time Exceeded"}

    def show_results(self):
        return self.types.get(self.type)
