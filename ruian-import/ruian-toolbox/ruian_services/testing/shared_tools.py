# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs

# SERVER_URL = "http://localhost:5689/"
from urllib.parse import unquote
from urllib.request import urlopen

SERVER_URL = "http://localhost/euradin/services/rest.py/"


# SERVER_URL = "http://www.vugtk.cz/euradin/services/rest.py/"


def setup_utf():
    pass


HTML_PREFIX = u"""
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
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

        th {
         background-color: #1370AB;
         color : #fff;
        }

        h1 {
            color: #1370AB;
            border-bottom: 1 solid #B6B6B6;
        }

        tr.alt td {
          color: #00;
          background-color: #EAF2D3;
        }

        table {
            border-collapse: collapse;
            font-size: small;
        }

        td, th {
            border: 1px solid #4F81BD;
            vertical-align:top;
        }
        </style>
        <title><#TITLE></title>
    </head>
    <body>"""

HTML_SUFFIX = """
    </body>
</html>"""

RESULTS_TABLE_HEADER_LONG = u"""
<table>
    <tr>
            <th>#</th><th></th><th>Vstup</th><th>Výsledek</th><th>Pozn</th>
    </tr>
"""

RESULTS_TABLE_HEADER = u"""
<table>
    <tr>
            <th>#</th><th></th><th align="left">Test</th>
    </tr>
"""


def make_delimeters_visible(result):
    result = result.replace("\t", "\\t")
    result = result.replace("\r", "\\r")
    result = result.replace("\n", "\\n")
    return result


class FormalTester:
    def __init__(self, page_title="", description=None, compiling_person=None, tester=None):
        self.description = description
        self.compilingPerson = compiling_person
        self.tester = tester
        self.testsHTML = None
        self.content = HTML_PREFIX
        self.content = self.content.replace("<#TITLE>", page_title)
        self.longPrint = False
        self.isOddRow = False
        self.numTests = 0

    def new_section(self, caption, desc, compiling_person, tester):
        self.numTests = 0
        self.isOddRow = False
        self.compilingPerson = compiling_person
        self.tester = tester
        self.testsHTML = RESULTS_TABLE_HEADER
        if caption != "":
            self.content += "<h1>" + caption + "</h1>\n"
        if desc != "":
            self.content += "<p>" + desc + \
                            u" Výpis výsledků testu nemusí být z důvodu úspory místa zcela přesný, pro přesnou podobu je možné použít odkaz." + \
                            u"<br><br>Testovaný server: <a href='" + SERVER_URL + "'>" + SERVER_URL + "</a><br>" + \
                            "</p>\n"

    def close_section(self):
        self.content += self.testsHTML + "</table>"
        self.testsHTML = u""

    def add_test(self, inputs, result, expected_result, error_message=""):
        # result = makeDelimetersVisible(result)
        # result = unicode(result)
        self.numTests = self.numTests + 1

        if isinstance(result, list):
            pom = expected_result.splitlines()
            if set(result) == set(pom):
                status = "checked"
                print("   ok :", inputs, "-->", "\n".join(result))
                expected_result_message = u""
            else:
                status = ""
                expected_result_message = u" ≠ " + expected_result
                print("chyba :", inputs, "-->", "\n".join(result), "<>", expected_result, error_message)
        else:
            if str(result) == expected_result:
                status = "checked"
                print("   ok :", inputs, "-->", result)
                expected_result_message = u""
            else:
                status = ""
                expected_result_message = u" ≠ " + expected_result
                print("chyba :", inputs, "-->", result, "<>", expected_result, error_message)

        if self.isOddRow:
            odd_text = ' class="alt"'
        else:
            odd_text = ''

        if self.longPrint:
            self.testsHTML += "<tr" + odd_text + ">\n"
            self.testsHTML += '    <td align="center">' + str(self.numTests) + "</td>"
            self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' />' + "</td>"

            self.testsHTML += "    <td>" + inputs + "</td>"
            self.testsHTML += "    <td>" + str(result) + expected_result_message + "</td>"  # →
            self.testsHTML += "    <td>" + error_message + "</td>"
            self.testsHTML += "</tr>\n"
        else:
            self.testsHTML += "<tr" + odd_text + ">\n"
            self.testsHTML += '    <td align="center">' + str(self.numTests) + "</td>"
            self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' />' + "</td>"

            caption = unquote(inputs)
            # caption = caption.encode("utf=8")
            self.testsHTML += '    <td><a href="' + SERVER_URL + inputs + '">' + caption + "</a><br>"
            self.testsHTML += str(result) + expected_result_message + "<br>"
            if error_message != "":
                self.testsHTML += "    <td>" + error_message + "</td>"
            self.testsHTML += "</tr>\n"

        self.isOddRow = not self.isOddRow

    def load_and_add_test(self, path, params, expected_value):
        # params_list = params.split("&")
        # query = []

        params = path + params
        try:
            result = urlopen(SERVER_URL + params).read()
        except Exception as inst:
            result = str(inst)
        # result = "\n".join(result.splitlines())
        result = result.splitlines()
        params = params.decode("utf-8")
        self.add_test(params, result, expected_value, "")

    def save_to_html(self, file_name):
        with codecs.open(file_name, "w", "utf-8") as outFile:
            html_content = self.content + HTML_SUFFIX
            outFile.write(codecs.encode(html_content, "utf-8"))
            outFile.close()


def test():
    tester = FormalTester("Caption text", """Description text""", "Compiling person", "Tester")
    tester.add_test("OK test", "Test value", "Test value", "OK Test")
    tester.add_test("Fail test", "Wrong test value", "Test value", "Error message")
    tester.save_to_html("shared_tools.html")


if __name__ == '__main__':
    test()
