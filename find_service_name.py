# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | find_service_name
# 12.07.2017 Tomasz Wisniewski

import socket
import argparse


def find_service_name(ports, protocol):
    ports_lst = ports.strip().split(" ")

    try:
        for port in ports_lst:
            print("Port: {} service name: {}".format(port, socket.getservbyport(int(port), protocol.lower())))
    except:
        pass


if __name__ == "__main__":
    port_help = """In case of request to check multiple ports please use list of port numbers, separated with space and
     wrapped in quotation marks, ex:\n
    \"21 25 80\" 
    """

    parser = argparse.ArgumentParser(description="Find service by name")
    parser.add_argument("ports", type=str, help=port_help)
    parser.add_argument("protocol", default="tcp", type=str, help="TCP or UDP")
    args = parser.parse_args()

    find_service_name(args.ports, args.protocol)
