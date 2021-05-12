# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        geocode
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
# -------------------------------------------------------------------------------
__author__ = 'Radek Augustýn'

from ruian_services.services import parse_address, ruian_connection
from ruian_services.services.http_shared import *


def geocode_id(address_id):
    coordinates = ruian_connection.find_coordinates(address_id)
    return coordinates


def geocode_address(
        builder, street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, with_id, with_address):
    if right_address(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number):
        dict_value = {
            "street": street,
            "houseNumber": house_number,
            "recordNumber": record_number,
            "orientationNumber": orientation_number,
            "orientationNumberCharacter": orientation_number_character,
            "zipCode": zip_code,
            "locality": locality,
            "localityPart": locality_part,
            "districtNumber": district_number
        }
        coordinates = ruian_connection.find_coordinates_by_address(dict_value)
        lines = []
        for item in coordinates:
            dictionary = {
                "JTSKY": item[0], "JTSKX": item[1], "id": str(item[2]), "locality": item[3],
                "localityPart": item[4], "street": item[5], "houseNumber": item[6], "recordNumber": item[7],
                "orientationNumber": item[8], "orientationNumberCharacter": item[9], "zipCode": item[10],
                "districtNumber": item[11]}
            lines.append(dictionary)
        s = builder.list_of_dictionaries_to_response_text(lines, with_id, with_address)
        return s
    else:
        return ""


def _fill_dictionary(temp):
    out = {
        "JTSKX": temp[0], "JTSKY": temp[1], "id": str(temp[2]), "locality": temp[3],
        "localityPart": temp[4], "street": temp[5], "houseNumber": temp[6],
        "recordNumber": temp[7], "orientationNumber": temp[8],
        "orientationNumberCharacter": temp[9], "zipCode": temp[10], "districtNumber": temp[11]
    }
    return out


def geocode_address_service_handler(query_params, response):
    def param(name, def_value=""):
        if name in query_params:
            return unquote(query_params[name])
        else:
            return def_value

    result_format = param("Format", "text")
    builder = MimeBuilder(result_format)
    response.mime_format = builder.get_mime_format()
    with_id = param("ExtraInformation") == "id"
    with_address = param("ExtraInformation") == "address"

    if "AddressPlaceId" in query_params:
        # response = IDCheck.IDCheckServiceHandler(queryParams, response, builder)
        query_params["AddressPlaceId"] = number_check(query_params["AddressPlaceId"])
        if query_params["AddressPlaceId"] != "":
            coordinates = geocode_id(query_params["AddressPlaceId"])
            if coordinates:
                temp = coordinates[0]
                dictionary = _fill_dictionary(temp)
                s = builder.list_of_dictionaries_to_response_text([dictionary], with_id, with_address)
            else:
                s = ""
        else:
            s = ""

    elif "SearchText" in query_params:
        parser = parse_address
        candidates = parser.full_text_search_address(query_params["SearchText"])
        lines = []
        for candidate in candidates:
            coordinates = geocode_id(candidate[0])
            if not coordinates:
                continue
            else:
                temp = coordinates[0]
            # if candidate[4] == "č.p.":
            #    houseNumber = candidate[5]
            #    recordNumber = ""
            # else:
            #    houseNumber = ""
            #    recordNumber = candidate[5]
            dictionary = _fill_dictionary(temp)
            lines.append(dictionary)
        s = builder.list_of_dictionaries_to_response_text(lines, with_id, with_address)
        # s = builder.coordintesToResponseText(temp)

    else:
        s = geocode_address(
            builder,
            param("Street"),
            param("HouseNumber"),
            param("RecordNumber"),
            param("OrientationNumber"),
            param("OrientationNumberCharacter"),
            param("ZIPCode"),
            param("Locality"),
            param("LocalityPart"),
            param("DistrictNumber"),
            with_id,
            with_address
        )
    response.html_data = s
    response.handled = True
    return response


def create_service_handlers():
    services.append(
        WebService("/Geocode", u"Geokódování", u"Vyhledávání definičního bodu adresního místa",
                   u"""<p>Umožňuje klientům jednotným způsobem získat souřadnice zadaného adresního místa.
            Adresní místo zadáme buď pomocí jeho identifikátoru RÚIAN nebo pomocí textového řetězce adresy.<br>""",
                   [
                       get_result_format_param()
                   ],
                   [
                       get_address_place_id_param_url(),
                       get_search_text_param(),
                       UrlParam("Locality", u"Obec", u"Obec", "", True, html_tags=' class="RUIAN_TOWN_INPUT" '),
                       UrlParam("LocalityPart", u"Část obce", u"Část obce, pokud je známa", "", True,
                                html_tags=' class="RUIAN_TOWNPART_INPUT" '),
                       get_district_number_url(),
                       UrlParam("Street", u"Ulice", u"Název ulice", "", True, html_tags=' class="RUIAN_STREET_INPUT" '),
                       get_house_number_url(),
                       get_record_number_url(),
                       get_orientation_number_url(),
                       get_orientation_number_character_url(),
                       get_zip_code_url(),
                       UrlParam("ExtraInformation", u"Další informace", u"Vypíše zvolený druh dodatečných informací",
                                "", False),
                       UrlParam("FillAddressButton", u"Doplň adresu",
                                u"Najde v databázi adresu odpovídající vyplněným hodnotám", "", True)
                   ],
                   geocode_address_service_handler,
                   send_button_caption=u"Najdi polohu",
                   html_input_template=""
                   )
    )
