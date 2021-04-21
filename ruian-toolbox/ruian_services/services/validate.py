# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        validate
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
# -------------------------------------------------------------------------------
__author__ = 'Radek Augustýn'

from ruian_services.services import ruian_connection
from ruian_services.services.http_shared import right_address, MimeBuilder, parameter, services, WebService, \
    get_result_format_param, UrlParam, get_district_number_url, get_house_number_url, get_record_number_url, \
    get_orientation_number_url, get_orientation_number_character_url, get_zip_code_url


def build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number):
    return {
        "street": street,
        "houseNumber": house_number,
        "recordNumber": record_number,
        "orientationNumber": orientation_number,
        "orientationNumberCharacter": orientation_number_character,
        "zipCode": str(zip_code).replace(" ", ""),
        "locality": locality,
        "localityPart": locality_part,
        "districtNumber": district_number
    }


def validate_address(
        builder,
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number):
    if not right_address(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number):
        return "False"

    dictionary = build_validate_dict(street, house_number, record_number, orientation_number,
                                     orientation_number_character, zip_code, locality, locality_part, district_number)

    result = ruian_connection.validate_address(dictionary)
    return builder.list_to_response_text(result)


def validate_address_service_handler(query_params, response):
    builder = MimeBuilder(query_params["Format"])
    response.mime_format = builder.get_mime_format()

    s = validate_address(
        builder,
        parameter(query_params, "Street"),
        parameter(query_params, "HouseNumber"),
        parameter(query_params, "RecordNumber"),
        parameter(query_params, "OrientationNumber"),
        parameter(query_params, "OrientationNumberCharacter"),
        parameter(query_params, "ZIPCode"),
        parameter(query_params, "Locality"),
        parameter(query_params, "LocalityPart"),
        parameter(query_params, "DistrictNumber")
    )
    response.html_data = s
    response.handled = True
    return response


def create_service_handlers():
    services.append(
        WebService("/Validate", "Ověření adresy", "Ověřuje existenci dané adresy",
                   """Umožňuje ověřit zadanou adresu. Adresa je zadána pomocí jednotlivých
                   prvků adresy.""",
                   [
                       get_result_format_param()
                   ],
                   [
                       UrlParam("Locality", "Obec", "Obec", html_tags=' class="RUIAN_TOWN_INPUT" '),
                       UrlParam("LocalityPart", "Část obce", "Část obce, pokud je známa", html_tags=' class="RUIAN_TOWNPART_INPUT" '),
                       get_district_number_url(False),
                       UrlParam("Street", "Ulice", "Název ulice", html_tags=' class="RUIAN_STREET_INPUT" '),
                       get_house_number_url(False),
                       get_record_number_url(False),
                       get_orientation_number_url(False),
                       get_orientation_number_character_url(False),
                       # URLParam("OrientationNumberCharacter", "Písmeno čísla<br>orientačního", ""),
                       get_zip_code_url(False),
                       UrlParam("FillAddressButton", "Doplň adresu", "Najde v databázi adresu odpovídající vyplněným hodnotám", "", False)
                   ],
                   validate_address_service_handler,
                   send_button_caption="Ověř adresu",
                   html_input_template=''
                   )
    )
