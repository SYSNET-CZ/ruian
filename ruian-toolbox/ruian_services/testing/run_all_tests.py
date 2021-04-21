# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

from ruian_services.testing import shared_tools, compile_address, fulltext_search, geocode, nearby_addresses, validate, \
    validate_address_id

if __name__ == '__main__':
    shared_tools.setup_utf()

    tester = shared_tools.FormalTester("Všechny testy")

    compile_address.test(tester)
    fulltext_search.test(tester)
    geocode.test(tester)
    nearby_addresses.test(tester)
    validate.test(tester)
    validate_address_id.test(tester)

    tester.save_to_html("TestResults.html")

    compile_address.test()
    fulltext_search.test()
    geocode.test()
    nearby_addresses.test()
    validate.test()
    validate_address_id.test()
