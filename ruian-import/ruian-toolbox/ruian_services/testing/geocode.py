# -*- coding: utf-8 -*-
__author__ = 'Augustyn'


# import shared_tools
# import urllib2
# import urllib
# import codecs
from ruian_services.testing import shared_tools


def test(tester_param=None):
    if tester_param is None:
        tester = shared_tools.FormalTester("Ověření funkčnosti služby Geocode")
    else:
        tester = tester_param
    tester.new_section("Ověření funkčnosti služby Geocode",
                       """Tento test ověřuje funkčnost služby Geocode, která slouží získání souřadnic zadaného adresního místa.
                Adresní místo zadáme buď pomocí jeho identifikátoru RÚIAN nebo pomocí textového řetězce adresy..
                 Textový řetězec adresy může být nestandardně formátován nebo může být i neúplný.""",
                       "Compiling person", "Tester")

    tester.load_and_add_test("/Geocode/text?", "AddressPlaceId=1408739", "1033052.61, 766195.05")
    tester.load_and_add_test("/Geocode/text?", "AddressPlaceId=20388802", "1056492.96, 529426.07")
    tester.load_and_add_test("/Geocode/text?", "AddressPlaceId=8123934", "1098618.98, 568885.13")
    tester.load_and_add_test("/Geocode/text?", "AddressPlaceId=8150656", "1086263.12, 572291.20")
    tester.load_and_add_test("/Geocode/text?", "AddressPlaceId=140k", "")

    tester.load_and_add_test("/Geocode/text?", "SearchText=Blahoslavova%201710,%20Louny", "1007250.67, 781971.94")
    tester.load_and_add_test("/Geocode/text?", "SearchText=U%20Kam,%20Vys",
                             "1051222.31, 759801.78\n1051248.61, 759804.26\n1051154.97, 759793.10")

    tester.load_and_add_test("/Geocode/text?", "SearchText=Mramorov%C3%A1,%20Tet%C3%ADn",
                             "1055481.79, 767602.15\n1055502.63, 767570.69\n1055447.02, 767576.82")
    tester.load_and_add_test("/Geocode/text?", "SearchText=12", "")

    tester.load_and_add_test("/Geocode/text?",
                             "Street=Hromadova&Locality=Kladno&HouseNumber=2741&ZIPCode=27201&LocalityPart=Kladno",
                             "1033052.61, 766195.05")
    tester.load_and_add_test("/Geocode/text?",
                             "Street=Mari%C3%A1nsk%C3%A1&Locality=Su%C5%A1ice&HouseNumber=67&ZIPCode=34201&LocalityPart=Su%C5%A1ice%20III",
                             "1128217.51, 820609.28")
    tester.load_and_add_test("/Geocode/text?",
                             "Street=Dlouh%C3%A1&Locality=Terez%C3%ADn&HouseNumber=22&ZIPCode=41155&LocalityPart=Terez%C3%ADn",
                             "993630.00, 755650.00")
    tester.load_and_add_test("/Geocode/text?",
                             "Street=Osadn%C3%AD&Locality=Rumburk&HouseNumber=1456&ZIPCode=40801&LocalityPart=Rumburk%201&OrientationNumber=12",
                             "947618.24, 719309.30")

    tester.load_and_add_test("/Geocode/text?", "HouseNumber=980f", "")
    tester.load_and_add_test("/Geocode/text?", "HouseNumber=f", "")

    tester.load_and_add_test("/Geocode/text?", "ZIPCode=14000a", "")
    tester.load_and_add_test("/Geocode/text?", "ZIPCode=a", "")

    tester.load_and_add_test("/Geocode/text?", "OrientationNumber=12a", "")
    tester.load_and_add_test("/Geocode/text?", "OrientationNumber=a", "")

    tester.load_and_add_test("/Geocode/text?", "RecordNumber=14d", "")
    tester.load_and_add_test("/Geocode/text?", "RecordNumber=d", "")

    tester.load_and_add_test("/Geocode/text?", "", "")

    tester.close_section()

    if tester_param is None:
        tester.save_to_html("Geocode.html")


if __name__ == '__main__':
    shared_tools.setup_utf()
    test()
