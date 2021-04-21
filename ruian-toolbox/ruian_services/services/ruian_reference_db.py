# -*- coding: utf-8 -*-

__author__ = 'Liska'

from ruian_services.services.ruian_connection import *

database = {
    "12351": Locality(Address("Arnošta Valenty", "670", "", "31", "", "19800", "Praha", "Černý Most", "9"), Coordinates(0, 0)),
    "12353": Locality(Address("Medová", "", "30", "", "", "10400", "Praha", "Křeslice", "10"), Coordinates(100, 100)),
    "12355": Locality(Address("Lhenická", "1120", "", "1", "", "37005", "České Budějovice", "České Budějovice 2", ""), Coordinates(80, 70)),
    "12356": Locality(Address("Lhenická", "1120", "", "", "", "37005", "České Budějovice", "České Budějovice 2", ""), Coordinates(0, 100)),
    "12358": Locality(Address("Žamberecká", "339", "", "", "", "51601", "Vamberk", "Vamberk", ""), Coordinates(200, 100)),
    "12361": Locality(Address("", "106", "", "", "", "53333", "Pardubice", "Dražkovice", ""), Coordinates(120, 180)),
    "12364": Locality(Address("", "111", "", "", "", "50333", "Praskačka", "Praskačka", ""), Coordinates(130, 120)),
}


def _find_coordinates(address_id):
    for id_value, location in database.items():
        if id_value == address_id:
            return Coordinates(str(location.coordinates.JTSKY), str(location.coordinates.JTSKX))


def _find_address(id_value):
    if id_value in database.keys():
        location = database[id_value]
        return location.address


def _find_coordinates_by_address(dict_value):
    coordinates = []
    for id_value, location in database.items():
        if (
                dict_value["street"].lower() == location.address.street.lower() or dict_value["street"] == "") and \
                (dict_value["houseNumber"] == location.address.house_number or dict_value["houseNumber"] == "") and \
                (dict_value["recordNumber"] == location.address.record_number or dict_value["recordNumber"] == "") and \
                (dict_value["orientationNumber"] == location.address.orientation_number or
                 dict_value["orientationNumber"] == "") and \
                (dict_value["zipCode"] == location.address.zip_code or dict_value["zipCode"] == "") and \
                (dict_value["locality"].lower() == location.address.locality.lower() or dict_value[
                    "locality"] == "") and \
                (dict_value["localityPart"] == location.address.locality_part or dict_value["localityPart"] == "") and \
                (dict_value["districtNumber"] == location.address.district_number or dict_value[
                    "districtNumber"] == ""):
            coordinates.append(Coordinates(str(location.coordinates.JTSKY), str(location.coordinates.JTSKX)))
    return coordinates


def _get_nearby_localities(x, y, max_distance):
    addresses = []
    for id_value, location in database.items():
        real_distance = ((float(x) - float(location.coordinates.JTSKX)) ** 2 + (
                float(y) - float(location.coordinates.JTSKY)) ** 2) ** 0.5
        if real_distance < float(max_distance):
            addresses.append(location.address)
    return addresses


def _validate_address(dictionary):
    for id_value, location in database.items():
        if (dictionary["street"].lower() == location.address.street.lower()) and (
                dictionary["houseNumber"] == location.address.house_number) \
                and (dictionary["recordNumber"] == location.address.record_number) and (
                dictionary["orientationNumber"] == location.address.orientation_number) \
                and (dictionary["zipCode"] == location.address.zip_code) and (
                dictionary["locality"].lower() == location.address.locality.lower()) \
                and (dictionary["localityPart"] == location.address.locality_part) and (
                dictionary["districtNumber"] == location.address.district_number):
            return True
    return False


def _get_ruian_version_date():
    return "unassigned RUIAN Version"


def _save_ruian_version_date_today():
    pass


def _get_db_details():
    return "getDBDetails() not implemented."


def _get_table_names():
    return ""
