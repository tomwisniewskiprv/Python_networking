# Base64 encoding and decoding
# Tomasz Wiśniewski
# 2017.10.08

import unittest
import argparse
import base64


def allowed_chars():
    letters_uppercase = [chr(c + 65) for c in range(26)]
    letters_lowercase = [chr(c + 97) for c in range(26)]
    numbers = list(range(10))
    allowed_chars = ["+", "/"]
    allowed_data = letters_uppercase + letters_lowercase + numbers + allowed_chars
    return allowed_data


def encode_b64(text):
    data = list(text)
    data = "".join(["{:0>8}".format(bin(ord(c))[2:]) for c in data])  # cut '0b' from string binary representation

    # check length if it's divisible by 24
    if len(data) % 24 == 16:  # =  for 1 missing byte (16)
        data += "="
    elif len(data) % 24 == 8:  # == for 2 missing bytes (8)
        data += "=="

    data = list(chunks(data, 6))  # split bin data into chunks
    encoded = []
    missing_bytes = ""

    for d in data:
        if d.find("=") == -1:
            encoded.append(str(int(d, 2)))
        elif list(d).count("=") == 1:
            d = d.replace("=", "00")
            encoded.append(str(int(d, 2)))
            missing_bytes = "="
        elif list(d).count("=") == 2:
            d = d.replace("=", "00")
            encoded.append(str(int(d, 2)))
            missing_bytes = "=="

    return "".join([str(allowed_chars()[int(i)]) for i in encoded]) + missing_bytes


def decode_b64(text):
    pass


def chunks(l, n):
    """Yield successive n-sized chunks from l"""
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="e|d  encode|decode", type=str, nargs="+")
    args = parser.parse_args()

    if args.mode[0] == "e":
        print(encode_b64(args.mode[1]))


class B64_Test(unittest.TestCase):
    def test_encode(self):
        text = ["kod", "Pentesty", "Format", "PACKT"]  # test cases
        funct_results = [encode_b64(t) for t in text]
        correct_results = [base64.b64encode(bytearray(t.encode())) for t in text]
        correct_results = [result.decode() for result in correct_results]

        self.assertEqual(funct_results, correct_results)
