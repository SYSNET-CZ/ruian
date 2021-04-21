# -*- coding: utf-8 -*-
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
__author__ = 'Augustyn'


class Coordinates:
    def __init__(self, jtsk_y, jtsk_x):
        self.JTSKX = jtsk_x
        self.JTSKY = jtsk_y


class Address:
    def __init__(
            self, street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number):
        self.street = street
        self.houseNumber = house_number
        self.recordNumber = record_number
        self.orientationNumber = orientation_number
        self.orientationNumberCharacter = orientation_number_character
        self.zipCode = zip_code
        self.locality = locality
        self.localityPart = locality_part
        self.districtNumber = district_number


class Locality:
    def __init__(self, address, coordinates):
        self.address = address
        self.coordinates = coordinates
