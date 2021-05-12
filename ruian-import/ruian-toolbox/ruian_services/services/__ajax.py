# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import psycopg2

from ruian_services.services.config import config
from ruian_services.services.postgis_db import add_to_query
from ruian_services.services.ruian_connection import Address, Coordinates

ITEM_TO_DBFIELDS = {
    "id": "gid",
    "street": "nazev_ulice",
    "houseNumber": "cislo_domovni",
    "recordNumber": "nazev_momc",
    "orientationNumber": "cisloOrientacni",
    "zipCode": "psc",
    "locality": "nazev_obce",
    "localityPart": "nazev_casti_obce",
    "districtNumber": "nazev_mop",
    "JTSKX": "latitude",
    "JTSKY": "longitude"
}


def none_to_string(item):
    if item is None:
        return ""
    else:
        return item


def _find_address(identifier):
    con = psycopg2.connect(
        host=config.databaseHost,
        database=config.databaseName,
        port=config.databasePort,
        user=config.databaseUserName,
        password=config.databasePassword)
    cur = con.cursor()
    sql = "SELECT {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7} FROM {8} WHERE {9} = {10}".format(
        'nazev_ulice', 'cislo_domovni', 'nazev_momc', 'cislo_orientacni', 'psc', 'nazev_obce', 'nazev_casti_obce',
        'nazev_mop', 'test', 'gid',
        str(identifier))
    cur.execute(sql)
    row = cur.fetchone()
    if row:
        return Address(
            none_to_string(row[0]), none_to_string(row[1]), none_to_string(row[2]), none_to_string(row[3]), '',
            none_to_string(row[4]), none_to_string(row[5]), none_to_string(row[6]), none_to_string(row[7]))
        # (street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber)
    else:
        return None


def _get_nearby_localities(x, y, distance):
    con = psycopg2.connect(
        host=config.databaseHost,
        database=config.databaseName,
        port=config.databasePort,
        user=config.databaseUserName,
        password=config.databasePassword)
    cur = con.cursor()
    fieldlist = 'nazev_ulice, cislo_domovni, nazev_momc, cislo_orientacni, psc, nazev_obce, nazev_casti_obce, nazev_mop'
    query = "SELECT {0} FROM {1} WHERE ST_DWithin({2},ST_GeomFromText('POINT({3} {4})',5514),{5});".format(
        fieldlist, 'test', 'the_geom', str(y), str(x), str(distance))
    cur.execute(query)
    rows = cur.fetchall()
    addresses = []
    for row in rows:
        adr = Address(
            (none_to_string(row[0]).decode("utf-8")), (none_to_string(row[1]).decode("utf-8")),
            (none_to_string(row[2]).decode("utf-8")), (none_to_string(row[3]).decode("utf-8")), '',
            (none_to_string(row[4]).decode("utf-8")), (none_to_string(row[5]).decode("utf-8")),
            (none_to_string(row[6]).decode("utf-8")), (none_to_string(row[7]).decode("utf-8")))
        addresses.append(adr)
    return addresses


def _validate_address(dictionary):
    # first = True
    con = psycopg2.connect(
        host=config.databaseHost,
        database=config.databaseName,
        port=config.databasePort,
        user=config.databaseUserName,
        password=config.databasePassword)
    cur = con.cursor()
    query = "SELECT * FROM {0} WHERE ".format('test')
    add_to_query(dictionary, query)
    cur.execute(query)
    row = cur.fetchone()
    if row:
        return True
    else:
        return False


def _find_coordinates(identifier):
    con = psycopg2.connect(
        host=config.databaseHost,
        database=config.databaseName,
        port=config.databasePort,
        user=config.databaseUserName,
        password=config.databasePassword)
    cur = con.cursor()
    cur.execute("SELECT {0}, {1} FROM {2} WHERE {3} = {4}".format(
        'latitude', 'longitude', 'test', 'gid', str(identifier)))
    row = cur.fetchone()
    if row:
        c = Coordinates(str(row[0]), str(row[1]))
        return [c]
    else:
        return []


def _find_coordinates_by_address(dictionary):
    # first = True
    con = psycopg2.connect(
        host=config.databaseHost,
        database=config.databaseName,
        port=config.databasePort,
        user=config.databaseUserName,
        password=config.databasePassword)
    cur = con.cursor()
    query = "SELECT {0}, {1} FROM {2} WHERE ".format('latitude', 'longitude', 'test')
    add_to_query(dictionary, query)

    cur.execute(query)
    rows = cur.fetchall()
    coordinates = []

    for row in rows:
        coordinates.append(Coordinates(str(row[0]), str(row[1])))
    return coordinates


class PostGISDatabase:
    DATABASE_HOST = "192.168.1.93"
    PORT = "5432"
    DATABSE_NAME = "adresni_misto"
    USER_NAME = "postgres"
    PASSWORD = "postgres"

    def __init__(self):
        self.conection = psycopg2.connect(
            host=self.DATABASE_HOST,
            database=self.DATABSE_NAME,
            port=self.PORT,
            user=self.USER_NAME,
            password=self.PASSWORD)

    def get_query_result(self, query):
        cursor = self.conection.cursor()
        cursor.execute(query)

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row)
        return rows

    def get_obec_by_name(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT {0} FROM {0} WHERE {1} like '%{2}%'".format('obce', 'nazev_obce', name))
        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            data = row[0]
            data = data[1:len(data) - 1]
            rows.append(data)
        return rows


def main():
    db = PostGISDatabase()
    print("Králův Dvůr:")
    print(db.get_obec_by_name("Králův Dvůr"))
    print("Krá:")
    print(db.get_obec_by_name("Krá"))
    del db
    print("Done")


if __name__ == '__main__':
    main()

# create table obce
# as
# select nazev_obce, psc from addresspoints group by nazev_obce, psc order by nazev_obce, psc
