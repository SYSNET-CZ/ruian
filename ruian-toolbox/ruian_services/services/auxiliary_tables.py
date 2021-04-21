# -*- coding: utf-8 -*-
# Creates supporting tables for full text search and autocomplete functions
# Contributor: Radim Jäger, 2021. Consolidated for Python 3

__author__ = 'raugustyn'

import codecs
import os
import sys

import psycopg2

from ruian_services.services import http_shared, compile_address
from shared_tools import shared
from ruian_services.services.postgis_db import open_connection
from shared_tools.configuration import get_ruian_services_sql_scripts_path
from shared_tools.log import logger

shared.setup_paths()


def exit_app():
    sys.exit()


def log_psycopg2_error(e):
    if e:
        if e.pgerror:
            msg = str(e.pgerror)
        else:
            msg = str(e)
    else:
        msg = "Not specified"
    logger.error("Database error:" + msg)


def exec_sql_script(sql, test=False):
    logger.info("   Executing SQL commands {}".format(''))
    connection = open_connection(test=test)
    cursor = connection.cursor()
    try:
        sql_items = sql.split(";")
        for sql_item in sql_items:
            logger.info("   Executing SQL command: {}".format(sql_item))
            sql_item = sql_item.replace('\n', ' ').replace('\r', '')
            sql_item = sql_item.strip()
            if sql_item != '':
                cursor.execute(sql_item)
                connection.commit()
    except psycopg2.Error as e:
        log_psycopg2_error(e)
        logger.error("   Executing SQL commands: {}".format(str(e)))
    finally:
        cursor.close()
        connection.close()
    logger.info("   Executing SQL commands - done.")
    pass


def exec_sql_script_file(sql_file_name, msg, exit_if_file_not_found=True, test=False):
    logger.info(msg)
    sql_file_name = os.path.join(get_ruian_services_sql_scripts_path(), sql_file_name)
    logger.info("   Loading SQL commands from {0}".format(sql_file_name))

    if not os.path.exists(sql_file_name):
        if exit_if_file_not_found:
            logger.error("ERROR: File %s not found." % sql_file_name)
            exit_app()
        else:
            logger.warning("ERROR: File %s not found." % sql_file_name)
            return

    in_file = codecs.open(sql_file_name, "r", "utf-8")
    sql = in_file.read()
    in_file.close()
    logger.info("   Loading SQL commands - done.")
    exec_sql_script(sql, test=test)


def create_temp_table(connection):
    logger.info("Creating table ac_gids")
    cursor = connection.cursor()
    try:
        cursor.execute("drop table if exists ac_gids;")
        cursor.execute("CREATE TABLE ac_gids (gid integer NOT NULL, address text);")
        logger.info("Done.")
    finally:
        cursor.close()


def get_address_rows(connection):
    logger.info("Retrieving address rows")
    cursor = connection.cursor()
    try:
        query = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text), ' \
                'cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, ' \
                'nazev_mop, gid from address_points '
        cursor.execute(query)
        logger.info("Done.")
        return cursor
    except psycopg2.Error:
        logger.error("Error:Selecting address rows failed.")
        exit_app()


def rename_temp_table(connection_item):
    logger.info("Renaming table _ac_gids to ac_gids.")
    cursor_item = connection_item.cursor()
    cursor_item.execute("drop table if exists ac_gids;alter table _ac_gids rename to ac_gids;")
    cursor_item.close()
    logger.info("Done.")


def build_towns_no_streets(test=False):
    def _get_rows(connection_item):
        sys.stdout.write("Retrieving records to be processes")
        cursor_item = connection_item.cursor()
        try:
            query = 'select nazev_ulice, nazev_casti_obce, nazev_obce ' \
                    'from address_points ' \
                    'group by nazev_casti_obce, nazev_ulice, nazev_obce ' \
                    'order by nazev_casti_obce, nazev_ulice, nazev_obce'
            cursor_item.execute(query)
            print(" - done.")
            return cursor_item
        except psycopg2.Error:
            print("Error:Selecting towns with no streets failed.")
            exit_app()

    print("Building table ac_townsnostreets")
    print("------------------------")
    connection = open_connection(test=test)
    try:
        # _createTable(connection)
        cursor = _get_rows(connection)

        try:
            if cursor is None:
                return

            print("Inserting rows")
            print("----------------------")
            insert_cursor = connection.cursor()

            def insert_row(nazev_casti_obce_txt, nazev_obce_txt):
                insert_sql = "INSERT INTO ac_townsnostreets (nazev_casti_obce, nazev_obce) VALUES ('%s', '%s')" % (
                    nazev_casti_obce_txt, nazev_obce_txt)
                insert_cursor.execute(insert_sql)
                connection.commit()
                pass

            row_count = 0
            gauge_count = 0
            last_nazev_casti_obce = None
            last_nazev_obce = None
            num_streets = 0
            for row in cursor:
                gauge_count += 1
                try:
                    nazev_ulice, nazev_casti_obce, nazev_obce = row

                    if (last_nazev_casti_obce is None or last_nazev_casti_obce == nazev_casti_obce) and (
                            last_nazev_obce is None or last_nazev_obce == nazev_obce):
                        if nazev_ulice is not None and nazev_ulice != "":
                            num_streets = num_streets + 1
                    else:
                        if last_nazev_casti_obce != "":
                            if num_streets == 0:
                                insert_row(nazev_casti_obce, nazev_obce)
                                row_count += 1

                        num_streets = 0
                        last_nazev_casti_obce = None
                        last_nazev_obce = None

                    last_nazev_casti_obce = nazev_casti_obce
                    last_nazev_obce = nazev_obce

                    if gauge_count >= 1000:
                        gauge_count = 0
                        print(str(row_count) + " rows")

                except psycopg2.Error as e:
                    log_psycopg2_error(e)
                    logger.error(str(row_count))
                    exit_app()
                    pass

            print("Done - %d rows inserted." % row_count)

        finally:
            cursor.close()
    finally:
        connection.close()


def build_gi_ds_table(test=False):
    insert_sql = None
    logger.info("Building table ac_gids")
    logger.info("------------------------")
    connection = open_connection(test=test)
    try:
        create_temp_table(connection)
        cursor = get_address_rows(connection)
        try:
            if cursor is None:
                return

            logger.info("Inserting rows")
            logger.info("----------------------")
            insert_cursor = connection.cursor()
            builder = http_shared.MimeBuilder("texttoonerow")
            row_count = 0
            gauge_count = 0

            for row in cursor:
                row_count += 1
                gauge_count += 1
                try:
                    street, house_number, locality, zip_code, orientation_number, orientation_number_character, locality_part, typ_so, nazev_mop, gid = row
                    house_number, record_number = http_shared.analyse_row(typ_so, house_number)
                    district_number = http_shared.extract_dictrict_number(nazev_mop)

                    row_label = compile_address.compile_address(
                        builder, street, house_number, record_number, orientation_number, orientation_number_character,
                        zip_code, locality, locality_part, district_number)
                    insert_sql = "INSERT INTO ac_gids (gid, address) VALUES (%s, '%s')" % (gid, row_label)
                    insert_cursor.execute(insert_sql)
                    connection.commit()
                    if gauge_count >= 1000:
                        gauge_count = 0
                        logger.info(str(row_count) + " rows")

                except psycopg2.Error as e:
                    log_psycopg2_error(e)
                    logger.error(str(row_count) + " " + insert_sql + " failed. ")
                    exit_app()
                    pass

            logger.info("Done - %d rows inserted." % row_count)

        finally:
            cursor.close()

        # renameTempTable(connection)
        logger.info("Building table ac_gids done.")
    finally:
        connection.close()
    pass


class SQLInfo:
    def __init__(self, file_name, description, exit_if_script_not_found=True):
        self.fileName = file_name
        self.description = description
        self.exitIfScriptNotFound = exit_if_script_not_found


def build_services_tables(test=False):
    script_list = [
        SQLInfo("typ_st_objektu.sql", "Table typ_st_objektu"),
        SQLInfo("address_points.sql", "Table address_points"),
        SQLInfo("full_text.sql", "Table fulltext"),
        SQLInfo("explode_array.sql", "Table explode_array"),
        SQLInfo("gids.sql", "Table gids"),
        SQLInfo("administrative_divisions.sql", "Reverse geolocation table administrative_division"),
        SQLInfo("administrative_divisions_ku.sql", "Reverse geolocation table administrative_division_ku"),
        SQLInfo("administrative_divisions_zsj.sql", "Reverse geolocation table administrative_division_zsj"),
        SQLInfo("after_import.sql", "User SQL commands after_import.sql", False)
    ]

    for sql_info in script_list:
        exec_sql_script_file(sql_info.fileName, sql_info.description, sql_info.exitIfScriptNotFound, test=test)


def build_autocomplete_tables(test=False):
    exec_sql_script_file("autocomplete_tables.sql", "Autocomplete tables.", test=test)
    build_gi_ds_table(test=False)


def build_all(test=False):
    build_services_tables(test=test)
    build_autocomplete_tables(test=test)
    pass


if __name__ == '__main__':
    build_all()