# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | port_scanner_with_threading
# 14.07.2017 Tomasz Wisniewski 
"""
    Full connection TCP port scanner and ping-sweeper (system command) with multithreading.
"""

import socket
import threading
import os, sys, platform
import subprocess
import argparse

from validate_ip import validate_ip


class scan_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass


class ping_thread(threading.Thread):
    def __init__(self, ip, hosts):
        threading.Thread.__init__(self)
        self.ip = ip
        self.hosts = hosts
        if len(hosts) == 1:
            self.only_one_host = True
        else:
            self.only_one_host = False
        self.shell_command = check_op_sys()

    def run(self):
        self.ping_sweep(self.hosts)

    def ping(self, ip):
        """
        Executes ping command.
        :return IP if machine responded to ICMP
        """
        command = self.shell_command + ip
        shell = os.popen(command)

        # execute shell with command
        for line in shell:
            if line.count("TTL"):
                return ip

        return None

    def ping_sweep(self, hosts=None):
        """
        Executes ping sweep.
        :param hosts:
        :return: list of machines which responded to ICMP.
        """
        hosts_live = []
        if self.only_one_host:
            if self.ping(self.ip):
                hosts_live.append(self.ip)

        else:
            for host in hosts:
                print("sanity check")
                if self.ping(host):
                    hosts_live.append(host)

        return hosts_live


def list_hosts(ip, end):
    """
    Creates IP lists for different threads.
    :return: list of hosts
    """
    address = ip.split(".")
    hosts = []

    for addr in range(int(address[3]), end):
        hosts.append(".".join([octet for octet in address[:3]]) + "." + str(addr))

    return hosts


def check_op_sys():
    """Check operating system for correct ping command."""
    try:
        system = platform.system()
        if system == "Windows":
            return "ping -n 2 "
        elif system == "Linux":
            return "ping -c 2 "

    except Exception as ex:
        print("Couldn't detect operating system.")
        sys.exit()


def main(arguments=None):
    help_e_arg = "Last number from IP range to scan. Default is limited to first host's IP, so it will scan only one machine."

    parser = argparse.ArgumentParser()
    parser.add_argument("IP", type=str)
    parser.add_argument("-e", type=int, help=help_e_arg)
    args = parser.parse_args()

    last_number = 0  # last number in IP address range
    ip_range = 0
    only_one_host = False
    host = None
    scan_targets = 0

    # check input parameters
    if validate_ip(args.IP):
        if args.e and args.e > -1 and args.e < 255:
            last_number = int(args.IP.split(".")[3])
            if args.e < last_number:
                print("Parameter -e {} is higher than {}. Quiting.".format(args.e, last_number))
                sys.exit()
            else:
                # calculate range of scan
                ip_range = args.e
                host = args.IP
                print("IP: {} range: {} <-> {} ".format(host, last_number, ip_range))
                ip_range += 1
                scan_targets = ip_range - last_number

        elif args.e and (args.e < -1 or args.e > 255):
            print("Parameter -e {} is not in range 0-255. Quiting.".format(args.e))
            sys.exit()

        else:
            only_one_host = True  # only one host
            host = args.IP

    else:
        print("Parameter {} is not valid IP address. Quiting.".format(args.IP))
        sys.exit()

    # execute ping sweep, threads
    threads = []

    if only_one_host:
        print("Scanning host.")
        thread = ping_thread(host, [])
        if thread.ping_sweep():
            print("{} is up.".format(host))
        else:
            print("{} does not respond for ICMP.".format(host))
    else:
        print("Scanning hosts. It will take a while...")
        hosts = list_hosts(host, ip_range)

        # TODO count how many threads are needed and create appropriate IP blocks
        total_threads = scan_targets // 20  # one thread for 20 IPs

        try:
            thread = ping_thread(host, hosts)
            thread.start()
            threads.append(thread)
        except KeyboardInterrupt:
            print("Interrupted.")
        except Exception as ex:
            print(ex)

        print("\tNumber of active threads {}".format(threading.active_count()))
        for t in threads:
            t.join()
        print("\tNumber of active threads {}".format(threading.active_count()))


if __name__ == "__main__":
    main()
