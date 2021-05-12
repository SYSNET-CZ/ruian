# -*- coding: cp1250 -*-
# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      raugustyn
#
# Created:     10/11/2013
# Copyright:   (c) raugustyn 2013
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import gzip
import math
import xml.parsers.expat

from ruian_services.services import match_tools

XML_PATH_SEPARATOR = "/"


class AddressFileParser:
    """ T��da implementuj�c� konverzi z exportn�ho form�tu R�IAN. """

    def __init__(self):
        """ Nastavuje prom�nnou databasePath a inicializuje seznam otev�en�ch
        soubor�"""
        self.subXML = []
        self.xmlSubPaths = {}
        self.recordValues = {}
        self.recordTagName = ""
        self.elemPathStr = ""
        self.elemLevel = 0
        self.elemPath = []
        self.elemCount = 0

    def log_info(self):
        do_print = 50000 * math.floor(self.elemCount / 50000) == self.elemCount

        count = len(match_tools.search_database.town_names)
        do_print = do_print or 1000 * math.floor(count / 1000) == count

        count = len(match_tools.search_database.street_names)
        do_print = do_print or 50000 * math.floor(count / 50000) == count

        if do_print:
            print('{0} tag�, {1} obc�, {2} ulic'.format(
                self.elemCount,
                len(match_tools.search_database.town_names),
                len(match_tools.search_database.street_names)))

    def import_data(self, input_file_name):
        """ Tato procedura importuje data ze souboru ve form�tu v�m�nn�ho souboru
            RUIAN inputFileName a ulo�� jednotliv� z�znamy pomoc� ovlada�e dbHandler.

            @param {String} inputFileName Vstupn� soubor ve form�tu v�m�nn�ho souboru R�IAN.
            @param {String} inputFileName Vstupn� soubor ve form�tu v�m�nn�ho souboru R�IAN.
        """

        def add_name_to_list(list_value, name):
            if name not in list_value:
                list_value.append(name)
            pass

        def start_element(name, attrs):
            """ Start element Handler. """
            self.elemCount = self.elemCount + 1
            self.elemLevel = self.elemLevel + 1
            self.log_info()

            self.elemPath.append(name)
            self.elemPathStr = XML_PATH_SEPARATOR.join(self.elemPath)

            if name == "obec":
                match_tools.search_database.town_names.append(attrs["nazev"])
                add_name_to_list(match_tools.search_database.zip_codes, attrs["nazev"])
                self.log_info()

            if name == "ulice":
                match_tools.search_database.street_names.append(attrs["nazev"])
                self.log_info()

        def end_element(name):
            """ End element Handler """
            # jsme uvnit� importovan� tabulky
            print(str(name))
            self.elemPath.remove(self.elemPath[len(self.elemPath) - 1])
            self.elemPathStr = XML_PATH_SEPARATOR.join(self.elemPath)
            self.elemLevel = self.elemLevel - 1
            pass

        def char_data(data):
            print(str(data))
            pass

        p = xml.parsers.expat.ParserCreate()

        # Assign event handlers to expat parser
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data

        # Open and process XML file
        file = None
        suffix = input_file_name.split('.')[-1]
        if suffix == 'xml':
            file = open(input_file_name, "rt")
        elif suffix == 'gz':
            file = gzip.open(input_file_name, "rb")
        else:
            print("Unexpected file format.")

        p.ParseFile(file)
        file.close()

        print('P�e�teno {0} xml element�'.format(self.elemCount))
        pass


parser = AddressFileParser()
parser.import_data('..\\..\\01_SampleData\\adresy.xml')
match_tools.search_database.save_to_files('..\\..\\01_SampleData\\')
