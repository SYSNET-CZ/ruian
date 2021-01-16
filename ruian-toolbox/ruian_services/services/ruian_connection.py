# -*- coding: utf-8 -*-
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
__author__ = 'Augustyn'

from postgisdb import _find_address, _get_nearby_localities, _validate_address, _find_coordinates, \
    _find_coordinates_by_address, _get_ruian_version_date, _save_ruian_version_date_today, _get_db_details, \
    _get_table_names, _get_addresses


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


find_address = _find_address
get_nearby_localities = _get_nearby_localities
validate_address = _validate_address
find_coordinates = _find_coordinates
find_coordinates_by_address = _find_coordinates_by_address
get_ruian_version_date = _get_ruian_version_date
save_ruian_version_date_today = _save_ruian_version_date_today
get_db_details = _get_db_details
get_table_names = _get_table_names
get_addresses = _get_addresses
