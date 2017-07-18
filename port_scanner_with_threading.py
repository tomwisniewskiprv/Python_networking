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
import argparse
from datetime import datetime
from collections import OrderedDict

from validate_ip import validate_ip

screenLock = threading.Semaphore(value=1)  # lock screen , only 1 thread can print output to screen at any given time
hosts_up = OrderedDict()  # results of scan/ping


class scan_thread(threading.Thread):
    def __init__(self, hosts, ports):
        threading.Thread.__init__(self)
        self.hosts = hosts
        self.ports = ports

    def run(self):
        self.scan_sweep()

    def scan_TCP_full_connection(self, address, port):
        """ Scan host """
        try:
            socket.setdefaulttimeout(0.5)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((address, port))

            sock.close()
            if result == 0:  # no error
                return 1
            else:
                return 0
        except socket.error as err:
            print(err)
        except KeyboardInterrupt:
            print("Interrupted.")
            sys.exit()

    def scan_sweep(self):
        for host in self.hosts:
            for port in self.ports:
                if self.scan_TCP_full_connection(host, port):
                    print(host, port)



class ping_thread(threading.Thread):
    def __init__(self, hosts):
        threading.Thread.__init__(self)
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
        self.hosts_up = []
        if self.only_one_host:
            if self.ping(self.hosts[0]):
                self.hosts_up.append(self.hosts[0])
                hosts_up[self.hosts[0]] = "up"

        else:
            for host in hosts:
                if self.ping(host):
                    self.hosts_up.append(host)
                    # screenLock.acquire()
                    # print(host)
                    hosts_up[host] = "up"
                    # screenLock.release()

        return self.hosts_up


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


def scan(host, ip_range, ports):
    """ execute port scan """
    port_lst = [20, 21, 25, 80, 443, 137]
    threads = []

    print("Scanning hosts. It will take a while...")  # sanity check
    hosts = list_hosts(host, ip_range)  # create list of hosts to scan
    nr_of_machines_per_thread = 10

    t0 = datetime.now()
    try:
        for x in range(0, len(hosts), nr_of_machines_per_thread):
            thread = scan_thread(hosts[x:x + nr_of_machines_per_thread], port_lst)
            thread.start()
            threads.append(thread)
    except KeyboardInterrupt:
        print("Interrupted.")
    except Exception as ex:
        print(ex)

    print("Number of active threads: {}".format(threading.active_count()))
    for t in threads:
        t.join()

    for h in sorted(hosts_up.keys()):
        print("{} is up.".format(h))

    t1 = datetime.now()
    print("Time: {}".format(t1 - t0))
    # end of ping sweep

def ping(host, ip_range, *args):
    """ execute ping sweep, create threads """
    threads = []

    print("Pinging hosts. It will take a while...")  # sanity check
    hosts = list_hosts(host, ip_range)  # create list of hosts to scan
    nr_of_machines_per_thread = 10

    t0 = datetime.now()
    try:
        for x in range(0, len(hosts), nr_of_machines_per_thread):
            thread = ping_thread(hosts[x:x + nr_of_machines_per_thread])
            thread.start()
            threads.append(thread)
    except KeyboardInterrupt:
        print("Interrupted.")
    except Exception as ex:
        print(ex)

    print("Number of active threads: {}".format(threading.active_count()))
    for t in threads:
        t.join()

    for h in sorted(hosts_up.keys()):
        print("{} is up.".format(h))

    t1 = datetime.now()
    print("Time: {}".format(t1 - t0))
    # end of ping sweep


def traceroute(host, *args):
    print("trace route")
    pass


def main(arguments=None):
    help_e_arg = "Last number from IP range to scan. Default is limited to first host's IP, so it will scan only one machine."

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=str, help="p|s - ping | scan")
    parser.add_argument("IP", type=str, help="ip address")
    parser.add_argument("-e", type=int, help=help_e_arg)
    parser.add_argument("-p",
                        help="port number or ports list with double quotation and space separated ex:\"25 80 1337\"",
                        type=str)
    args = parser.parse_args()

    last_number = 0  # last number in IP address range
    ip_range = 0  # last machine number in range
    ports = []
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
                print("IP: {}-{} ".format(host, ip_range))
                ip_range += 1
                scan_targets = ip_range - last_number

        elif args.e and (args.e < -1 or args.e > 255):
            print("Parameter -e {} is not in range 0-255. Quiting.".format(args.e))
            sys.exit()

        elif args.m == "s" and args.p:
            ports = args.p.strip().split(" ")

        else:
            host = args.IP
            ip_range = int(host.split(".")[3]) + 1

    else:
        print("Parameter {} is not valid IP address. Quiting.".format(args.IP))
        sys.exit()

    # execute function based on user input
    mode = {'s': scan, 'p': ping, 't': traceroute}
    mode[args.m](host, ip_range, ports)


if __name__ == "__main__":
    main()
