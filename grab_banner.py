# -*- coding: utf-8 -*-
# Python 3.6
# CookBook | grab_banner
# 27.06.2017 Tomasz Wisniewski

"""
    Simple banner grabber
"""

import socket
import argparse
import sys
from validate_ip import validate_ip


def get_service_banner(ip, port, timeout):
    """ Try to get service banner """
    try:
        socket.setdefaulttimeout(timeout)  # default timeout (a)
        sock = socket.socket()
        sock.connect((ip, port))
        banner = sock.recv(2048)

        if banner:
            return banner

        sock.close()
    except:
        return


def main(ip, timeout=0.5):
    ports = [21, 22, 25, 53, 79, 80, 105, 106, 110, 135, 143, 443, 3306, 8000, 8001, 8002, 8005, 8009, 8080, 14147,
             33389]  # default ports (a)
    result = []

    if timeout == None:
        timeout = 0.5

    print('Working...')
    for port in ports:
        banner = get_service_banner(ip, port, timeout)

        if banner:
            try:
                result.append("[{}:{}] {}".format(ip, port, banner.decode().strip()))
            except Exception as ex:
                result.append("[{}:{}] {}".format(ip, port, banner.strip()))

    for banner in result:
        print(banner)

    print("Done! Total banners found : {} ".format(len(result)))
    print("Saving results in \'grabbed_banners.txt\'")

    # save results in file
    try:
        with open('grabbed_banners.txt', 'w')as fout:
            for line in result:
                fout.writelines(line + "\n")
    except Exception as e:
        print("Error! {}".format(e))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address to check")
    parser.add_argument("-t", help="timeout value, default 0.5 sec", type=float)
    args = parser.parse_args()

    if args.ip:
        if validate_ip(args.ip):
            print('IP address is correct.')
            main(ip=args.ip, timeout=args.t)
        else:
            print('IP address is incorrect.')
            sys.exit(1)
