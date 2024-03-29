# -*- coding: utf-8 -*-
from swagger_server.models import PointJtsk, PointWgs, PolygonJtsk, PolygonWgs


def list_to_xml(list_of_lines, line_separator="\n", tag="FormattedOutput"):
    result = '<?xml version="1.0" encoding="UTF-8"?>' + line_separator + "<xml>" + line_separator
    for line in list_of_lines:
        result += "<" + tag + ">" + line_separator + line + "</" + tag + ">" + line_separator
    return result + "</xml>"


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


def coordinates_to_html(list_of_coordinates, line_separator="<br>"):
    result = ""
    for line in list_of_coordinates:
        if result != "":
            result += line_separator
        result += line.JTSKY + ", " + line.JTSKX
    return result


def addresses_to_xxx(list_of_addresses, line_separator="\n"):
    result = ""
    for line in list_of_addresses:
        print(str(line) + line_separator)
    return result


def coordinates_to_text(list_of_coordinates, line_separator="\n"):
    result = ""
    for line in list_of_coordinates:
        result += line.x + ", " + line.y + line_separator
    return result[:-1]


def coordinates_to_json(list_of_coordinates, line_separator="\n", tag="Coordinates"):
    result = "{"
    index = 0
    for line in list_of_coordinates:
        index += 1
        if index > 1:
            result += ','
        result += line_separator + '"' + tag + str(index) + (
                '" : {' + line_separator + ' \t"Y": "' + line.y + '",') + (
                          line_separator + '\t"X": "' + line.x + '"' + line_separator + "\t}")
    result += line_separator + "}"
    return result


class TextFormat:
    plain_text = 0
    xml = 1
    json = 2
    html = 3


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


def number_check(possible_number):
    if possible_number is not None and str(possible_number).isdigit():
        return str(possible_number)
    else:
        return ""


def is_int(value):
    if value is None:
        return False
    if value == "":
        return False
    else:
        for i in range(len(value)):
            if "0123456789".find(value[i:i + 1]) < 0:
                return False
        return True


def _check_polygon(polygon_str: str):
    # Je tesxtový polygon správně formátován?
    if polygon_str is None:
        return False
    polygon_str = polygon_str.upper()
    if not polygon_str.startswith('POLYGON(('):
        return False
    if not polygon_str.endswith('))'):
        return False
    return True


def _parse_polygon_to_list(polygon_str: str):
    # parsuje textový polygon do seznamu dvojic souřadnic
    if not _check_polygon(polygon_str):
        return None
    data_str = polygon_str[9:len(polygon_str) - 2]
    return data_str.split(',')


def parse_polygon_string_to_dictionary(polygon_str: str, geom='jtsk'):
    # parsuje textový polygon do dictionary
    data_str_list = _parse_polygon_to_list(polygon_str=polygon_str)
    if data_str_list is None:
        return None
    out = []
    if geom == 'jtsk':
        for point_str in data_str_list:
            p = point_str.split(' ')
            point = {
                'x': float(p[0]),
                'y': float(p[1]),
            }
            out.append(point)
    elif geom == 'wgs':
        for point_str in data_str_list:
            p = point_str.split(' ')
            point = {
                'lon': float(p[0]),
                'lat': float(p[1]),
            }
            out.append(point)
    else:
        out = None
    return out


def parse_polygon_string_to_dictionary_jtsk(polygon_str: str):
    # parsuje textový polygon do dictionary (JTSK)
    return parse_polygon_string_to_dictionary(polygon_str=polygon_str, geom='jtsk')


def parse_polygon_string_to_dictionary_wgs(polygon_str: str):
    # parsuje textový polygon do dictionary (WGS-84)
    return parse_polygon_string_to_dictionary(polygon_str=polygon_str, geom='wgs')


def load_polygon(polygon_str: str, geom='jtsk'):
    # natáhne textový polygon do objektu PolygonXXX
    p = parse_polygon_string_to_dictionary_jtsk(polygon_str)
    if geom == 'jtsk':
        out = PolygonJtsk()
        if p is not None:
            polygon = []
            for point in p:
                polygon.append(PointJtsk(x=point['x'], y=point['y']))
            out._polygon = polygon
        else:
            out._polygon = None
    elif geom == 'wgs':
        out = PolygonWgs()
        if p is not None:
            polygon = []
            for point in p:
                polygon.append(PointWgs(lat=point['lat'], lon=point['lon']))
            out._polygon = polygon
        else:
            out._polygon = None
    else:
        out = None
    return out


def load_polygon_jtsk(polygon_str: str):
    # natáhne textový polygon do objektu PolygonJtsk
    return load_polygon(polygon_str=polygon_str, geom='jtsk')


def load_polygon_wgs(polygon_str: str):
    # natáhne textový polygon do objektu PolygonWgs
    return load_polygon(polygon_str=polygon_str, geom='wgs')


def get_polygon_string(polygon, geom='jtsk'):
    out = ''
    if geom != 'jtsk' and geom != 'wgs':
        return out
    if polygon is not None:
        work = []
        for point in polygon.polygon:
            if geom == 'jtsk':
                work.append(str(point.x) + ' ' + str(point.y))
            else:
                work.append(str(point.lon) + ' ' + str(point.lat))
        data_str = ','.join(work)
        out = 'POLYGON(({0}))'.format(data_str)
    return out


def get_polygon_string_jtsk(polygon: PolygonJtsk):
    return get_polygon_string(polygon=polygon, geom='jtsk')


def get_polygon_string_wgs(polygon: PolygonWgs):
    return get_polygon_string(polygon=polygon, geom='wgs')


def get_polygon_object(polygon_str: str, geom='jtsk'):
    # Totéž, co load_polygon
    return load_polygon(polygon_str=polygon_str, geom=geom)
