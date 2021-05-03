# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        import_ruian
# Purpose:     Imports VFR data downloaded directory
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------
import os
import sys
from subprocess import call

import shared_tools.log as log
from importer import build_html_log
from ruian_services.services.auxiliary_tables import post_import
from ruian_services.services.geolocation import save_ruian_version_date_today
from shared_tools import shared
from shared_tools.base import extract_file_name2, \
    RUNS_ON_WINDOWS, RUNS_ON_LINUX, COMMAND_FILE_EXTENSION, setup_utf
from shared_tools.configuration import ruian_importer_config, get_data_dir_full_path, Configuration

shared.setup_paths()

help_str = """
Import VFR data to database.

Requires: Python 3.8.0 or later
          OS4Geo with WFS Support (https://geo1.fsv.cvut.cz/landa/vfr/OSGeo4W_vfr.zip)

Usage: ImportRUIAN.py [-dbname <database name>] [-host <host name>] [-port <database port>] [-user <user name>]
                      [-password <database password>] [-layers layer1,layer2,...] [-os4GeoPath <path>]
                      [-buildServicesTables <{True} {False}>] [-buildAutocompleteTables <{True} {False}>] [-help]')

       -dbname
       -host
       -port
       -user
       -password
       -layers
       -os4GeoPath
       -buildServicesTables
       -buildAutocompleteTables
       -Help         Print help
"""

DEMO_MODE = False  # If set to true, there will be just few rows in every state database import lines applied.

RUIAN2PG_LIBRARY_ZIP_URL = [
    "https://www.vugtk.cz/euradin/VFRLibrary/OSGeo4W_vfr_1.9.73.zip",
    "https://github.com/ctu-geoforall-lab/gdal-vfr/archive/master.zip"
][RUNS_ON_LINUX]
LIST_FILE_TAIL = "_list.txt"

config = Configuration()  # type: Configuration


def create_command_file(file_name_base, commands):
    """
    Creates either fileNameBase.bat file_instance or fileNameBase.sh file_instance, depending on the operating system.
    If runs on Linux, then chmod 777 fileName is applied.

    :param file_name_base: Base of the command script file_instance name.
    :param commands: Context of the command file_instance.
    :return:
    """
    print("create_command_file - START")

    assert isinstance(file_name_base, (str, bytes))
    assert isinstance(commands, (str, bytes))

    file_name = file_name_base + COMMAND_FILE_EXTENSION
    file_instance = open(file_name, "w")

    if RUNS_ON_LINUX:
        # file_instance.write("#!/usr/bin/env bash\n")
        file_instance.write("#!/bin/bash\n")

    file_instance.write(commands)
    if RUNS_ON_LINUX:
        os.chmod(file_name, 0o777)

    file_instance.close()
    print("create_command_file - END")
    return file_name


def get_osgeo_path():
    #    if RUNS_ON_WINDOWS:
    #        path = config.WINDOWS_os4GeoPath
    #    else:
    #        path = config.LINUX_vfr2pgPath
    #
    #    return joinPaths(os.path.dirname(__file__), path)
    path = config.GDAL_VFR_PATH
    return path


# Převede obsah souboru Download_<rrrr.mm.dd>.txt do souboru se seznamem názvů souborů
def convert_file_to_download_lists(http_list_name):
    print("convertFileToDownloadLists - START")
    assert isinstance(http_list_name, (str, bytes))

    result = []
    in_file = open(http_list_name, "r")
    try:
        file_name = (http_list_name[:http_list_name.find(".txt")]) + LIST_FILE_TAIL
        out_file = open(file_name, "w")
        result.append(file_name)
        lines_in_file = 0
        for line in in_file:
            lines_in_file = lines_in_file + 1
            if DEMO_MODE and lines_in_file > 3:
                continue
            line = line[line.rfind("/") + 1:line.find("\n")]
            out_file.write(line + "\n")
        out_file.close()
        log.logger.info("convert_file_to_download_lists - seznam názvů souborů: {0}".format(file_name))

    finally:
        in_file.close()

    print("convertFileToDownloadLists - END")
    return result


def build_download_batch(file_list_file_name, file_names):
    print('buildDownloadBatch - START')

    assert isinstance(file_list_file_name, (str, bytes))
    assert os.path.exists(file_list_file_name)
    assert isinstance(file_names, list)

    command_file_name = None
    path = os.path.dirname(file_list_file_name)
    os4geo_path = get_osgeo_path()

    (vfr_log_file_name, vfr_err_file_name) = build_html_log.get_log_file_names(file_list_file_name)
    commands = 'cd {0}\n'.format(path)
    overwrite_command = '--o'
    for file_name in file_names:
        fnc = os.path.join(path, file_name)
        do_it = False
        if os.path.exists(fnc):
            do_it = True
        else:
            if os.path.exists(fnc + "'"):
                file_name += "'"
                do_it = True
        if do_it:
            vfr_command = 'vfr2pg --file {0} --host {1} --dbname {2} --user {3} --passwd {4} {5}'.format(
                extract_file_name2(file_name), config.host, config.dbname, config.user, config.password,
                overwrite_command)

            if RUNS_ON_WINDOWS:
                import_cmd = 'call {0}\\{1}'.format(os4geo_path, vfr_command)
            else:
                import_cmd = '{0}/{1}  2>>{2} 3>>{3}'.format(
                    os4geo_path, vfr_command, vfr_log_file_name, vfr_err_file_name)
            if config.layers != '':
                import_cmd += ' --layer ' + config.layers

            log.logger.debug(import_cmd)
            commands += import_cmd + '\n'
            overwrite_command = '--append'
            command_file_name = create_command_file(os.path.join(path, 'Import'), commands)
    print('buildDownloadBatch - END')
    return command_file_name, vfr_log_file_name, vfr_err_file_name


def delete_files_in_lists(path, file_lists, extension):
    assert isinstance(path, (str, bytes))
    assert os.path.exists(path)
    assert isinstance(file_lists, list)
    assert isinstance(extension, (str, bytes))

    # path = path_with_last_slash(path)
    for file_list in file_lists:
        list_file = open(file_list, "r")
        i = 0
        for line in list_file:
            i += 1
            file_name = os.path.join(path, line.rstrip() + extension)
            if os.path.exists(file_name):
                os.remove(file_name)
            log.logger.debug(str(i), ":", file_name)
        list_file.close()
        os.remove(file_list)


def create_state_database(path, file_list_file_name):
    assert isinstance(path, (str, bytes))
    assert isinstance(file_list_file_name, (str, bytes))

    log.logger.info("Načítám stavovou databázi ze seznamu " + file_list_file_name)
    gdal_file_list_names = convert_file_to_download_lists(file_list_file_name)
    download_batch_file_name, vf_rlog_file_name, vf_rerr_file_name = build_download_batch(
        file_list_file_name, gdal_file_list_names)

    log.logger.info(
        "Spouštím %s, průběh viz. %s a %s." % (download_batch_file_name, vf_rlog_file_name, vf_rerr_file_name))
    call(download_batch_file_name)
    delete_files_in_lists(path, gdal_file_list_names, ".xml.gz")
    os.remove(download_batch_file_name)
    rename_file(file_list_file_name, "__")


def extract_dates_and_type(patch_file_name):
    assert isinstance(patch_file_name, (str, bytes))
    print("extractDatesAndType - START (" + patch_file_name + ")")

    def get_date(line_item):
        result = line_item[line_item.rfind("/") + 1:]
        result = result[:result.find("_")]
        return result

    def get_type(line_item):
        line_type_item = line_item[line_item.rfind("/") + 1:]
        line_type_item = line_type_item[line_type_item.find("_") + 1:line_type_item.find(".")]
        return line_type_item

    start_date = ""
    end_date = ""
    line_type = ""

    in_file = open(patch_file_name, "r")
    first_line = True
    for line in in_file:
        if first_line:
            end_date = get_date(line)
            line_type = get_type(line)
            first_line = False
        else:
            start_date = get_date(line)
    in_file.close()

    print("extractDatesAndType - END")
    return start_date, end_date, line_type


def rename_file(file_name, prefix):
    assert isinstance(file_name, (str, bytes))
    assert isinstance(prefix, (str, bytes))

    parts = file_name.split(os.sep)
    result_parts = parts[:len(parts) - 1]
    result_parts.append(prefix + parts[len(parts) - 1])

    new_file_name = os.sep.join(result_parts)
    if os.path.exists(new_file_name):
        os.remove(new_file_name)

    os.rename(file_name, new_file_name)
    return new_file_name


def update_database(update_file_name):
    assert isinstance(update_file_name, (str, bytes))
    print("updateDatabase - START (" + update_file_name + ")")

    def remove_data_files():
        data_path = os.path.split(update_file_name)[0]
        in_file = open(update_file_name, "r")
        try:
            for line in in_file:
                file_name = os.path.basename(line)
                if os.path.exists(os.path.join(data_path, file_name)):
                    os.remove(os.path.join(data_path, file_name))
        finally:
            in_file.close()
        pass

    log.logger.info("Importing update data from " + update_file_name)

    (startDate, endDate, data_type) = extract_dates_and_type(update_file_name)
    log.logger.info("\tPočáteční datum:" + startDate)
    log.logger.info("\tKonečné datum:" + endDate)
    log.logger.info("\tTyp dat:" + data_type)

    os4geo_path = os.path.join(get_osgeo_path(), "vfr2pg")

    (VFRlogFileName, VFRerrFileName) = build_html_log.get_log_file_names(update_file_name)

    params = ' '.join([os4geo_path,
                       "--host", config.host,
                       "--dbname", config.dbname,
                       "--user ", config.user,
                       "--passwd ", config.password,
                       "--date", startDate + ":" + endDate,
                       "--type", data_type])

    if config.layers != "":
        params += " --layer " + config.layers

    if RUNS_ON_WINDOWS:
        params += " >%s 2>%s" % (VFRlogFileName, VFRerrFileName)
    else:
        params += " 2>%s 3>%s" % (VFRlogFileName, VFRerrFileName)

    commands = "cd " + os.path.dirname(os.path.abspath(update_file_name)) + "\n"
    commands += params + "\n"
    batch_file_name = create_command_file(
        os.path.dirname(os.path.abspath(update_file_name)) + os.sep + "Import", commands)

    call(batch_file_name)
    os.remove(batch_file_name)
    remove_data_files()

    rename_file(update_file_name, "__")
    log.logger.info("Import update data done.")
    print("updateDatabase - END")


def process_downloaded_directory(path):
    print("processDownloadedDirectory - START")
    assert isinstance(path, (str, bytes))

    log.logger.info("Načítám stažené soubory do databáze...")
    # log.logger.info("--------------------------------------")
    log.logger.info("Zdrojová data : " + path)

    path = str(path)   # path_with_last_slash(path)
    state_file_name = ''
    updates_file_list = []
    # najit stavové soubory se seznamem ke zpracování
    for file_item in os.listdir(path):
        if file_item.endswith('.txt'):
            if file_item.startswith('Download_') and not file_item.endswith(LIST_FILE_TAIL):
                state_file_name = os.path.join(path, file_item)  # stavový soubor
                log.logger.info('Download: ' + os.path.join(path, file_item))
            elif file_item.startswith('Patch_'):
                updates_file_list.append(os.path.join(path, file_item))  # soubory s aktualizacemi
                log.logger.info('Patch: ' + os.path.join(path, file_item))
    result = False
    if state_file_name != '':
        create_state_database(path, state_file_name)  # vytvořit stavovou databázi
        result = True
    else:
        log.logger.info('Stavová data nejsou obsahem zdrojových dat.')

    if len(updates_file_list) == 0:
        log.logger.info('Denní aktualizace nejsou obsahem zdrojových dat.')
    else:
        result = True
        for updateFileName in updates_file_list:
            update_database(updateFileName)  # aktualizovat datrabázi
            sys.stdout.write("u")

    log.logger.info(u"Generuji sestavu importů.")
    build_html_log.build_html_log()

    log.logger.info("Načítání stažených souborů do databáze - hotovo.")
    print("processDownloadedDirectory - END")
    return result


def do_import(argv):
    global config

    print("do_import - START")
    setup_utf()  # does nothing in Python 3

    config = ruian_importer_config()
    config.load_from_command_line(argv, help_str)
    log.create_logger(os.path.join(get_data_dir_full_path(), 'Import.log'))
    log.logger.info("Importing VFR data to database.")

    os_geo_path = get_osgeo_path()
    if not os.path.exists(os_geo_path):
        print("Error: RUIAN import library {0} doesn't exist".format(os_geo_path))
        print(
            "Download file {0}, expand it into RUIANToolbox base directory and run script again.".format(
                RUIAN2PG_LIBRARY_ZIP_URL))
        exit()

    # zpracovat stažená data
    rebuild_auxiliary_tables = process_downloaded_directory(get_data_dir_full_path())  # výkonný příkaz

    if config.buildServicesTables and rebuild_auxiliary_tables:
        from ruian_services.services.auxiliary_tables import build_all, build_services_tables
        if config.buildAutocompleteTables:
            print("do_import buildAll - START")
            build_all()
            print("do_import buildAll - END")
        else:
            print("do_import buildServicesTables - START")
            post_import()
            build_services_tables()
            print("do_import buildServicesTables - END")

    print("call saveRUIANVersionDateToday() - START")
    save_ruian_version_date_today()
    print("call saveRUIANVersionDateToday() - END")
    print("do_import - END")


if __name__ == "__main__":
    do_import(sys.argv)
