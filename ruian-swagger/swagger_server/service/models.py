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

from swagger_server.models import KatastralniUzemi, AdministrativeDivision, MapovyList50, \
    Parcela, Povodi, Zsj, Address, Coordinates, Jtsk, Wgs, Settlement, CadastralTerritory
from swagger_server.service.database import execute_sql, DATABASE_NAME_RUIAN


class CoordinatesInternal(dict, object):
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


class CoordinatesGpsInternal(dict, object):
    # WGS
    lat: float
    lon: float

    def __init__(self, lat, lon):
        dict.__init__(self, lat=lat, lon=lon)
        self.lat = lat
        self.lon = lon


class AddressInternal(dict, object):
    def __init__(self, street, house_number, record_number, orientation_number, orientation_number_character,
                 zip_code, locality, locality_part, district_number, district, ruian_id, jtsk_x, jtsk_y):
        dict.__init__(
            self, street=street, house_number=house_number, record_number=record_number,
            orientation_number=orientation_number, orientation_number_character=orientation_number_character,
            zip_code=zip_code, locality=locality, locality_part=locality_part, district_number=district_number,
            district=district, ruian_id=ruian_id, jtsk_x=jtsk_x, jtsk_y=jtsk_y
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
        self.jtsk_x = jtsk_x
        self.jtsk_y = jtsk_y

    @property
    def to_pretty(self):
        out = PrettyAddressInternal(
            self.street, self.house_number, self.record_number, self.orientation_number,
            self.orientation_number_character, self.zip_code, self.locality, self.locality_part,
            self.district_number, self.district, self.ruian_id, self.jtsk_x, self.jtsk_y
        )
        return out

    @property
    def to_swagger(self):
        def _to_wgs():
            if (self.jtsk_x is not None) and (self.jtsk_y is not None):
                x = abs(self.jtsk_x)
                y = abs(self.jtsk_y)
                geom = "ST_GeomFromText('POINT(-%s -%s)',5514)" % (str(x), str(y))
                sql = "SELECT ST_Transform(" + geom + ", 4326) AS wgs_geom;"
                cur = execute_sql(DATABASE_NAME_RUIAN, sql)
                row = cur.fetchone()
                cur.close()
                if row is None:
                    return None
                wgs_value = {'lon': row[0].coords[0], 'lat': row[0].coords[1]}
                return wgs_value
            else:
                return None

        jtsk = Jtsk(x=self.jtsk_x, y=self.jtsk_y)
        work = _to_wgs()
        wgs = None
        if work is not None:
            wgs = Wgs(lat=work['lat'], lon=work['lon'])
        coordinates = Coordinates(jtsk=jtsk, wgs=wgs)
        out = Address(
            street=self.street, ruian_id=self.ruian_id, zip_code=self.zip_code, locality=self.locality,
            locality_part=self.locality_part, house_number=self.house_number, record_number=self.record_number,
            district_number=self.district_number, orientation_number=self.orientation_number,
            orientation_number_character=self.orientation_number_character, district=self.district,
            coordinates=coordinates
        )
        return out


class PrettyAddressInternal(dict, object):
    def __init__(self, street, house_number, record_number, orientation_number, orientation_number_character,
                 zip_code, locality, locality_part, district_number, district, ruian_id, jtsk_x, jtsk_y):
        # Convert None values to "".
        (street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
         locality_part, district_number, district, ruian_id, jtsk_x, jtsk_y) = none_to_string(
            (street, house_number, record_number, orientation_number, orientation_number_character, zip_code, locality,
             locality_part, district_number, district, ruian_id, jtsk_x, jtsk_y)
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
        self.jtsk_x = jtsk_x
        self.jtsk_y = jtsk_y

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
            self.nazev = row[3]

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
    def __init__(self, row: tuple, offset=0):
        if row is not None:
            self.ku_kod = row[offset + 2]
            self.ku_nazev = row[offset + 3]
            self.obec_kod = row[offset + 4]
            self.obec_nazev = row[offset + 5]
            self.obec_statuskod = row[offset + 6]
            self.orp_kod = int(row[offset + 7])
            self.orp_nazev = row[offset + 8]
            self.spravni_obec_kod = row[offset + 8]
            self.spravni_obec_nazev = row[offset + 10]
            self.pou_kod = row[offset + 11]
            self.pou_nazev = row[offset + 12]
            self.okres_kod = row[offset + 15]
            self.okres_nazev = row[offset + 16]
            self.vusc_kod = row[offset + 17]
            self.vusc_nazev = row[offset + 18]
            self.regionsoudrznosti_kod = row[offset + 19]
            self.regionsoudrznosti_nazev = row[offset + 20]
            self.nuts_1 = 'CZ'
            self.nuts_2 = row[offset + 21]
            self.nuts_3 = row[offset + 22]
            self.nuts_lau1 = row[offset + 23]
            self.nuts_lau2 = row[offset + 24]
            self.id = self.ku_kod
            self.nazev = self.ku_nazev
            mp = row[offset + 26]
            self.jtsk_x = mp.geoms[0].x
            self.jtsk_y = mp.geoms[0].y

    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=None)

    @property
    def administrative_division(self):
        out = AdministrativeDivision(
            ku_kod=self.ku_kod, ku_nazev=self.ku_nazev, nuts_lau1=self.nuts_lau1, nuts_lau2=self.nuts_lau2,
            orp_nazev=self.orp_nazev, pou_nazev=self.pou_nazev, vusc_nazev=self.vusc_nazev,
            obec_nazev=self.obec_nazev, spravni_obec_nazev=self.spravni_obec_nazev,
            spravni_obec_kod=self.spravni_obec_kod, orp_kod=self.orp_kod, obec_kod=self.obec_kod,
            nuts_1=self.nuts_1, nuts_2=self.nuts_2, nuts_3=self.nuts_3, okres_nazev=self.okres_nazev,
            obec_statuskod=self.obec_statuskod, regionsoudrznosti_kod=self.regionsoudrznosti_kod,
            regionsoudrznosti_nazev=self.regionsoudrznosti_nazev, vusc_kod=self.vusc_kod, pou_kod=self.pou_kod,
            okres_kod=self.okres_kod
        )
        return out

    @property
    def to_swagger(self):
        out = KatastralniUzemi(
            id_value=self.ku_kod,
            nazev=self.ku_nazev,
            administrative_division=self.administrative_division
        )
        return out

    @property
    def cadastral_territory(self):
        ct = CadastralTerritory(
            id_value=self.ku_kod,
            nazev=self.ku_nazev
        )
        return ct


class ZsjInternal(KatastralniUzemiInternal):
    # Zakladni sidelni jednotka
    def __init__(self, row: tuple):
        if row is not None:
            super().__init__(row=row, offset=2)
            self.id = row[2]
            self.zsj_id = row[2]
            self.nazev = row[3]
            self.zsj_nazev = row[3]

        """
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
        """

    @property
    def to_swagger(self):
        sett = Settlement(id_value=self.zsj_id, nazev=self.zsj_nazev)
        out = Zsj(
            settlement=sett,
            administrative_division=self.administrative_division
        )
        return out

    @property
    def settlement(self):
        sett = Settlement(id_value=self.zsj_id, nazev=self.zsj_nazev)
        return sett


class ParcelaInternal(KatastralniUzemiInternal):
    def __init__(self, row: tuple):
        if row is not None:
            super().__init__(row=row, offset=4)
            self.id = row[2]
            self.parcela_id = row[2]
            self.kmenovecislo = row[3]
            self.pododdelenicisla = row[4]
            self.vymeraparcely = row[5]
            # self.nazev = ''
        """
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
        """

    @property
    def to_swagger(self):
        out = Parcela(
            id_value=self.parcela_id,
            kmenovecislo=self.kmenovecislo, pododdelenicisla=self.pododdelenicisla, vymeraparcely=self.vymeraparcely,
            administrative_division=self.administrative_division)
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
    coordinates: CoordinatesInternal
    coordinates_gps: CoordinatesGpsInternal
    zsj: ZsjInternal

    def __init__(self, address, coordinates=None, coordinates_gps=None, zsj=None):
        dict.__init__(self, address=address, coordinates=coordinates, coordinates_gps=coordinates_gps, zsj=zsj)
        self.address = address
        self.coordinates = coordinates
        self.coordinates_gps = coordinates_gps
        self.zsj = zsj


class AdresniBodInternal:
    id: int  # 00 adresnimista.kod
    cislo_domovni: int  # 01 adresnimista.cislodomovni
    cislo_orientacni: int  # 02 adresnimista.cisloorientacni
    cislo_orientacni_pismeno: str  # 03 adresnimista.cisloorientacnipismeno
    typ_so: str  # 05 typ čísla (č.p., č.ev.)
    psc: int  # 04 adresnimista.psc,
    cast_obce: str  # 09 castiobci.nazev,
    obec: str  # 11 obce.nazev,
    ulice: str  # 12 ulice.nazev,
    momc: str  # 13 momc.nazev,
    mop: str  # 15 mop.nazev,
    jtsk_x: float  # 16 latitude = -x,
    jtsk_y: float  # 17 longitude = -y
    dist: float  # 18 vzdalenost od bodu

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
            self.jtsk_x = -float(row[16])
            self.jtsk_y = -float(row[17])
            self.dist = row[18]

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
            district=None,
            jtsk_y=self.jtsk_y,
            jtsk_x=self.jtsk_x
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
