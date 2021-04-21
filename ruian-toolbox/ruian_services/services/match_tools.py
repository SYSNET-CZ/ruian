# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        MatchTools
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import codecs
import os
import unittest


def save_names_list_to_file(names_list, file_name):
    print("Creating file", file_name)
    file = codecs.open(file_name, "w", "utf-8")
    for name in names_list:
        file.write(name + "\n")
    file.close()


class SearchDatabase:
    TOWN_NAMES_FILENAME = 'TownNames.txt'
    STREET_NAMES_FILENAME = 'StreetNames.txt'
    town_names = ['chodov', 'praha']
    street_names = [u'budovatelů', u'mrkvičkova']
    zip_codes = ['35735', '16300']
    address_data = {
        'chodov': {
            'budovatelů': ['676', '677', '678', '679', '680', '681']
        },
        'praha': {
            'mrkvičkova': ['1370', '1371', '1372', '1373', '1374', '1375']
        },
    }

    def is_town_name(self, value):
        return value.lower() in self.town_names

    def is_street_name(self, value):
        return value.lower() in self.street_names

    def is_zip_code(self, value):
        return value.lower() in self.zip_codes

    def get_town(self, town_name):
        return self.address_data[town_name]

    def save_to_files(self, path):
        save_names_list_to_file(self.town_names, os.path.join(path, self.TOWN_NAMES_FILENAME))
        save_names_list_to_file(self.street_names, os.path.join(path, self.STREET_NAMES_FILENAME))
        pass


search_database = SearchDatabase()

ADDRESS_STRING_SEPARATOR = ","
CISLO_ORIENTACNI_SEPARATOR = "/"


def normalize_address_string(address_string):
    """ Normalizuje adresní řetězec addressString """
    result = address_string
    result = result.replace("  ", " ")  # Více mezer je chápáno jako jedna
    result = result.replace(";", ADDRESS_STRING_SEPARATOR)  # Středník je chápán jako oddělovač čárka
    result = result.replace(":", ADDRESS_STRING_SEPARATOR)  # Dvojtečka je chápána jako oddělovač čárka
    result = result.replace(",,", ADDRESS_STRING_SEPARATOR)  # Více čárek je chápáno jako prázdná informace
    return result


class Adresa:
    def __init__(self):
        """ """
        self.mesto = ""
        self.psc = ""
        self.ulice = ""
        self.cislo_domovni = ""
        self.cislo_orientacni = ""
        self.cislo_orientacni_pismeno = ""
        self.names = []
        pass

    def parse_address_string(self, address_string):
        address_string = normalize_address_string(address_string)
        address_items = address_string.split(ADDRESS_STRING_SEPARATOR)
        for item in address_items:
            item_no_spaces = item.replace(" ", "")
            if item_no_spaces.isdigit() is True:  # Číslo domovní nebo PSČ
                if len(item) == 5:
                    self.psc = item
                else:
                    self.cislo_domovni = item_no_spaces
            else:
                separator_pos = item_no_spaces.find(CISLO_ORIENTACNI_SEPARATOR)
                if separator_pos >= 0:
                    self.cislo_domovni = item_no_spaces[0:separator_pos - 1]
                    self.cislo_orientacni = item_no_spaces[separator_pos + 1:]
                else:
                    self.names.append(item)

        return True

    def match_database(self):
        town = None
        for name in self.names:
            if town is not None:
                if name in town:
                    self.ulice = name
                else:
                    pass  # error
            elif search_database.is_town_name(name):
                town = search_database.get_town(name)
                self.mesto = name
            elif search_database.is_street_name(name):
                self.ulice = name
            else:
                pass  # error
        pass


class AdresniMisto(Adresa):
    def __init__(self):
        """ """
        Adresa.__init__(self)
        pass


if __name__ == '__main__':
    address = Adresa()
    address.parse_address_string("chodov, budovatelů, 677")
    address.match_database()
    import match_tools_unit_tests

    match_tools_unit_tests.main()
    unittest.main()
