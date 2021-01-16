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
from os.path import join
from subprocess import call

import build_html_log
import shared
import shared_tools.log as log
from shared_tools.configuration import ruian_importer_config, get_data_dir_full_path, Configuration
from shared_tools.base import path_with_last_slash, extract_file_name2, \
    RUNS_ON_WINDOWS, RUNS_ON_LINUX, COMMAND_FILE_EXTENSION, setup_utf

shared.setup_paths()

help_str = """
Import VFR data to database.

Requires: Python 2.7.5 or later
          OS4Geo with WFS Support (http://geo1.fsv.cvut.cz/landa/vfr/OSGeo4W_vfr.zip)

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
    "http://www.vugtk.cz/euradin/VFRLibrary/OSGeo4W_vfr_1.9.73.zip",
    "https://github.com/ctu-geoforall-lab/gdal-vfr/archive/master.zip"
][RUNS_ON_LINUX]
LIST_FILE_TAIL = "_list.txt"

config = Configuration()  # type: Configuration


def create_command_file(file_name_base, commands):
    """Creates either fileNameBase.bat file_instance or fileNameBase.sh file_instance, depending on the operating system.
    If runs on Linux, then chmod 777 fileName is applied.

    :param file_name_base: Base of the command script file_instance name.
    :param commands: Context of the command file_instance.
    :return:
    """
    print("create_command_file - START")

    assert isinstance(file_name_base, basestring)
    assert isinstance(commands, basestring)

    file_name = file_name_base + COMMAND_FILE_EXTENSION
    file_instance = open(file_name, "w")

    if RUNS_ON_LINUX:
        file_instance.write("#!/usr/bin/env bash\n")
    file_instance.write(commands)
    if RUNS_ON_LINUX:
        os.chmod(file_name, 0o777)

    file_instance.close()
    print("createCommandFile - END")
    return file_name


def join_paths(base_path, relative_path):
    assert isinstance(base_path, basestring)
    assert isinstance(relative_path, basestring)

    base_path = base_path.replace("/", os.sep)
    relative_path = relative_path.replace("/", os.sep)
    if os.path.exists(relative_path):
        return relative_path
    else:
        basePathItems = base_path.split(os.sep)
        relativePathItems = relative_path.split(os.sep)
        endBaseIndex = len(basePathItems)
        startRelative = 0
        for subPath in relativePathItems:
            if subPath == "..":
                endBaseIndex = endBaseIndex - 1
                startRelative = startRelative + 1
            elif subPath == ".":
                startRelative = startRelative + 1
            else:
                break

        fullPath = os.sep.join(basePathItems[:endBaseIndex]) + os.sep + os.sep.join(relativePathItems[startRelative:])
        return fullPath


def get_osgeo_path():
    #    if RUNS_ON_WINDOWS:
    #        path = config.WINDOWS_os4GeoPath
    #    else:
    #        path = config.LINUX_vfr2pgPath
    #
    #    return joinPaths(os.path.dirname(__file__), path)
    path = config.GDAL_VFR_PATH
    return path


def convert_file_to_download_lists(http_list_name):
    print("convertFileToDownloadLists - START")
    assert isinstance(http_list_name, basestring)

    result = []

    inFile = open(http_list_name, "r")
    try:
        fileName = (http_list_name[:http_list_name.find(".txt")]) + LIST_FILE_TAIL
        outFile = open(fileName, "w")
        result.append(fileName)
        linesInFile = 0
        for line in inFile:
            linesInFile = linesInFile + 1
            if DEMO_MODE and linesInFile > 3:
                continue

            line = line[line.rfind("/") + 1:line.find("\n")]
            outFile.write(line + "\n")

        outFile.close()
    finally:
        inFile.close()

    print("convertFileToDownloadLists - END")
    return result


def build_download_batch(file_list_file_name, file_names):
    print("buildDownloadBatch - START")

    assert isinstance(file_list_file_name, basestring)
    assert os.path.exists(file_list_file_name)
    assert isinstance(file_names, list)

    commandFileName = None
    path = os.path.dirname(file_list_file_name)
    os4GeoPath = get_osgeo_path()

    (vfr_log_file_name, vfr_err_file_name) = build_html_log.get_log_file_names(file_list_file_name)
    commands = "cd %s\n" % path
    overwriteCommand = "--o"
    for fileName in file_names:

        vfrCommand = "vfr2pg --file %s --host %s --dbname %s --user %s --passwd %s %s" % (
            extract_file_name2(fileName), config.host, config.dbname, config.user, config.password, overwriteCommand)

        if RUNS_ON_WINDOWS:
            importCmd = "call %s %s" % (os4GeoPath, vfrCommand)
        else:
            importCmd = "%s%s  2>>%s 3>>%s" % (os4GeoPath, vfrCommand, vfr_log_file_name, vfr_err_file_name)

        if config.layers != "":
            importCmd += " --layer " + config.layers

        log.logger.debug(importCmd)
        commands += importCmd + "\n"
        overwriteCommand = "--append"

        commandFileName = create_command_file(path + os.sep + "Import", commands)

    print("buildDownloadBatch - END")
    return commandFileName, vfr_log_file_name, vfr_err_file_name


def delete_files_in_lists(path, file_lists, extension):
    assert isinstance(path, basestring)
    assert os.path.exists(path)
    assert isinstance(file_lists, list)
    assert isinstance(extension, basestring)

    path = path_with_last_slash(path)
    for fileList in file_lists:
        listFile = open(fileList, "r")
        i = 0
        for line in listFile:
            i += 1
            fileName = path + line.rstrip() + extension
            if os.path.exists(fileName):
                os.remove(fileName)
            log.logger.debug(str(i), ":", fileName)
        listFile.close()
        os.remove(fileList)


def create_state_database(path, file_list_file_name):
    assert isinstance(path, basestring)
    assert isinstance(file_list_file_name, basestring)

    log.logger.info("Načítám stavovou databázi ze seznamu " + file_list_file_name)
    GDALFileListNames = convert_file_to_download_lists(file_list_file_name)
    downloadBatchFileName, VFRlogFileName, VFRerrFileName = build_download_batch(file_list_file_name, GDALFileListNames)

    log.logger.info("Spouštím %s, průběh viz. %s a %s." % (downloadBatchFileName, VFRlogFileName, VFRerrFileName))
    call(downloadBatchFileName)
    delete_files_in_lists(path, GDALFileListNames, ".xml.gz")
    os.remove(downloadBatchFileName)
    rename_file(file_list_file_name, "__")


def extract_dates_and_type(patch_file_name):
    assert isinstance(patch_file_name, basestring)
    print("extractDatesAndType - START (" + patch_file_name + ")")

    def get_date(line_item):
        result = line_item[line_item.rfind("/") + 1:]
        result = result[:result.find("_")]
        return result

    def get_type(line_item):
        line_type_item = line_item[line_item.rfind("/") + 1:]
        line_type_item = line_type_item[line_type_item.find("_") + 1:line_type_item.find(".")]
        return line_type_item

    startDate = ""
    endDate = ""
    line_type = ""

    in_file = open(patch_file_name, "r")
    first_line = True
    for line in in_file:
        if first_line:
            endDate = get_date(line)
            line_type = get_type(line)
            first_line = False
        else:
            startDate = get_date(line)
    in_file.close()

    print("extractDatesAndType - END")
    return startDate, endDate, line_type


def rename_file(file_name, prefix):
    assert isinstance(file_name, basestring)
    assert isinstance(prefix, basestring)

    parts = file_name.split(os.sep)
    result_parts = parts[:len(parts) - 1]
    result_parts.append(prefix + parts[len(parts) - 1])

    new_file_name = os.sep.join(result_parts)
    if os.path.exists(new_file_name):
        os.remove(new_file_name)

    os.rename(file_name, new_file_name)
    return new_file_name


def update_database(update_file_name):
    assert isinstance(update_file_name, basestring)
    print("updateDatabase - START (" + update_file_name + ")")

    def remove_data_files():
        data_path = path_with_last_slash(os.path.split(update_file_name)[0])
        in_file = open(update_file_name, "r")
        try:
            for line in in_file:
                file_name = os.path.basename(line)
                if os.path.exists(data_path + file_name):
                    os.remove(data_path + file_name)
        finally:
            in_file.close()
        pass

    log.logger.info("Importing update data from " + update_file_name)

    (startDate, endDate, data_type) = extract_dates_and_type(update_file_name)
    log.logger.info("\tPočáteční datum:" + startDate)
    log.logger.info("\tKonečné datum:" + endDate)
    log.logger.info("\tTyp dat:" + data_type)

    os4GeoPath = os.path.join(get_osgeo_path(), "vfr2pg")

    (VFRlogFileName, VFRerrFileName) = build_html_log.get_log_file_names(update_file_name)

    params = ' '.join([os4GeoPath,
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
    batchFileName = create_command_file(os.path.dirname(os.path.abspath(update_file_name)) + os.sep + "Import", commands)

    call(batchFileName)
    os.remove(batchFileName)
    remove_data_files()

    rename_file(update_file_name, "__")
    log.logger.info("Import update data done.")
    print("updateDatabase - END")


def process_downloaded_directory(path):
    print("processDownloadedDirectory - START")
    assert isinstance(path, basestring)

    log.logger.info("Načítám stažené soubory do databáze...")
    log.logger.info("--------------------------------------")
    log.logger.info("Zdrojová data : " + path)

    path = path_with_last_slash(path)
    stateFileList = ""
    updatesFileList = []
    for file_item in os.listdir(path):
        if file_item.endswith(".txt"):
            if file_item.startswith("Download_") and not file_item.endswith(LIST_FILE_TAIL):
                stateFileList = join(path, file_item)
                log.logger.info("Download: " + join(path, file_item))
            elif file_item.startswith("Patch_"):
                updatesFileList.append(join(path, file_item))
                log.logger.info("Patch: " + join(path, file_item))
    result = False
    if stateFileList != "":
        create_state_database(path, stateFileList)
        result = True
    else:
        log.logger.info("Stavová data nejsou obsahem zdrojových dat.")

    if len(updatesFileList) == 0:
        log.logger.info("Denní aktualizace nejsou obsahem zdrojových dat.")
    else:
        result = True
        for updateFileName in updatesFileList:
            update_database(updateFileName)
            sys.stdout.write("u")

    log.logger.info(u"Generuji sestavu importů.")
    build_html_log.build_html_log()

    log.logger.info("Načítání stažených souborů do databáze - hotovo.")
    print("processDownloadedDirectory - END")
    return result


def get_full_path(config_file_name, path):
    assert isinstance(config_file_name, basestring)
    assert isinstance(path, basestring)

    if not os.path.exists(path):
        path = path_with_last_slash(config_file_name) + path
    return path


def do_import(argv):
    global config

    print("doImport - START")
    setup_utf()

    config = ruian_importer_config()
    config.load_from_command_line(argv, help_str)
    log.create_logger(get_data_dir_full_path() + "Download.log")
    log.logger.info("Importing VFR data to database.")

    os_geo_path = get_osgeo_path()
    if not os.path.exists(os_geo_path):
        print("Error: RUIAN import library %s doesn't exist" % os_geo_path)
        print(
                "Download file %s, expand it into RUIANToolbox base directory and run script again." % RUIAN2PG_LIBRARY_ZIP_URL)
        sys.exit()

    rebuild_auxiliary_tables = process_downloaded_directory(get_data_dir_full_path())

    if config.build_services_tables and rebuild_auxiliary_tables:
        from ruian_services.services.auxiliary_tables import build_all, build_services_tables
        if config.build_autocomplete_tables:
            print("doImport buildAll - START")
            build_all()
            print("doImport buildAll - END")
        else:
            print("doImport buildServicesTables - START")
            build_services_tables()
            print("doImport buildServicesTables - END")

    from ruian_services.services.ruian_connection import save_ruian_version_date_today
    print("call saveRUIANVersionDateToday() - START")
    save_ruian_version_date_today()
    print("call saveRUIANVersionDateToday() - END")
    print("doImport - END")


if __name__ == "__main__":
    do_import(sys.argv)
