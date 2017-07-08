# -*- coding: utf-8 -*-
# Python 3.6
# Python_networking | ip_validation
# 07.07.2017 Tomasz Wisniewski 

import re
import unittest


def validate_ip(ip):
    """
     IP address validation,
     :return 1 if IP is correct , else returns 0
    """

    ipregex = re.compile(
        "^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$")

    if ipregex.match(ip):
        return 1
    else:
        return 0


if __name__ == "__main__":
    unittest.main()


class Test_validate_ip(unittest.TestCase):
    def test_correct_ip(self):
        ip_list = ['10.0.0.64', '192.168.10.20', '8.8.8.8']
        for ip in ip_list:
            self.assertEqual(validate_ip(ip), True)

    def test_incorrect_ip(self):
        ip_list = ['10.0.0.', '192.168.10.270', '8.8.8.256', ]
        for ip in ip_list:
            self.assertEqual(validate_ip(ip), False, ip)

    def test_empty_input(self):
        self.assertEqual(validate_ip(''), False)
