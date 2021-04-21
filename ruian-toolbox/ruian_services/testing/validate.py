# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs
from urllib.parse import quote
from urllib.request import urlopen

from ruian_services.testing import shared_tools


def test(tester_param=None):
    if tester_param is None:
        tester = shared_tools.FormalTester()
    else:
        tester = tester_param

    tester.new_section(
        "Ověření funkčnosti služby Validate",
        """Tento test ověřuje funkčnost služby Validate, která slouží k ověření zadané adresy.
                Adresa je zadána pomocí jednotlivých prvků adresního místa.""",
        "Compiling person", "Tester")

    def add_test(path, params, expected_value):
        params_list = params.split("&")
        query = []
        if params_list != [""]:
            for param in params_list:
                v = param.split("=")
                query.append(v[0] + "=" + quote(codecs.encode(v[1], "utf-8")))
            params = "&".join(query)
        else:
            params = ""

        params = path + params
        try:
            result = urlopen(shared_tools.SERVER_URL + params).read()
        except Exception as inst:
            result = str(inst)
        # result = result.strip()
        result = quote(codecs.encode(result, "utf-8"))
        params = params.decode("utf-8")
        tester.add_test(params, result, expected_value, "")

    add_test("/Validate/text?", "Street=Severní", "False")
    add_test("/Validate/text?", "Street=Severní&HouseNumber=507", "False")
    add_test("/Validate/text?", "Street=Severní&Locality=Kladno&HouseNumber=507", "False")
    add_test("/Validate/text?", "Street=Severn%C3%AD&RecordNumber=25", "False")
    add_test("/Validate/text?", "Street=Fillova&HouseNumber=980&OrientationNumber=5", "False")

    add_test("/Validate/text?", "Street=Severní&Locality=Kladno&HouseNumber=507&ZIPCode=27204&LocalityPart=Kladno", "True")
    add_test("/Validate/text?", "Street=Severní&Locality=Kladno&HouseNumber=507&ZIPCode=27206&LocalityPart=Kladno", "False")
    add_test("/Validate/text?", "Street=Žižkova&Locality=Jirkov&ZIPCode=43111&LocalityPart=Jirkov&RecordNumber=263", "True")
    add_test("/Validate/text?", "Street=Rodinná&Locality=Havířov&HouseNumber=1003&ZIPCode=73601&LocalityPart=Bludovice&OrientationNumber=25", "True")
    add_test("/Validate/text?", "Street=U%20Jeslí&Locality=Broumov&HouseNumber=222&ZIPCode=55001&LocalityPart=Nové%20Město", "True")
    add_test("/Validate/text?", "Street=Žižkova&Locality=Jirkov&ZIPCode=43111&LocalityPart=Jirkov&RecordNumber=273", "False")
    add_test("/Validate/text?", "Street=Rodinná&Locality=Havířov&HouseNumber=1027&ZIPCode=73601&LocalityPart=Bludovice", "False")
    add_test("/Validate/text?", "Street=U%20Jeslí&Locality=Broumov&HouseNumber=226&ZIPCode=55001&LocalityPart=Nové%20Město", "False")

    add_test("/Validate/text?", "HouseNumber=507a", "False")
    add_test("/Validate/text?", "RecordNumber=145s", "False")
    add_test("/Validate/text?", "OrientationNumber=12a", "False")
    add_test("/Validate/text?", "ZIPCode=27206r", "False")
    add_test("/Validate/text?", "", "False")

    tester.close_section()

    if tester_param is None:
        tester.save_to_html("Validate.html")


if __name__ == '__main__':
    shared_tools.setup_utf()
    test()
