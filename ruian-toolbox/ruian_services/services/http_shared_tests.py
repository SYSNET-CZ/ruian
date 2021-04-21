# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        HTTPShared_Tests
# Purpose:     Module HTTPShared tests implementation.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

import unittest

from ruian_services.services import http_shared


class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testnoneToString(self):
        self.assertEqual(http_shared.none_to_string(None), "", "None must be converted to string.")
        self.assertEqual(http_shared.none_to_string("34"), "34", "String must be converted to string.")
        self.assertEqual(http_shared.none_to_string(34), "34", "Int must be converted to string.")
        self.assertEqual(http_shared.none_to_string([34, "44"]), ["34", "44"],
                         "List must be converted to list of strings.")
        self.assertEqual(http_shared.none_to_string(("34", None, 15, "ff")), ("34", "", "15", "ff"),
                         "Tuple must be converted to tuple strings.")
        pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
