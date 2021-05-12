# -*- coding: utf-8 -*-
from shared_tools import ruian_download_config, ruian_importer_config
import tabulate

TABLE_HEADER = ["Položka konfigurace", "Hodnota"]
# TABLE_FORMAT = "fancy_grid"
# TABLE_FORMAT = "pretty"
# TABLE_FORMAT = "github"
TABLE_FORMAT = "simple"


def print_config():
    print('\nDOWNLOAD')
    print_download_config()

    print('\nIMPORT')
    print_import_config()


def print_download_config():
    config = ruian_download_config()

    table = [
        ["Konfigurace", config.fileName],
        ["Data", config.dataDir],
        ["Spustit importer", config.runImporter],
        ["Rozbalit soubory", config.uncompressDownloadedFiles],
        ["Stáhnout úplnou databázi", config.downloadFullDatabase],
        ["Ignorovat hist. data", config.ignoreHistoricalData]
    ]
    print(tabulate.tabulate(table, TABLE_HEADER, tablefmt=TABLE_FORMAT))


def print_import_config():
    config = ruian_importer_config()

    table = [
        ["Konfigurace", config.fileName],
        ["Data", config.dataDir],
        ["Databáze", config.dbname],
        ["Host", config.host],
        ["Port", config.port],
        ["Uživatel", config.user],
        ["Heslo", config.password],
        ["Vrstvy", config.layers],
        ["OS4Geo", config.os4GeoPath],
        ["Servisní tabulky", config.buildServicesTables],
        ["Servisní tabulky 2", config.build_services_tables],
        ["Auto tabulky", config.buildAutocompleteTables],
        ["Auto tabulky 2", config.build_autocomplete_tables]
    ]
    print(tabulate.tabulate(table, TABLE_HEADER, tablefmt=TABLE_FORMAT))


if __name__ == '__main__':
    print_config()
