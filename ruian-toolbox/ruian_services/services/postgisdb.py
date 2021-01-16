# -*- coding: utf-8 -*-
__author__ = 'SYSNET'

import psycopg2
import sys

import shared
from config import config
from ruian_connection import *

from shared_tools.log import logger
from shared_tools.configuration import get_ruian_services_html_path
from shared_tools.base import get_file_content
import HTTPShared

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


SERVER_HTTP = config.serverHTTP
PORT_NUMBER = config.portNumber
SERVICES_WEB_PATH = config.servicesWebPath

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
        (houseNumber, recordNumber) = HTTPShared.analyseRow(row[2], number_to_string(row[1]))
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


def add_to_query(attribute, comparator, first):
    if first:
        query = attribute + " " + comparator + " %s"
    else:
        query = " AND " + attribute + " " + comparator + " %s"
    return query


def _validate_address(dictionary, return_row=False, test=False):
    first = True
    oneHouseNumber = False
    conn = open_connection(test=test)
    cursor = conn.cursor()

    query = "SELECT " + \
            "gid, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, nazev_casti_obce, " + \
            "nazev_mop, nazev_ulice, typ_so FROM " + TABLE_NAME + " WHERE "
    address_tuple = ()
    for key in dictionary:
        if key == "houseNumber":
            if dictionary[key] != "":
                if oneHouseNumber:
                    return ["False"]
                else:
                    oneHouseNumber = True
                query += add_to_query("typ_so", "=", first)
                first = False
                address_tuple = address_tuple + (u"č.p.",)
            else:
                continue
        if key == "recordNumber":
            if dictionary[key] != "":
                if oneHouseNumber:
                    return ["False"]
                else:
                    oneHouseNumber = True
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
        (houseNumber, recordNumber) = HTTPShared.analyseRow(row[7], number_to_string(row[6]))
        c = (str("{:10.2f}".format(row[1])).strip(), str("{:10.2f}".format(row[0])).strip(), row[2], row[3],
             none_to_string(row[4]), none_to_string(row[5]), houseNumber, recordNumber, number_to_string(row[8]),
             none_to_string(row[9]), number_to_string(row[10]), number_value(none_to_string(row[11])))
        return [c]
    else:
        return []


def _find_coordinates_by_address(dictionary, test=False):
    if "districtNumber" in dictionary and dictionary["districtNumber"] != "":
        dictionary["districtNumber"] = "Praha " + dictionary["districtNumber"]

    first = True
    con = open_connection(test=test)
    cur = con.cursor()

    query = "SELECT " + \
            "latitude, longitude, gid, nazev_obce, nazev_casti_obce, nazev_ulice, cislo_domovni, typ_so, " + \
            "cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop FROM " + TABLE_NAME + " WHERE "

    for key in dictionary:
        if dictionary[key] != "":
            if first:
                query += ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"
                first = False
            else:
                query += " AND " + ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"

    query += "LIMIT 25"
    cur.execute(query)
    rows = cur.fetchall()
    coordinates = []

    for row in rows:
        if (row[0] is not None) and (row[1] is not None):
            (houseNumber, recordNumber) = HTTPShared.analyseRow(row[7], number_to_string(row[6]))
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
            query = 'select * from ruian_dates'
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


def _get_db_details(service_path_info, response, test=False):
    if service_path_info is not None and len(service_path_info) > 1 and service_path_info[0].lower() == "recordcount":
        response.htmlData = get_table_count(service_path_info[1])
        response.mimeFormat = "text/plain"
        response.handled = True
    else:
        response.mimeFormat = "text/html"
        response.handled = True

        result = get_file_content(get_ruian_services_html_path() + "DatabaseDetails.html")
        result = result.replace("#DATABASE_NAME#", DATABASE_NAME)

        connection = open_connection(test=test)
        cursor = connection.cursor()
        try:
            oddRow = False
            tablesList = "<table>\n"
            tablesList += '\t\t<tr valign="bottom"><th align="left">Tabulka</th><th>Záznamů</th></tr>\n'
            cursor.execute(
                "SELECT table_name FROM information_schema.tables where table_schema='public'ORDER BY table_name;")
            tableNames = []
            rows = cursor.fetchall()
            for row in rows:
                tableName = row[0]
                tableNames.append(tableName)
                tablesList += '\t\t<tr %s><td>%s</td><td align="right" id="%s_TD"></td></tr>\n' % (
                    ["", 'class="altColor"'][int(oddRow)], tableName, tableName)
                oddRow = not oddRow
            tablesList += "\t</table>"
            result = result.replace("#TABLES_LIST#", tablesList)
            result = result.replace("#TABLES_COUNT#", str(len(rows) + 1))
            result = result.replace("#TABLE_NAMES#", str(tableNames))
            restPyURL = "http://" + SERVER_HTTP + get_port_specification() + "/" + SERVICES_WEB_PATH + "/"
            result = result.replace("#SERVICES_PATH#", restPyURL)
            result = result.replace("\r\n", "\n")
            response.htmlData = result
        finally:
            cursor.close()
            connection.close()
    pass


def _get_addresses(query_params):
    sqlItems = {
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

    sqlParts = []
    for key in sqlItems:
        dictKey = key[:1].lower() + key[1:]
        if dictKey in query_params and query_params[dictKey] != "":
            sqlParts.append(sqlItems[key] % (query_params[dictKey]))

    if len(sqlParts) == 0:
        return []

    sqlBase = u" from %s where " % ADDRESS_POINTS_TABLE_NAME + " and ".join(sqlParts)

    searchSQL = u"select %s %s order by nazev_obce, nazev_casti_obce, psc, nazev_ulice, nazev_mop, typ_so, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho limit 2" % (
        fields, sqlBase)
    rows = select_sql(searchSQL)
    result = []
    for row in rows:
        result.append(row)

    return result


def _get_table_names():
    return '"ahoj", "table2"'
