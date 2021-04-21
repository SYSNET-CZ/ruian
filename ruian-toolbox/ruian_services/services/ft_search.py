# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        compileaddress
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
# -------------------------------------------------------------------------------

from ruian_services.services import parse_address
from ruian_services.services.http_shared import *


def search_address(builder, search_flag, search_text, with_id=True):
    parser = parse_address
    candidates = parser.full_text_search_address(search_text)
    items = parser.build_address(builder, candidates, with_id)
    s = builder.list_to_response_text(items, rrecord_separator=builder.record_separator)
    print(str(search_flag))
    return s


def search_address_service_handler(query_params, response):
    builder = MimeBuilder(query_params["Format"])
    response.mime_format = builder.get_mime_format()
    if "ExtraInformation" in query_params:
        with_id = query_params["ExtraInformation"] == "id"
    else:
        with_id = False

    # searchText = p(queryParams, "SearchText")
    # searchText = queryParams[name]
    s = search_address(
        builder,
        parameter(query_params, "SearchFlag"),
        parameter(query_params, "SearchText"),
        with_id
    )
    response.html_data = s
    response.handled = True
    return response


def create_service_handlers():
    services.append(
        WebService("/FullTextSearch", u"Fulltextové vyhledávání", u"Vyhledávání adresního místa podle řetězce",
                   u"""Umožňuje nalézt a zobrazit seznam pravděpodobných adres na základě textového řetězce adresy.
            Textový řetězec adresy může být nestandardně formátován nebo může být i neúplný.""",
                   [get_result_format_param()],
                   [
                       get_search_text_param(),
                       UrlParam("ExtraInformation", u"Další informace", u"Vypíše zvolený druh dodatečných informací",
                                "", False)
                   ],
                   search_address_service_handler,
                   send_button_caption=u"Vyhledej adresu",
                   html_input_template=''
                   )
    )
