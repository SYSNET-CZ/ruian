# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         query
# Purpose:      Querying the database
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------
# from collections import defaultdict
from collections import defaultdict
from typing import List, Any
# from urllib.parse import unquote
from urllib.parse import unquote

import psycopg2
from lat_lon_parser import parser

from swagger_server.service.common import compile_address_as_json, compile_address_as_text, compile_address_as_xml, \
    compile_address_to_one_row, number_to_string, analyse_row, right_address, TEXT_FORMAT_TEXT, TEXT_FORMAT_JSON, \
    TEXT_FORMAT_XML, TEXT_FORMAT_TEXT2ONEROW, TEXT_FORMAT_HTML2ONEROW, list_to_response_text, \
    list_of_dictionaries_to_response_text, compile_address_as_obj
from swagger_server.service.database import execute_sql, number_value, \
    PostGisDatabase, format_to_query, DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, commit_sql, \
    get_ruian_version, DATABASE_NAME_POVODI, get_row, get_cast_obce_by_name, get_ulice_by_name, get_obec_by_name, \
    TOWNNAME_FIELDNAME, STREETNAME_FIELDNAME, GIDS_FIELDNAME, GID_FIELDNAME, CISLO_DOMOVNI_FIELDNAME, \
    ZIP_CODE_FIELDNAME, CISLO_ORIENTACNI_FIELDNAME, ZNAK_CISLA_ORIENTACNIHO_FIELDNAME, TOWNPART_FIELDNAME, \
    TYP_SO_FIELDNAME, get_result, MOP_NAME, \
    ADMINISTRATIVE_DIVISION_TABLE_NAME, ADDRESSPOINTS_TABLE_NAME, ADMINISTRATIVE_DIVISION_ZSJ_TABLE_NAME, \
    ADMINISTRATIVE_DIVISION_KU_TABLE_NAME, ZVM50KLAD_TABLENAME, DATABASE_NAME_MAPY, FULLTEXT_EXTENDED_TABLENAME
from swagger_server.service.models import AddressInternal, PovodiInternal, Coordinates, CoordinatesGps, ParcelaInternal, AdresniBodInteral, ZsjInternal, \
    Locality, \
    none_to_string, KatastralniUzemiInternal, MapovyList50Internal
from swagger_server.service.utils import is_int, number_check

__author__ = 'SYSNET'

exact_match_needed = False

# Konstanty pro logickou strukturu databáze
MAX_TEXT_COUNT = 3  # maximální počet textových položek v adrese ulice, obec, část obce = 3
ORIENTATION_NUMBER_ID = "/"
RECORD_NUMBER_ID = "č.ev."
DESCRIPTION_NUMBER_ID = "č.p."
RECORD_NUMBER_MAX_LEN = 4
ORIENTATION_NUMBER_MAX_LEN = 3
DESCRIPTION_NUMBER_MAX_LEN = 3
HOUSE_NUMBER_MAX_LEN = 4
ZIPCODE_LEN = 5

# URL parameters
URL_PARAM_ADDRESS_PLACE_ID = "AddressPlaceId"
URL_PARAM_RESULT_FORMAT = "Format"
URL_PARAM_WITH_ID = "id"
URL_PARAM_WITH_ADDRESS = "address"
URL_PARAM_EXTRA_INFORMATION = "ExtraInformation"
URL_PARAM_SEARCH_TEXT = "SearchText"
URL_PARAM_STREET = "Street"
URL_PARAM_HOUSE_NUMBER = "HouseNumber"
URL_PARAM_RECORD_NUMBER = "RecordNumber"
URL_PARAM_ORIENTATION_NUMBER = "OrientationNumber"
URL_PARAM_ORIENTATION_NUMBER_CHARACTER = "OrientationNumberCharacter"
URL_PARAM_ZIP_CODE = "ZIPCode"
URL_PARAM_LOCALITY = "Locality"
URL_PARAM_LOCALITY_PART = "LocalityPart"
URL_PARAM_DISTRICR_NUMBER = "DistrictNumber"
URL_PARAM_DISTRICR_NAME = "DistrictNamer"

# Address dictionary
ADDR_X = "x"
ADDR_Y = "y"
ADDR_ID = "id"
ADDR_LOCALITY = "locality"
ADDR_LOCALITY_PART = "locality_part"
ADDR_STREET = "street"
ADDR_HOUSE_NUMBER = "house_number"
ADDR_RECORD_NUMBER = "record_number"
ADDR_ORIENTATION_NUMBER = "orientation_number"
ADDR_ORIENTATION_NUMBER_CHARACTER = "orientation_number_character"
ADDR_ZIP_CODE = "zip_code"
ADDR_DISTRICT_NUMBER = "district_number"
ADDR_DISTRICT = "district"

ITEM_TO_FIELD = {
    "id": "gid",
    "street": "nazev_ulice",
    "house_number": "cislo_domovni",
    "record_number": "cislo_domovni",
    "orientation_number": "cislo_orientacni",
    "orientation_number_character": "znak_cisla_orientacniho",
    "zip_code": "psc",
    "locality": "nazev_obce",
    "locality_part": "nazev_casti_obce",
    "district_number": "nazev_mop",
    "district_name": "nazev_mop",
    "x": "latitude",
    "y": "longitude"
}

ADDRESSPOINTS_COLUMNS_FIND = \
    "nazev_ulice, cislo_domovni, typ_so, cislo_orientacni, znak_cisla_orientacniho, psc, " \
    "nazev_obce, nazev_casti_obce, nazev_mop "
ADDRESSPOINTS_COLUMNS_NEARBY = \
    "gid, nazev_obce, nazev_casti_obce, nazev_ulice, typ_so, cislo_domovni, " \
    "cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop"
ADDRESSPOINTS_COLUMNS_VALIDATE = \
    "gid, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, " \
    "nazev_casti_obce, nazev_mop, nazev_ulice, typ_so"
ADDRESSPOINTS_COLUMNS_FIND_COORD = \
    "latitude, longitude, gid, nazev_obce, nazev_casti_obce, nazev_ulice, " \
    "cislo_domovni, typ_so, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop"
ADDRESSPOINTS_COLUMNS_GET_LIST = \
    "gid, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, typ_so, " \
    "'kod_ulice', kod_casti_obce, 'momckod', nazev_casti_obce, kod_obce, nazev_obce, " \
    "nazev_ulice, nazev_momc, 'mopkod', nazev_mop"

ROZVODNICE_COLUMNS_GET = "*"
ROZVODNICE_COLUMNS_GET_LIST = \
    "rozvodnice_4.fid, rozvodnice_4.chp, rozvodnice_4.chp_u, rozvodnice_4.chp_d, " \
    "rozvodnice_4.naz_tok, rozvodnice_4.naz_tok_2, rozvodnice_3.fid, rozvodnice_3.naz_pov, " \
    "rozvodnice_2.fid, rozvodnice_2.naz_pov, rozvodnice_1.fid, rozvodnice_1.naz_pov"
ROZVODNICE_TABLE_NAME = "rozvodnice_4"
PARCELY_COLUMNS_GET_LIST = \
    "parcely.id, parcely.kmenovecislo, parcely.pododdelenicisla, parcely.vymeraparcely, " \
    "parcely.katastralniuzemikod, katastralniuzemi.nazev, katastralniuzemi.obeckod, " \
    "obce.nazev, obce.statuskod, obce.okreskod, obce.poukod, " \
    "okresy.nazev, okresy.krajkod, okresy.vusckod, pou.nazev, pou.orpkod, " \
    "kraje.nazev, kraje.statkod, vusc.nazev, vusc.regionsoudrznostikod, vusc.nutslau, " \
    "orp.nazev, staty.nazev, staty.nutslau, " \
    "regionysoudrznosti.nazev, regionysoudrznosti.nutslau "
ADRESY_COLUMNS_GET_LIST = \
    "adresnimista.kod, adresnimista.cislodomovni, adresnimista.cisloorientacni, " \
    "adresnimista.cisloorientacnipismeno, adresnimista.psc, adresnimista.stavebniobjektkod, " \
    "adresnimista.ulicekod, stavebniobjekty.castobcekod, stavebniobjekty.momckod, " \
    "castiobci.nazev, castiobci.obeckod, obce.nazev, ulice.nazev, momc.nazev, " \
    "momc.mopkod, mop.nazev "

MAX_COUNT = 10
DISTANCE_GET_ADRESA = 500
DISTANCE_GET_NEARBY = 2000


def _convert_point_to_wgs(y, x):
    x = abs(x)
    y = abs(y)
    geom = "ST_GeomFromText('POINT(-%s -%s)',5514)" % (str(x), str(y))
    # sql = "SELECT ST_AsText(ST_Transform(" + geom + ", 4326)) AS wgs_geom;"
    sql = "SELECT ST_Transform(" + geom + ", 4326) AS wgs_geom;"
    cur = execute_sql(DATABASE_NAME_POVODI, sql)
    row = cur.fetchone()
    cur.close()
    if row is None:
        return None
    out = CoordinatesGps(lon=row[0].coords[0], lat=row[0].coords[1])
    return out


def _convert_str_wgs_to_jtsk(str_coord):
    if str_coord is None:
        return None
    c = str_coord.split(',')
    if len(c) != 2:
        return None
    lat = parser.parse(c[0])
    lon = parser.parse(c[1])
    if ('W' in c[0]) or ('E' in c[0]):
        lat = parser.parse(c[1])
        lon = parser.parse(c[0])
    return _convert_point_to_jtsk(lat=lat, lon=lon)


def _convert_point_to_jtsk(lat, lon):
    geom = "ST_GeomFromText('POINT({0} {1})',4326)".format(str(lon), str(lat))
    sql = "SELECT ST_Transform(" + geom + ", 5514) AS jtsk_geom;"
    cur = execute_sql(DATABASE_NAME_POVODI, sql)
    row = cur.fetchone()
    cur.close()
    if row is None:
        return None
    out = Coordinates(x=row[0].coords[0], y=row[0].coords[1])
    return out


def _convert_coord_to_wgs(coord: Coordinates):
    point = _convert_point_to_wgs(coord.y, coord.x)
    if point is not None:
        out = CoordinatesGps(lat=point.lat, lon=point.lon)
        return out
    return None


def _convert_coord_to_jtsk(coord: CoordinatesGps):
    point = _convert_point_to_jtsk(coord.lat, coord.lon)
    if point is not None:
        out = Coordinates(point.y, point.x)
        return out
    return None


def _get_adresa(y, x):
    x = abs(x)
    y = abs(y)
    geom = "address_points.geom,ST_GeomFromText('POINT(-{0} -{1})',5514)".format(str(x), str(y))
    dist = "ST_Distance({0}) {1}".format(geom, 'd1')
    within = "ST_DWithin({0},{1}) ".format(geom, str(DISTANCE_GET_ADRESA))
    sql = "SELECT {0}, {1} FROM {2} WHERE {3} ORDER BY {4} LIMIT 1;".format(
        ADDRESSPOINTS_COLUMNS_GET_LIST, dist, 'address_points', within, 'd1')
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    row = cur.fetchone()
    cur.close()
    if row is None:
        return None
    out: AdresniBodInteral = AdresniBodInteral(row)
    return out


def _get_adresa_sav(y, x):
    x = abs(x)
    y = abs(y)
    geom = "adresnimista.adresnibod,ST_GeomFromText('POINT(-%s -%s)',5514)" % (str(x), str(y))
    dist = "ST_Distance(%s) d1," % geom
    within = "ST_DWithin(" + geom + ",%s) " % str(DISTANCE_GET_ADRESA)
    sql = "SELECT " + dist + ADRESY_COLUMNS_GET_LIST + \
          "FROM adresnimista  " \
          "LEFT OUTER JOIN stavebniobjekty ON (adresnimista.stavebniobjektkod=stavebniobjekty.kod) " \
          "LEFT OUTER JOIN castiobci ON (stavebniobjekty.castobcekod=castiobci.kod) " \
          "LEFT OUTER JOIN obce ON (castiobci.obeckod=obce.kod) " \
          "LEFT OUTER JOIN ulice ON (adresnimista.ulicekod=ulice.kod) " \
          "LEFT OUTER JOIN momc ON (stavebniobjekty.momckod=momc.kod) " \
          "LEFT OUTER JOIN mop ON (momc.mopkod=mop.kod) " \
          "WHERE " + within + \
          "ORDER BY d1 " \
          "LIMIT 1;"
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    row = cur.fetchone()
    cur.close()
    if row is None:
        return None
    out: AdresniBodInteral = AdresniBodInteral(row)
    return out


def geom_point(column_name, x, y):
    geom = column_name + ",ST_GeomFromText('POINT(-{0} -{1})',5514)".format(str(abs(x)), str(abs(y)))
    return geom


def _get_map_sheet_50(y, x):
    geom = geom_point("geom", x, y)
    sql = "SELECT * FROM {0} WHERE {1}({2});".format(ZVM50KLAD_TABLENAME, 'ST_Contains', geom)
    row = get_row(DATABASE_NAME_MAPY, sql)
    if row is None:
        return None
    out: MapovyList50Internal = MapovyList50Internal(row)
    return out


def _get_administrative_division_parcela(y, x):
    print(y, x)
    geom = geom_point("geom_polygon", x, y)
    sql = "SELECT * FROM {0} WHERE {1}({2});".format(ADMINISTRATIVE_DIVISION_TABLE_NAME, 'ST_Contains', geom)
    row = get_row(DATABASE_NAME_RUIAN, sql)
    if row is None:
        return None
    out: ParcelaInternal = ParcelaInternal(row)
    return out


def _get_administrative_division_zsj(y, x):
    geom = geom_point("geom_polygon", x, y)
    sql = "SELECT * FROM " + ADMINISTRATIVE_DIVISION_ZSJ_TABLE_NAME + " WHERE ST_Contains(%s);" % geom
    row = get_row(DATABASE_NAME_RUIAN, sql)
    if row is None:
        return None
    out: ZsjInternal = ZsjInternal(row)
    return out


def _get_administrative_division_ku(y, x):
    geom = geom_point("geom_polygon", x, y)
    sql = "SELECT * FROM " + ADMINISTRATIVE_DIVISION_KU_TABLE_NAME + " WHERE ST_Contains(%s);" % geom
    row = get_row(DATABASE_NAME_RUIAN, sql)
    if row is None:
        return None
    out: KatastralniUzemiInternal = KatastralniUzemiInternal(row)
    return out


def _get_parcela(y, x):
    # HOTOVO
    geom = geom_point("parcely.originalnihranice", x, y)
    sql = "SELECT " + PARCELY_COLUMNS_GET_LIST + \
          "FROM parcely " \
          "LEFT OUTER JOIN katastralniuzemi ON (parcely.katastralniuzemikod=katastralniuzemi.kod) " \
          "LEFT OUTER JOIN obce ON (katastralniuzemi.obeckod=obce.kod) " \
          "LEFT OUTER JOIN okresy ON (obce.okreskod=okresy.kod) " \
          "LEFT OUTER JOIN pou ON (obce.poukod=pou.kod) " \
          "LEFT OUTER JOIN kraje ON (okresy.krajkod=kraje.kod) " \
          "LEFT OUTER JOIN vusc ON (okresy.vusckod=vusc.kod) " \
          "LEFT OUTER JOIN orp ON (pou.orpkod=orp.kod) " \
          "LEFT OUTER JOIN staty ON (kraje.statkod=staty.kod) " \
          "LEFT OUTER JOIN regionysoudrznosti ON (vusc.regionsoudrznostikod=regionysoudrznosti.kod) " \
          "WHERE ST_Contains(%s);" \
          % geom
    row = get_row(DATABASE_NAME_RUIAN, sql)
    if row is None:
        return None
    out: ParcelaInternal = ParcelaInternal(row)
    return out


def _get_rozvodnice(y, x):
    # HOTOVO
    x = abs(x)
    y = abs(y)
    geom = "rozvodnice_4.geom,ST_GeomFromText('POINT(-%s -%s)',5514)" % (str(x), str(y))
    sql = "SELECT " + ROZVODNICE_COLUMNS_GET_LIST + \
          " " + "FROM rozvodnice_4 " \
                "LEFT OUTER JOIN rozvodnice_3 ON (SUBSTRING(rozvodnice_4.chp, 1, 7)=rozvodnice_3.chp_3r) " \
                "LEFT OUTER JOIN rozvodnice_2 ON (SUBSTRING(rozvodnice_4.chp, 1, 4)=rozvodnice_2.chp_2r) " \
                "LEFT OUTER JOIN rozvodnice_1 ON (SUBSTRING(rozvodnice_4.chp, 1, 1)=rozvodnice_1.chp_1r) " \
                "WHERE ST_Contains(%s);" \
          % geom
    cur = execute_sql(DATABASE_NAME_POVODI, sql)
    row = cur.fetchone()
    cur.close()
    if row is None:
        return None
    out: PovodiInternal = PovodiInternal(row)
    # jtsk = Coordinates(y, x)
    # wgs = _convert_coord_to_wgs(jtsk)
    # out.jtsk = jtsk
    # out.wgs = wgs
    return out


def _get_rozvodnice_wgs(lat, lon):
    # TODO: NEFUNGUJE
    c0 = CoordinatesGps(lat, lon)
    c1: Coordinates = _convert_coord_to_jtsk(c0)
    out = _get_rozvodnice(-c1.y, -c1.x)
    return out


def _find_address(identifier):
    sql = "SELECT " + ADDRESSPOINTS_COLUMNS_FIND + \
          " FROM " + ADDRESSPOINTS_TABLE_NAME + \
          " WHERE gid = " + str(identifier)
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    row = cur.fetchone()
    if row:
        (house_number, record_number) = analyse_row(row[2], number_to_string(row[1]))
        a = number_value(none_to_string(row[8]))
        address = AddressInternal(
            none_to_string(row[0]), house_number, record_number, number_to_string(row[3]), none_to_string(row[4]),
            number_to_string(row[5]), none_to_string(row[6]), none_to_string(row[7]),
            a, none_to_string(row[8]), identifier
        )
        return address
    else:
        return None


def _get_nearby_addresses(y, x, distance=DISTANCE_GET_NEARBY, max_count=MAX_COUNT):
    rows = _get_nearby_localities(y=y, x=x, distance=distance, max_count=max_count)
    if rows is None:
        return None
    addres_list = []
    i = 0
    for row in rows:
        address_point = AdresniBodInteral(row)
        address = address_point.to_address
        i += 1
        item = {
            "order": i,
            "distance": row[16],
            "address": address
        }
        addres_list.append(item)
    return addres_list


"""
"0-gid, 1-nazev_obce, 2-nazev_casti_obce, 3-nazev_ulice, 4-typ_so, 5-cislo_domovni, 6-"cislo_orientacni, 7-znak_cisla_orientacniho, 8-psc, 9-nazev_mop", 10-d1
       self.street = street
        self.house_number = house_number
        self.record_number = record_number
        self.orientation_number = orientation_number
        self.orientation_number_character = orientation_number_character
        self.zip_code = zip_code
        self.locality = locality
        self.locality_part = locality_part
        self.district_number = district_number
        self.district = district
        self.ruian_id = ruian_id
"""


def _get_nearby_localities(y, x, distance, max_count=MAX_COUNT):
    x = abs(x)
    y = abs(y)
    max_count = int(max_count)
    if max_count > 10000:
        max_count = 10000
    column_distance = 'd1'
    geom = "{0},ST_GeomFromText('POINT(-{1} -{2})',5514)".format('geom', str(x), str(y))
    dist = 'ST_Distance({0})'.format(geom, column_distance)
    within = 'ST_DWithin({0},{1})'.format(geom, str(distance))
    sql = "SELECT {0}, {1} {4} FROM {2} WHERE {3} ORDER BY {4} LIMIT {5};".format(
        ADDRESSPOINTS_COLUMNS_GET_LIST, dist, ADDRESSPOINTS_TABLE_NAME, within, column_distance, str(max_count))
    # print(sql)
    rows = get_result(DATABASE_NAME_RUIAN, sql)
    return rows


def _validate_address(dictionary, return_row=False):
    print("DICTIONARY: ", dictionary)
    first = True
    one_house_number = False
    db = PostGisDatabase(DATABASE_NAME_RUIAN)
    cur = db.get_cursor()

    sql = "SELECT " + ADDRESSPOINTS_COLUMNS_VALIDATE + " FROM " + ADDRESSPOINTS_TABLE_NAME + " WHERE "
    work_tuple = ()
    for key in dictionary:
        if key == "house_number":
            if dictionary[key] != "":
                if one_house_number:
                    return ["False"]
                else:
                    one_house_number = True
                sql += add_to_query("typ_so", "=", first)
                first = False
                work_tuple = work_tuple + (u"č.p.",)
            else:
                continue
        if key == "record_number":
            if dictionary[key] != "":
                if one_house_number:
                    return ["False"]
                else:
                    one_house_number = True
                sql += add_to_query("typ_so", "=", first)
                first = False
                work_tuple = work_tuple + (u"č.ev.",)
            else:
                continue

        if key == "district_number" and dictionary[key] != "":
            value = format_to_query(dictionary["locality"] + " " + dictionary["district_number"])
        else:
            value = format_to_query(dictionary[key])

        if value is None:
            comparator = "is"
        else:
            comparator = "="
        if key != "district_name" and dictionary[key] != '':
            work_tuple = work_tuple + (value,)
            sql += add_to_query(ITEM_TO_FIELD[key], comparator, first)
        first = False

    a = cur.mogrify(sql, work_tuple)
    print("SQL: ", a)
    cur.execute(a)
    row = cur.fetchone()
    cur.close()

    result = None
    if return_row:
        if row:
            result = row
    else:
        if row:
            result = ["True"]
        else:
            result = ["False"]
    return result


def _find_coordinates(identifier):
    sql = "SELECT {0} FROM {1} WHERE {2} = {3}".format(
        ADDRESSPOINTS_COLUMNS_FIND_COORD, ADDRESSPOINTS_TABLE_NAME, 'gid', str(identifier))
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    row = cur.fetchone()
    if row and row[0] is not None and row[1] is not None:
        (house_number, record_number) = analyse_row(row[7], number_to_string(row[6]))
        c = (
            str("{:10.2f}".format(row[1])).strip(), str("{:10.2f}".format(row[0])).strip(),
            row[2], row[3], none_to_string(row[4]), none_to_string(row[5]),
            house_number, record_number, number_to_string(row[8]), none_to_string(row[9]),
            number_to_string(row[10]), number_value(none_to_string(row[11]))
        )
        return [c]
    else:
        return []
    # latitude, longitude,
    # gid, nazev_obce, nazev_casti_obce, nazev_ulice,
    # cislo_domovni, typ_so, cislo_orientacni,
    # znak_cisla_orientacniho, psc, nazev_mop


def _find_locality(identifier, details=True):  # identifikator adresniho bodu
    work = _find_coordinates(identifier)
    if not work:
        return None
    row = work[0]
    coord = Coordinates(float(row[0]), float(row[1]))
    coord_gps = _convert_coord_to_wgs(coord=coord)
    addr = AddressInternal(row[5], row[6], row[7], row[8], row[9], row[10], row[3], row[4], None, row[11], row[2])
    zsj = None
    if details:
        zsj = _get_administrative_division_zsj(y=coord.y, x=coord.x)
    locality = Locality(address=addr, coordinates=coord, coordinates_gps=coord_gps, zsj=zsj)
    return locality


def geocode_id(address_id):
    locality = _find_locality(address_id)
    return locality


def geocode_address(street, house_number, record_number, orientation_number, orientation_number_character,
                    zip_code, locality, locality_part, district_number, district_name):
    # Všechny položky se zadávají jako text!!!
    if right_address(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number, district_name):
        dictionary = {
            ADDR_STREET: street,
            ADDR_HOUSE_NUMBER: house_number,
            ADDR_RECORD_NUMBER: record_number,
            ADDR_ORIENTATION_NUMBER: orientation_number,
            ADDR_ORIENTATION_NUMBER_CHARACTER: orientation_number_character,
            ADDR_ZIP_CODE: zip_code,
            ADDR_LOCALITY: locality,
            ADDR_LOCALITY_PART: locality_part,
            ADDR_DISTRICT_NUMBER: district_number,
            ADDR_DISTRICT: district_name,
        }
        coordinates = _find_coordinates_by_address(dictionary)
        return coordinates
    else:
        return []


def coordinates0_to_dictionary(coordinates):
    return coordinates_to_dictionary(coordinates[0])


def coordinates_to_dictionary(coordinates):
    temp = coordinates
    dictionary = {
        ADDR_X: temp[0], ADDR_Y: temp[1], ADDR_ID: str(temp[2]), ADDR_LOCALITY: temp[3], ADDR_LOCALITY_PART: temp[4],
        ADDR_STREET: temp[5], ADDR_HOUSE_NUMBER: temp[6], ADDR_RECORD_NUMBER: temp[7], ADDR_ORIENTATION_NUMBER: temp[8],
        ADDR_ORIENTATION_NUMBER_CHARACTER: temp[9], ADDR_ZIP_CODE: temp[10],
        ADDR_DISTRICT_NUMBER: temp[11], ADDR_DISTRICT: temp[11]
    }
    return dictionary


def dictionary_to_locality(dictionary):
    locality = None
    if dictionary:
        coordinates = None
        if dictionary[ADDR_X] and dictionary[ADDR_Y]:
            coordinates = Coordinates(dictionary[ADDR_Y], dictionary[ADDR_X])
        address = AddressInternal(
            dictionary[ADDR_STREET], dictionary[ADDR_HOUSE_NUMBER], dictionary[ADDR_RECORD_NUMBER],
            dictionary[ADDR_ORIENTATION_NUMBER], dictionary[ADDR_ORIENTATION_NUMBER_CHARACTER],
            dictionary[ADDR_ZIP_CODE], dictionary[ADDR_LOCALITY], dictionary[ADDR_LOCALITY_PART],
            dictionary[ADDR_DISTRICT_NUMBER], dictionary[ADDR_DISTRICT], dictionary[ADDR_ID]
        )
        locality = Locality(address, coordinates)
    return locality


def geocode_address_service_handler(query_params):
    def p(name, def_value=""):
        if name in query_params:
            return unquote(query_params[name])
        else:
            return def_value

    result_format = p(URL_PARAM_RESULT_FORMAT, "text")
    with_id = p(URL_PARAM_EXTRA_INFORMATION) == "id"
    with_address = p(URL_PARAM_EXTRA_INFORMATION) == "address"

    if URL_PARAM_ADDRESS_PLACE_ID in query_params:
        query_params[URL_PARAM_ADDRESS_PLACE_ID] = number_check(query_params[URL_PARAM_ADDRESS_PLACE_ID])
        if query_params[URL_PARAM_ADDRESS_PLACE_ID] != "":
            coordinates = geocode_id(query_params[URL_PARAM_ADDRESS_PLACE_ID])
            if coordinates:
                dictionary = coordinates0_to_dictionary(coordinates)
                s = list_of_dictionaries_to_response_text(result_format, [dictionary], with_id, with_address)
            else:
                s = ""
        else:
            s = ""
    elif URL_PARAM_SEARCH_TEXT in query_params:
        # parser = parseaddress.AddressParser()
        candidates = full_text_search_address(query_params["SearchText"])
        lines = []
        for candidate in candidates:
            coordinates = geocode_id(candidate[0])
            if not coordinates:
                continue
            else:
                dictionary = coordinates0_to_dictionary(coordinates)
                lines.append(dictionary)
        s = list_of_dictionaries_to_response_text(result_format, lines, with_id, with_address)
    else:
        s = geocode_address(
            p(URL_PARAM_STREET), p(URL_PARAM_HOUSE_NUMBER), p(URL_PARAM_RECORD_NUMBER),
            p(URL_PARAM_ORIENTATION_NUMBER), p(URL_PARAM_ORIENTATION_NUMBER_CHARACTER), p(URL_PARAM_ZIP_CODE),
            p(URL_PARAM_LOCALITY), p(URL_PARAM_LOCALITY_PART), p(URL_PARAM_DISTRICR_NUMBER),
            p(URL_PARAM_DISTRICR_NAME)
        )
    return s


def _find_coordinates_by_address(dictionary):
    if "district_number" in dictionary:
        if dictionary["district_number"] != "":
            dictionary["district_number"] = "Praha " + dictionary["district_number"]

    first = True
    sql = "SELECT " + ADDRESSPOINTS_COLUMNS_FIND_COORD + \
          " FROM " + ADDRESSPOINTS_TABLE_NAME + \
          " WHERE "
    for key in dictionary:
        if dictionary[key] != "":
            if first:
                sql += ITEM_TO_FIELD[key] + " = '" + dictionary[key] + "'"
                first = False
            else:
                sql += " AND " + ITEM_TO_FIELD[key] + " = '" + dictionary[key] + "'"

    sql += "LIMIT " + str(MAX_COUNT)
    cur = execute_sql(DATABASE_NAME_RUIAN, sql)
    rows = cur.fetchall()
    coordinates = []
    localities = []
    for row in rows:
        if (row[0] is not None) and (row[1] is not None):
            (house_number, record_number) = analyse_row(row[7], number_to_string(row[6]))
            coordinates.append(
                (str("{:10.2f}".format(row[0])).strip(), str("{:10.2f}".format(row[1])).strip(),
                 row[2], row[3], none_to_string(row[4]), none_to_string(row[5]),
                 house_number, record_number, number_to_string(row[8]), none_to_string(row[9]),
                 number_to_string(row[10]), number_value(none_to_string(row[11])))
            )
            # latitude, longitude, gid, nazev_obce, nazev_casti_obce, nazev_ulice, cislo_domovni, typ_so,
            # cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop
            coord = Coordinates(row[0], row[1])
            addr = AddressInternal(row[5], house_number, record_number, row[8], row[9], row[10], row[3], row[4], None, row[11],
                                   row[2])
            loc = Locality(addr, coord)
            localities.append(loc)
        else:
            # co se ma stat kdyz adresa nema souradnice?
            pass
    cur.close()
    # return coordinates
    return localities


def _get_ruian_version_date():
    return get_ruian_version()


def _set_ruian_version_data_today():
    try:
        sql = 'DROP TABLE IF EXISTS ruian_dates;'
        sql += 'CREATE TABLE ruian_dates (id serial PRIMARY KEY, validfor varchar);'
        import time
        value = time.strftime("%d.%m.20%y")
        sql += "INSERT INTO {0} ({1}) VALUES ('{2}')".format('ruian_dates', 'validfor', value)
        commit_sql(DATABASE_NAME_RUIAN, sql)
    except psycopg2.Error as e:
        result = "Error: Could connect to %s at %s:%s as %s\n%s" \
                 % (DATABASE_NAME_RUIAN, DATABASE_HOST, DATABASE_PORT, DATABASE_USER, str(e))
        print(result)
    pass


def get_table_count(table_name):
    cur = None
    try:
        sql = "SELECT count(*) FROM %s;" % table_name
        cur = execute_sql(DATABASE_NAME_RUIAN, sql)
        row = cur.fetchone()
        result = row[0]

    finally:
        cur.close()

    return str(result)


def _get_database_details():
    return None


def _get_table_names():
    return None


def _get_addresses(query_params):
    sql_items = {
        "house_number": "cast(cislo_domovni as text) like '%s%%' and typ_so='č.p.'",
        "record_number": "cast(cislo_domovni as text) ilike '%s%%' and typ_so<>'č.p.'",
        "orientation_number": "cast(cislo_orientacni as text) like '%s%%'",
        "orientation_number_character": "znak_cisla_orientacniho = '%s'",
        "zip_code": "cast(psc as text) like '%s%%'",
        "locality": "nazev_obce ilike '%%%s%%'",
        "street": "nazev_ulice ilike '%%%s%%'",
        "locality_part": "nazev_casti_obce ilike '%%%s%%'",
        "district_number": "nazev_mop = 'Praha %s'"
    }
    fields = " cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, nazev_casti_obce, " \
             "nazev_mop, nazev_ulice, typ_so, gid "

    sql_parts = []
    for key in sql_items:
        dict_key = key[:1].lower() + key[1:]
        if dict_key in query_params:
            if query_params[dict_key] is not None:
                if query_params[dict_key] != "":
                    sql_parts.append(sql_items[key] % (query_params[dict_key]))

    if len(sql_parts) == 0:
        return []

    sql_base = u" from %s where " % ADDRESSPOINTS_TABLE_NAME + " and ".join(sql_parts)

    search_sql = u"select %s %s order by nazev_obce, nazev_casti_obce, psc, nazev_ulice, nazev_mop, " \
                 u"typ_so, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho limit 10" % (fields, sql_base)
    print("SQL: ", search_sql)
    rows = execute_sql(DATABASE_NAME_RUIAN, search_sql)

    result: List[Any] = []
    for row in rows:
        result.append(row)

    return result


def add_to_query(attribute, comparator, first):
    if first:
        query = attribute + " " + comparator + " %s"
    else:
        query = " AND " + attribute + " " + comparator + " %s"
    return query


def compile_address_id(identifier):
    adr = _find_address(identifier=identifier)
    out = None
    if adr is not None:
        out = compile_address_as_obj(
            street=adr.street,
            orientation_number_character=adr.orientation_number_character,
            orientation_number=adr.orientation_number,
            house_number=adr.house_number,
            record_number=adr.record_number,
            district_number=adr.district_number,
            locality=adr.locality,
            locality_part=adr.locality_part,
            zip_code=adr.zip_code,
            ruian_id=identifier)
    return out


# noinspection DuplicatedCode
def compile_address(
        text_format, street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, district_name, do_validate=False, with_ruian_id=False):
    """
        :param text_format:                     string  Formát výstupu
        :param street:                          string  Název ulice
        :param house_number:                    number  Číslo popisné
        :param record_number:                   number  Číslo evidenční
        :param orientation_number:              number  Číslo orientační
        :param orientation_number_character:    string  Písmeno čísla orientačního
        :param zip_code:                        number  Poštovní směrovací číslo
        :param locality:                        string  Obec
        :param locality_part:                   string  Část obce, pokud je známa
        :param district_number:                 number  Obvod
        :param district_name:                   string  Název obvodu
        :param do_validate:                     boolean validovat adresu
        :param with_ruian_id:                   boolean vratit ruian id
    """
    dictionary = build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, district_name
    )
    print("DICTIONARY: ", dictionary)
    work = {}
    work_list = []
    if do_validate or with_ruian_id:
        rows = _get_addresses(dictionary)
        print("ROWS: ", rows)
        if len(rows) > 0:
            for row in rows:
                work = {}
                (
                    work['house_number'], work['orientation_number'], work['orientation_number_character'],
                    work['zip_code'], work['locality'], work['locality_part'], work['nazev_mop'], work['street'],
                    work['typ_so'], work['ruian_id']
                ) = row
                work['record_number'] = ''
                work['district_number'] = ''
                if work['typ_so'] != "č.p.":
                    work['record_number'] = work['house_number']
                    work['house_number'] = ""
                if work['nazev_mop'] is not None and work['nazev_mop'] != "":
                    work['district_number'] = work['nazev_mop'][work['nazev_mop'].find(" ") + 1:]
                if not with_ruian_id:
                    work['ruian_id'] = ""
                work_list.append(work)
        else:
            # TODO OPRAVDU????
            return ""
    else:
        dictionary['ruian_id'] = ""
        work_list.append(dictionary)

    out_list = []
    for work in work_list:
        out = None
        if text_format is None or text_format == "" or text_format == TEXT_FORMAT_TEXT:
            out = str((
                work['street'], work['house_number'], work['record_number'], work['orientation_number'],
                work['orientation_number_character'], work['zip_code'], work['locality'], work['locality_part'],
                work['district_number'], work['ruian_id']
            ))
        elif text_format == 'obj':
            out = compile_address_as_obj(
                work['street'], work['house_number'], work['record_number'], work['orientation_number'],
                work['orientation_number_character'], work['zip_code'], work['locality'], work['locality_part'],
                work['district_number'], work['ruian_id']
            )
        elif text_format == TEXT_FORMAT_JSON:
            out = compile_address_as_json(
                work['street'], work['house_number'], work['record_number'], work['orientation_number'],
                work['orientation_number_character'], work['zip_code'], work['locality'], work['locality_part'],
                work['district_number'], work['ruian_id']
            )
        elif text_format == TEXT_FORMAT_XML:
            out = compile_address_as_xml(
                work['street'], work['house_number'], work['record_number'], work['orientation_number'],
                work['orientation_number_character'], work['zip_code'], work['locality'], work['locality_part'],
                work['district_number'], work['ruian_id']
            )
        elif text_format == TEXT_FORMAT_TEXT2ONEROW or text_format == TEXT_FORMAT_HTML2ONEROW:
            out = compile_address_to_one_row(
                work['street'], work['house_number'], work['record_number'], work['orientation_number'],
                work['orientation_number_character'], work['zip_code'], work['locality'], work['locality_part'],
                work['district_number'], work['ruian_id']
            )
        else:
            out = text_format.listToResponseText(
                compile_address_as_text(
                    work['street'], work['house_number'], work['record_number'], work['orientation_number'],
                    work['orientation_number_character'], work['zip_code'], work['locality'], work['locality_part'],
                    work['district_number'], work['ruian_id']
                ))
        if out is not None:
            out_list.append(out)
    return out_list


def search_address(
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, district_name):
    """
        :param street:                          string  Název ulice
        :param house_number:                    number  Číslo popisné
        :param record_number:                   number  Číslo evidenční
        :param orientation_number:              number  Číslo orientační
        :param orientation_number_character:    string  Písmeno čísla orientačního
        :param zip_code:                        number  Poštovní směrovací číslo
        :param locality:                        string  Obec
        :param locality_part:                   string  Část obce, pokud je známa
        :param district_number:                 number  Obvod
        :param district_name:                   string  Název obvodu
    """
    dictionary = build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, district_name
    )
    print("DICTIONARY: ", dictionary)
    work = {}
    work_list = []
    rows = _get_addresses(dictionary)
    print("ROWS: ", rows)
    if len(rows) > 0:
        for row in rows:
            work = {}
            (
                work['house_number'], work['orientation_number'], work['orientation_number_character'],
                work['zip_code'], work['locality'], work['locality_part'], work['nazev_mop'], work['street'],
                work['typ_so'], work['ruian_id']
            ) = row
            work['record_number'] = ''
            work['district_number'] = ''
            work['district'] = ''
            if work['typ_so'] != "č.p.":
                work['record_number'] = work['house_number']
                work['house_number'] = ''
            if work['nazev_mop'] is not None and work['nazev_mop'] != "":
                work['district_number'] = work['nazev_mop'][work['nazev_mop'].find(" ") + 1:]
                work['district'] = work['nazev_mop']
            work_list.append(work)
    else:
        # TODO OPRAVDU????
        return None

    out_list = []
    for work in work_list:
        out = AddressInternal(
            street=work['street'], orientation_number_character=work['orientation_number_character'],
            district=work['district'], district_number=work['district_number'], house_number=work['house_number'],
            orientation_number=work['orientation_number'], record_number=work['record_number'],
            ruian_id=work['ruian_id'], zip_code=work['zip_code'], locality=work['locality'],
            locality_part=work['locality_part']
        )
        if out is not None:
            out_list.append(out)
    return out_list


def build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, district_name):
    return {
        "street": street,
        "house_number": house_number,
        "record_number": record_number,
        "orientation_number": orientation_number,
        "orientation_number_character": orientation_number_character,
        "zip_code": str(zip_code).replace(" ", ""),
        "locality": locality,
        "locality_part": locality_part,
        "district_number": district_number,
        "district_name": district_name
    }


def validate_address(
        text_format, street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, district_name):
    (
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, district_name
    ) = none_to_string((
        street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, district_name
    ))
    if not right_address(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number, district_name):
        return "False"

    print("right_address OK")
    dictionary = build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number, district_name)

    result = _validate_address(dictionary)
    return list_to_response_text(text_format, result)


def validate_address_items(
        text_format, street, house_number, record_number, orientation_number, orientation_number_character,
        zip_code, locality, locality_part, district_number, district_name):
    if not right_address(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number, district_name):
        return "False"

    dictionary = build_validate_dict(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
        locality_part, district_number, district_name)

    result = _validate_address(dictionary)
    return list_to_response_text(text_format, result)


class AddressItem:
    def __init__(self, value, search_db=True):
        self.value = value
        self.towns = []
        self.town_parts = []
        self.streets = []
        self.is_record_number = False
        self.is_orientation_number = False
        self.is_description_number = False
        self.is_zip = False
        self.is_house_number = False
        self.number = None
        self.max_number_len = 0
        self.is_number_id = False
        self.is_text_field = False
        self.analyse_value(search_db)

    def __repr__(self):
        result = ""
        if self.is_zip:
            result += "PSČ "
        if self.is_orientation_number:
            result += "č.or. "
        if self.is_record_number:
            result += RECORD_NUMBER_ID + " "
        if self.is_description_number:
            result += DESCRIPTION_NUMBER_ID + " "
        if self.number is None:
            result += '"' + self.value + '"'
        else:
            result += self.number

        return result

    def match_percent(self, candidate_value, field_index):
        # field_index meaning:
        # 0=GID_FIELDNAME
        # 1=TOWNNAME_FIELDNAME
        # 2=TOWNPART_FIELDNAME
        # 3=STREETNAME_FIELDNAME
        # 4=TYP_SO_FIELDNAME
        # 5=CISLO_DOMOVNI_FIELDNAME
        # 6=CISLO_ORIENTACNI_FIELDNAME
        # 7=ZNAK_CISLA_ORIENTACNIHO_FIELDNAME
        # 8=ZIP_CODE_FIELDNAME
        # 9=MOP_NUMBER
        # print('match_percent:', candidate_value, field_index, str(self.value))
        candidate_value = str(candidate_value).lower()
        if candidate_value == "677":
            pass
        if self.is_zip:
            if field_index != 8 or len(candidate_value) != 5:
                return 0
        else:
            if field_index == 0:
                if len(candidate_value) != len(self.value):
                    return 0
            if field_index == 8:
                if len(candidate_value) == 5 and candidate_value == self.value:
                    return 100
                else:
                    return 0
        if candidate_value.find(self.value.lower()) != 0:
            return 0
        else:
            out = 1.0 * len(str(self.value)) / len(candidate_value)
            return out

    def __str__(self):
        result = ""
        if self.is_zip:
            result += "PSČ "
        if self.is_orientation_number:
            result += "č.or. "
        if self.is_record_number:
            result += RECORD_NUMBER_ID + " "
        if self.is_description_number:
            result += DESCRIPTION_NUMBER_ID + " "
        if self.number is None:
            result += '"' + self.value + '" ' + str(len(self.streets)) + "," + str(len(self.towns)) + \
                      "," + str(len(self.town_parts))
        else:
            result += self.number

        return result

    def analyse_value(self, search_db=True):
        if is_int(self.value):
            self.number = self.value
            pass
        elif self.value == ORIENTATION_NUMBER_ID:
            self.is_orientation_number = True
            self.is_number_id = True
            self.max_number_len = ORIENTATION_NUMBER_MAX_LEN
        elif self.value == RECORD_NUMBER_ID:
            self.is_record_number = True
            self.is_number_id = True
            self.max_number_len = RECORD_NUMBER_MAX_LEN
        elif self.value == DESCRIPTION_NUMBER_ID:
            self.is_description_number = True
            self.is_number_id = True
            self.max_number_len = DESCRIPTION_NUMBER_MAX_LEN
        else:
            self.is_text_field = True
            if search_db:
                self.towns = get_obec_by_name(self.value)
                self.streets = get_ulice_by_name(self.value)
                self.town_parts = get_cast_obce_by_name(self.value)


def full_text_search_address_object(address):
    result = full_text_search_address(address)
    if result:
        out = []
        for item in result:
            typ_so = item[4]
            record_number = ""
            house_number = ""
            if typ_so == "č.p.":
                house_number = item[5]
            else:
                record_number = item[5]
            a = AddressInternal(
                item[3], house_number, record_number, item[6], item[7], item[8], item[1], item[2], None, item[9],
                item[0]
            )
            out.append(a)
        return out
    else:
        return []


def full_text_search_address(address):
    items = analyze(address, False)
    print('ITEMS:', items)
    candidates_ids = get_candidate_values(items)
    results_dict = defaultdict(list)
    for candidate in candidates_ids:
        match_percent = compare(items, candidate)
        # print(str(match_percent), str(candidate))
        if match_percent > 0:
            if match_percent in results_dict:
                results_dict[match_percent].append(candidate)
            else:
                results_dict[match_percent] = [candidate]
    results = []
    exact_match_needed = False

    def add_candidate(key1, candidate1):
        global exact_match_needed
        if not results:
            exact_match_needed = (key1 == 1)
        continue_loop = not exact_match_needed or (exact_match_needed and key1 == 1)
        if continue_loop:
            results.append(candidate1)
        return continue_loop

    for key in reversed(sorted(results_dict)):
        candidate_item = results_dict[key]
        if isinstance(candidate_item, list):
            for candidate in candidate_item:
                add_candidate(key, candidate)
        else:
            add_candidate(key, candidate_item)
    return results


def analyze(address, search_db=True):
    items = parse(address, search_db)
    return analyze_items(items)


def analyze_items(items):
    new_items = []
    index = 0
    next_item_to_be_skipped = False
    for item in items:
        if next_item_to_be_skipped:
            next_item_to_be_skipped = False
            continue

        if index == len(items) - 1:
            next_item = None
        else:
            next_item = items[index + 1]

        to_be_skipped = False
        if item.is_number_id:
            if next_item is None or next_item.number is None or len(next_item.number) > item.maxNumberLen:
                to_be_skipped = True
                # Error, za indikátorem č.ev.,č.or.,/ nenásleduje číslice nebo je příliš dlouhá
            else:
                item.number = next_item.number
                next_item_to_be_skipped = True

        elif item.number is not None:
            if next_item is not None and \
                    next_item.number is not None and \
                    len(item.number) + len(next_item.number) == ZIPCODE_LEN:
                item.number += next_item.number
                next_item_to_be_skipped = True

            if len(item.number) == ZIPCODE_LEN:
                item.isZIP = True
            elif len(item.number) <= HOUSE_NUMBER_MAX_LEN:
                item.isHouseNumber = True
            else:
                # Error, příliš dlouhé číslo domovní nebo evidenční
                pass
        else:
            # else textový řetezec
            # TODO udelat
            # if item.streets == [] and item.streets == [] and item.streets == []:
            #    to_be_skipped = True
            pass

        if not to_be_skipped:
            new_items.append(item)

        index = index + 1

    return new_items


def parse(address, search_db=True):
    address = normalize(address)
    string_items = address.split(",")
    items = []
    for value in string_items:
        item = AddressItem(value, search_db)
        items.append(item)
    return items


def normalize(address):
    address = normalize_separators(address)
    address = normalize_description_number_id(address)
    address = normalize_record_number_id(address)
    address = expand_nad_pod(address)
    address = separate_numbers(address)
    return address


def normalize_separators(address):
    address = address.replace(ORIENTATION_NUMBER_ID, " ")
    address = address.replace("  ", " ")
    address = address.replace(",,", ",")
    address = address.replace(" ,", ",")
    address = address.replace(", ", ",")
    address = address.replace("\r\r", "\r")
    address = address.replace("\r", ",")
    address = address.replace("\n\n", ",")
    address = address.replace("\n", ",")
    return address


def normalize_description_number_id(address):
    address = address.replace("čp ", DESCRIPTION_NUMBER_ID + " ")
    address = address.replace("č. p.", DESCRIPTION_NUMBER_ID)
    address = address.replace("čp.", DESCRIPTION_NUMBER_ID)
    return address


def normalize_record_number_id(address):
    address = address.replace("ev.č.", RECORD_NUMBER_ID)
    address = address.replace("ev č.", RECORD_NUMBER_ID)
    address = address.replace("evč.", RECORD_NUMBER_ID)
    address = address.replace("eč.", RECORD_NUMBER_ID)
    address = address.replace("ev. č.", RECORD_NUMBER_ID)
    address = address.replace("č. ev.", RECORD_NUMBER_ID)
    address = address.replace("čev.", RECORD_NUMBER_ID)
    if address.find("č.ev") >= 0 and address.find("č.ev") != address.find(RECORD_NUMBER_ID):
        address = address.replace("č.ev", RECORD_NUMBER_ID, 1)
    return address


def expand_nad_pod(address):
    address = address.replace(" n ", " nad ")
    address = address.replace(" n.", " nad ")
    address = address.replace(" p ", " pod ")
    address = address.replace(" p.", " pod ")
    return address


def separate_numbers(address):
    new_address = ""
    was_number = False
    for i in range(len(address)):
        act_char = address[i:i + 1]
        if "0123456789".find(act_char) >= 0:
            if i > 0 and not was_number:
                new_address += ","
            was_number = True
            new_address += act_char
        elif was_number:
            new_address += act_char + ","
            was_number = False
        else:
            new_address += act_char

    return normalize_separators(new_address)


def get_candidate_query(analysed_items):
    sql_items = []
    sql = ''
    for item in analysed_items:
        if item.is_text_field and len(item.value) >= 2:
            sql_items.append("searchstr ILIKE '%{0}%'".format(item.value))
        elif str(item).isnumeric():
            sql_items.append("searchstr ILIKE '%{0}%'".format(str(item.value)))
    if sql_items:
        inner_sql = "SELECT {3}({0}) FROM {1} WHERE {2}".format(
            GIDS_FIELDNAME, FULLTEXT_EXTENDED_TABLENAME, " AND ".join(sql_items), 'explode_array')
        sql = "SELECT {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {11} FROM {9} WHERE {0} IN ({10} LIMIT 100)".format(
            GID_FIELDNAME, TOWNNAME_FIELDNAME, TOWNPART_FIELDNAME, STREETNAME_FIELDNAME, TYP_SO_FIELDNAME,
            CISLO_DOMOVNI_FIELDNAME, CISLO_ORIENTACNI_FIELDNAME, ZNAK_CISLA_ORIENTACNIHO_FIELDNAME,
            ZIP_CODE_FIELDNAME, ADDRESSPOINTS_TABLE_NAME, str(inner_sql), MOP_NAME)
    return sql


def get_candidate_values(analysed_items):
    sql = get_candidate_query(analysed_items)
    print('SQL:', sql)
    if sql != "":
        candidates = get_result(DATABASE_NAME_RUIAN, sql)
        return candidates
    else:
        return []


def compare(items, field_values):
    sum_match_percent = 0
    num_matches = 0
    found = False
    for item in items:
        field_index = 0
        for field_value in field_values:
            match_percent = item.match_percent(field_value, field_index)
            if match_percent > 0:
                sum_match_percent = sum_match_percent + match_percent
                num_matches = num_matches + 1
                found = True
                break
            field_index = field_index + 1
        if not found:
            return 0
    return sum_match_percent / num_matches
