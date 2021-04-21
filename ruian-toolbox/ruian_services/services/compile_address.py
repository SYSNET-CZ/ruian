#!C:/Python27/python.exe
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

from ruian_services.services import http_shared, id_check, ft_search, ruian_connection, validate
from ruian_services.services.http_shared import *


def error_message(msg):
    print(msg)
    pass


class TextFormat:
    plainText = 0
    xml = 1
    json = 2
    html = 3


def compile_address(
        builder=None, street=None, house_number=None, record_number=None,
        orientation_number=None, orientation_number_character=None, zip_code=None, locality=None,
        locality_part=None, district_number=None, do_validate=False, with_ruian_id=False):
    """
        @param builder            object   HTML builder
        @param record_number      string   Číslo záznamu???
        @param district_number    string   Číslo okresu???
        @param do_validate        boolean  proveď validaci
        @param with_ruian_id      boolean  vrať ID RUIAN
        @param street             string   Název ulice
        @param locality           string   Obec
        @param house_number       number   Číslo popisné
        @param zip_code           number   Poštovní směrovací číslo
        @param locality_part      string   Část obce, pokud je známa
        @param orientation_number number   Číslo orientační
        @param orientation_number_character string  Písmeno čísla orientačního
    """
    dict_value = validate.build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number)

    if do_validate or with_ruian_id:
        rows = ruian_connection.get_addresses(dict_value)

        if len(rows) == 1:
            (house_number, orientation_number, orientation_number_character, zip_code, locality, locality_part,
             nazev_mop, street, typ_so, ruian_id) = rows[0]
            if typ_so != "č.p.":
                record_number = house_number
                house_number = ""
            if nazev_mop is not None and nazev_mop != "":
                district_number = nazev_mop[nazev_mop.find(" ") + 1:]
            if not with_ruian_id:
                ruian_id = ""
        else:
            return ""
    else:
        ruian_id = ""

    if builder is None:
        return str((
            street, house_number, record_number, orientation_number, orientation_number_character,
            zip_code, locality, locality_part, district_number, ruian_id))
    elif builder.formatText == "json":
        return compile_address_as_json(
            street, house_number, record_number, orientation_number, orientation_number_character,
            zip_code, locality, locality_part, district_number, ruian_id)
    elif builder.formatText == "xml":
        return compile_address_as_xml(
            street, house_number, record_number, orientation_number, orientation_number_character,
            zip_code, locality, locality_part, district_number, ruian_id)
    elif builder.formatText == "texttoonerow" or builder.formatText == "htmltoonerow":
        return compile_address_to_one_row(
            street, house_number, record_number, orientation_number, orientation_number_character,
            zip_code, locality, locality_part, district_number, ruian_id)
    else:
        return builder.listToResponseText(
            compile_address_as_text(
                street, house_number, record_number, orientation_number, orientation_number_character,
                zip_code, locality, locality_part, district_number, ruian_id))


def compile_address_service_handler(query_params, response):
    """
    def add_id(id_value, str_value, builder_object):
        if builder_object.formatText == "json":
            return '\t"id": ' + id_value + ",\n" + str_value
        elif builder_object.formatText == "xml":
            return "\t<id>" + id_value + "</id>\n" + str_value
        else:
            return id_value + builder_object.lineSeparator + str_value
    """
    def get_query_param_inner(name, def_value=""):
        return http_shared.get_query_param(query_params, name, def_value)

    result_format = get_query_param_inner("Format", "text")
    builder = MimeBuilder(result_format)
    response.mime_format = builder.get_mime_format()

    if "ExtraInformation" in query_params:
        with_id = query_params["ExtraInformation"].lower() == "id"
    else:
        with_id = False

    if "AddressPlaceId" in query_params:
        query_params["AddressPlaceId"] = number_check(query_params["AddressPlaceId"])
        if query_params["AddressPlaceId"] != "":
            response = id_check.id_check_service_handler(query_params, response, builder)
        else:
            response.html = ""
            response.handled = True
            response.mime_format = builder.get_mime_format()
        return response

    elif "SearchText" in query_params:
        s = ft_search.search_address(builder, None, query_params["SearchText"], with_id)
        response.html_data = s

    else:
        do_validate = get_query_param_inner("Validate", "true").lower() == "true"
        s = compile_address(
            street=get_query_param_inner("Street"),
            house_number=get_query_param_inner("HouseNumber"),
            record_number=get_query_param_inner("RecordNumber"),
            orientation_number=get_query_param_inner("OrientationNumber"),
            orientation_number_character=get_query_param_inner("OrientationNumberCharacter"),
            zip_code=get_query_param_inner("ZIPCode"),
            locality=get_query_param_inner("Locality"),
            locality_part=get_query_param_inner("LocalityPart"),
            district_number=get_query_param_inner("DistrictNumber"),
            do_validate=do_validate,
            with_ruian_id=with_id
        )
        response.html_data = builder.list_to_response_text([s])
    response.handled = True
    return response


def create_service_handlers():
    services.append(
        WebService("/CompileAddress", u"Sestavení adresy", u"Formátování adresy ve standardizovaném tvaru",
                   u"""Umožňuje sestavit zápis adresy ve standardizovaném tvaru podle § 6 vyhlášky č. 359/2011 Sb.,
            kterou se provádí zákon č. 111/2009 Sb., o základních registrech, ve znění zákona č. 100/2010 Sb.
            Adresní místo lze zadat buď pomocí jeho identifikátoru RÚIAN, textového řetězce adresy nebo jednotlivých prvků adresy.""",
                   [
                       get_result_format_param()
                   ],
                   [
                       get_address_place_id_param_url(),
                       get_search_text_param(),
                       UrlParam("Locality", u"Obec", u"Obec", "", True, html_tags=' class="RUIAN_TOWN_INPUT" '),
                       UrlParam("LocalityPart", u"Část obce", u"Část obce, pokud je známa", "", True,
                                html_tags=' class="RUIAN_TOWNPART_INPUT" '),
                       get_district_number_url(False),
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
                   compile_address_service_handler,
                   send_button_caption=u"Sestav adresu",
                   html_input_template='''<select>
                                        <option value="text">text</option>
                                        <option value="xml">xml</option>
                                        <option value="html">html</option>
                                        <option value="json">json</option>
                                    </select>'''
                   )
    )


if __name__ == '__main__':
    import shared_tools.base

    shared_tools.base.setup_utf()
    # print(compileAddress(None, u"Mrkvičkova", u"1370", "", "", "", "", "", "", ""))
    print(compile_address(MimeBuilder("texttoonerow"), u"", u"14", "", "", "", "", "", "Stará Chodovská", ""))
