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

# import ruian_connection
# from http_shared import *
# import parse_address
# from ruian_services import services
from ruian_services.services import ruian_connection, parse_address
from ruian_services.services.http_shared import MimeBuilder, parameter, WebService, get_result_format_param, RestParam, \
    UrlParam, services


def format_address(address):
    formated_address = u""
    house_number_str = u""

    if address.house_number != "":
        house_number_str += address.house_number
        if address.orientation_number != "":
            house_number_str += "/" + address.orientation_number + address.orientationNumberCharacter
    elif address.record_number != "":
        house_number_str = u"č. ev. " + address.record_number

    if address.street != "":
        formated_address += address.street + " " + house_number_str + ", "
        if address.locality == "Praha":
            formated_address += address.locality_part + ", " + address.zip_code + ", " + address.locality + " " + address.district_number
        elif address.locality == address.locality_part:
            formated_address += address.zip_code + " " + address.locality
        else:
            formated_address += address.locality_part + ", " + address.zip_code + " " + address.locality
    else:
        if address.locality == address.locality_part:
            if address.record_number != "":
                formated_address += house_number_str + ", "
            else:
                formated_address += u"č.p. " + address.house_number + ", "
            formated_address += address.zip_code + " " + address.locality
        else:
            formated_address += address.locality_part + " " + house_number_str + ", " + address.zip_code + " " + address.locality
            if address.locality == "Praha":
                formated_address += ", " + address.district_number

    return formated_address


def near_by_addresses(builder, jtsk_y, jtsk_x, distance, with_id, with_distance, max_count):
    if jtsk_y.find(".") >= 0:
        jtsk_y = jtsk_y[:jtsk_y.find(".")]
    if jtsk_y.find(",") >= 0:
        jtsk_y = jtsk_y[:jtsk_y.find(",")]
    if jtsk_x.find(".") >= 0:
        jtsk_x = jtsk_x[:jtsk_x.find(".")]
    if jtsk_x.find(",") >= 0:
        jtsk_x = jtsk_x[:jtsk_x.find(",")]
    if jtsk_x.isdigit() and jtsk_y.isdigit() and distance.isdigit():
        addresses = ruian_connection.get_nearby_localities(jtsk_x, jtsk_y, distance, max_count)
        parser = parse_address
        formatted_address = parser.build_address(builder, addresses, with_id, with_distance)
        s = builder.list_to_response_text(formatted_address, True)
        return s
    else:
        return ""


def near_by_addresses_service_handler(query_params, response):
    builder = MimeBuilder(query_params["Format"])
    response.mime_format = builder.get_mime_format()
    if "ExtraInformation" in query_params:
        with_id = query_params["ExtraInformation"].lower() == "id"
        with_distance = query_params["ExtraInformation"].lower() == "distance"
    else:
        with_id = False
        with_distance = False

    s = near_by_addresses(
        builder,
        parameter(query_params, "JTSKY", ""),
        parameter(query_params, "JTSKX", ""),
        parameter(query_params, "Distance", ""),
        with_id, with_distance,
        parameter(query_params, "MaxCount", "1000"),
    )
    response.html_data = s
    response.handled = True
    return response


def create_service_handlers():
    services.append(
        WebService(
            "/NearbyAddresses", u"Blízké adresy", u"Hledá adresu nejbližší daným souřadnicím",
            u"""Umožňuje vyhledat adresní místa v okolí zadaných souřadnic do určité vzdálenosti.
                   Vrací záznamy databáze RÚIAN setříděné podle vzdálenosti od zadaných souřadnic.""",
            [
                get_result_format_param(),
                RestParam(
                    "/JTSKY", u"JTSK Y [m]", u"Souřadnice Y v systému S-JTSK v metrech",
                    html_tags=' required title="Souřadnice Y v metrech" onkeypress="return isNumber(event, this, 6, 900000)" '),
                RestParam(
                    "/JTSKX", u"JTSK X [m]", u"Souřadnice X v systému S-JTSK v metrech",
                    html_tags=' required title="Souřadnice X v metrech" onkeypress="return isNumber(event, this, 7, 1230000)" '),
                RestParam(
                    "/Distance", u"Vzdálenost [m]", u"Vzdálenost v metrech od vloženého bodu",
                    html_tags=' required title="Vzdálenost v metrech od vloženého bodu" onkeypress="return isNumber(event, this, 6, 0)" '),
                RestParam(
                    "MaxCount", u"Počet záznamů",
                    u"Maximální počet záznamů, implicitně 1000, maximálně 10000",
                    html_tags=' title="Maximální počet záznamů, implicitně 1000, maximálně 10000" onkeypress="return isNumber(event, this, 6, 10000)" '),
            ],
            [
                UrlParam("ExtraInformation", u"Další informace", u"Vypíše zvolený druh dodatečných informací",
                         "", False)
            ],
            near_by_addresses_service_handler,
            send_button_caption=u"Hledej blízké adresy",
            html_input_template='''<select>
                                        <option value="text">text</option>
                                        <option value="xml">xml</option>
                                        <option value="html">html</option>
                                        <option value="json">json</option>
                                    </select>'''
        )
    )
