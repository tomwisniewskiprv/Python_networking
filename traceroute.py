import socket
import random
import time
import struct

from IPv4_Header import *

"""
    Simple Traceroute script with ICMP support.
    TODO:
    get host name -> IP
"""


class Traceroute(object):
    def __init__(self, dst, hops=15):
        """
        Initializes a new tracer object
        """
        self.dst = dst
        self.ip_dst = socket.gethostbyname(dst)
        self.hops = hops
        self.ttl = 1
        self.port = 33434  # starting port

    def run(self):
        """
        Run the tracer
        """
        print('Tracing to {} [{}], {} hops max'.format(self.dst, self.ip_dst, self.hops))

        while True:
            startTimer = time.time()
            receiver = self.create_receiver()
            sender = self.create_sender()
            sender.sendto(b'', (self.ip_dst, self.port))

            addr = None
            endTimer = None
            try:
                data, addr = receiver.recvfrom(1024)
                endTimer = time.time()

                # print source and destination of IP
                ip_header = IPv4_Header(data[:20])
                print("\t {} -> {}".format(ip_header.src_address, ip_header.dst_address))

                start_icmp = ip_header.ihl * 4  # Calculate start of ICMP
                icmp_header = ICMP(data[start_icmp:start_icmp + sizeof(ICMP)])
                print("\t type:{} code:{} {}".format(icmp_header.type, icmp_header.code, icmp_header.show_results()))

            except socket.error as e:
                # Handling failed connection.
                # print(e)
                pass
            finally:
                receiver.close()
                sender.close()

            if addr:
                timeToDst = round((endTimer - startTimer) * 1000, 2)
                print('{:<4} {} {} ms'.format(self.ttl, addr[0], timeToDst))

                print(type(addr[0]), addr)
                if addr[0] == self.ip_dst:
                    print("Destination reached.")
                    break
            else:
                print('{:<4} *'.format(self.ttl))

            self.ttl += 1
            self.port += 1

            if self.ttl > self.hops:
                break

    def create_receiver(self):
        """
        Creates a receiver socket
        :return: a socket instance
        """
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_RAW, proto=socket.IPPROTO_ICMP)

        # include headers in packets
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        timeout = struct.pack("ll", 10, 0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)

        s.bind(('', self.port))
        return s

    def create_sender(self):
        """
        Creates a sender socket
        :returns: a socket instance
        """
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
        return s


traceroute = Traceroute("www.onet.pl", hops=15)
traceroute.run()
