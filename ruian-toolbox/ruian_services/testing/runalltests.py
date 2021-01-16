# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import compileaddress
import fulltextsearch
import geocode
import nearbyaddresses
import validate
import validateaddressid

if __name__ == '__main__':
    sharedtools.setup_utf()

    tester = sharedtools.FormalTester("Všechny testy")

    compileaddress.test(tester)
    fulltextsearch.test(tester)
    geocode.test(tester)
    nearbyaddresses.test(tester)
    validate.test(tester)
    validateaddressid.test(tester)

    tester.saveToHTML("TestResults.html")

    compileaddress.test()
    fulltextsearch.test()
    geocode.test()
    nearbyaddresses.test()
    validate.test()
    validateaddressid.test()
