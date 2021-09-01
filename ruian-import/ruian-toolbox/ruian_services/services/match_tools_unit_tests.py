# -*- coding: utf-8 -*-
# This file was originally generated by PyScripter's unitest wizard

import unittest

from ruian_services.services import match_tools as mt


class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_address_match(self):
        # self.assertEqual(mt.addressMatch("Praha, Mrkvičkova 1270"), True)
        pass

    def testnormalize_address_string(self):
        self.assertEqual(mt.normalize_address_string("Karlovy  Vary,  Mrkvičkova  1270"),
                         "Karlovy Vary, Mrkvičkova 1270", "Více mezer je chápáno jako jedna")
        self.assertEqual(mt.normalize_address_string("Karlovy Vary;Mrkvičkova 1270"), "Karlovy Vary,Mrkvičkova 1270",
                         "Středník je chápán jako oddělovač čárka")
        self.assertEqual(mt.normalize_address_string("Karlovy Vary:Mrkvičkova 1270"), "Karlovy Vary,Mrkvičkova 1270",
                         "Dvojtečka je chápána jako oddělovač čárka")
        self.assertEqual(mt.normalize_address_string("Karlovy Vary,,Mrkvičkova 1270"), "Karlovy Vary,Mrkvičkova 1270",
                         "Více čárek je chápáno jako prázdná informace")
        pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()