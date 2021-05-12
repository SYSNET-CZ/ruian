# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        compileaddress_UnitTests
# Purpose:     Module compileaddress unit tests implementation.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

import unittest

from ruian_services.services.compile_address import compile_address, TextFormat

address_compile_samples = []


class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testcompileAddress(self):
        for sample in address_compile_samples:
            self.assertEqual(
                compile_address(
                    builder=TextFormat.plainText,
                    street=sample.street, house_number=sample.house_number, record_number=sample.record_number,
                    orientation_number=sample.orientation_number, zip_code=sample.zip_code,
                    locality=sample.locality, locality_part=sample.locality_part,
                    district_number=sample.district_number),
                sample.text_result
            )
        pass


class AddressSample:
    def __init__(self, street, house_number, record_number, orientation_number, zip_code, locality, locality_part,
                 district_number, text_result):
        self.street = street
        self.house_number = house_number
        self.record_number = record_number
        self.orientation_number = orientation_number
        self.zip_code = zip_code
        self.locality = locality
        self.locality_part = locality_part
        self.district_number = district_number
        self.text_result = text_result

    def to_xml(self):
        out = ""
        out += 'http' + '://www.vugtk.cz/euradin/services/rest'
        out += "/CompileAddress/txt?"
        out += "Street=" + self.street
        out += "&HouseNumber=" + self.house_number
        out += "&RecordNumber=" + self.record_number
        out += "&OrientationNumber=" + self.orientation_number
        out += "&ZIPCode=" + self.zip_code
        out += "&Locality=" + self.locality
        out += "&LocalityPart=" + self.locality_part
        out += "&DistrictNumber=" + self.district_number
        out += "\n" + self.text_result + "\n"
        return out


address_compile_samples.append(
    AddressSample(
        u"Arnošta Valenty", u"670", u"", u"31", u"19800", u"Praha", u"Černý Most", u"9",
        u"Arnošta Valenty 670/31\nČerný Most\n198 00 Praha 9"))
address_compile_samples.append(
    AddressSample(
        u"Arnošta Valenty", u"670", u"", u"", u"198 00", u"Praha", u"Černý Most", u"9",
        u'Arnošta Valenty 670\nČerný Most\n198 00 Praha 9'))
address_compile_samples.append(
    AddressSample(
        u"Medová", u"", u"30", u"", u"10400", u"Praha", u"Křeslice", u"10",
        u'Medová č. ev. 30\nKřeslice\n104 00 Praha 10'))
address_compile_samples.append(
    AddressSample(
        u"", u"", u"42", u"", u"10400", u"Praha", u"Křeslice", u"10", u'Křeslice č. ev. 42\n104 00 Praha 10'))
address_compile_samples.append(
    AddressSample(
        u"Lhenická", u"1120", u"", u"1", u"37005", u"České Budějovice", u"České Budějovice 2", u"",
        u'Lhenická 1120/1\nČeské Budějovice 2\n370 05 České Budějovice'))
address_compile_samples.append(
    AddressSample(u'Lhenická', u'1120', u'', u'', u'370 05', u'České Budějovice', u'České Budějovice 2', u'',
                  u'Lhenická 1120\nČeské Budějovice 2\n37005 České Budějovice'))
address_compile_samples.append(
    AddressSample(
        u'Lhenická', u'', u'12', u'', u'37005', u'České Budějovice', u'České Budějovice 2', u'',
        u'Lhenická č. ev. 12\nČeské Budějovice 2\n37005 České Budějovice'))
address_compile_samples.append(
    AddressSample(
        u'Žamberecká', u'339', u'', u'-', u'51601', u'Vamberk', u'Vamberk', u'',
        u'Žamberecká 339\n51601 Vamberk\n'))
address_compile_samples.append(
    AddressSample(
        u'Žamberecká', u'339', u'', u'1', u'51601', u'Vamberk', u'Vamberk', u'',
        u'Žamberecká 339/1\n51601 Vamberk'))
address_compile_samples.append(
    AddressSample(
        u'Žamberecká', u'', u'21', u'', u'51601', u'Vamberk', u'Vamberk', u'',
        u'Žamberecká č. ev. 21\n51601 Vamberk'))
address_compile_samples.append(
    AddressSample(
        u'', u'106', u'', u'', u'53333', u'Pardubice', u'Dražkovice', u'',
        u'Dražkovice 106\n53333 Pardubice'))
address_compile_samples.append(
    AddressSample(
        u'', u'106', u'', u'12', u'53333', u'Pardubice', u'Dražkovice', u'',
        u'Dražkovice 106/12\n53333 Pardubice'))
address_compile_samples.append(
    AddressSample(
        u'', u'', u'32', u'', u'53333', u'Pardubice', u'Dražkovice', u'',
        u'Dražkovice č. ev. 32\n53333 Pardubice'))
address_compile_samples.append(
    AddressSample(u'', u'111', u'', u'', u'50333', u'Praskačka', u'Praskačka', u'', u'č. p. 111\n50333 Praskačka'))
address_compile_samples.append(
    AddressSample(u'', u'111', u'', u'1', u'53333', u'Praskačka', u'Praskačka', u'', u'č .p. 111/1\n53333 Praskačka'))
address_compile_samples.append(
    AddressSample(u'', u'', u'32', u'', u'53333', u'Praskačka', u'Praskačka', u'', u'č .ev. 32\n53333 Pardubice'))

for s in address_compile_samples:
    print(s.to_xml())


def main():
    unittest.main()


if __name__ == '__main__':
    main()
