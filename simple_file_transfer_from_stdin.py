# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | simple_file_transfer_from_stdin
# 20.07.2017 Tomasz Wisniewski


import socket
import os, sys
import platform
import argparse

from validate_ip import validate_ip


def usage():
    help = """
    Simple file transfer script (Python 3.6)
    
    First run receiver(1)
    Second run sender (2)
    
    Use stream to upload/receive file, for example:
        (1) python script.py r > output_file                (receiving machine)
        (2) python script.py s 192.168.9.1 < input_file     (sending machine)
        
    Or type in data using keyboard:
        (1) python script.py r > output_file                             (receiving machine)
        (2) python script.py s 10.12.13.11 (finish with ctrl-D or ctrl-z)(sending machine)
    """
    print(help)


def create_local_listener():
    port = 20000
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("", port))
    return listener, port


def create_sender():
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sender


def receive_data():
    server, port = create_local_listener()
    server.listen(1)
    connection, conn_name = server.accept()

    data = bytearray()
    while True:
        buff = connection.recv(1024)
        if not buff:
            connection.close()
            server.close()
            break
        else:
            data += buff

    sys.stdout.write(data.decode())


def send_data(ip):
    sender = create_sender()
    data = sys.stdin.read()

    if validate_ip(ip) and data:
        sender.connect((ip, 20000))
        sender.sendall(data.encode())
        sender.shutdown(2)
        print("Closing connection. All data sent.")
    else:
        print("Wrong IP or there is no data.")

    sender.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="r - receive , s <ip> - send", type=str, nargs='+')
    args = parser.parse_args()

    if args.mode[0] == "r":
        receive_data()
    elif args.mode[0] == "s" and args.mode[1]:
        send_data(args.mode[1])
    else:
        print("Unknown command. Please use -h for help")
        usage()
        sys.exit()


if __name__ == '__main__':
    main()
