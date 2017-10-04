# Decoding and encoding to URL format.
# 04.10.2017 Tomasz Wiśniewski

import argparse
import sys


def url_decode(text):
    # Function decodes given text into URL format.
    # Reverse function is called url_encode

    parts = []
    end = ""

    if "%" in text:
        parts = text.split("%")
        if parts[0] == "":
            parts = parts[1:]
        if len(parts[len(parts) - 1]) < 2:
            pass
            end = parts[len(parts) - 1]
            parts = parts[:len(parts) - 1]

        parts = "".join([chr(int(e[:2], 16)) + e[2:] for e in parts])
        if end != "":
            parts += end

    else:
        parts = [text]

    return parts

def url_encode(text):
    pass


def url_double_decode(text):
    #TODO
    pass


def url_double_encode(text):
    #TODO
    pass


if __name__ == "__main__":
    text = "%3CAlert(0)%3E"
    text = url_decode(text)
    print(text)



