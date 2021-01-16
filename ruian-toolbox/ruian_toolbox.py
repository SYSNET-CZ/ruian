# -*- coding: utf-8 -*-
from shared_tools import ruian_download_config, ruian_importer_config
import tabulate

TABLE_HEADER = ["Položka konfigurace".decode('utf-8'), "Hodnota"]
# TABLE_FORMAT = "fancy_grid"
# TABLE_FORMAT = "pretty"
# TABLE_FORMAT = "github"
TABLE_FORMAT = "simple"


def print_config():
    print ('\nDOWNLOAD')
    print_download_config()

    print ('\nIMPORT')
    print_import_config()


def print_download_config():
    config = ruian_download_config()

    table = [
        ["Konfigurace", config.fileName],
        ["Data", config.dataDir],
        ["Spustit importer", config.runImporter],
        ["Rozbalit soubory", config.uncompressDownloadedFiles],
        ["Ignorovat hist. data".decode('utf-8'), config.ignoreHistoricalData]
    ]
    print(tabulate.tabulate(table, TABLE_HEADER, tablefmt=TABLE_FORMAT))


def print_import_config():
    config = ruian_importer_config()

    table = [
        ["Konfigurace", config.fileName],
        ["Data", config.dataDir],
        ["Databáze".decode('utf-8'), config.dbname],
        ["Host", config.host],
        ["Port", config.port],
        ["Uživatel".decode('utf-8'), config.user],
        ["Heslo", config.password],
        ["Vrstvy", config.layers],
        ["OS4Geo", config.os4GeoPath]
    ]
    print(tabulate.tabulate(table, TABLE_HEADER, tablefmt=TABLE_FORMAT))


if __name__ == '__main__':
    print_config()
