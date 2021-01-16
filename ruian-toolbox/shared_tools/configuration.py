# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        config
# Purpose:     Config files persistence classes implementations.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------

import codecs
import os
import sys

import base
import log

S = "ruian"

IMPORT_RUIAN_CFG = os.path.join("config", "ImportRUIAN.cfg")
DOWNLOAD_RUIAN_CFG = os.path.join("config", "DownloadRUIAN.cfg")
OS4GEO_PATH = "/opt/ruian/vfr"
DB_NAME = "ruian"
DB_SCHEMA = "public"
DB_HOSTNAME = "postgis"
DB_PORT = "5432"
DB_USER = "docker"
DB_PASSWORD = "docker"
GIS_LAYERS = "AdresniMista,Ulice,StavebniObjekty,CastiObci,Obce,Mop,Momc"
SERVICE_TABLES = "True"
AUTOCOMPLETE_TABLES = "True"
DOWNLOADED_DATA = "DownloadedData"

x_RUIANDownloadConfig = None
x_RUIANImporterConfig = None
x_RUIANDownloadInfoFile = None
x_RUIANToolboxPath = None
# x_RUIANDownloadInfoFile = None

TRUE_ID = "true"


def bool_to_str(v):
    if v:
        return TRUE_ID
    else:
        return "false"


def str_to_bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def str_to127(s):
    result = ""
    for index in range(len(s)):
        ch = s[index:index + 1]
        if 32 <= ord(ch) <= 127:
            result += ch
    return result


def is_true(value):
    out = False
    if value is not None:
        if isinstance(value, basestring):
            out = value.lower() == TRUE_ID
    return out


def get_sub_dir_path(sub_dir):
    path = os.path.dirname(__file__)
    masterPath = os.path.split(path)[0]
    return base.path_with_last_slash(os.path.join(masterPath, sub_dir))


def get_parent_path(module_file):
    if module_file == "":
        module_file = __file__
    path = os.path.dirname(module_file)
    parentPath = os.path.split(path)[0]
    return base.path_with_last_slash(parentPath)


def get_master_path(module_file):
    path = get_parent_path(module_file)
    masterPath = os.path.split(path)[0]
    return base.path_with_last_slash(masterPath)


class Configuration:
    def __init__(
            self,
            file_name=None,
            attrs=None,
            after_load_proc=None,
            base_path="",
            def_sub_dir="",
            module_file="",
            create_if_not_found=True
    ):
        self.runImporter = None
        self.uncompressDownloadedFiles = None
        self.downloadFullDatabase = None
        self.dataDir = None
        self.ignoreHistoricalData = True
        self.downloadURLs = None
        self.layers = GIS_LAYERS
        self.password = DB_PASSWORD
        self.user = DB_USER
        self.dbname = DB_NAME
        self.host = DB_HOSTNAME
        self.GDAL_VFR_PATH = OS4GEO_PATH
        self.automaticDownloadTime = 0
        self.os4GeoPath = OS4GEO_PATH
        if attrs is None:
            attrs = {}
        if base_path != "":
            base_path = base.path_with_last_slash(base_path)
            if not os.path.exists(base_path):
                log.logger.error("Config.__init__, cesta " + base_path + def_sub_dir + " neexistuje.")
                base_path = ""

        self.fileName = file_name
        if file_name is not None:
            self.fileName = base_path + file_name
        self.afterLoadProc = after_load_proc
        self.attrs = attrs  # Tabulka vsech atributu, jak nactenych, tak povolenych
        self._remapTable = {}  # Tabulka mapovani downloadfulldatabase -> downloadFullDatabase
        self.moduleFile = module_file
        self.createIfNotFound = create_if_not_found
        self.isDefault = True

        if attrs is not None:
            for key in attrs:
                setattr(self, key, attrs[key])
                if key != key.lower():
                    self._remapTable[key.lower()] = key

        if file_name is not None:
            if os.path.exists(base_path + file_name):
                self.fileName = base_path + file_name
            else:
                path = base.normalize_path_sep(os.path.dirname(__file__))
                pathItems = path.split(os.sep)
                for i in range(0, len(pathItems)):
                    path = os.sep.join(pathItems[0:i]) + os.sep + file_name
                    if os.path.exists(path):
                        self.fileName = path
                        break
            if self.fileName == "":
                self.fileName = base_path + file_name
                if create_if_not_found:
                    msg = u"Konfigurační soubor %s nebyl nalezen." % (
                            base.path_with_last_slash(base_path) + self.fileName)
                    log.logger.error(msg)
                    self.save()
                    log.logger.error(
                        u"Soubor byl vytvořen ze šablony. Nastavte prosím jeho hodnoty a spusťte program znovu.")
                    import sys
                    sys.exit()
            else:
                self.load_file()

    def evaluate_data_dir(self):
        if self.dataDir is not None:
            self.dataDir = self.dataDir.replace("/", os.sep)
            self.dataDir = self.dataDir.replace("\\", os.sep)
            self.dataDir = base.path_with_last_slash(self.dataDir)
            if not os.path.isabs(self.dataDir):
                result = os.path.dirname(self.moduleFile) + os.path.sep + self.dataDir
                result = os.path.normpath(result)
                self.dataDir = base.path_with_last_slash(result)

    def load_file(self):
        if os.path.exists(self.fileName):
            file_to_load = codecs.open(self.fileName, "r", "utf-8")
            for line in file_to_load:
                if line.find("#") >= 0:
                    line = line[:line.find("#") - 1]
                line = str_to127(line.strip())
                delPos = line.find("=")
                name = self._get_attr_name(line[:delPos])
                value = line[delPos + 1:]
                self.set_attr(name, value)
                pass

            file_to_load.close()
            if self.afterLoadProc is not None:
                self.afterLoadProc(self)
            self.isDefault = False

    def set_attr(self, name, value):
        name = self._get_attr_name(name)
        setattr(self, name, value)
        self.attrs[name] = value

    def _get_attr_name(self, name):
        name = name.lower()
        if name in self._remapTable:
            return self._remapTable[name]
        else:
            return name

    def get_value(self, name, def_value=""):
        name = self._get_attr_name(name)
        if name in self.attrs:
            return self.attrs[name]
        else:
            return def_value

    def save(self, config_file_name=""):
        if config_file_name != "":
            self.fileName = config_file_name

        pathParts = self.fileName.split(os.sep)
        base.safe_mk_dir(os.sep.join(pathParts[:len(pathParts) - 1]))

        outFile = codecs.open(self.fileName, "w", "utf-8")
        for key in self.attrs:
            name = self._get_attr_name(key)
            value = getattr(self, name)
            outFile.write(name + "=" + str(value) + "\n")
        outFile.close()

    def load_from_command_line(self, argv, usage_message):
        if argv is None:
            pass
        if len(argv) > 1:
            i = 1
            while i < len(argv):
                arg = argv[i].lower()
                if arg.startswith("-"):
                    command = arg[1:]
                    foundCommand = False
                    i = i + 1
                    if i < len(argv):
                        for attrKey in self.attrs:
                            if attrKey == command:
                                self.attrs[attrKey] = argv[i]
                                foundCommand = True

                    if not foundCommand:
                        log.logger.warning('Unrecognised command option: %s' % arg)
                        log.logger.info(usage_message)
                        sys.exit()
                i = i + 1
        pass


def convert_info_file(config):
    if config is None:
        return

    if config.numPatches == "":
        config.numPatches = 0
    else:
        config.numPatches = is_true(config.numPatches)

    config.fullDownloadBroken = is_true(config.fullDownloadBroken)


class InfoFile(Configuration):
    def __init__(self, file_name, def_sub_dir="", module_file=""):
        Configuration.__init__(
            self, "info.txt",
            {
                "lastPatchDownload": "",
                "lastFullDownload": "",
                "numPatches": 0,
                "fullDownloadBroken": "false"
            },
            convert_info_file, "", "RUIANDownloader", module_file, False
        )
        self.fileName = file_name
        self.subDir = def_sub_dir
        self.lastFullDownload = None
        self.lastPatchDownload = None

    def valid_for(self):
        if self.lastPatchDownload != "":
            return self.lastPatchDownload
        else:
            return self.lastFullDownload

    def load(self, file_name):
        self.fileName = file_name
        self.load_file()


def ruian_download_info_file():
    global x_RUIANDownloadInfoFile
    if x_RUIANDownloadInfoFile is None:
        x_RUIANDownloadInfoFile = InfoFile("")
    return x_RUIANDownloadInfoFile


def convert_ruian_download_cfg(config):
    if config is None:
        return
    config.downloadFullDatabase = is_true(config.downloadFullDatabase)
    config.uncompressDownloadedFiles = is_true(config.uncompressDownloadedFiles)
    config.runImporter = is_true(config.runImporter)
    config.evaluate_data_dir()
    config.ignoreHistoricalData = is_true(config.ignoreHistoricalData)
    ruian_download_info_file().load(config.dataDir + "Info.txt")
    pass


def data_dir():
    return os.path.join("..", DOWNLOADED_DATA)


def ruian_download_config():
    global x_RUIANDownloadConfig
    if x_RUIANDownloadConfig is None:
        x_RUIANDownloadConfig = Configuration(
            DOWNLOAD_RUIAN_CFG,
            {
                "downloadFullDatabase": False,
                "uncompressDownloadedFiles": False,
                "runImporter": False,
                "dataDir": data_dir(),
                "downloadURLs": "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=" +
                                "U&vf.up=ST&vf.ds=K&vf.vu=Z&_vf.vu=on&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat;" +
                                "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&" +
                                "vf.up=OB&vf.ds=K&vf.vu=Z&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&vf.uo=A&search=Vyhledat",
                "ignoreHistoricalData": True

            },
            convert_ruian_download_cfg,
            def_sub_dir="downloader",
            module_file=__file__,
            base_path=get_ruian_downloader_path()
        )
        d1 = os.getenv('DOWNLOAD_DATA')
        if d1 is not None:
            if d1 != "":
                x_RUIANDownloadConfig.dataDir = d1
        d2 = os.getenv('RUIAN_DOWNLOAD_DATA')
        if d2 is not None:
            if d2 != "":
                x_RUIANDownloadConfig.dataDir = d2
    return x_RUIANDownloadConfig


def convert_ruian_importer_config(config):
    if config is None:
        return
    config.evaluate_data_dir()
    config.buildServicesTables = is_true(config.buildServicesTables)
    config.buildAutocompleteTables = is_true(config.buildAutocompleteTables)


def ruian_importer_config():
    global x_RUIANImporterConfig
    if x_RUIANImporterConfig is None:
        x_RUIANImporterConfig = Configuration(
            IMPORT_RUIAN_CFG,
            {
                "dbname": DB_NAME,
                "host": DB_HOSTNAME,
                "port": DB_PORT,
                "user": DB_USER,
                "password": DB_PASSWORD,
                "schemaName": DB_SCHEMA,
                "layers": GIS_LAYERS,
                "WINDOWS_os4GeoPath": os.path.join("..", "..", "OSGeo4W_vfr", "OSGeo4W.bat"),
                "LINUX_vfr2pgPath": OS4GEO_PATH,
                "GDAL_VFR_PATH": OS4GEO_PATH,
                "os4GeoPath": OS4GEO_PATH,
                "buildServicesTables": SERVICE_TABLES,
                "buildAutocompleteTables": AUTOCOMPLETE_TABLES,
                "dataDir": data_dir(),
            },
            convert_ruian_importer_config,
            def_sub_dir="importer",
            module_file=__file__,
            base_path=get_ruian_importer_path()
        )
    return x_RUIANImporterConfig


def get_ruian_toolbox_path():
    global x_RUIANToolboxPath
    if x_RUIANToolboxPath is None:
        x_RUIANToolboxPath = base.path_with_last_slash(os.path.split(os.path.dirname(__file__))[0])
        x_RUIANToolboxPath = x_RUIANToolboxPath.replace("/", os.sep)
        x_RUIANToolboxPath = x_RUIANToolboxPath.replace("\\", os.sep)
    return x_RUIANToolboxPath


def get_ruian_importer_path():
    return os.path.join(get_ruian_toolbox_path(), "importer") + os.sep


def get_ruian_downloader_path():
    return os.path.join(get_ruian_toolbox_path(), "downloader") + os.sep


def get_ruian_services_base_path():
    return os.path.join(get_ruian_toolbox_path(), "ruian_services") + os.sep


def get_ruian_services_path():
    return os.path.join(get_ruian_toolbox_path(), "ruian_services", "services") + os.sep


def get_ruian_services_html_path():
    return os.path.join(get_ruian_toolbox_path(), "ruian_services", "HTML") + os.sep


def get_ruian_services_sql_scripts_path():
    return os.path.join(get_ruian_toolbox_path(), "ruian_services", "SqlScripts") + os.sep


def get_data_dir_full_path():
    result = ruian_download_config().dataDir
    if not os.path.isabs(result):
        result = get_ruian_downloader_path() + result
        result = os.path.normpath(result)
        result = base.path_with_last_slash(result)
    return result


def main():
    print "This module is a library, it can't be run as an application."

    if True:
        print "Download Config:", ruian_download_config().fileName
        print "Importer Config:", ruian_importer_config().fileName
        print "getRUIANToolboxPath:", get_ruian_toolbox_path()
        print "getRUIANImporterPath:", get_ruian_importer_path()
        print "getRUIANServicesBasePath:", get_ruian_services_base_path()
        print "getRUIANServicesPath:", get_ruian_services_path()
        print "getRUIANServicesHTMLPath:", get_ruian_services_html_path()
        print "getRUIANServicesSQLScriptsPath:", get_ruian_services_sql_scripts_path()


if __name__ == '__main__':
    main()
