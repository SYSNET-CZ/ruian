# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        build_html_log
# Purpose:     Builds HTML log file in imported directory.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------
import codecs
import os
import sys
import time

from shared_tools import shared
from shared_tools.configuration import get_data_dir_full_path, ruian_importer_config

help_str = """
Builds import HTML Log file.

Requires: Python 2.7.5 or later

Usage: build_html_log.py

"""

TXT_EXTENSION = ".txt"
LOG_EXTENSION = ".log"

DATE_STR_EXAMPLE = "2014.11.09"
DETAILS = [".VFRlog", ".VFRerr"]

shared.setup_paths()

is_download = True


def get_log_file_names(file_name):
    global is_download
    result = []

    file_name = os.path.basename(file_name)
    file_name = file_name[:len(file_name) - len(TXT_EXTENSION)]
    file_name = file_name.lower()
    is_download = True
    for prefix in ["download_", "patch_"]:
        if file_name.startswith(prefix):
            date_str = file_name[len(prefix):]
            if len(date_str) == len(DATE_STR_EXAMPLE):
                for detail in DETAILS:
                    result.append("__" + prefix + date_str + detail + LOG_EXTENSION)
        is_download = False
    return result


html_template = u"""<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Detaily importů z databáze RÚIAN</title>
        <style>
            body {
                font-family: Arial;
                font-size: small;
                color: #575757;
                margin: 10 10 10 10;
            }
            a {
                color: #1370AB;
            }

            tr, td, th {
                vertical-align:top;
                font-size:small;
            }

            th {
                background-color: #1370AB;
                color : #fff;
            }


            h1, h2 {
                font-size:large;
                color: #2c4557;
                font-weight:normal;
                padding: 10px 0px 0px 0px;
                margin: 0px 0px 0px 0px;
            }

            h1 {
                color: #1370AB;
                border-bottom: 1 solid #B6B6B6;
            }

            table {
                border-collapse: collapse;
                font-size: small;
                border: 1px solid #4F81BD;
            }

            td, th {
                vertical-align:top;
                padding: 2px 5px 2px 5px;
            }

            th {
                border: 1px solid #4F81BD;
            }

            td {
                border-left: 1px solid #4F81BD;
                border-right: 1px solid #4F81BD;
            }

            .altColor {
                background-color:#C6D9F1;
            }

        </style>
    </head>
    <body>
        <h1>Detaily importů do databáze RÚIAN</h1>
        <br>Databáze <b><a href="../dbdetails">#DATABASE_NAME#</a></b> je aktuální k #DATABASE_DATE#.
        #LAYERS_DETAILS#
        <br><br>
        #IMPORTS_TABLE_ID#
    </body>
</html>
"""

DATABASE_SERVER_ID = "#DATABASE_SERVER#"
DATABASE_PORT_ID = "#DATABASE_PORT#"
DATABASE_NAME_ID = "#DATABASE_NAME#"
IMPORTS_TABLE_ID = "#IMPORTS_TABLE_ID#"
DATABASE_DATE_ID = "#DATABASE_DATE#"
LAYERS_DETAILS_ID = "#LAYERS_DETAILS#"


def build_html_log():
    import_types = [u"Aktualizace", u"Stavová databáze"]
    data_path = get_data_dir_full_path()
    config = ruian_importer_config()
    log = html_template

    log = log.replace(DATABASE_SERVER_ID, config.host)
    log = log.replace(DATABASE_PORT_ID, config.port)
    log = log.replace(DATABASE_NAME_ID, config.dbname)
    log = log.replace(DATABASE_DATE_ID, time.strftime("%d.%m.20%y"))

    if config.layers == "":
        msg = u"Do databáze jsou načteny všechny vrstvy."
    else:
        msg = u"Do databáze jsou načteny vrstvy %s." % config.layers
    log = log.replace(LAYERS_DETAILS_ID, msg)

    odd_row = False
    imports_table = u"<table>"
    imports_table += u'<tr valign="bottom"><th>Datum</th><th>Import</th><th>Konverze<br>VFR</th><th>Chyby</th></tr>'
    for file_item in os.listdir(data_path):
        file_name = file_item.lower()
        if file_name.endswith(TXT_EXTENSION):
            file_name = file_name[:len(file_name) - len(TXT_EXTENSION)]
            download = True
            for prefix in ["__download_", "__patch_"]:
                if file_name.startswith(prefix):
                    date_str = file_name[len(prefix):]
                    if len(date_str) == len("2014.11.09"):
                        imports_table += '<tr %s><td>%s</td><td><a href="%s">%s</a></td>' % (
                            ["", 'class="altColor"'][int(odd_row)], date_str, prefix + date_str + TXT_EXTENSION,
                            import_types[download])
                        for detail in DETAILS:
                            detail_name = prefix + date_str + detail + LOG_EXTENSION
                            file_name = os.path.join(data_path, detail_name)
                            caption = ""
                            if os.path.exists(file_name) and os.path.getsize(file_name) != 0:
                                caption = "Info"
                            imports_table += u'<td align="center"><a href="%s">%s</a></td>' % (detail_name, caption)

                        imports_table += "</tr>"
                        odd_row = not odd_row
                download = False

    imports_table += "</table>"
    log = log.replace(IMPORTS_TABLE_ID, imports_table)

    out_f = codecs.open(os.path.join(data_path, 'Import.html'), 'w', 'utf-8')
    try:
        out_f.write(log)
    finally:
        out_f.close()


def main(argv=None):
    from shared_tools.configuration import ruian_download_config
    config = ruian_download_config()
    config.load_from_command_line(argv, help_str)
    print("Building import HTML Log file.")
    build_html_log()
    print("Done.")


if __name__ == '__main__':
    main(argv=sys.argv)
