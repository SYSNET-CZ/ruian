# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs
from urllib.parse import quote
from urllib.request import urlopen

from ruian_services.testing import shared_tools
from ruian_services.testing.shared_tools import FormalTester


def test(tester_param=None):
    if tester_param is None:
        tester = FormalTester("Ověření funkčnosti služby ValidateAddressID")
    else:
        tester = tester_param

    tester.new_section(
        "Ověření funkčnosti služby ValidateAddressID",
        """Tento test ověřuje funkčnost služby ValidateAddressID, která ověřuje existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
        "Compiling person", "Tester")

    def add_test(path, expected_value):
        try:
            result = urlopen(shared_tools.SERVER_URL + path).read()
        except Exception as inst:
            result = str(inst)
        # result = result.strip()
        result = quote(codecs.encode(result, "utf-8"))
        tester.add_test(path, result, expected_value, "")

    add_test("/ValidateAddressId/txt?AddressPlaceId=1408739", "True")
    add_test("/ValidateAddressId/txt?AddressPlaceId=18480", "False")
    add_test("/ValidateAddressId/txt?AddressPlaceId=1498011", "True")
    add_test("/ValidateAddressId/txt?AddressPlaceId=40094944", "True")
    add_test("/ValidateAddressId/txt?AddressPlaceId=11505095", "True")
    add_test("/ValidateAddressId/txt?AddressPlaceId=1550080", "True")
    add_test("/ValidateAddressId/txt?AddressPlaceId=11390808", "True")
    add_test("/ValidateAddressId/txt?AddressPlaceId=150", "False")
    add_test("/ValidateAddressId/txt?AddressPlaceId=6084810", "False")
    add_test("/ValidateAddressId/txt?AddressPlaceId=18753880", "False")
    add_test("/ValidateAddressId/txt?AddressPlaceId=12j", "False")
    add_test("/ValidateAddressId/txt?AddressPlaceId=k", "False")

    tester.close_section()

    if tester_param is None:
        tester.save_to_html("ValidateAddressID.html")


if __name__ == '__main__':
    shared_tools.setup_utf()
    test()
