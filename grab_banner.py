# -*- coding: utf-8 -*-
# Python 3.6
# CookBook | grab_banner
# 27.06.2017 Tomasz Wisniewski

"""
    Simple banner grabber
    # TODO:
    port list
"""

import socket
import argparse


def get_banner(ip, port, timeout):
    """ Try to grab """
    try:
        socket.setdefaulttimeout(timeout)  # default timeout (a)
        sock = socket.socket()
        sock.connect((ip, port))
        banner = sock.recv(2048)

        if banner:
            return banner
    except:
        return


def main(default_ip='10.0.0.', default_range=(1, 10), timeout=0.5, verbose=False):
    ports = [21, 22, 25, 80, 110, 443]  # default ports (a)
    ip_range = range(default_range[0], default_range[1])
    result = []

    if timeout == None:
        timeout = 0.5

    print('IP block: {}{} - {}'.format(args.ip, default_range[0], default_range[1]))
    if not verbose:
        print('working...')

    for r in ip_range:
        ip = default_ip + str(r)  # some local ip (a) ip to check
        for port in ports:
            banner = get_banner(ip, port, timeout)

            if verbose:
                print("Trying {} at {}".format(port, ip), end=' ')

            if banner:
                result.append("{} {} {}".format(ip, port, banner.decode('utf8').strip()))
                if not verbose:
                    print("IP: {} PORT: {}".format(ip, port), end=' ')

                print(banner.decode('utf8').strip())
            if verbose:
                print()

    print("Done! Total banners found : {} ".format(len(result)))
    print("Saving results in \'grabbed_banners_txt\'")

    # save results in file
    try:
        with open('grabbed_banners.txt', 'w')as fout:
            for line in result:
                fout.writelines(line + "\n")
    except Exception as e:
        print("Error! {}".format(e))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", help="IP address to check. (First three octets with dot at the end) ex: 192.168.10. ")
    parser.add_argument("-rs", help="first ip, default 1", type=int)
    parser.add_argument("-re", help="last ip, default 50", type=int)
    parser.add_argument("-t", help="timeout value, default 0.5 sec", type=float)
    parser.add_argument("-v", help="verbose", action="store_true")
    args = parser.parse_args()

    if args.ip:
        last_octet = []
        if args.rs:
            last_octet.append(args.rs)
        else:
            last_octet.append(1)

        if args.re and args.rs and args.rs > args.re:
            args.re = args.rs + 1
            last_octet.append(args.re)
        elif args.re:
            last_octet.append(args.re)
        else:
            last_octet.append(args.re)

        ip_range = tuple(last_octet)
        main(args.ip, default_range=ip_range, timeout=args.t, verbose=args.v)
    else:
        print('There is no optional argument, using default values.')
        main()
