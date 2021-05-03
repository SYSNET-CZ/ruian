# -*- coding: utf-8 -*-
# Creates supporting tables for full text search and autocomplete functions
# Contributor: Radim Jäger, 2021. Consolidated for Python 3

__author__ = 'raugustyn'

import codecs
import os
import sys

import psycopg2
import sqlparse
from sqlparse import tokens

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


def exec_complex_sql_script(sql_items, test=False):
    logger.info("   Executing SQL statements {}".format(''))
    out = False
    connection = open_connection(test=test)
    cursor = connection.cursor()
    try:
        for sql_item in sql_items:
            logger.info("   Executing SQL statement: {}".format(sql_item))
            if sql_item != '':
                cursor.execute(sql_item)
                connection.commit()
        out = True
    except psycopg2.Error as e:
        log_psycopg2_error(e)
        logger.error("   Executing SQL statements: {}".format(str(e)))
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
    logger.info("   Executing SQL statements - done.")
    return out


def load_sql_script_file(sql_file_name, msg='load_sql_script_file', exit_if_file_not_found=True):
    logger.info(msg)
    ignore = {'CREATE FUNCTION'}  # extend this

    def _filter(statement, allow=0):
        ddl = [t for t in statement.tokens if t.ttype in (tokens.DDL, tokens.Keyword)]
        start = ' '.join(d.value for d in ddl[:2])
        if ddl and start in ignore:
            allow = 1
        for tok in statement.tokens:
            if allow or not isinstance(tok, sqlparse.sql.Comment):
                yield tok

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
    raw = in_file.read()
    in_file.close()
    statements = []
    for stmt in sqlparse.split(raw):
        sql = sqlparse.parse(stmt)[0]
        tl = sqlparse.sql.TokenList([t for t in _filter(sql)])
        statements.append(tl.value)
    logger.info("   Loading SQL commands - done.")
    return statements


def exec_sql_script_file(sql_file_name, msg='exec_sql_script_file', exit_if_file_not_found=True, test=False):
    logger.info(msg)
    statements = load_sql_script_file(sql_file_name=sql_file_name, exit_if_file_not_found=exit_if_file_not_found)
    return exec_complex_sql_script(sql_items=statements, test=test)


def create_temp_table(connection):
    logger.info("Creating table ac_gids")
    cursor = connection.cursor()
    try:
        cursor.execute('drop table if exists {0};'.format('ac_gids'))
        cursor.execute('CREATE TABLE {0} ({1} integer NOT NULL, {2} text);'.format(
            'ac_gids', 'gid', 'address'))
        logger.info("Done.")
    finally:
        cursor.close()


def get_address_rows(connection):
    logger.info("Retrieving address rows")
    cursor = connection.cursor()
    try:
        query = 'select {0}, cast({1} AS {11}), {2}, cast({3} AS {11}), cast({4} AS {11}), {5}, {6}, {7}, {8}, {9} from {10} '.format(
            'nazev_ulice', 'cislo_domovni', 'nazev_obce', 'psc', 'cislo_orientacni', 'znak_cisla_orientacniho',
            'nazev_casti_obce', 'typ_so', 'nazev_mop', 'gid', 'address_points', 'TEXT'
        )
        cursor.execute(query)
        logger.info("Done.")
        return cursor
    except psycopg2.Error:
        logger.error("Error:Selecting address rows failed.")
        exit_app()


def rename_temp_table(connection_item):
    logger.info("Renaming table _ac_gids to ac_gids.")
    cursor_item = connection_item.cursor()
    cursor_item.execute('drop table if exists ac_gids;')
    cursor_item.execute('alter table _ac_gids rename to ac_gids;')
    cursor_item.close()
    logger.info("Done.")


def build_towns_no_streets(test=False):
    def _get_rows(connection_item):
        sys.stdout.write("Retrieving records to be processes")
        cursor_item = connection_item.cursor()
        try:
            query = 'select {0}, {1}, {2} from {3} group by {1}, {0}, {2} order by {1}, {0}, {2}'.format(
                'nazev_ulice', 'nazev_casti_obce', 'nazev_obce', 'address_points', )
            cursor_item.execute(query)
            print(" - done.")
            return cursor_item
        except psycopg2.Error:
            print('Error: Selecting towns with no streets failed.')
            logger.error('Selecting towns with no streets failed.')
            exit_app()

    print("Building table ac_townsnostreets")
    print("------------------------")
    connection = None
    try:
        connection = open_connection(test=test)
        cursor = _get_rows(connection)
        try:
            if cursor is None:
                return
            print("Inserting rows")
            print("----------------------")
            insert_cursor = connection.cursor()

            def insert_row(nazev_casti_obce_txt, nazev_obce_txt):
                insert_sql = "INSERT INTO {0} ({1}, {2}) VALUES ('{3}', '{4}')".format(
                    'ac_townsnostreets', 'nazev_casti_obce', 'nazev_obce', nazev_casti_obce_txt, nazev_obce_txt)
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
            if cursor is not None:
                cursor.close()
    except psycopg2.Error as e:
        log_psycopg2_error(e)
        logger.error(str(e))
        exit_app()
        pass
    finally:
        if connection is not None:
            connection.close()


def build_gi_ds_table(test=False):
    insert_sql = None
    logger.info("Building table ac_gids")
    logger.info("------------------------")
    connection = open_connection(test=test)
    out = False
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
                    insert_sql = "INSERT INTO {0} ({1}, {2}) VALUES ({3}, '{4}')".format(
                        'ac_gids', 'gid', 'address', gid, row_label)
                    insert_cursor.execute(insert_sql)
                    connection.commit()
                    if gauge_count >= 1000:
                        gauge_count = 0
                        logger.info(str(row_count) + " rows")
                    out = True
                except psycopg2.Error as e:
                    log_psycopg2_error(e)
                    logger.error(str(row_count) + " " + insert_sql + " failed. ")
                    exit_app()
                    out = False
                    pass
            logger.info("Done - %d rows inserted." % row_count)
        finally:
            cursor.close()
        # renameTempTable(connection)
        logger.info("Building table ac_gids done.")
    finally:
        connection.close()
        return out


class SQLInfo:
    def __init__(self, file_name, description, exit_if_script_not_found=True):
        self.fileName = file_name
        self.description = description
        self.exitIfScriptNotFound = exit_if_script_not_found


def sql_files_post_import():
    file_name_list = [
        SQLInfo("remove_duplicates.sql", "Remove duplicities")
    ]
    return file_name_list


def sql_files_service():
    file_name_list = [
        SQLInfo("typ_st_objektu.sql", "Table typ_st_objektu"),
        SQLInfo("address_points.sql", "Table address_points"),
        SQLInfo("full_text.sql", "Table fulltext"),
        SQLInfo("explode_array.sql", "Table explode_array"),
        SQLInfo("gids.sql", "Table gids"),
        SQLInfo("after_import.sql", "User SQL commands after_import.sql", False)
    ]
    return file_name_list


def sql_files_geolocation():
    file_name_list = [
        SQLInfo("ad_ku.sql", "Reverse geolocation table administrative_division_ku"),
        SQLInfo("ad_zsj.sql", "Reverse geolocation table administrative_division_zsj"),
        SQLInfo("ad_parcely.sql", "Reverse geolocation table administrative_division"),
        SQLInfo("autocomplete_tables.sql", "Autocomplete tables.")
    ]
    return file_name_list


def execute_sql_script_list(sql_script_list, test=False):
    if sql_script_list is None:
        return False
    out = True
    for sql_info in sql_script_list:
        reply = exec_sql_script_file(sql_info.fileName, sql_info.description, sql_info.exitIfScriptNotFound, test=test)
        out = out and reply
    return out


def post_import(test=False):
    return execute_sql_script_list(sql_script_list=sql_files_post_import(), test=test)


def build_services_tables(test=False):
    return execute_sql_script_list(sql_script_list=sql_files_service(), test=test)


def build_autocomplete_tables(test=False):
    out = execute_sql_script_list(sql_script_list=sql_files_geolocation(), test=test)
    reply = build_gi_ds_table(test=test)
    return out and reply


def build_all(test=False):
    post_import(test=test)
    build_services_tables(test=test)
    build_autocomplete_tables(test=test)
    pass


if __name__ == '__main__':
    build_all()
