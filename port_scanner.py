# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | port_scanner
# 07.07.2017 Tomasz Wisniewski
"""
    Simple port scanner. Script tries to connect with given host using full TCP 3 way hand shake.
    If port on target machine responds, scripts assumes it's open.

    Add : UDP scan , ICMP sweep , IP range, threading
    MEMO: to do that I need to go lower in stack.
"""
import socket
import sys
import argparse
from datetime import datetime
from validate_ip import validate_ip


def scan_TCP_full_connection(address, port):
    """ Scan host """
    socket.setdefaulttimeout(0.5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address, port))

    sock.close()
    if result == 0:  # no error
        return 1
    else:
        return 0


def parse_command_line():
    parser = argparse.ArgumentParser(description="Simple port scanner (remote and local)")
    parser.add_argument("ip", help="IP address")
    parser.add_argument("-p",
                        help="port number or ports list with double quotation and space separated ex:\"25 80 1337\"",
                        type=str)
    parser.add_argument("-v", help="verbose", action="store_true")

    args = parser.parse_args()

    if validate_ip(args.ip):
        if args.p:
            ports_lst = args.p.strip().split(" ")
            return args.ip, args.v, ports_lst
        else:
            return args.ip, args.v, None

    else:
        print("Wrong IP address. Quiting.")
        sys.exit(1)


def main():
    ports_default = [21, 22, 25, 53, 79, 80, 105, 106, 110, 135, 137, 143, 443, 3306, 8000, 8001, 8002, 8005, 8009,
                     8080, 14147,
                     33389]  # default ports

    ip, verbose, ports = parse_command_line()

    if ports is None:
        ports = ports_default
        print("Using default ports list.")

    t0 = datetime.now()
    print('Scanning. Ctrl + c , ^c  to stop.')
    try:
        for port in ports:
            if scan_TCP_full_connection(ip, int(port)):
                print('[{}:{}] is open'.format(ip, port))
            elif verbose:
                print('[{}:{}] is closed'.format(ip, port))

    except KeyboardInterrupt:
        print("Scanning interrupted.")
        sys.exit()

    except socket.error as s_err:
        print("Socket error: {}".format(s_err))
        sys.exit()

    t1 = datetime.now()
    print('Scan of {} finished in {}'.format(ip, t1 - t0))


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("There was an error: {} ".format(ex))
        sys.exit(1)
