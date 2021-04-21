# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        validate_address_id
# Purpose:
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

# from http_shared import *
from ruian_services.services import ruian_connection
from ruian_services.services.http_shared import MimeBuilder, get_query_value, services, WebService, \
    get_result_format_param, get_address_place_id_param_url_id_not_disabled


def validate_address_id(result_format, address_place_id):
    print(str(result_format), str(address_place_id))
    # TODO
    return ""


def validate_address_id_service_handler(query_params, response):
    builder = MimeBuilder(query_params["Format"])
    response.mime_format = builder.get_mime_format()
    address_place_id = get_query_value(query_params, "AddressPlaceId", "")
    if address_place_id.isdigit():
        address = ruian_connection.find_address(address_place_id)
        if address:
            response.html_data = builder.list_to_response_text(["True"])
        else:
            response.html_data = builder.list_to_response_text(["False"])
    else:
        response.html_data = builder.list_to_response_text(["False"])
    response.handled = True
    return response


def create_service_handlers():
    services.append(
        WebService("/ValidateAddressId", "Ověření identifikátoru adresy", "Ověřuje existenci daného identifikátoru adresy",
                   """Umožňuje ověřit existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
                   [get_result_format_param()],
                   [get_address_place_id_param_url_id_not_disabled()],
                   validate_address_id_service_handler,
                   send_button_caption="Ověř identifikátor adresy",
                   html_input_template='''<select>
                                        <option value="text">text</option>
                                        <option value="xml">xml</option>
                                        <option value="html">html</option>
                                        <option value="json">json</option>
                                    </select>'''
                   )
    )
