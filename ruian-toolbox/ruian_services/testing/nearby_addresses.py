# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

from urllib.request import urlopen

from ruian_services.testing import shared_tools


def test(tester_param=None):
    if tester_param is None:
        tester = shared_tools.FormalTester("Ověření funkčnosti služby NearByAddresses")
    else:
        tester = tester_param
    tester.new_section(
        "Ověření funkčnosti služby NearByAddresses",
        """Tento test ověřuje funkčnost služby NearByAddresses, která umožňuje vyhledat adresní místa v okolí
zadaných souřadnic do určité vzdálenosti. Vrací záznamy databáze RÚIAN setříděné podle vzdálenosti od zadaných souřadnic.""",
        "Compiling person", "Tester")

    def add_test(path, expected_value):
        try:
            result = urlopen(shared_tools.SERVER_URL + path).read()
        except Exception as inst:
            result = str(inst)
        # result = result.strip()
        # result = urllib.quote(codecs.encode(result, "utf-8"))
        result = "\n".join(result.splitlines())
        tester.add_test(path, result, expected_value, "")

    add_test("/NearbyAddresses/textToOneRow/655180/1030800/50", "č.p. 22, 50315 Pšánky")
    add_test("/NearbyAddresses/textToOneRow/625350/1025770/200", "č.p. 54, 55203 Říkov")
    add_test("/NearbyAddresses/textToOneRow/724948/1007742/65", "č.p. 42, 27735 Kanina\nč.p. 47, 27735 Kanina")
    add_test("/NearbyAddresses/textToOneRow/560670/1026662/80", "Kamenička č.ev. 31, 79069 Bílá Voda")
    add_test("/NearbyAddresses/textToOneRow/697180/1066880/120", "Červený Hrádek 44, 28504 Bečváry")

    add_test("/NearbyAddresses/text/655180/1030800/50", "č.p. 22\n50315 Pšánky")
    add_test("/NearbyAddresses/text/625350/1025770/200", "č.p. 54\n55203 Říkov")
    add_test("/NearbyAddresses/text/724948/1007742/65? ", "č.p. 42\n27735 Kanina\nč.p. 47\n27735 Kanina")
    add_test("/NearbyAddresses/text/560670/1026662/80", "Kamenička č.ev. 31\n79069 Bílá Voda")
    add_test("/NearbyAddresses/text/697180/1066880/120", "Červený Hrádek 44\n28504 Bečváry")

    add_test("/NearbyAddresses/text/a/1025770/200", "")
    add_test("/NearbyAddresses/text/625350/b/200", "")
    add_test("/NearbyAddresses/text/625350/1025770/c", "")
    add_test("/NearbyAddresses/text/a/b/c", "")
    add_test("/NearbyAddresses/text/a/b/200", "")
    add_test("/NearbyAddresses/text/625350/b/c", "")
    add_test("/NearbyAddresses/text/a/1025770/c", "")

    tester.close_section()

    if tester_param is None:
        tester.save_to_html("NearByAddresses.html")


if __name__ == '__main__':
    shared_tools.setup_utf()
    test()
