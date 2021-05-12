# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         models
# Purpose:      Models used in the service
#
# Author:       Radim Jager
# Copyright:    (c) SYSNET s.r.o. 2019
# License:      CC BY-SA 4.0
# -------------------------------------------------------------------------------
import json

__author__ = 'SYSNET'

from swagger_server.models import KatastralniUzemi, AdministrativeDivision, MapovyList50, Parcela, Povodi, Zsj, Address


class Coordinates(dict, object):
    # JTSK (5514)
    x: float
    y: float

    def __init__(self, y, x):
        dict.__init__(self, y=y, x=x)
        self.x = abs(x) * -1
        self.y = abs(y) * -1
        dict.__init__(self, y=self.y, x=self.x)

        # This field will not be sent in the response
        # self.status = 'active'


class CoordinatesGps(dict, object):
    # WGS
    lat: float
    lon: float

    def __init__(self, lat, lon):
        dict.__init__(self, lat=lat, lon=lon)
        self.lat = lat
        self.lon = lon


class AddressInternal(dict, object):
    def __init__(self, street, house_number, record_number, orientation_number, orientation_number_character,
                 zip_code, locality, locality_part, district_number, district, ruian_id):
        dict.__init__(
            self, street=street, house_number=house_number, record_number=record_number,
            orientation_number=orientation_number, orientation_number_character=orientation_number_character,
            zip_code=zip_code, locality=locality, locality_part=locality_part, district_number=district_number,
            district=district, ruian_id=ruian_id
        )
        self.street = street
        self.house_number = house_number
        self.record_number = record_number
        self.orientation_number = orientation_number
        self.orientation_number_character = orientation_number_character
        self.zip_code = zip_code
        self.locality = locality
        self.locality_part = locality_part
        self.district_number = district_number
        self.district = district
        self.ruian_id = ruian_id

    @property
    def to_pretty(self):
        out = PrettyAddressInternal(
            self.street, self.house_number, self.record_number, self.orientation_number,
            self.orientation_number_character, self.zip_code, self.locality, self.locality_part,
            self.district_number, self.district, self.ruian_id
        )
        return out

    @property
    def to_swagger(self):
        out = Address(
            street=self.street, ruian_id=self.ruian_id, zip_code=self.zip_code, locality=self.locality,
            locality_part=self.locality_part, house_number=self.house_number, record_number=self.record_number,
            district_number=self.district_number, orientation_number=self.orientation_number,
            orientation_number_character=self.orientation_number_character, district=self.district
        )
        return out


class PrettyAddressInternal(dict, object):
    def __init__(self, street, house_number, record_number, orientation_number, orientation_number_character,
                 zip_code, locality, locality_part, district_number, district, ruian_id):
        # Convert None values to "".
        (street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
         locality_part, district_number, district, ruian_id) = none_to_string(
            (street, house_number, record_number, orientation_number,
             orientation_number_character, zip_code, locality, locality_part, district_number, district, ruian_id))

        self.street = street
        self.house_number = house_number
        self.record_number = record_number
        self.orientation_number = orientation_number
        self.orientation_number_character = orientation_number_character
        self.zip_code = zip_code
        self.locality = locality
        self.locality_part = locality_part
        self.district_number = district_number
        self.district = district
        self.ruian_id = ruian_id

        self.zip_code = formatzip_code(self.zip_code)
        self.house_number = empty_string_if_no_number(self.house_number)
        self.orientation_number = empty_string_if_no_number(self.orientation_number)
        self.district_number = empty_string_if_no_number(self.district_number)
        self.orientation_number_character = alpha_check(self.orientation_number_character)
        self.town_info = self.zip_code + " " + self.locality
        if self.district_number != "":
            self.town_info += " " + self.district_number
        if self.house_number != "":
            self.house_number_str = " " + self.house_number
            if self.orientation_number != "":
                self.house_number_str += u"/" + self.orientation_number + self.orientation_number_character
        elif self.record_number != "":
            self.house_number_str = u" č.ev. " + self.record_number
        else:
            self.house_number_str = ""
        dict.__init__(
            self, street=self.street, house_number=self.house_number, record_number=self.record_number,
            orientation_number=self.orientation_number, orientation_number_character=self.orientation_number_character,
            zip_code=self.zip_code, locality=self.locality, locality_part=self.locality_part,
            district_number=self.district_number, district=self.district,
            ruian_id=self.ruian_id, town_info=self.town_info,
            house_number_str=self.house_number_str
        )

    def get_lines(self):
        lines = []  # Result list, initiated for case of error
        if self.locality.upper() == "PRAHA":
            if self.street != "":
                lines.append(self.street + self.house_number_str)
                lines.append(self.locality_part)
                lines.append(self.town_info)
            else:
                lines.append(self.locality_part + self.house_number_str)
                lines.append(self.town_info)
        else:
            if self.street != "":
                lines.append(self.street + self.house_number_str)
                if self.locality_part != self.locality:
                    lines.append(self.locality_part)
                lines.append(self.town_info)
            else:
                if self.locality_part != self.locality:
                    lines.append(self.locality_part + self.house_number_str)
                else:
                    if self.house_number != "":
                        lines.append(u"č.p." + self.house_number_str)
                    else:
                        lines.append(self.house_number_str[1:])
                lines.append(self.town_info)
        if self.ruian_id != "":
            lines.insert(0, str(self.ruian_id))

        return lines

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)


class MapovyList50Internal:
    id: str
    nazev: str

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[0]
            self.nazev = row[2]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)

    @property
    def to_swagger(self):
        out = MapovyList50(
            id_value=self.id, nazev=self.nazev
        )
        return out


class KatastralniUzemiInternal:

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[2]
            self.nazev = row[3]
            self.obec_kod = row[4]
            self.obec_nazev = row[5]
            self.obec_statuskod = row[6]
            self.orp_kod = int(row[7])
            self.orp_nazev = row[8]
            self.spravni_obec_kod = row[8]
            self.spravni_obec_nazev = row[10]
            self.pou_kod = row[11]
            self.pou_nazev = row[12]
            self.okres_kod = row[15]
            self.okres_nazev = row[16]
            self.vusc_kod = row[17]
            self.vusc_nazev = row[18]
            self.regionsoudrznosti_kod = row[19]
            self.regionsoudrznosti_nazev = row[20]
            self.nuts_1 = 'CZ'
            self.nuts_2 = row[21]
            self.nuts_3 = row[22]
            self.nuts_lau1 = row[23]
            self.nuts_lau2 = row[24]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)

    @property
    def to_swagger(self):
        out = KatastralniUzemi(
            id_value=self.id,
            nazev=self.nazev,
            administrative_division=AdministrativeDivision(
                ku_kod=self.id, ku_nazev=self.nazev, nuts_lau1=self.nuts_lau1, nuts_lau2=self.nuts_lau2,
                orp_nazev=self.orp_nazev, pou_nazev=self.pou_nazev, vusc_nazev=self.vusc_nazev,
                obec_nazev=self.obec_nazev, spravni_obec_nazev=self.spravni_obec_nazev,
                spravni_obec_kod=self.spravni_obec_kod, orp_kod=self.orp_kod, obec_kod=self.obec_kod,
                nuts_1=self.nuts_1, nuts_2=self.nuts_2, nuts_3=self.nuts_3, okres_nazev=self.okres_nazev,
                obec_statuskod=self.obec_statuskod, regionsoudrznosti_kod=self.regionsoudrznosti_kod,
                regionsoudrznosti_nazev=self.regionsoudrznosti_nazev, vusc_kod=self.vusc_kod, pou_kod=self.pou_kod,
                okres_kod=self.okres_kod
            ))
        return out


class ZsjInternal:
    # Zakladni sidelni jednotka

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[2]
            self.nazev = row[3]
            self.ku_kod = row[4]
            self.ku_nazev = row[5]
            self.obec_kod = row[6]
            self.obec_nazev = row[7]
            self.obec_statuskod = row[8]
            self.orp_kod = int(row[9])
            self.orp_nazev = row[10]
            self.spravni_obec_kod = row[11]
            self.spravni_obec_nazev = row[12]
            self.pou_kod = row[13]
            self.pou_nazev = row[14]
            self.okres_kod = row[17]
            self.okres_nazev = row[18]
            self.vusc_kod = row[19]
            self.vusc_nazev = row[20]
            self.regionsoudrznosti_kod = row[21]
            self.regionsoudrznosti_nazev = row[22]
            self.nuts_1 = 'CZ'
            self.nuts_2 = row[23]
            self.nuts_3 = row[24]
            self.nuts_lau1 = row[25]
            self.nuts_lau2 = row[26]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)

    @property
    def to_swagger(self):
        out = Zsj(
            id_value=self.id, nazev=self.nazev,
            administrative_division=AdministrativeDivision(
                ku_kod=self.ku_kod, ku_nazev=self.ku_nazev, nuts_lau1=self.nuts_lau1, nuts_lau2=self.nuts_lau2,
                orp_nazev=self.orp_nazev, pou_nazev=self.pou_nazev, vusc_nazev=self.vusc_nazev,
                obec_nazev=self.obec_nazev, spravni_obec_nazev=self.spravni_obec_nazev,
                spravni_obec_kod=self.spravni_obec_kod, orp_kod=self.orp_kod, obec_kod=self.obec_kod,
                nuts_1=self.nuts_1, nuts_2=self.nuts_2, nuts_3=self.nuts_3, okres_nazev=self.okres_nazev,
                obec_statuskod=self.obec_statuskod, regionsoudrznosti_kod=self.regionsoudrznosti_kod,
                regionsoudrznosti_nazev=self.regionsoudrznosti_nazev, vusc_kod=self.vusc_kod, pou_kod=self.pou_kod,
                okres_kod=self.okres_kod
            ))
        return out


class ParcelaInternal:

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[2]
            self.kmenovecislo = row[3]
            self.pododdelenicisla = row[4]
            self.vymeraparcely = row[5]
            self.ku_kod = row[6]
            self.ku_nazev = row[7]
            self.obec_kod = row[8]
            self.obec_nazev = row[9]
            self.obec_statuskod = row[10]
            self.orp_kod = int(row[11])
            self.orp_nazev = row[12]
            self.spravni_obec_kod = row[13]
            self.spravni_obec_nazev = row[14]
            self.pou_kod = row[15]
            self.pou_nazev = row[16]
            self.okres_kod = row[19]
            self.okres_nazev = row[20]
            self.vusc_kod = row[21]
            self.vusc_nazev = row[22]
            self.regionsoudrznosti_kod = row[23]
            self.regionsoudrznosti_nazev = row[24]
            self.nuts_1 = 'CZ'
            self.nuts_2 = row[25]
            self.nuts_3 = row[26]
            self.nuts_lau1 = row[27]
            self.nuts_lau2 = row[28]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)

    @property
    def to_swagger(self):
        out = Parcela(
            id_value=self.id,
            kmenovecislo=self.kmenovecislo, pododdelenicisla=self.pododdelenicisla, vymeraparcely=self.vymeraparcely,
            administrative_division=AdministrativeDivision(
                ku_kod=self.ku_kod, ku_nazev=self.ku_nazev, nuts_lau1=self.nuts_lau1, nuts_lau2=self.nuts_lau2,
                orp_nazev=self.orp_nazev, pou_nazev=self.pou_nazev, vusc_nazev=self.vusc_nazev,
                obec_nazev=self.obec_nazev, spravni_obec_nazev=self.spravni_obec_nazev,
                spravni_obec_kod=self.spravni_obec_kod, orp_kod=self.orp_kod, obec_kod=self.obec_kod,
                nuts_1=self.nuts_1, nuts_2=self.nuts_2, nuts_3=self.nuts_3, okres_nazev=self.okres_nazev,
                obec_statuskod=self.obec_statuskod, regionsoudrznosti_kod=self.regionsoudrznosti_kod,
                regionsoudrznosti_nazev=self.regionsoudrznosti_nazev, vusc_kod=self.vusc_kod, pou_kod=self.pou_kod,
                okres_kod=self.okres_kod
            ))
        return out


class PovodiInternal:
    id: int  # 00
    chp: str  # 01
    chp_u: str  # 02
    chp_d: str  # 03
    naz_tok: str  # 04
    naz_tok_2: str  # 05
    id_3: int  # 06
    naz_pov_3: str  # 07
    id_2: int  # 08
    naz_pov_2: str  # 09
    id_1: int  # 10
    naz_pov_1: str  # 11

    # wgs: CoordinatesGps
    # jtsk: Coordinates

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[0]
            self.chp = row[1]
            self.chp_u = row[2]
            self.chp_d = row[3]
            self.naz_tok = row[4]
            self.naz_tok_2 = row[5]
            self.id_3 = row[6]
            self.naz_pov_3 = row[7]
            self.id_2 = row[8]
            self.naz_pov_2 = row[9]
            self.id_1 = row[10]
            self.naz_pov_1 = row[11]

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None, ensure_ascii=False)

    @property
    def to_swagger(self):
        out = Povodi(
            id_value=self.id, naz_pov_1=self.naz_pov_1, naz_pov_2=self.naz_pov_2, naz_pov_3=self.naz_pov_3,
            naz_tok_2=self.naz_tok_2, naz_tok=self.naz_tok, chp=self.chp, chp_d=self.chp_d, chp_u=self.chp_u,
            id_1=self.id_1, id_2=self.id_2, id_3=self.id_3
        )
        return out


class Locality(dict, object):
    address: AddressInternal
    coordinates: Coordinates
    coordinates_gps: CoordinatesGps
    zsj: ZsjInternal

    def __init__(self, address, coordinates=None, coordinates_gps=None, zsj=None):
        dict.__init__(self, address=address, coordinates=coordinates, coordinates_gps=coordinates_gps, zsj=zsj)
        self.address = address
        self.coordinates = coordinates
        self.coordinates_gps = coordinates_gps
        self.zsj = zsj


class AdresniBodInteral:
    dist: float  # OO vzdalenost od bodu
    id: int  # 01 adresnimista.kod
    cislo_domovni: int  # 02 adresnimista.cislodomovni
    cislo_orientacni: int  # 03 adresnimista.cisloorientacni
    cislo_orientacni_pismeno: str  # 04 adresnimista.cisloorientacnipismeno
    typ_so: str  # typ čísla (č.p., č.ev.)
    psc: int  # 05 adresnimista.psc,
    cast_obce: str  # 10 castiobci.nazev,
    obec: str  # 12 obce.nazev,
    ulice: str  # 13 ulice.nazev,
    momc: str  # 14 momc.nazev,
    mop: str  # 16 mop.nazev

    def __init__(self, row: tuple):
        if row is not None:
            self.id = row[0]
            self.cislo_domovni = row[1]
            self.cislo_orientacni = row[2]
            self.cislo_orientacni_pismeno = row[3]
            self.typ_so = row[5]
            self.psc = row[4]
            self.cast_obce = row[9]
            self.obec = row[11]
            self.ulice = row[12]
            self.momc = row[13]
            self.mop = row[15]
            self.dist = row[16]
    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None, ensure_ascii=False)

    @property
    def to_address(self):
        adr = AddressInternal(
            street=self.ulice,
            zip_code=self.psc,
            locality=self.obec,
            locality_part=self.cast_obce,
            district_number=None,
            house_number=self.cislo_domovni,
            record_number=None,
            orientation_number=self.cislo_orientacni,
            orientation_number_character=self.cislo_orientacni_pismeno,
            ruian_id=self.id,
            district=None
        )
        if self.typ_so == 'č.ev.':
            adr.record_number = self.cislo_domovni
            adr.house_number = None
        else:
            adr.house_number = self.cislo_domovni
            adr.record_number = None
        if self.mop is not None:
            # Praha
            adr.district_number = self.mop.split(' ')[1]
            adr.locality_part = self.momc + '-' + self.cast_obce
        elif self.momc is not None:
            # velké město mimo Prahu
            adr.district = self.momc
            adr.district_number = None
        else:
            adr.district_number = None
            adr.district = None
        return adr


class _SearchItem:
    def __init__(self, item, text, field_name):
        self.item = item
        self.text = text
        self.fieldName = field_name

    def __repr__(self):
        return self.text + " (" + self.item.value + ")"

    def get_where_item(self):
        if self.item is None:
            return ""
        else:
            return self.fieldName + "= '" + self.text + "'"

    def get_id(self):
        return self.fieldName + ':' + self.text


def none_to_string(item):
    """
    Converts item to string, unlike str or repr, None is represented as "".

    1. None is represented as "".
    2. For tuple items, tupple with values as string returned
    3. For list items, list with values as string returned

    noneToString(None) = ""
    noneToString(3) = "3"
    noneToString('3') = "3"
    noneToString((None, 3, None)) = ("", "3", "")
    noneToString([None, 3, None]) = ["", "3", ""]

    :param item: Value to be converted to string.
    :return: String representation of item, none represented as ""
    """
    if isinstance(item, tuple):
        result = ()
        for sub_item in item:
            result = result + (none_to_string(sub_item),)
        return result
    elif isinstance(item, list):
        result = []
        for sub_item in item:
            result.append(none_to_string(sub_item))
        return result
    else:
        return [str(item), ""][item is None]


def formatzip_code(code):
    if code is None:
        return ""
    else:
        code = str(code)
        code = code.replace(" ", "")
        if code.isdigit():
            return code
        else:
            return ""


def empty_string_if_no_number(possible_number):
    out = ""
    if possible_number is not None:
        if str(possible_number).isdigit():
            out = str(possible_number)
    return out


def alpha_check(possible_alpha):
    out = ""
    if possible_alpha is not None and possible_alpha.isalpha():
        out = possible_alpha
    return out
