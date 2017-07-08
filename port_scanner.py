# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | port_scanner
# 07.07.2017 Tomasz Wisniewski


import socket
import os
import platform
import re
from datetime import datetime
from validate_ip import validate_ip


def scan_TCP(address, port):
    socket.setdefaulttimeout(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address, port))

    if result == 0: # no error
        return 1
    else:
        return 0


def main():
    ip = '10.0.0.64'
    ports_list = [80, 8000, 135, 443, 21, 22]
    t0 = datetime.now()
    print('Scanning.')
    for port in ports_list:
        if scan_TCP(ip, port):
            print('[{}:{}] is open'.format(ip, port))

    t1 = datetime.now()
    print('Scanning finished in {}'.format(t1 - t0))


if __name__ == "__main__":
    main()
