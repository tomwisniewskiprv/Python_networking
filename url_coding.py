# Decoding and encoding to URL format.
# 04.10.2017
# Tomasz Wiśniewski

import unittest
import argparse


def url_decode(text):
    # Function decodes given text from URL format.
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

        parts = "".join([chr(int(part[:2], 16)) + part[2:] for part in parts])
        if end != "":
            parts += end

    else:
        parts = [text]

    return parts


def url_encode(text):
    # Function encodes text to ULR format

    # Chars to encode in text
    forbidden_chars = {":": "%3A", "/": "%2F", "#": "%23", "?": "%3F", "&": "%24", "@": "%40", "%": "%25", "+": "%2B",
                       " ": "%20", ";": "%3B", "=": "%3D", "$": "%26", ",": "%2C", "<": "%3C", ">": "%3E", "^": "%5E",
                       "`": "%60", "\\": "%5c", "[": "%5B", "]": "%5D", "{": "%7B", "}": "%7D", "|": "%7C", "\"": "%22"}

    chars = list(text)

    for i in range(len(chars)):
        if chars[i] in forbidden_chars.keys():
            chars.insert(i, forbidden_chars.get(chars[i]))
            del (chars[i + 1])

    return "".join(chars)


def url_double_decode(text):
    # TODO
    pass


def url_double_encode(text):
    # Sometime text needs to be encoded twice to deceive parsers
    # TODO
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="e|d encode|decode", type=str, nargs="+")
    args = parser.parse_args()

    try:
        if args.mode[0] == "e":
            url_encode(args.mode[1])
        elif args.mode[0] == "d":
            url_decode(args.mode[1])
    except Exception as ex:
        print(ex)
        exit(-1)


class URL_Coding_Test(unittest.TestCase):
    def test_decode(self):
        text = "%3CAlert(0)%3E"
        correct = "<Alert(0)>"
        self.assertEqual(url_decode(text), correct)

    def test_encode(self):
        text = "<Alert(0)>"
        correct = "%3CAlert(0)%3E"
        self.assertEqual(url_encode(text), correct)
