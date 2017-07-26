# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | remote_shell
# 22.07.2017 Tomasz Wisniewski


"""
Remote command shell for Windows (for now).
Alpha stage.
TODO:
    - work on coding both sides
"""

import socket
import subprocess, os, sys
import argparse
import locale

remote_server = "localhost"
port = 6666
# encoding = "utf-8"
# encoding = "windows-1250"

# Configure locale from the user's environment settings.
locale.setlocale(locale.LC_ALL, '')

# Wrap stdout with an encoding-aware writer.
lang, encoding = locale.getdefaultlocale()


def create_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("", port))
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
    """ Far end of the connection. This should be running on remote system. """
    server = create_server()
    server.listen(1)
    print("Shell server is running on port {}".format(port))

    connection, address = server.accept()

    welcome_msg = "Hello {}".format(address[0]).encode(encoding)
    connection.sendall(welcome_msg)

    try:
        while True:
            received = connection.recv(1024)  # receive commands
            if not received:
                break

            # execute command
            cmd = received.decode(encoding)
            output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # send back the results
            if not output.stdout:
                print(output) # debug
                if output.returncode == 0:
                    data = "command successfully executed.".encode(encoding)
                elif output.returncode == 1:
                    data = "command failed.\n" + output.stderr.decode(encoding)
                    data = data.encode(encoding)
                print(data)
            else:
                data = output.stdout
                print(data.decode(encoding))

            connection.sendall(data)

    except KeyboardInterrupt:
        print("Interrupted.")

    except TypeError as terr:
        connection.sendall("stop".encode(encoding))

    finally:
        server.close()
        connection.close()


def client_connection():
    """ Client sends commands to execute on remote server."""
    client = create_client()
    client.connect((remote_server, port))

    try:
        data = client.recv(1024)
        print(data.decode())

        while True:
            cmd = input("$:").strip()
            if cmd == "stop":  # temporary exit route
                cmd = cmd.encode(encoding)
                client.sendall(cmd)
                data = client.recv(4096)
                print(data.decode(encoding))
                client.shutdown(2)
                break
            else:
                cmd = cmd.encode(encoding)
                client.sendall(cmd)
                data = client.recv(4096)
                print("server:\n{}".format(data.decode(encoding)))
                if data == "stop":
                    break

    except KeyboardInterrupt as key:
        print(key)
    except TypeError as terr:
        client.sendall("quit")
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="c | s  - client / server")
    args = parser.parse_args()

    if args.mode == "s":
        server_loop()
    elif args.mode == "c":
        client_connection()


if __name__ == '__main__':
    main()
