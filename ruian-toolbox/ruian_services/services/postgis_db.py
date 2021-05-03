# -*- coding: utf-8 -*-
__author__ = 'SYSNET'

import psycopg2
import sys

from ruian_services.services import http_shared
from ruian_services.services.config import config, SERVER_HTTP, SERVICES_WEB_PATH
from ruian_services.services.ruian_connection import Address
from shared_tools import shared
from shared_tools.log import logger
from shared_tools.configuration import get_ruian_services_html_path
from shared_tools.base import get_file_content

shared.setup_paths()

DATABASE_HOST = config.databaseHost
PORT = config.databasePort
DATABASE_NAME = config.databaseName
USER_NAME = config.databaseUserName
PASSWORD = config.databasePassword

DB_CONF = {
    "host": config.databaseHost,
    "database": config.databaseName,
    "port": config.databasePort,
    "user": config.databaseUserName,
    "password": config.databasePassword,
}

DB_CONF_TEST = {
    "host": "localhost",
    "database": "ruian",
    "port": "25432",
    "user": "docker",
    "password": "docker",
}

TABLE_NAME = "address_points"
ADDRESS_POINTS_TABLE_NAME = "address_points"

ITEM_TO_DBFIELDS = {
    "id": "gid",
    "street": "nazev_ulice",
    "houseNumber": "cislo_domovni",
    "recordNumber": "cislo_domovni",
    "orientationNumber": "cislo_orientacni",
    "orientationNumberCharacter": "znak_cisla_orientacniho",
    "zipCode": "psc",
    "locality": "nazev_obce",
    "localityPart": "nazev_casti_obce",
    "districtNumber": "nazev_mop",
    "JTSKX": "latitude",
    "JTSKY": "longitude"
}


def open_connection(test=False):
    conf = DB_CONF
    if test:
        conf = DB_CONF_TEST
    try:
        conn = psycopg2.connect(
            host=conf["host"],
            database=conf["database"],
            port=conf["port"],
            user=conf["user"],
            password=conf["password"]
        )
    except psycopg2.Error as e:
        logger.error(str(e))
        conn = None
    return conn


def none_to_string(item):
    if item is None:
        return ""
    else:
        return item


def number_to_string(number):
    if number is None:
        return ""
    else:
        return str(number)


def format_to_query(item):
    if item == "":
        return None
    elif item.strip().isdigit():
        return int(item)
    else:
        return item


def number_value(value):
    if value != "":
        s = value.split(" ")
        return s[1]
    else:
        return ""


class PostGISDatabase:
    conn = None

    def __init__(self, test=False):
        self.conn = open_connection(test=test)

    def get_query_result(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row)
        return rows


def select_sql(search_sql):
    if search_sql is None or search_sql == "":
        return None
    try:
        db = PostGISDatabase()
        cursor = db.conn.cursor()
        cursor.execute(search_sql)
        return cursor
    except psycopg2.Error as e:
        logger.error(str(e))
        return [sys.exc_info()[0]]


def _find_address(identifier, test=False):
    conn = open_connection(test=test)
    cur = conn.cursor()
    cur.execute(
        "SELECT " +
        "nazev_ulice, cislo_domovni, typ_so, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, " +
        "nazev_casti_obce, nazev_mop FROM " + TABLE_NAME + " WHERE gid = " + str(identifier))
    row = cur.fetchone()
    if row:
        (houseNumber, recordNumber) = http_shared.analyse_row(row[2], number_to_string(row[1]))
        a = number_value(none_to_string(row[8]))
        return Address(none_to_string(row[0]), houseNumber, recordNumber, number_to_string(row[3]),
                       none_to_string(row[4]),
                       number_to_string(row[5]), none_to_string(row[6]), none_to_string(row[7]), a)
    else:
        return None


def _get_nearby_localities(y, x, distance, max_count=100, test=False):
    max_count = int(max_count)
    if max_count > 10000:
        max_count = 10000
    conn = open_connection(test=test)
    cur = conn.cursor()
    geom = "the_geom,ST_GeomFromText('POINT(-%s -%s)',5514)" % (str(x), str(y))
    query = "SELECT gid, nazev_obce, nazev_casti_obce, nazev_ulice, typ_so, cislo_domovni, cislo_orientacni, " + \
            "znak_cisla_orientacniho, psc, nazev_mop, " + \
            "ST_Distance(%s) d1 FROM %s WHERE ST_DWithin(%s,%s) order by d1 LIMIT %s;" % (
                geom, TABLE_NAME, geom, str(distance), str(max_count))
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def add_to_query(attribute, comparator, first=True):
    if first:
        query = attribute + " " + comparator + " %s"
    else:
        query = " AND " + attribute + " " + comparator + " %s"
    return query


def _validate_address(dictionary, return_row=False, test=False):
    first = True
    one_house_number = False
    conn = open_connection(test=test)
    cursor = conn.cursor()
    query = "SELECT {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9} FROM {10} WHERE ".format(
        'gid', 'cislo_domovni', 'cislo_orientacni', 'znak_cisla_orientacniho', 'psc', 'nazev_obce',
        'nazev_casti_obce', 'nazev_mop', 'nazev_ulice', 'typ_so', TABLE_NAME)
    address_tuple = ()
    for key in dictionary:
        if key == "houseNumber":
            if dictionary[key] != "":
                if one_house_number:
                    return ["False"]
                else:
                    one_house_number = True
                query += add_to_query("typ_so", "=", first)
                first = False
                address_tuple = address_tuple + (u"č.p.",)
            else:
                continue
        if key == "recordNumber":
            if dictionary[key] != "":
                if one_house_number:
                    return ["False"]
                else:
                    one_house_number = True
                query += add_to_query("typ_so", "=", first)
                first = False
                address_tuple = address_tuple + (u"č.ev.",)
            else:
                continue
        if key == "districtNumber" and dictionary[key] != "":
            value = format_to_query(dictionary["locality"] + " " + dictionary["districtNumber"])
        else:
            value = format_to_query(dictionary[key])
        address_tuple = address_tuple + (value,)
        if value is None:
            comparator = "is"
        else:
            comparator = "="
        query += add_to_query(ITEM_TO_DBFIELDS[key], comparator, first)
        first = False

    a = cursor.mogrify(query, address_tuple)
    cursor.execute(a)
    row = cursor.fetchone()

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


def _find_coordinates(identifier, test=False):
    conn = open_connection(test=test)
    cur = conn.cursor()
    cur.execute(
        "SELECT " +
        "latitude, longitude, gid, nazev_obce, nazev_casti_obce, nazev_ulice, cislo_domovni, typ_so, " +
        "cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop FROM " +
        TABLE_NAME + " WHERE gid = " + str(identifier))
    row = cur.fetchone()
    if row and row[0] is not None and row[1] is not None:
        (houseNumber, recordNumber) = http_shared.analyse_row(row[7], number_to_string(row[6]))
        c = (str("{:10.2f}".format(row[1])).strip(), str("{:10.2f}".format(row[0])).strip(), row[2], row[3],
             none_to_string(row[4]), none_to_string(row[5]), houseNumber, recordNumber, number_to_string(row[8]),
             none_to_string(row[9]), number_to_string(row[10]), number_value(none_to_string(row[11])))
        return [c]
    else:
        return []


def _add_dict_to_query(dictionary, query, first):
    query_list = []
    for key in dictionary:
        if dictionary[key] != "":
            query_list.append(ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'")
    if query_list:
        if first:
            query += ' AND ' + ' AND '.join(query_list)
        else:
            query += ' AND '.join(query_list)


def _find_coordinates_by_address(dictionary, test=False):
    if "districtNumber" in dictionary and dictionary["districtNumber"] != "":
        dictionary["districtNumber"] = "Praha " + dictionary["districtNumber"]

    first = True
    con = open_connection(test=test)
    cur = con.cursor()
    query = "SELECT {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11} FROM {12} WHERE ".format(
        'latitude', 'longitude', 'gid', 'nazev_obce', 'nazev_casti_obce', 'nazev_ulice', 'cislo_domovni',
        'typ_so', 'cislo_orientacni', 'znak_cisla_orientacniho', 'psc', 'nazev_mop', TABLE_NAME)
    add_to_query(dictionary, query, first)
    query += "LIMIT 25"
    cur.execute(query)
    rows = cur.fetchall()
    coordinates = []
    for row in rows:
        if (row[0] is not None) and (row[1] is not None):
            (houseNumber, recordNumber) = http_shared.analyse_row(row[7], number_to_string(row[6]))
            coordinates.append((str("{:10.2f}".format(row[0])).strip(), str("{:10.2f}".format(row[1])).strip(), row[2],
                                row[3], none_to_string(row[4]), none_to_string(row[5]), houseNumber, recordNumber,
                                number_to_string(row[8]), none_to_string(row[9]), number_to_string(row[10]),
                                number_value(none_to_string(row[11]))))
        else:
            pass  # co se ma stat kdyz adresa nema souradnice?
    return coordinates


def _get_ruian_version_date(test=False):
    try:
        connection = open_connection(test=test)
        cursor = connection.cursor()
        try:
            query = 'select * from {0}'.format('ruian_dates')
            cursor.execute(query)
            row = cursor.fetchone()
            result = row[1]
        except psycopg2.Error as e:
            logger.error(str(e))
            return "ERROR:" + e.pgerror
        finally:
            cursor.close()
            connection.close()

    except psycopg2.Error as e:
        result = "Error: Could connect to %s at %s:%s as %s\n%s" % (
            DATABASE_NAME, DATABASE_HOST, PORT, USER_NAME, str(e))
        logger.error(result)

    return result


def _save_ruian_version_date_today(test=False):
    connection = open_connection(test=test)
    cursor = connection.cursor()
    try:
        query = 'DROP TABLE IF EXISTS ruian_dates;'
        query += 'CREATE TABLE ruian_dates (id serial PRIMARY KEY, validfor varchar);'
        import time
        value = time.strftime("%d.%m.20%y")
        query += "INSERT INTO ruian_dates (validfor) VALUES ('%s')" % value
        cursor.execute(query)
        connection.commit()
    finally:
        cursor.close()
        connection.close()
    pass


def get_table_count(table_name, test=False):
    connection = open_connection(test=test)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT count(*) FROM %s;" % table_name)
        row = cursor.fetchone()
        result = row[0]
    finally:
        cursor.close()
        connection.close()
    return str(result)


def get_port_specification():
    if config.portNumber == 80:
        return ""
    else:
        return ":" + str(config.portNumber)


def get_db_details(service_path_info, response, test=False):
    if service_path_info is not None and len(service_path_info) > 1 and service_path_info[0].lower() == "recordcount":
        response.html_data = get_table_count(service_path_info[1])
        response.mime_format = "text/plain"
        response.handled = True
    else:
        response.mime_format = "text/html"
        response.handled = True

        result = get_file_content(get_ruian_services_html_path() + "DatabaseDetails.html")
        result = result.replace("#DATABASE_NAME#", DATABASE_NAME)

        connection = open_connection(test=test)
        cursor = connection.cursor()
        try:
            odd_row = False
            tables_list = "<table>\n"
            tables_list += '\t\t<tr valign="bottom"><th align="left">Tabulka</th><th>Záznamů</th></tr>\n'
            sql = "SELECT {0} FROM {1} where {2} ORDER BY {0};".format(
                'table_name', 'information_schema.tables', "table_schema='public'")
            cursor.execute(sql)
            table_names = []
            rows = cursor.fetchall()
            for row in rows:
                table_name = row[0]
                table_names.append(table_name)
                tables_list += '\t\t<tr %s><td>%s</td><td align="right" id="%s_TD"></td></tr>\n' % (
                    ["", 'class="altColor"'][int(odd_row)], table_name, table_name)
                odd_row = not odd_row
            tables_list += "\t</table>"
            result = result.replace("#TABLES_LIST#", tables_list)
            result = result.replace("#TABLES_COUNT#", str(len(rows) + 1))
            result = result.replace("#TABLE_NAMES#", str(table_names))
            rest_py_url = "http" + "://" + SERVER_HTTP + get_port_specification() + "/" + SERVICES_WEB_PATH + "/"
            result = result.replace("#SERVICES_PATH#", rest_py_url)
            result = result.replace("\r\n", "\n")
            response.html_data = result
        finally:
            cursor.close()
            connection.close()
    pass


def _get_addresses(query_params):
    sql_items = {
        "HouseNumber": "cast(cislo_domovni as text) like '%s%%' and typ_so='č.p.'",
        "RecordNumber": "cast(cislo_domovni as text) ilike '%s%%' and typ_so<>'č.p.'",
        "OrientationNumber": "cast(cislo_orientacni as text) like '%s%%'",
        "OrientationNumberCharacter": "znak_cisla_orientacniho = '%s'",
        "ZIPCode": "cast(psc as text) like '%s%%'",
        "Locality": "nazev_obce ilike '%%%s%%'",
        "Street": "nazev_ulice ilike '%%%s%%'",
        "LocalityPart": "nazev_casti_obce ilike '%%%s%%'",
        "DistrictNumber": "nazev_mop = 'Praha %s'"
    }
    fields = " cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, nazev_casti_obce, " + \
             "nazev_mop, nazev_ulice, typ_so, gid "
    sql_parts = []
    for key in sql_items:
        dict_key = key[:1].lower() + key[1:]
        if dict_key in query_params and query_params[dict_key] != "":
            sql_parts.append(sql_items[key] % (query_params[dict_key]))
    if len(sql_parts) == 0:
        return []
    sql_base = u" from %s where " % ADDRESS_POINTS_TABLE_NAME + " and ".join(sql_parts)
    search_sql = "select {0} {1} order by {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10} limit 2".format(
        fields, sql_base, 'nazev_obce', 'nazev_casti_obce', 'psc', 'nazev_ulice', 'nazev_mop', 'typ_so',
        'cislo_domovni', 'cislo_orientacni', 'znak_cisla_orientacniho')
    rows = select_sql(search_sql)
    result = []
    for row in rows:
        result.append(row)
    return result


def _get_table_names():
    return '"ahoj", "table2"'
