# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | remote_shell
# 22.07.2017 Tomasz Wisniewski

import socket
import subprocess, os, sys
import argparse


def create_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("", 6666))
        return server
    except Exception as ex:
        print("Error creating socket.")


def create_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client
    except Exception as ex:
        print("Error creating socket.")


def server_loop():
    server = create_server()
    server.listen(1)
    connection, address = server.accept()

    welcome_msg = "Hello".encode("ascii")
    connection.sendall(welcome_msg)

    data = bytearray()
    while True:
        received = connection.recv(1024)
        if not received:
            break
        else:
            data += received

        # execute command
        data = data.decode()
        output = subprocess.run(data, shell=True, stdout=subprocess.PIPE)
        print(output.stdout.decode('ISO 8859-13'))
        connection.sendall(output.stdout)
        # data = bytearray() # dont remove yet !

    server.close()
    connection.close()


def client_connection():
    client = create_client()
    client.connect(("localhost", 6666))

    try:
        data = client.recv(1024)
        print(data.decode())

        while True:
            cmd = "dir".encode("ascii") # example command
            client.sendall(cmd)
            data = client.recv(2048)
            print("{}".format(data.decode('ISO 8859-13'))) # decode the answer
            break
    except KeyboardInterrupt as key:
        print(key)
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="client / server")
    args = parser.parse_args()

    if args.mode == "s":
        server_loop()
    elif args.mode == "c":
        client_connection()


if __name__ == '__main__':
    main()
