# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        HTTPShared
# Purpose:
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

from urllib.parse import unquote

services = []


def get_result_format_param():
    return RestParam("/Format", u"Formát", u"Formát výsledku služby (HTML, XML, Text, JSON)")


def get_search_text_param():
    return UrlParam("SearchText", u"Adresa", u"Adresa ve tvaru ulice číslo, část obce, obec, PSČ",
                    html_tags=' class="RUIAN_TEXTSEARCH_INPUT" required ')


def get_address_place_id_param_rest():
    return RestParam("/AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa")


def get_zip_code_url(disabled=True):
    # psc = 10000...79862
    return UrlParam("zip_code", u"PSČ", u"Poštovní směrovací číslo v rozsahu 100000 až 79862", "", disabled,
                    html_tags=' class="RUIAN_ZIP_INPUT" onkeypress="return isNumber(event, this, 5, 79862)" ')  # onpaste="return isNumber(event, this, 5, 79862)"')


def get_house_number_url(disabled=True):
    # cislo_domovni (cislo popisne a cislo evidencni) = 1..9999
    return UrlParam("house_number", u"Číslo popisné", "Číslo popisné v rozsahu 1 až 9999", "", disabled,
                    html_tags=' class="RUIAN_HOUSENUMBER_INPUT" onkeypress="return isNumber(event, this, 4, 0)" ')  # onpaste="return isNumber(event, this, 4, 0)"')


def get_record_number_url(disabled=True):
    # cislo_domovni (cislo popisne a cislo evidencni) = 1..9999
    return UrlParam(
        "record_number", u"Číslo evidenční", u"Číslo evidenční, pokud je přiděleno, v rozsahu 1 až 9999", "", disabled,
        html_tags=' class="RUIAN_RECORDNUMBER_INPUT"  onkeypress="return isNumber(event, this, 4, 0)" ')
    # onpaste="return isNumber(event, this, 4, 0)"')


def get_orientation_number_url(disabled=True):
    # cislo_orientacni = 1..999
    return UrlParam("orientation_number", u"Číslo orientační", "Číslo orientační v rozsahu 1 až 999", "", disabled,
                    html_tags=' class="RUIAN_ORIENTATIONNUMBER_INPUT" onkeypress="return isNumber(event, this, 3, 0)" ')  # onpaste="return isNumber(event, this, 3, 0)"')


def get_orientation_number_character_url(disabled=True):
    # Písmeno čísla orientačního a..z, A..Z
    return UrlParam("orientation_number_character", u"Písmeno čísla<br>orientačního",
                    "Písmeno čísla orientačního a..z, A..Z", "", disabled,
                    html_tags=' class="RUIAN_ORIENTATIONNUMBERCHARACTER_INPUT" onkeypress="return isENLetter(event, this)" ')


def get_district_number_url(disabled=True):
    # 1..10
    return UrlParam("district_number", u"Městský obvod", u"Číslo městského obvodu v Praze",
                    "", disabled,
                    html_tags=' class="RUIAN_DISTRICTNUMBER_INPUT" onkeypress="return isNumber(event, this, 2, 10)" ')  # onpaste="return isNumber(event, this, 2, 10)"')


def get_address_place_id_param_url():
    # gid = 19..72628626
    return UrlParam("AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa, maximálně 8 číslic", "", True,
                    html_tags=' class="RUIAN_ID_INPUT" onkeypress="return isNumber(event, this, 8, 0)" required ')


def get_address_place_id_param_url_id_not_disabled():
    return UrlParam("AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa, maximálně 8 číslic", "",
                    False,
                    html_tags=' class="RUIAN_ID_INPUT" onkeypress="return isNumber(event, this, 8, 0)" required ')


class HTTPResponse:
    def __init__(self, handled, mime_format="text/html", html_data=""):
        self.handled = handled
        self.mime_format = mime_format
        self.html_data = html_data


class UrlParam:
    def __init__(self, name, caption, short_desc, html_desc="", disabled=False, html_tags=""):
        self.name = name
        self.caption = caption
        self.short_desc = short_desc
        self.html_desc = html_desc
        self.disabled = disabled
        self.html_tags = html_tags


class RestParam(UrlParam):
    def __init__(self, path_name, caption, short_desc, html_desc="", html_tags=""):
        UrlParam.__init__(self, path_name, caption, short_desc, html_desc, False, html_tags)

    def get_path_name(self):
        return self.name

    path_name = property(fget=get_path_name)


def get_mime_format(self, format_text):
    a = self[format_text].lower()
    if a in ["html", "htmltoonerow"]:
        return "text/" + self[format_text].lower()
    elif a in ["xml", "json"]:
        return "application/" + self[format_text].lower()
    else:  # Default value text
        return "text/plain"


def none_to_string(item):
    """
    Converts item to string, unlike str or repr, None is represented as "".

    1. None is represented as "".
    2. For tuple items, tupple with values as string returned
    3. For list items, list with values as string returned

    noneToString(None) = ""
    noneToString(3) = "3"
    noneToString('3') = "3"
    noneToString((None, 3, None)) = ("", "3", "")
    noneToString([None, 3, None]) = ["", "3", ""]

    :param item: Value to be converted to string.
    :return: String representation of item, none represented as ""
"""
    if isinstance(item, tuple):
        result = ()
        for subItem in item:
            result = result + (none_to_string(subItem),)
        return result
    elif isinstance(item, list):
        result = []
        for subItem in item:
            result.append(none_to_string(subItem))
        return result
    else:
        return [str(item), ""][item is None]


def list_to_xml(list_of_lines, line_separator="\n", tag="FormattedOutput"):
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator
    for line in list_of_lines:
        result += "<" + tag + ">" + line_separator + line + "</" + tag + ">" + line_separator
    return result + "</xml>"


def list_to_json(list_of_lines, line_separator="\n", tag="FormattedOutput"):
    result = "{"
    index = 0
    for item in list_of_lines:
        index += 1
        if index > 1:
            result += ','
        if item == "True" or item == "False":
            addition1 = '\t"valid" : '
            addition2 = "\n"
        else:
            addition1 = ""
            addition2 = ""
        result += line_separator + '"' + tag + str(
            index) + '" : {' + line_separator + addition1 + item + addition2 + "\t}"
    result += line_separator + "}"
    return result


def list_to_text(list_of_lines, line_separator="\n"):
    result = ""
    for line in list_of_lines:
        result += line + line_separator
    return result[:-len(line_separator)]


def list_to_html(list_of_lines, line_separator="<br>"):
    result = ""
    for line in list_of_lines:
        if result != "":
            result += line_separator
        result += line
    return result


def dictionary_to_text(dictionary, with_id, with_address):
    response = dictionary["JTSKY"] + ", " + dictionary["JTSKX"]
    if with_id:
        response = dictionary["id"] + ", " + response
    if with_address:
        response += ", " + compile_address_to_one_row(dictionary["street"], dictionary["house_number"],
                                                      dictionary["record_number"], dictionary["orientation_number"],
                                                      dictionary["orientation_number_character"],
                                                      dictionary["zip_code"], dictionary["locality"],
                                                      dictionary["locality_part"], dictionary["district_number"])
    return response


def dictionary_to_xml(dictionary, with_id, with_address):
    response = "<record>\n"
    if with_id:
        response += "\t<id>" + dictionary["id"] + "</id>\n"
    response += "\t<JTSKY>" + dictionary["JTSKY"] + "</JTSKY>\n"
    response += "\t<JTSKX>" + dictionary["JTSKX"] + "</JTSKX>\n"
    if with_address:
        response += compile_address_as_xml(
            dictionary["street"], dictionary["house_number"], dictionary["record_number"],
            dictionary["orientation_number"], dictionary["orientation_number_character"],
            dictionary["zip_code"], dictionary["locality"], dictionary["locality_part"],
            dictionary["district_number"])
    response += "</record>\n"
    return response


def dictionary_to_json(dictionary, with_id, with_address):
    response = "\n\t{\n"
    if with_id:
        response += '\t"id":' + dictionary["id"] + ",\n"
    response += '\t"JTSKY":' + dictionary["JTSKY"] + ",\n"
    response += '\t"JTSKX":' + dictionary["JTSKX"]
    if with_address:
        response += ",\n" + compile_address_as_json(
            dictionary["street"], dictionary["house_number"], dictionary["record_number"],
            dictionary["orientation_number"], dictionary["orientation_number_character"],
            dictionary["zip_code"], dictionary["locality"], dictionary["locality_part"],
            dictionary["district_number"])
    else:
        response += "\n"
    response += "\t}"
    return response


def coordinates_to_xml(list_of_coordinates, line_separator="\n", tag="Coordinates"):
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator
    index = 0
    for coordinates in list_of_coordinates:
        index = index + 1
        result += "<" + tag + str(
            index) + ">" + line_separator + "<Y>" + coordinates.JTSKY + "</Y>" + line_separator + "<X>" + coordinates.JTSKX + "</X>" + line_separator + "</" + tag + str(
            index) + ">" + line_separator
    result += "</xml>"
    return result


def coordinates_to_html(list_of_coordinates, line_separator="<br>"):
    result = ""
    for line in list_of_coordinates:
        if result != "":
            result += line_separator
        result += line.JTSKY + ", " + line.JTSKX
    return result


def coordinates_to_json(list_of_coordinates, line_separator="\n", tag="Coordinates"):
    result = "{"
    index = 0
    for line in list_of_coordinates:
        index += 1
        if index > 1:
            result += ','
        result += line_separator + '"' + tag + str(
            index) + '" : {' + line_separator + ' \t"Y": "' + line.JTSKY + '",' + line_separator + '\t"X": "' + line.JTSKX + '"' + line_separator + "\t}"
    result += line_separator + "}"
    return result


def coordinates_to_text(list_of_coordinates, line_separator="\n"):
    result = ""
    for line in list_of_coordinates:
        result += line.JTSKX + ", " + line.JTSKY + line_separator
    return result[:-1]


def addresses_to_xml(list_of_addresses, line_separator="\n", tag="Adresa"):
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator
    index = 0
    for line in list_of_addresses:
        orientation_number = none_to_string(line[6])
        sign = none_to_string(line[4])
        if orientation_number != "":
            house_numbers = "\t<" + sign + ">" + none_to_string(line[5]) + "</" + sign + ">" + line_separator + \
                            "\t<orientacni_cislo>" + orientation_number + \
                            none_to_string(line[7]) + "</orientacni_cislo>"
        else:
            house_numbers = "\t<" + sign + ">" + none_to_string(line[5]) + "</" + sign + ">"
        index = index + 1
        street = none_to_string(line[3])

        if street != "":
            street = "\t<ulice>" + street + "</ulice>" + line_separator

        town = none_to_string(line[1])
        district = none_to_string(line[2])

        if town == district or district == "":
            town_district = "\t<obec>" + town + "</obec>"
        else:
            town_district = "\t<obec>" + town + "</obec>" + line_separator + "\t<cast_obce>" + district + "</cast_obce>"

        result += "<" + tag + str(index) + ">" + line_separator + "<ID>" + none_to_string(line[
                                                                                              0]) + "</ID>" + line_separator + town_district + line_separator + street + house_numbers + line_separator + "\t<PSČ>" + none_to_string(
            line[8]) + "</PSČ>" + line_separator + "</" + tag + str(index) + ">" + line_separator
    result += "</xml>"
    return result


def addresses_to_json(list_of_addresses, line_separator="\n", tag="Adresa"):
    result = "{"
    index = 0
    for line in list_of_addresses:
        index += 1
        if index > 1:
            result += ','

        orientation_number = none_to_string(line[6])
        sign = none_to_string(line[4])
        if orientation_number != "":
            house_numbers = '\t"' + sign + '": ' + none_to_string(
                line[5]) + ',' + line_separator + '\t"orientační_číslo":' + orientation_number + none_to_string(
                line[7]) + ','
        else:
            house_numbers = '\t"' + sign + '": ' + none_to_string(line[5]) + ','

        street = none_to_string(line[3])

        if street != "":
            street = '\t"ulice": ' + street + "," + line_separator

        town = none_to_string(line[1])
        district = none_to_string(line[2])

        if town == district or district == "":
            town_district = '\t"obec" : ' + town + ","
        else:
            town_district = '\t"obec" : ' + town + "," + line_separator + '\t"část_obce": ' + district + ","

        result += line_separator + '"' + tag + str(index) + '" : {' + line_separator + '\t"ID": ' + none_to_string(
            line[
                0]) + line_separator + town_district + line_separator + street + house_numbers + line_separator + '\t"PSČ" :' + none_to_string(
            line[8]) + line_separator + "\t}"
    result += line_separator + "}"
    return result


def addresses_to_text(list_of_addresses, line_separator="\n"):
    result = ""
    for line in list_of_addresses:
        orientation_number = none_to_string(line[6])
        if orientation_number != "":
            house_numbers = none_to_string(line[5]) + "/" + orientation_number + none_to_string(line[7])
        else:
            house_numbers = none_to_string(line[5])
        street = none_to_string(line[3])
        if street != "":
            street += " "
        town = none_to_string(line[1])
        district = none_to_string(line[2])
        if town == district:
            town_district = town
        else:
            town_district = town + "-" + district
        result += none_to_string(line[0]) + " " + street + none_to_string(
            line[4]) + " " + house_numbers + ", " + town_district + ", " + none_to_string(line[8]) + line_separator
    return result


class MimeBuilder:
    def __init__(self, format_text="text"):
        self.formatText = format_text.lower()
        self.record_separator = "\n"

        if self.formatText in ["xml", "json"]:
            self.line_separator = "\n"
        elif self.formatText == "html":
            self.line_separator = "<br>"
        elif self.formatText in ["htmltoonerow", "texttoonerow"]:
            self.line_separator = ", "
        else:  # default value text
            self.line_separator = "\n"

        pass

    def get_mime_format(self):
        if self.formatText in ["xml", "json"]:
            return "application/" + self.formatText
        elif self.formatText in ["html", "htmltoonerow"]:
            return "text/html"
        else:  # Default value text
            return "text/plain"

    def list_to_response_text(self, list_of_lines, ignore_one_row=False, record_separator="\n"):
        if record_separator == "":
            line_separator = self.line_separator
        else:
            line_separator = record_separator
        print(str(ignore_one_row))

        if self.formatText == "xml":
            return list_to_xml(list_of_lines, line_separator)
        elif self.formatText == "html" or self.formatText == "htmltoonerow":
            return list_to_html(list_of_lines, line_separator)
        elif self.formatText == "json":
            return list_to_json(list_of_lines, line_separator)
        else:  # default value text
            return list_to_text(list_of_lines, line_separator)

    def list_of_dictionaries_to_response_text(self, list_of_dictionaries, with_id, with_address):
        response = ""
        if self.formatText == "xml":
            head = '<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n'
            body = ""
            tail = "</xml>"
            for dictionary in list_of_dictionaries:
                body += dictionary_to_xml(dictionary, with_id, with_address)
            return head + body + tail
        elif self.formatText == "json":
            head = '{\n"records": ['
            body = ""
            tail = "\n]}"
            first = True
            for dictionary in list_of_dictionaries:
                if first:
                    first = False
                else:
                    body += ","
                body += dictionary_to_json(dictionary, with_id, with_address)
            return head + body + tail
        else:
            for dictionary in list_of_dictionaries:
                response += dictionary_to_text(dictionary, with_id, with_address) + self.line_separator
            response = response[:-len(self.line_separator)]
        return response

    def coordintes_to_response_text(self, list_of_coordinates):
        if self.formatText == "xml":
            return coordinates_to_xml(list_of_coordinates)
        elif self.formatText == "html":
            return coordinates_to_html(list_of_coordinates)
        elif self.formatText == "htmltoonerow":
            return coordinates_to_html(list_of_coordinates, "; ")
        elif self.formatText == "json":
            return coordinates_to_json(list_of_coordinates)
        elif self.formatText == "texttoonerow":
            return coordinates_to_text(list_of_coordinates, "; ")
        else:  # default value text
            return coordinates_to_text(list_of_coordinates)

    def addresses_to_response_text(self, list_of_addresses):
        if self.formatText == "xml":
            return addresses_to_xml(list_of_addresses)
        elif self.formatText == "html" or self.formatText == "htmltoonerow":
            return addresses_to_text(list_of_addresses, "<br>")
        elif self.formatText == "json":
            return addresses_to_json(list_of_addresses)
        else:  # default value text
            return addresses_to_text(list_of_addresses)


class WebService:
    """ Webova sluzba
    """

    def __init__(
            self, path_name, caption, short_desc, html_desc="", rest_path_params=None, query_params=None,
            process_handler=None, send_button_caption=u"Odeslat", html_input_template=""):
        """ Webova sluzba """
        if query_params is None:
            query_params = []
        if rest_path_params is None:
            rest_path_params = []
        self.pathName = path_name
        self.caption = caption
        self.shortDesc = short_desc
        self.htmlDesc = html_desc
        self.restPathParams = rest_path_params
        self.query_params = query_params
        self.processHandler = process_handler
        self.sendButtonCaption = send_button_caption
        self.htmlInputTemplate = html_input_template  # Šablona elementu HTML, implicitně INPUT
        self._params = None
        pass

    def get_params(self):
        if self._params is None or len(self.restPathParams) + len(self.query_params) != len(self._params):
            self._params = {}
            self._params.update(self.restPathParams)
            self._params.update(self.query_params)

        return self._params

    params = property(get_params)  # "REST and Query params together"

    def get_service_path(self):
        result = "/REST" + self.pathName
        for param in self.restPathParams:
            result = result + "/&#60;" + param.path_name[1:] + "&#62;"
        if len(self.query_params) > 0:
            query_params_list = []
            result += "?"
            for param in self.query_params:
                query_params_list.append(param.name + "=")
            result += "&".join(query_params_list)

        return result

    def build_service_url(self, query_params):
        result = self.pathName
        for param in self.restPathParams:
            result = result + param.path_name
        if len(self.query_params) > 0:
            query_params_list = []
            result += "?"
            for param in self.query_params:
                if param.name in query_params:
                    value_str = query_params[param.name]
                else:
                    value_str = ""
                query_params_list.append(param.name + "=" + value_str)
            result += "&".join(query_params_list)

        return result

    def process_http_request(self, path, query_params):
        pass


def parameter(query_params, name, def_value=""):
    if name in query_params:
        return unquote(query_params[name])
    else:
        return def_value


def get_query_value(query_params, id_value, def_value):
    # Vrací hodnotu URL Query parametruy id, pokud neexistuje, vrací hodnotu defValue
    return get_query_param(query_params, id_value, def_value)


def get_query_param(query_params, name, def_value=""):
    if name in query_params:
        return unquote(query_params[name])
    else:
        return def_value


def number_check(possible_number):
    if possible_number is not None and str(possible_number).isdigit():
        return str(possible_number)
    else:
        return ""


def empty_string_if_no_number(possible_number):
    if possible_number is not None and str(possible_number).isdigit():
        return str(possible_number)
    else:
        return ""


def alpha_check(possible_alpha):
    if possible_alpha is not None and possible_alpha.isalpha():
        return possible_alpha
    else:
        return ""


def right_address(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
        locality_part, district_number):
    psc = zip_code.replace(" ", "")
    if house_number != "" and not house_number.isdigit():
        return False
    if orientation_number != "" and not orientation_number.isdigit():
        return False
    if record_number != "" and not record_number.isdigit():
        return False
    if orientation_number_character != "" and not orientation_number_character.isalpha():
        return False
    if psc != "" and not psc.isdigit():
        return False
    if district_number != "" and not district_number.isdigit():
        return False
    if street == "" and house_number == "" and record_number == "" and orientation_number == "" and orientation_number_character == "" and psc == "" and locality == "" and locality_part == "" and district_number == "":
        return False
    return True


def format_zip_code(code):
    if code is None:
        return ""
    else:
        code = str(code)
        code = code.replace(" ", "")
        if code.isdigit():
            return code
        else:
            return ""


def compile_address_as_json(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id=""):
    (street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
     locality_part, district_number, ruian_id) = none_to_string(
        (street, house_number, record_number, orientation_number,
         orientation_number_character, zip_code, locality, locality_part,
         district_number, ruian_id))
    if house_number != "":
        sign = u"č.p."
        address_number = house_number
    else:
        sign = u"č.ev."
        address_number = record_number

    if orientation_number != "":
        house_number_str = '\t"' + sign + '": ' + address_number + ',\n\t"orientační_číslo": ' + orientation_number + orientation_number_character + ','
    else:
        house_number_str = '\t"' + sign + '":"%s", ' % address_number

    if street != "":
        street = '\t"ulice": "%s",\n' % street

    if district_number != "":
        district_number_str = ',\n\t"číslo_městského_obvodu": %s,\n ' % district_number
    else:
        district_number_str = ""

    if locality == locality_part or locality_part == "":
        town_district = '\t"obec":"%s"%s' % (locality, district_number_str)
    else:
        town_district = '\t"obec": "%s"%s\t"část_obce": "%s" ' % (locality, district_number_str, locality_part)

    if ruian_id != "":
        ruian_id_text = '\t"ruian_id": %s,\n' % ruian_id
    else:
        ruian_id_text = ""

    result = ruian_id_text + street + house_number_str + '\n\t"PSČ": "%s",\n%s\n' % (zip_code, town_district)
    return result


def compile_address_as_xml(
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, ruian_id=""):
    (
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
        locality_part, district_number, ruian_id) = none_to_string(
        (street, house_number, record_number, orientation_number,
         orientation_number_character, zip_code, locality, locality_part,
         district_number, ruian_id))
    if house_number != "":
        sign = "c.p."
        address_number = house_number
    else:
        sign = "c.ev."
        address_number = record_number

    if orientation_number != "":
        house_number_str = '\t<' + sign + '>' + address_number + '</' + sign + '>\n\t<orientacni_cislo>' + orientation_number + orientation_number_character + '</orientacni_cislo>'
    else:
        house_number_str = '\t<' + sign + '>' + address_number + '</' + sign + '>'

    if street != "":
        street = '\t<ulice>' + street + "</ulice>\n"

    if district_number != "":
        district_number_str = '\n\t<cislo_mestskeho_obvodu>' + district_number + '</cislo_mestskeho_obvodu>'
    else:
        district_number_str = ""

    if locality == locality_part or locality_part == "":
        town_district = '\t<obec>' + locality + "</obec>" + district_number_str
    else:
        town_district = '\t<obec>' + locality + '</obec>' + district_number_str + '\n\t<cast_obce>' + locality_part + '</cast_obce>'

    if ruian_id != "":
        ruian_id_str = "\t<ruian_id>%s</ruian_id>\n" % ruian_id
    else:
        ruian_id_str = ""

    result = street + house_number_str + '\n\t<PSC>' + zip_code + "</PSC>\n" + town_district + "\n" + ruian_id_str
    return result


def compile_address_to_one_row(
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, ruian_id=""):
    address_list = compile_address_as_text(
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, ruian_id)
    separator = ', '
    address_str = separator.join(address_list)
    return address_str


def str_is_not_empty(v):
    return v is not None and v != ""


def compile_address_as_text(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, ruian_id=""):
    """
    Sestaví adresu dle hodnot v parametrech, prázdný parametr je "" nebo None.

    @param: street : String                     Jméno ulice
    @param: house_number : String                Číslo popisné
    @param: record_number : String               Číslo evidenční
    @param: orientation_number : String          Číslo orientační
    @param: orientation_number_character : String Písmeno čísla orientačního
    @param: zip_code : object String             Poštovní směrovací číslo
    @param: locality : object String            Obec
    @param: locality_part : String Street        Část obce
    @param: district_number : String             Číslo městského obvodu v Praze
    """
    lines = []  # Result list, initiated for case of error

    try:
        # Convert None values to "".
        (street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
         locality_part, district_number, ruian_id) = none_to_string(
            (street, house_number, record_number, orientation_number,
             orientation_number_character, zip_code, locality,
             locality_part, district_number, ruian_id))

        zip_code = format_zip_code(zip_code)
        house_number = number_check(house_number)
        orientation_number = number_check(orientation_number)
        district_number = number_check(district_number)
        orientation_number_character = alpha_check(orientation_number_character)
        town_info = zip_code + " " + locality
        if district_number != "":
            town_info += " " + district_number
        if house_number != "":
            house_number_str = " " + house_number
            if orientation_number != "":
                house_number_str += u"/" + orientation_number + orientation_number_character
        elif record_number != "":
            house_number_str = u" č.ev. " + record_number
        else:
            house_number_str = ""

        if locality.upper() == "PRAHA":
            if street != "":
                lines.append(street + house_number_str)
                lines.append(locality_part)
                lines.append(town_info)
            else:
                lines.append(locality_part + house_number_str)
                lines.append(town_info)
        else:
            if street != "":
                lines.append(street + house_number_str)
                if locality_part != locality:
                    lines.append(locality_part)
                lines.append(town_info)
            else:
                if locality_part != locality:
                    lines.append(locality_part + house_number_str)
                else:
                    if house_number != "":
                        lines.append(u"č.p." + house_number_str)
                    else:
                        lines.append(house_number_str[1:])
                lines.append(town_info)

        if ruian_id != "":
            lines.insert(0, str(ruian_id))
    except ValueError:
        pass

    return lines


def value_to_str(value):
    if value is None:
        return ""
    else:
        return str(value)


def number_to_string(number):
    return value_to_str(number)


def extract_dictrict_number(nazev_mop):
    # Extracts district number for Prague: Praha 10 -> 10
    if (nazev_mop is not None) and (nazev_mop != "") and (nazev_mop.find(" ") >= 0):
        return nazev_mop.split(" ")[1]
    else:
        return ""


def analyse_row(typ_so, cislo_domovni):
    # Analyses typ_so value and sets either house_number or record_number to cislo_domovni.
    house_number = cislo_domovni
    record_number = 0
    try:
        if typ_so[-3:] == ".p.":
            house_number = number_to_string(cislo_domovni)
            record_number = ""
        elif typ_so[-3:] == "ev.":
            house_number = ""
            record_number = number_to_string(cislo_domovni)
        else:
            pass
    finally:
        return house_number, record_number


def item_to_str(item):
    # This function return str representation of item and if item is empty then empty string.
    if item is None:
        return ""
    else:
        return str(item)


if __name__ == "__main__":
    print("This is module file, it can not be run!")
