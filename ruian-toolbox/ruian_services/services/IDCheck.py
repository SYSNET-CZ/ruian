#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

from HTTPShared import *

import ruian_connection

import compile_address
import sharetools

def IDCheckServiceHandler(queryParams, response, builder):
    response.mimeFormat = builder.getMimeFormat()
    address = ruian_connection.find_address(sharetools.get_key_value(queryParams, "AddressPlaceId"))
    response.handled = True
    if address:
        html = compile_address.compileAddress(builder, address.street, address.houseNumber, address.recordNumber, address.orientationNumber, address.orientationNumberCharacter, address.zipCode, address.locality, address.localityPart, address.districtNumber)
        response.htmlData = builder.listToResponseText([html])

    return response