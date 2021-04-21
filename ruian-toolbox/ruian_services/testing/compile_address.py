# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs
from urllib.parse import quote
from urllib.request import urlopen

from ruian_services.testing import shared_tools


def build_param_string(
        street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
        locality, locality_part, district_number):
    url = "/CompileAddress?"
    params = {
        "Street": street,
        "HouseNumber": house_number,
        "RecordNumber": record_number,
        "OrientationNumber": orientation_number,
        "OrientationNumberCharacter": orientation_number_character,
        "ZIPCode": zip_code,
        "Locality": locality,
        "LocalityPart": locality_part,
        "DistrictNumber": district_number
    }

    for key in params:
        url += key + "=" + quote(codecs.encode(params[key], "utf-8")) + "&"

    return url


def test(tester_param=None):
    if tester_param is None:
        tester = shared_tools.FormalTester("Ověření funkčnosti služby CompileAddress")
    else:
        tester = tester_param
    tester.new_section(
        "Ověření funkčnosti služby CompileAddress",
        """
Tento test ověřuje sestavení zápisu adresy ve standardizovaném tvaru podle § 6 vyhlášky č. 359/2011 Sb.,
kterou se provádí zákon č. 111/2009 Sb., o základních registrech, ve znění zákona č. 100/2010 Sb.
Adresní místo lze zadat buď pomocí jeho identifikátoru RÚIAN, textového řetězce adresy nebo jednotlivých prvků adresy.
                """,
        "Compiling person", "Tester")

    def add_test(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number, expected_value):
        params = build_param_string(
            street, house_number, record_number, orientation_number, orientation_number_character, zip_code,
            locality, locality_part, district_number)
        try:
            result = urlopen(shared_tools.SERVER_URL + params).read()
            result = "\n".join(result.splitlines())
        except Exception as inst:
            result = str(inst)
        # result = "aaa" #result.decode("utf-8")
        # expectedValue = "ev"
        # params = params.decode("utf-8")
        # expectedValue = expectedValue.decode("utf-8")
        tester.add_test(params, result, expected_value, "")

    def add_test_by_id(path, expected_value):
        try:
            result = urlopen(shared_tools.SERVER_URL + path).read()
        except Exception as inst:
            result = str(inst)
        # result = result.strip()
        result = "\n".join(result.splitlines())
        # result = urllib.quote(codecs.encode(result, "utf-8"))
        tester.add_test(path, result, expected_value, "")

    """
    def add_test_full_text(param=None):
        if param is None:
            tester = sharedtools.FormalTester("Ověření funkčnosti služby FullTextSearch")
        else:
            tester = param
    """
    tester.load_and_add_test(
        "/CompileAddress/text/?",
        "SearchText=Mramor,%20Tet%C3%ADn",
        "Mramorová 234\n26601 Tetín\nMramorová 243\n26601 Tetín\nMramorová 236\n26601 Tetín")
    tester.load_and_add_test(
        "/CompileAddress/text/?",
        "SearchText=12",
        "")
    add_test_by_id("/CompileAddress/text?AddressPlaceId=41326474", "U Kamene 181\n26716 Vysoký Újezd")
    add_test_by_id("/CompileAddress/text?AddressPlaceId=21907145", "Na lánech 598/13\nMichle\n14100 Praha 4")
    add_test_by_id("/CompileAddress/text?AddressPlaceId=25021478", "Lesní 345/5\n35301 Mariánské Lázně")
    add_test_by_id("/CompileAddress/text?AddressPlaceId=16512171", "Pašinovice 8\n37401 Komařice")
    add_test_by_id("/CompileAddress/text?AddressPlaceId=165k", "")  # ošetření chyby - zadání omylem znaku do identifikátoru
    add_test_by_id("/CompileAddress/text?AddressPlaceId=12", "")  # ošetření chyby - zadání identifikátoru, který není v DB

    add_test(u"Arnošta Valenty", "670", "", "31", "", "19800", "Praha", "Černý Most", "9", "Arnošta Valenty 670/31\nČerný Most\n19800 Praha 9")
    add_test(u"Arnošta Valenty", "670", "", "", "", "198 00", "Praha", "Černý Most", "9", "Arnošta Valenty 670\nČerný Most\n19800 Praha 9")
    add_test(u"Medová", "", "30", "", "", "10400", "Praha", "Křeslice", "10", "Medová č.ev. 30\nKřeslice\n10400 Praha 10")
    add_test(u"", "", "42", "", "", "10400", "Praha", "Křeslice", "10", "Křeslice č.ev. 42\n10400 Praha 10")
    add_test(u"Lhenická", "1120", "", "1", "", "37005", "České Budějovice", "České Budějovice 2", "", "Lhenická 1120/1\nČeské Budějovice 2\n37005 České Budějovice")
    add_test(u"Holická", "568", "", "31", "y", "779 00", "Olomouc", "Hodolany", "", "Holická 568/31y\nHodolany\n77900 Olomouc")
    add_test(u"Na Herinkách", "85", "", "", "", "26601", "Beroun", "Beroun-Závodí", "", "Na Herinkách 85\nBeroun-Závodí\n26601 Beroun")
    add_test(u"Na Herinkách", "", "97", "", "", "26601", "Beroun", "Beroun-Závodí", "", "Na Herinkách č.ev. 97\nBeroun-Závodí\n26601 Beroun")
    add_test(u"Žamberecká", "339", "", "", "", "51601", "Vamberk", "Vamberk", "", "Žamberecká 339\n51601 Vamberk")
    add_test(u"Žamberecká", "339", "", "1", "", "51601", "Vamberk", "Vamberk", "", "Žamberecká 339/1\n51601 Vamberk")
    add_test(u"Lidická", "2858", "", "49", "F", "78701", "Šumperk", "Šumperk", "", "Lidická 2858/49F\n78701 Šumperk")
    add_test(u"Žamberecká", "", "21", "", "", "51601", "Vamberk", "Vamberk", "", "Žamberecká č.ev. 21\n51601 Vamberk")
    add_test(u"", "106", "", "", "", "53333", "Pardubice", "Dražkovice", "", "Dražkovice 106\n53333 Pardubice")
    add_test(u"", "", u'32', u'', "", "53333", "Pardubice", "Dražkovice", "", "Dražkovice č.ev. 32\n53333 Pardubice")
    add_test(u"", "111", "", "", "", "50333", "Praskačka", "Praskačka", "", "č.p. 111\n50333 Praskačka")
    add_test(u"", "", "86", "", "", "53943", "Krouna", "Krouna", "", "č.ev. 86\n53943 Krouna")
    tester.close_section()

    if tester_param is None:
        tester.save_to_html("CompileAddress.html")


if __name__ == '__main__':
    shared_tools.setup_utf()
    test()
