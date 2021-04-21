# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import codecs
from collections import defaultdict

from ruian_services.services import compile_address
from ruian_services.services.postgis_db import open_connection, none_to_string
from shared_tools import shared

shared.setup_paths()

ADDRESS_POINTS_TABLENAME = "address_points"
FULLTEXT_TABLENAME = "fulltext"

TOWN_NAME_FIELDNAME = "nazev_obce"
STREET_NAME_FIELDNAME = "nazev_ulice"
TOWN_PART_FIELDNAME = "nazev_casti_obce"
GID_FIELDNAME = "gid"
GIDS_FIELDNAME = "gids"
TYP_SO_FIELDNAME = "typ_so"
CISLO_DOMOVNI_FIELDNAME = "cislo_domovni"
CISLO_ORIENTACNI_FIELDNAME = "cislo_orientacni"
ZNAK_CISLA_ORIENTACNIHO_FIELDNAME = "znak_cisla_orientacniho"
ZIP_CODE_FIELDNAME = "psc"
MOP_NUMBER = "nazev_mop"

# Konstanty pro logickou strukturu databáze
MAX_TEXT_COUNT = 3  # maximální počet textových položek v adrese ulice, obec, část obce = 3
ORIENTATION_NUMBER_ID = "/"
RECORD_NUMBER_ID = "č.ev."
DESCRIPTION_NUMBER_ID = "č.p."
RECORD_NUMBER_MAX_LEN = 4
ORIENTATION_NUMBER_MAX_LEN = 3
DESCRIPTION_NUMBER_MAX_LEN = 3
HOUSE_NUMBER_MAX_LEN = 4
ZIPCODE_LEN = 5

exact_match_needed = False


class RUIANDatabase:
    def __init__(self, test=False):
        self.connection = open_connection(test=test)

    def get_query_result(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row)
        return rows

    def get_obec_by_name(self, name):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT {0} FROM {1} WHERE {0} ilike '%{2}%' group by {0} limit 25".format(
                TOWN_NAME_FIELDNAME, "obce", name))

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row[0])
        return rows

    def get_ulice_by_name(self, name):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT {0} FROM {1} WHERE {0} ilike '%{2}%' group by {0} limit 25".format(
                STREET_NAME_FIELDNAME, "ulice", name))

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row[0])
        return rows

    def get_cast_obce_by_name(self, name):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT {0} FROM {1} WHERE {2} ilike '%{3}%' group by {0} limit 25".format(
                "nazev_casti_obce", "ac_casti_obce", "nazev_casti_obce", name
            )
        )

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row[0])
        return rows

    def get_select_results(self, sql_select_clause):
        cursor = self.connection.cursor()
        cursor.execute(sql_select_clause)

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row)
        return rows


ruian_database = RUIANDatabase(test=False)


def is_int(value):
    if value is None or value == "":
        return False
    else:
        for i in range(len(value)):
            if "0123456789".find(value[i:i + 1]) < 0:
                return False
        return True


class AddressItem:
    def __init__(self, value, search_db=True):
        self.value = value
        self.towns = []
        self.townParts = []
        self.streets = []
        self.isRecordNumber = False
        self.isOrientationNumber = False
        self.isDescriptionNumber = False
        self.isZIP = False
        self.isHouseNumber = False
        self.number = None
        self.maxNumberLen = 0
        self.isNumberID = False
        self.isTextField = False
        self.analyse_value(search_db)

    def __repr__(self):
        result = ""
        if self.isZIP:
            result += "PSČ "
        if self.isOrientationNumber:
            result += "č.or. "
        if self.isRecordNumber:
            result += RECORD_NUMBER_ID + " "
        if self.isDescriptionNumber:
            result += DESCRIPTION_NUMBER_ID + " "
        if self.number is None:
            result += '"' + self.value + '"'
        else:
            result += self.number

        return result

    def match_percent(self, candidate_value, field_index):
        # fieldIndex meaning:
        # 0=GID_FIELDNAME
        # 1=TOWN_NAME_FIELDNAME
        # 2=TOWN_PART_FIELDNAME
        # 3=STREET_NAME_FIELDNAME
        # 4=TYP_SO_FIELDNAME
        # 5=CISLO_DOMOVNI_FIELDNAME
        # 6=CISLO_ORIENTACNI_FIELDNAME
        # 7=ZNAK_CISLA_ORIENTACNIHO_FIELDNAME
        # 8=ZIP_CODE_FIELDNAME
        # 9=MOP_NUMBER
        candidate_value = str(candidate_value).lower()
        if candidate_value == "677":
            pass
        if self.isZIP:
            if field_index != 8 or len(candidate_value) != 5:
                return 0
        else:
            if field_index == 0:
                if len(candidate_value) != len(self.value):
                    return 0
            if field_index == 8:
                if len(candidate_value) == 5 and candidate_value == self.value:
                    return 100
                else:
                    return 0

        if candidate_value.find(self.value.lower()) != 0:
            return 0
        else:
            return 1.0 * len(str(self.value)) / len(candidate_value)

    def __str__(self):
        result = ""
        if self.isZIP:
            result += "PSČ "
        if self.isOrientationNumber:
            result += "č.or. "
        if self.isRecordNumber:
            result += RECORD_NUMBER_ID + " "
        if self.isDescriptionNumber:
            result += DESCRIPTION_NUMBER_ID + " "
        if self.number is None:
            result += '"' + self.value + '" ' + str(len(self.streets)) + "," + str(len(self.towns)) + \
                      "," + str(len(self.townParts))
        else:
            result += self.number

        return result

    def analyse_value(self, search_db=True):
        if is_int(self.value):
            self.number = self.value
            pass
        elif self.value == ORIENTATION_NUMBER_ID:
            self.isOrientationNumber = True
            self.isNumberID = True
            self.maxNumberLen = ORIENTATION_NUMBER_MAX_LEN
        elif self.value == RECORD_NUMBER_ID:
            self.isRecordNumber = True
            self.isNumberID = True
            self.maxNumberLen = RECORD_NUMBER_MAX_LEN
        elif self.value == DESCRIPTION_NUMBER_ID:
            self.isDescriptionNumber = True
            self.isNumberID = True
            self.maxNumberLen = DESCRIPTION_NUMBER_MAX_LEN
        else:
            self.isTextField = True
            if search_db:
                self.towns = ruian_database.get_obec_by_name(self.value)
                self.streets = ruian_database.get_ulice_by_name(self.value)
                self.townParts = ruian_database.get_cast_obce_by_name(self.value)


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


def normalize_separators(address):
    address = address.replace(ORIENTATION_NUMBER_ID, " ")
    address = address.replace("  ", " ")
    address = address.replace(",,", ",")
    address = address.replace(" ,", ",")
    address = address.replace(", ", ",")
    address = address.replace("\r\r", "\r")
    address = address.replace("\r", ",")
    address = address.replace("\n\n", ",")
    address = address.replace("\n", ",")
    return address


def normalize_description_number_id(address):
    address = address.replace("čp ", DESCRIPTION_NUMBER_ID + " ")
    address = address.replace("č. p.", DESCRIPTION_NUMBER_ID)
    address = address.replace("čp.", DESCRIPTION_NUMBER_ID)
    return address


def expand_nad_pod(address):
    address = address.replace(" n ", " nad ")
    address = address.replace(" n.", " nad ")
    address = address.replace(" p ", " pod ")
    address = address.replace(" p.", " pod ")
    return address


def normalise_record_number_id(address):
    address = address.replace("ev.č.", RECORD_NUMBER_ID)
    address = address.replace("ev č.", RECORD_NUMBER_ID)
    address = address.replace("evč.", RECORD_NUMBER_ID)
    address = address.replace("eč.", RECORD_NUMBER_ID)
    address = address.replace("ev. č.", RECORD_NUMBER_ID)
    address = address.replace("č. ev.", RECORD_NUMBER_ID)
    address = address.replace("čev.", RECORD_NUMBER_ID)
    if address.find("č.ev") >= 0 and address.find("č.ev") != address.find(RECORD_NUMBER_ID):
        address = address.replace("č.ev", RECORD_NUMBER_ID, 1)
    return address


def separate_numbers(address):
    new_address = ""
    was_number = False
    for i in range(len(address)):
        act_char = address[i:i + 1]
        if "0123456789".find(act_char) >= 0:
            if i > 0 and not was_number:
                new_address += ","
            was_number = True
            new_address += act_char
        elif was_number:
            new_address += act_char + ","
            was_number = False
        else:
            new_address += act_char

    return normalize_separators(new_address)


def normalize(address):
    address = normalize_separators(address)
    address = normalize_description_number_id(address)
    address = normalise_record_number_id(address)
    address = expand_nad_pod(address)
    address = separate_numbers(address)
    return address


def parse(address, search_db=True):
    address = normalize(address)
    string_items = address.split(",")
    items = []
    for value in string_items:
        item = AddressItem(value, search_db)
        items.append(item)
    return items


def analyse_items(items):
    new_items = []
    index = 0
    next_item_to_be_skipped = False
    for item in items:
        if next_item_to_be_skipped:
            next_item_to_be_skipped = False
            continue

        if index == len(items) - 1:
            next_item = None
        else:
            next_item = items[index + 1]

        to_be_skipped = False
        if item.isNumberID:
            if next_item is None or next_item.number is None or len(next_item.number) > item.maxNumberLen:
                to_be_skipped = True
                # Error, za indikátorem č.ev.,č.or.,/ nenásleduje číslice nebo je příliš dlouhá
            else:
                item.number = next_item.number
                next_item_to_be_skipped = True

        elif item.number is not None:
            if next_item is not None and next_item.number is not None and len(item.number) + len(
                    next_item.number) == ZIPCODE_LEN:
                item.number += next_item.number
                next_item_to_be_skipped = True

            if len(item.number) == ZIPCODE_LEN:
                item.isZIP = True
            elif len(item.number) <= HOUSE_NUMBER_MAX_LEN:
                item.isHouseNumber = True
            else:
                # Error, příliš dlouhé číslo domovní nebo evidenční
                pass
        else:
            # else textový řetezec
            # @TODO Udelat
            # if item.streets == [] and item.streets == [] and item.streets == []:
            #    toBeSkipped = True
            pass

        if not to_be_skipped:
            new_items.append(item)

        index = index + 1

    return new_items


def analyze(address, search_db=True):
    items = parse(address, search_db)
    return analyse_items(items)


def old_get_combined_text_searches(items):
    sql_list = []
    sql_sub_list = []

    def add_combination(sql_condition):
        if not sql_sub_list:
            sql_sub_list.append(sql_condition)
        else:
            for i in range(len(sql_sub_list)):
                sql_sub_list[i] += " and " + sql_condition

    def add_candidates(field_name, value_list):
        if value_list is not None and value_list != []:
            for list_item in value_list:
                add_combination(field_name + " = '" + list_item + "'")

    for item in items:
        if item.isTextField():
            sql_sub_list = []
            add_candidates(TOWN_NAME_FIELDNAME, item.towns)
            add_candidates(TOWN_PART_FIELDNAME, item.townParts)
            add_candidates(STREET_NAME_FIELDNAME, item.streets)

            if not sql_list:
                sql_list.extend(sql_sub_list)
            else:
                new_list = []
                for oldItem in sql_list:
                    for newItem in sql_sub_list:
                        new_list.append(oldItem + " and " + newItem)
                sql_list = []
                sql_list.extend(new_list)
    return sql_list


def get_text_items(items):
    result = []
    for item in items:
        if item.isTextField():
            result.append(item)
        if len(result) == MAX_TEXT_COUNT:
            break
    return result


def get_text_variants(text_items):
    streets = extract_street_items(text_items)
    towns = extract_town_items(text_items)
    town_parts = extract_town_part_items(text_items)
    if not streets:
        streets = [_SearchItem(None, None, None)]
    if not towns:
        towns = [_SearchItem(None, None, None)]
    if not town_parts:
        town_parts = [_SearchItem(None, None, None)]
    return streets, towns, town_parts


def expanded_text_items(search_items):
    result = [
        extract_street_items(search_items),
        extract_town_items(search_items),
        extract_town_part_items(search_items)
    ]
    return result


def extract_street_items(search_items):
    result = []
    for item in search_items:
        for street in item.streets:
            result.append(_SearchItem(item, street, STREET_NAME_FIELDNAME))
    return result


def extract_town_items(search_items):
    result = []
    for item in search_items:
        for town in item.towns:
            result.append(_SearchItem(item, town, TOWN_NAME_FIELDNAME))
    return result


def extract_town_part_items(search_items):
    result = []
    for item in search_items:
        for town_part in item.townParts:
            result.append(_SearchItem(item, town_part, TOWN_PART_FIELDNAME))
    return result


def get_combined_text_searches(items):
    text_items = get_text_items(items)
    sql_items = []
    for item in text_items:
        sql_items.append(item)

    return []


def get_candidate_values(analyzed_items):
    sql_items = []
    for item in analyzed_items:
        if item.isTextField and len(item.value) >= 2:
            sql_items.append("searchstr ilike '%" + item.value + "%'")
    if sql_items:
        inner_sql = "select {0}({1}) from {2} where {3}".format(
            "explode_array", GIDS_FIELDNAME, FULLTEXT_TABLENAME, " and ".join(sql_items))
        sql = "select {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {11} from {9} where {12} IN ({10} limit 1000)".format(
            GID_FIELDNAME, TOWN_NAME_FIELDNAME, TOWN_PART_FIELDNAME, STREET_NAME_FIELDNAME, TYP_SO_FIELDNAME,
            CISLO_DOMOVNI_FIELDNAME, CISLO_ORIENTACNI_FIELDNAME, ZNAK_CISLA_ORIENTACNIHO_FIELDNAME,
            ZIP_CODE_FIELDNAME, ADDRESS_POINTS_TABLENAME, str(inner_sql), MOP_NUMBER, "gid")
        candidates = ruian_database.get_query_result(sql)
        return candidates
    else:
        return []


def compare(items, field_values):
    sum_match_percent = 0
    num_matches = 0
    for item in items:
        found = False
        field_index = 0
        for field_value in field_values:
            match_percent = item.match_percent(field_value, field_index)
            if match_percent > 0:
                sum_match_percent = sum_match_percent + match_percent
                num_matches = num_matches + 1
                found = True
                break
            field_index = field_index + 1

        if not found:
            return 0

    return sum_match_percent / num_matches


def add_id(identifier, value, string_item, builder):
    if builder.formatText == "json":
        return '\t"%s": %s,\n%s' % (identifier, value, string_item)
    elif builder.formatText == "xml":
        return '\t<%s>%s</%s>\n%s' % (identifier, value, identifier, string_item)
    else:
        return value + builder.lineSeparator + string_item


def build_address(builder, candidates, with_id, with_distance=False):
    items = []
    for item in candidates:
        if item[4] == "č.p.":
            house_number = str(item[5])
            record_number = ""
        else:
            house_number = ""
            record_number = str(item[5])

        mop = none_to_string(item[9])
        if mop != "":
            pom = mop.split()
            district_number = pom[1]
        else:
            district_number = ""

        sub_str = compile_address.compile_address(
            builder,
            none_to_string(item[3]),
            house_number,
            record_number,
            none_to_string(item[6]),
            none_to_string(item[7]),
            str(item[8]),
            none_to_string(item[1]),
            none_to_string(item[2]),
            district_number
        )
        if with_id:
            sub_str = add_id("id", str(item[0]), sub_str, builder)
        if with_distance:
            sub_str = add_id("distance", str(item[10]), sub_str, builder)
        items.append(sub_str)
    return items


def full_text_search_address(address):
    items = analyze(address, False)
    candidates_ids = get_candidate_values(items)

    results_dict = defaultdict(list)
    for candidate in candidates_ids:
        match_percent = compare(items, candidate)
        if match_percent > 0:
            if match_percent in results_dict:
                results_dict[match_percent].append(candidate)
            else:
                results_dict[match_percent] = [candidate]
    results = []

    def add_candidate(key_item, candidate_item_value):
        global exact_match_needed
        if not results:
            exact_match_needed = key_item == 1

        continue_loop = not exact_match_needed or (exact_match_needed and key_item == 1)
        if continue_loop:
            results.append(candidate_item_value)
        return continue_loop

    for key in reversed(sorted(results_dict)):
        candidate_item = results_dict[key]
        if isinstance(candidate_item, list):
            for candidate in candidate_item:
                add_candidate(key, candidate)
        else:
            add_candidate(key, candidate_item)
    return results


def init_module():
    global ruian_database
    ruian_database = RUIANDatabase()


class FormalTester:
    def __init__(self, caption, desc, compiling_person, tester):
        self.numTests = 0
        self.caption = caption
        self.desc = desc
        self.compilingPerson = compiling_person
        self.tester = tester
        self.testsHTML = """
<table>
    <tr>
            <th>#</th><th></th><th>Vstup</th><th>Výsledek</th><th>Pozn</th>
    </tr>
"""

    def add_test(self, inputs, result, expected_result, error_message=""):
        self.numTests = self.numTests + 1

        if str(result) == expected_result:
            status = "checked"
            print("   ok :", inputs, "-->", result)
            expected_result_message = ""
        else:
            status = ""
            expected_result_message = " &lt; &gt; " + expected_result
            print("chyba :", inputs, "-->", result, "<>", expected_result, error_message)
        self.testsHTML += "<tr>\n"
        self.testsHTML += "    <td>" + str(self.numTests) + "</td>"
        self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' />' + "</td>"

        self.testsHTML += "    <td>" + inputs + "</td>"
        self.testsHTML += "    <td>--> " + str(result) + expected_result_message + "</td>"
        self.testsHTML += "    <td>" + error_message + "</td>"
        self.testsHTML += "</tr>\n"

    def get_html(self):
        result = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    </head>
    <body>"""
        if self.caption != "":
            result += "<h1>" + self.caption + "</h1>\n"
        if self.desc != "":
            result += "<p>" + self.desc + "</p>\n"
        result += self.testsHTML + "</table>"
        result += """
    </body>
</html>"""

        return result


def test_analyse():
    # parser = AddressParser()
    tester = FormalTester(
        "Rozpoznávání typů adresních položek",
        """Skupina testů zajišťujících rozpoznání jednotlivých typů adresních položek v adresním řetězci.
Jednotlivé testy spadají do kategorie tzv. "unit testů", tj. hodnoty a kombinace nemusí být zcela reálné, cílem je
úplná sada eliminující možné chyby.
V této skupině testů je také testováno párování identifikátorů jednotlivých položek se svými hodnotami.
""",
        "Ing. Tomáš Vacek", "Ing. Radek Makovec")

    def do_test(value, expected_value, error_message=""):
        tester.add_test(value, analyze(value), expected_value, error_message)

    do_test("Pod lesem 1370 č. ev. 1530 Lipník n ", '["Pod lesem", 1370, č.ev. 1530, "Lipník nad "]')

    do_test("3/13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")
    do_test("3/ 13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")
    do_test("3 / 13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")

    do_test("č. p. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    do_test("čp. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    do_test("č.p. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    do_test("č.p.113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    do_test("čp 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    do_test("čp113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')

    do_test("16300", "[PSČ 16300]", 'Rozpoznání PSČ')
    do_test("1 6300", "[PSČ 16300]", 'Rozpoznání PSČ')
    do_test("16 300", "[PSČ 16300]", 'Rozpoznání PSČ')
    do_test("163 00", "[PSČ 16300]", 'Rozpoznání PSČ')
    do_test("1630 0", "[PSČ 16300]", 'Rozpoznání PSČ')

    do_test("Pod lesem 1370 č. ev. 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]',
            'Rozpoznání čísla evidenčního')
    do_test("Pod lesem 1370 č.ev. 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]',
            'Rozpoznání čísla evidenčního')
    do_test("Pod lesem 1370 č. ev.1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]',
            'Rozpoznání čísla evidenčního')
    do_test("Pod lesem 1370 č.ev 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]',
            'Rozpoznání čísla evidenčního')
    do_test("Pod lesem 1370 č.ev1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]',
            'Rozpoznání čísla evidenčního')
    do_test("Pod lesem 1370 čev.1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]',
            'Rozpoznání čísla evidenčního')

    do_test("Roudnice n Labem", '["Roudnice nad Labem"]', "Chybný zápis nad")
    do_test("Roudnice n. Labem", '["Roudnice nad Labem"]', "Chybný zápis nad")

    do_test("Brněnská 1370 č. p. 113, Březová", '["Brněnská", 1370, č.p. 113, "Březová"]')

    do_test("Pod lesem 1370 č. ev. 1530 Svatý Jan p skalo", '["Pod lesem", 1370, č.ev. 1530, "Svatý Jan pod skalo"]')
    do_test("Pod lesem 1370 č. ev. 1530 Lipník n ", '["Pod lesem", 1370, č.ev. 1530, "Lipník nad "]')

    with codecs.open("parseaddress_tests.html", "w", "utf-8") as outFile:
        html_content = tester.get_html()
        outFile.write(html_content)
        outFile.close()


def test_full_text_search_address():
    tester = FormalTester(
        "Rozpoznávání typů adresních položek",
        """Skupina testů zajišťujících rozpoznání jednotlivých typů adresních položek v adresním řetězci.
Jednotlivé testy spadají do kategorie tzv. "unit testů", tj. hodnoty a kombinace nemusí být zcela reálné, cílem je
úplná sada eliminující možné chyby.
V této skupině testů je také testováno párování identifikátorů jednotlivých položek se svými hodnotami.
""",
        "Ing. Tomáš Vacek", "Ing. Radek Makovec")

    # parser.fullTextSearchAddress("Klostermannova 586, Hořovice, 26801")
    # parser.fullTextSearchAddress("Hořo, Klostermann 586, 26801")
    full_text_search_address("Hořo, Klostermann 7, 26801")
    full_text_search_address("Budovatelů 677")
    full_text_search_address("Budovatelů 676")
    full_text_search_address("Budovatelů 678")

    with codecs.open("parseaddress.html", "w", "utf-8") as outFile:
        html_content = tester.get_html()
        outFile.write(html_content)
        outFile.close()


def test_case():
    # print full_text_search_address("Mezilesní 550/18")
    # print full_text_search_address("U kamene 181")
    # print full_text_search_address("Na lánech 598/13")
    # res = full_text_search_address("Fialková, Čakovičky")
    # print len(res), res

    # print parser.fullTextSearchAddress("22316418 praha")
    # print parser.fullTextSearchAddress("1 Cílkova")
    print(full_text_search_address("67 budovatelů"))


init_module()


def main():
    # test_analyse()
    # test_full_text_search_address()
    test_case()


if __name__ == '__main__':
    main()
