# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | IPv4_Header
# 23.07.2017 Tomasz Wisniewski

"""
    Module for low level binary data extractions from IPv4 packet headers, including ICMP.
"""

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

        self.control_messages = {
            (0, 0): "Echo reply (used to ping)",
            (1, 0): "Reserved",
            (2, 0): "Reserved",
            (3, 0): "Destination Unreachable: Destination network unreachable",
            (3, 1): "Destination Unreachable: Destination host unreachable",
            (3, 2): "Destination Unreachable: Destination protocol unreachable",
            (3, 3): "Destination Unreachable: Destination port unreachable",
            (3, 4): "Destination Unreachable: Fragmentation required, and DF flag set",
            (3, 5): "Destination Unreachable: Source route failed",
            (3, 6): "Destination Unreachable: Destination network unknown",
            (3, 7): "Destination Unreachable: Destination host unknown",
            (3, 8): "Destination Unreachable: Source host isolated",
            (3, 9): "Destination Unreachable: Network administratively prohibited",
            (3, 10): "Destination Unreachable: Host administratively prohibited",
            (3, 11): "Destination Unreachable: Network unreachable for ToS",
            (3, 12): "Destination Unreachable: Host unreachable for ToS",
            (3, 13): "Destination Unreachable: Communication administratively prohibited",
            (3, 14): "Destination Unreachable: Host Precedence Violation",
            (3, 15): "Destination Unreachable: Precedence cutoff in effect",
            (4, 0): "Source quench (congestion control) deprecated",
            (11, 0): "Time Exceeded, TTL expired in transit",
            (11, 1): "Time Exceeded, Fragment reassembly time exceeded",
        }

    def get_description(self):
        """ Translate ICMP.type and ICMP.code for description. """
        ctrl_msg = self.control_messages.get((self.type, self.code))
        if ctrl_msg:
            return ctrl_msg
        else:
            return "There is no Control Message description for type {}, code {}" \
                   "\nHowever there is a response which means that it's up.".format(
                self.type, self.code)
