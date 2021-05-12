# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        html_log
# Purpose:     Creates HTML log file from download
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------

import os
import logging


def save_str_to_file(file_name, string_item):
    try:
        with open(file_name, "w") as f:
            f.write(string_item)
            f.close()
    except IOError as e:
        logging.error(str(e))
    finally:
        pass


class HtmlLog:
    CHANGES_START_ID = "<!-- CHANGES START -->"
    CHANGES_END_ID = "<!-- CHANGES END -->"
    TEMPLATE_FILENAME = os.path.dirname(__file__) + os.sep + 'log_template.html'

    def __init__(self):
        self.htmlCode = ""
        pass

    def add_header(self, caption):
        self.htmlCode += "<h2>" + caption + "</h2>\n"

    def open_table(self):
        self.htmlCode += "<table>\n"

    def close_table(self):
        self.htmlCode += "</table>\n"

    def open_table_row(self, tags=""):
        if tags != "" and tags[:1] != " ":
            tags = " " + tags
        self.htmlCode += '<tr' + tags + '>'

    def close_table_row(self):
        self.htmlCode += "</tr>\n"

    def add_col(self, value, tags=""):
        if tags != "" and tags[:1] != " ":
            tags = " " + tags

        self.htmlCode += '<td' + tags + ' >' + str(value) + "</td>"

    def get_html_content(self, file_name):
        file_name = os.path.dirname(__file__) + os.sep + file_name
        if not os.path.exists(file_name):
            file_name = self.TEMPLATE_FILENAME
        with open(file_name, "r") as f:
            result = f.read()
            f.close()
        return result

    def close_section(self, file_name):
        html_page = self.get_html_content(file_name)
        html_page = html_page.replace(self.CHANGES_START_ID, "")
        html_page = html_page.replace(self.CHANGES_END_ID, self.CHANGES_START_ID + self.CHANGES_END_ID)
        html_page = html_page.replace("AutoRefresh = true", "AutoRefresh = false")
        save_str_to_file(file_name, html_page)

    def save(self, file_name):
        html_page = self.get_html_content(file_name)
        html_page = html_page.replace("AutoRefresh = false", "AutoRefresh = true")
        prefix = html_page[:html_page.find(self.CHANGES_START_ID) + len(self.CHANGES_START_ID)]
        suffix = html_page[html_page.find(self.CHANGES_END_ID):]
        save_str_to_file(file_name, prefix + self.htmlCode + suffix)

    def clear(self):
        self.htmlCode = ""


html_log = HtmlLog()
