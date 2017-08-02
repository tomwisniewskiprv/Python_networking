# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | xor
# 02.08.2017 Tomasz Wisniewski


def xor(msg, key):
    """
    Visual representation of XOR cipher on binary level.
    :returns encoded/decoded message as string
    """
    print("Message: {}\nKey:\t {}".format(msg, key))
    bin_msg = [format(ord(letter), '08b') for letter in msg]
    bin_key = [format(ord(letter), '08b') for letter in key]
    xor_bin = []
    for (x, y) in zip(bin_msg, bin_key):
        xor_bin.append("".join([str(int(x) ^ int(y)) for (x, y) in zip(x, y)]))

    print(" ".join(bin_msg))
    print(" ".join(bin_key))
    print(" ".join(xor_bin))

    xor_int = [int(binary, 2) for binary in xor_bin]
    result = []

    for position in range(len(xor_int)):
        print("{:8c}".format(xor_int[position]), end=" ")
        result.append(chr(xor_int[position]))

    result = "".join(result)
    print("\nResult: {}".format(result))
    return result

def xor_silent(msg, key):
    """
    XOR cipher without display.
    :returns encoded/decoded message as string
    """
    bin_msg = [format(ord(letter), '08b') for letter in msg]
    bin_key = [format(ord(letter), '08b') for letter in key]
    xor_bin = []
    for (x, y) in zip(bin_msg, bin_key):
        xor_bin.append("".join([str(int(x) ^ int(y)) for (x, y) in zip(x, y)]))

    xor_int = [int(binary, 2) for binary in xor_bin]
    result = []

    for position in range(len(xor_int)):
        result.append(chr(xor_int[position]))

    result = "".join(result)
    return result


if __name__ == '__main__':
    msg = "adeabecc"
    key = "12341234"
    xor(msg, key)
    xor_silent(msg,key)
