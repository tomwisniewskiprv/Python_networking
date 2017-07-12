# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | remote_machine_ip
# 12.07.2017 Tomasz Wisniewski

import socket
import argparse
import sys


def get_remote_machine_ip(remote_host):
    try:
        print("IP address of {} : {}".format(remote_host, socket.gethostbyname(remote_host)))
    except socket.error:
        print("{}".format(socket.error))
        print("Please check your host name.")


def main(remote_host):
    get_remote_machine_ip(remote_host)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check IP address for remote host.")
    parser.add_argument("host", help="Remote or local host name.")

    args = parser.parse_args()
    main(args.host)

    sys.exit()
