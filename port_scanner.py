# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | port_scanner
# 07.07.2017 Tomasz Wisniewski


import socket
import sys
import argparse
from datetime import datetime
from validate_ip import validate_ip

"""
Add : UDP scan , ICMP sweep , IP range 
"""


def scan_TCP(address, port):
    """ Scan host """
    socket.setdefaulttimeout(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address, port))

    if result == 0:  # no error
        return 1
    else:
        return 0


def parse_command_line():
    parser = argparse.ArgumentParser(description="Simple port scanner (remote and local)")
    parser.add_argument("ip", help="IP address")
    parser.add_argument("-v", help="verbose", action="store_true")
    parser.add_argument("-t", help="TCP") #
    parser.add_argument("-u", help="UDP")

    args = parser.parse_args()

    if validate_ip(args.ip):
        return args.ip
    else:
        print("Wrong IP address. Quiting.")
        sys.exit(1)


def main():
    ports = [21, 22, 25, 53, 79, 80, 105, 106, 110, 135, 143, 443, 3306, 8000, 8001, 8002, 8005, 8009, 8080, 14147,
             33389]  # default ports (a)

    ip = parse_command_line()

    t0 = datetime.now()
    print('Scanning.')
    for port in ports:
        if scan_TCP(ip, port):
            print('[{}:{}] is open'.format(ip, port))

    t1 = datetime.now()
    print('Scan of {} finished in {}'.format(ip, t1 - t0))


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("There was an error: {} ".format(ex))
        sys.exit(1)
