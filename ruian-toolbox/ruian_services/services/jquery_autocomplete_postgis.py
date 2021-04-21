# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        jqueryautocompletePostGIS
# Purpose:     Implementuje funkcionalitu pro autocomplete pomocí jQuery
#              napojením na databázi RÚIAN uloženou v PostGIS.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------
import logging

import psycopg2

from ruian_services.services import compile_address, http_shared
from ruian_services.services.config import config
from ruian_services.services.http_shared import value_to_str, extract_dictrict_number
from shared_tools import DatabaseRuianError

AC_OBCE = "ac_obce"
AC_PSC = "ac_psc"
AC_ULICE = "ac_ulice"
AC_CASTI_OBCE = "ac_casti_obce"
ADDRESSPOINTS_TABLENAME = "address_points"
LOCALITY_QUERY_ID = "Locality"
LOCALITY_PART_QUERY_ID = "LocalityPart"
PAGESIZE_QUERYPARAM = "PageSize"
FIRSTROW_QUERYPARAM = "FirstRow"


class PostGISDatabase:
    def __init__(self):
        self.conection = psycopg2.connect(
            host=config.databaseHost, database=config.databaseName,
            port=config.databasePort, user=config.databaseUserName,
            password=config.databasePassword)

    def get_query_result(self, query):
        cursor = self.conection.cursor()
        cursor.execute(query)

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row)
        return rows

    def get_obec_by_name(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT obce FROM " + AC_OBCE + " WHERE nazev_obce like '%" + name + "%'")

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            data = row[0]
            data = data[1:len(data) - 1]
            rows.append(data)
        return rows

    def get_zip_by_street_and_town(self, street_name, town_name):
        cursor = self.conection.cursor()
        sql = "SELECT {0} FROM {1} WHERE {2} = '{3}' AND {4} = '{5}'".format(
            'psc', 'addresspoints', 'nazev_obce', town_name, 'nazev_ulice', street_name)
        cursor.execute(sql)

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            data = row[0]
            data = data[1:len(data) - 1]
            rows.append(data)
        return rows


def analyse_row(typ_so, cislo_domovni):
    house_number = None
    record_number = None
    if typ_so[-3:] == ".p.":
        house_number = http_shared.number_to_string(cislo_domovni)
        record_number = ""
    elif typ_so[-3:] == "ev.":
        house_number = ""
        record_number = http_shared.number_to_string(cislo_domovni)
    else:
        pass
    return house_number, record_number


def item_to_str(item):
    return value_to_str(item)


builder = http_shared.MimeBuilder("texttoonerow")

ID_VALUE = 'id'


def get_autocomplete_one_item_results(ruian_type, name_token, max_count=10):
    if ruian_type == "":
        ruian_type = ID_VALUE
    name_token = name_token.lower()
    sql = None
    # join_separator = ", "
    if ruian_type == ID_VALUE:
        sql = "SELECT {0} FROM {1} WHERE cast({0} AS TEXT) ILIKE '{2}%'".format('gid', 'gids', name_token)
        # sql = "select gid from gids where cast(gid as text) ilike '" + name_token + "%'"
    sql += " LIMIT " + str(max_count)
    cursor = _execute_sql(sql)
    if cursor is None:
        raise DatabaseRuianError(module=__name__, message=sql)
    rows = []
    row_count = 0
    for row in cursor:
        row_count += 1
        v = str(row[0])
        value = '{"id":"' + v + '","label":"' + v + '","value":"' + v + '"}'
        rows.append(value)
        if row_count >= max_count:
            break

    return rows


def parse_full_text_token(query_params, name_token):
    has_number = False

    if name_token.isdigit():
        # jedná se o PSČ nebo číslo bez ulice
        if len(name_token) < 2:
            return False, ""
        else:
            name = ""
            cislo = name_token
            has_number = True
    else:
        name = name_token
        cislo = ""
        del_pos = name_token.rfind(" ")
        if del_pos >= 0:
            # je druhá část cislo?
            name = name_token[:del_pos]
            cislo = name_token[del_pos + 1:]
            if cislo.isdigit():
                has_number = True
            else:
                cislo = ""
                name = name_token

    if has_number:
        where_list = []
        if name != "":
            where_list.append("nazev_ulice ilike '%{0}%'".format(name))
        else:
            where_list.append("nazev_ulice is null")

        if cislo != "":
            where_list.append("(cast({0} as text) ilike '{1}%' or cast({2} as text) ilike '{1}%')".format(
                'cislo_domovni', cislo, 'cislo_orientacni'))
        sql = 'select {0}, cast({1} as text), {2}, cast({3} as text), cast({4} as text), '.format(
            'nazev_ulice', 'cislo_domovni', 'nazev_obce', 'psc', 'cislo_orientacni')
        sql += '{0}, {1}, {2}, {3} from {4} where {5}'.format(
            'znak_cisla_orientacniho', 'nazev_casti_obce', 'typ_so', 'nazev_mop', 'address_points',
            " and ".join(where_list)
        )
        """
        sql = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text),' \
              'cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop from ' \
              'address_points where ' + " and ".join(where_list)
        """

    else:
        sql = "select nazev_ulice, nazev_obce from " + AC_ULICE + " where nazev_ulice ilike '%" + name_token + "%' group by nazev_ulice, nazev_obce order by nazev_ulice, nazev_obce"

    locality_name = get_query_value(query_params, "localityName", "")
    if locality_name != "":
        sql += " and nazev_obce ilike '%" + locality_name + "%'"

    locality_part = get_query_value(query_params, "localityPart", "")
    if locality_part != "":
        sql += " and nazev_casti_obce ilike '%" + locality_part + "%'"

    return has_number, sql


def get_rows(search_sql, max_count=15):
    rows = []
    if search_sql != "" and max_count != 0:
        search_sql += " limit " + str(max_count)
        cursor = _execute_sql(search_sql)
        if cursor is None:
            raise DatabaseRuianError(module=__name__, message=search_sql)
        row_count = 0
        row_label = None
        for row in cursor:
            row_count += 1
            html_items = []
            for i in range(len(row)):
                html_items.insert(0, row[i])
                row_label = None
            if len(row) == 1:
                id_value = ""
                row_value = row[0]
            else:
                row_value = row[1]
                id_value = row[0]
            if row_label is None:
                row_label = ", ".join(html_items)
            value = '{ "id" : "%s", "label" : "%s", "value" : "%s" }' % (id_value, row_label, row_value)
            rows.append(value)
            if row_count >= max_count:
                break
    return rows


def get_autocomplete_rows(search_sql, field_count=0, max_count=15):
    rows = []
    if search_sql != "":
        search_sql += " limit " + str(max_count)
        cursor = _execute_sql(search_sql)
        if cursor is None:
            raise DatabaseRuianError(module=__name__, message=search_sql)
        row_count = 0
        for row in cursor:
            row_count += 1

            label_items = []
            id_items = []
            for field in row:
                label_items.append(str(field))
                id_items.append(str(field))

            while len(id_items) < field_count:
                id_items.append("")

            row_label = ", ".join(label_items)
            id_value = ", ".join(id_items[1:])

            value = '{ "id" : "%s", "label" : "%s", "value" : "%s" }' % (id_value, row_label, row[0])

            rows.append(value)

            if row_count >= max_count:
                break

    return rows


def get_query_value(query_params, id_value, default_value):
    # Vrací hodnotu URL Query parametruy id, pokud neexistuje, vrací hodnotu defValue
    if id_value in query_params:
        return query_params[id_value]
    else:
        return default_value


def get_sql_where_clause(query_params, param_list, and_is_before_clause=True):
    result = u""
    for key in param_list:
        value = get_query_value(query_params, key, "")
        if value != "":
            if and_is_before_clause:
                result += " and "
            result += param_list[key] + " ilike '%" + value + "%'"
            if not and_is_before_clause:
                result += " and "

    return result


def select_sql(search_sql):
    if search_sql is None or search_sql == "":
        return None
    cursor = _execute_sql(search_sql)
    if cursor is None:
        raise DatabaseRuianError(module=__name__, message=search_sql)
    return cursor


def get_fill_results(query_params):
    sql_items = {
        "house_number": "cast(cislo_domovni as text) like '%s%%' and typ_so='č.p.'",
        "RecordNumber": "cast(cislo_domovni as text) ilike '%s%%' and typ_so<>'č.p.'",
        "OrientationNumber": "cast(cislo_orientacni as text) like '%s%%'",
        "OrientationNumberCharacter": "znak_cisla_orientacniho = '%s'",
        "zip_code": "cast(psc as text) like '%s%%'",
        "Locality": "nazev_obce ilike '%%%s%%'",
        "Street": "nazev_ulice ilike '%%%s%%'",
        "LocalityPart": "nazev_casti_obce ilike '%%%s%%'",
        "DistrictNumber": "nazev_mop = 'Praha %s'"
    }
    first_row = int(get_query_value(query_params, FIRSTROW_QUERYPARAM, "0"))
    if first_row < 0:
        first_row = 0
    page_size = int(get_query_value(query_params, PAGESIZE_QUERYPARAM, "15"))

    limit_value = 100
    if limit_value < first_row + page_size:
        limit_value = first_row + page_size

    fields = " cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, nazev_casti_obce, nazev_mop, nazev_ulice, typ_so "
    # result = ""

    sql_parts = []
    for key in sql_items:
        value = get_query_value(query_params, key, "")
        if value != "":
            sql_parts.append(sql_items[key] % value)  # tak to musi zustat - viz sql_items
    if len(sql_parts) == 0:
        return ""
    sql_base = " from {0} where {1}".format(ADDRESSPOINTS_TABLENAME, " and ".join(sql_parts))
    search_sql = "select {0} {1} order by  {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10} limit {11}".format(
        fields, sql_base, 'nazev_obce', 'nazev_casti_obce', 'psc', 'nazev_ulice', 'nazev_mop', 'typ_so',
        'cislo_domovni', 'cislo_orientacni', 'znak_cisla_orientacniho', limit_value)
    rows = select_sql(search_sql)

    result_array = []
    row_number = 0
    for row in rows:
        if row_number >= first_row:
            html_items = []
            for i in range(len(row)):
                html_items.append(http_shared.number_to_string(row[i]))
            (house_number, orientation_number, orientation_number_character, zip_code,
             locality, locality_part, nazev_mop, street, typ_so) = row
            house_number, record_number = analyse_row(typ_so, house_number)
            district_number = extract_dictrict_number(nazev_mop)
            row_label = compile_address.compile_address(
                builder,
                street, house_number, record_number, orientation_number, orientation_number_character,
                zip_code, locality, locality_part, district_number)
            result_array.append(":".join(html_items) + ":" + row_label)
            if len(result_array) >= page_size:
                break
        row_number = row_number + 1
    row_count = rows.row_count
    if row_count == limit_value:
        count_sql = u"select count(*) " + sql_base
        count_rows = select_sql(count_sql)
        count_row = count_rows.fetchone()
        row_count = count_row[0]
    result = "%d#%d#%d#%s" % (first_row, len(result_array), row_count, ";".join(result_array))
    return result


def get_town_part_results(query_params, name_token, smart_autocomplete, max_count=10):
    locality_clause = ""
    if smart_autocomplete:
        locality = get_query_value(query_params, LOCALITY_QUERY_ID, "")
        if locality != "":
            locality_clause = " nazev_obce = '%s' and " % locality
    search_sql = u"select {0}, {1} from {2} where {3} {0} ilike '%{4}%'".format(
        'nazev_casti_obce', 'nazev_obce', AC_CASTI_OBCE, locality_clause, name_token
    )
    """
    search_sql = u"select nazev_casti_obce, nazev_obce from %s where %s nazev_casti_obce ilike '%%%s%%'" % (
        AC_CASTI_OBCE, locality_clause, name_token)
    """
    rows = get_autocomplete_rows(search_sql, 0, max_count)

    return rows


def get_street_results(query_params, name_token, smart_autocomplete, max_count=10):
    if smart_autocomplete:
        where_clause = get_sql_where_clause(
            query_params, {"Locality": u"nazev_obce", "LocalityPart": u"nazev_casti_obce"}, False)
    else:
        where_clause = ""
    search_sql = "select {0}, {1} from {2} where {3} {0} ilike '%%{4}%%' group by {1}, {0} order by {1}, {0}".format(
        'nazev_ulice', 'nazev_obce', AC_ULICE, where_clause, name_token
    )
    """
    search_sql = (
    u"select nazev_ulice, nazev_obce from %s where %s nazev_ulice ilike '%%%s%%' group by nazev_obce, nazev_ulice order by nazev_obce, nazev_ulice") 
    % (AC_ULICE, where_clause, name_token)
    """
    rows = get_autocomplete_rows(search_sql, 0, max_count)
    return rows


def get_town_autocomplete_results(query_params, name_token, smart_autocomplete, max_count=10):
    locality_part = get_query_value(query_params, LOCALITY_PART_QUERY_ID, "")
    if locality_part == "" or smart_autocomplete is False:
        search_sql = "select {0} from {1} where {2} ilike '%{3}%'".format(
            'nazev_obce', AC_OBCE, 'nazev_obce', name_token)
        rows = get_rows(search_sql)
        search_sql = "select {0}, {1} from {2} where {0} ilike '%{3}%' and {0} <> {1}".format(
            'nazev_casti_obce', 'nazev_obce', AC_CASTI_OBCE, name_token)
        rows.extend(get_rows(search_sql, max_count))
    else:
        search_sql = "select {0} from {1} where {2} = '{3}' and {0} ilike '%{4}%'".format(
            'nazev_obce', AC_OBCE, 'nazev_casti_obce', locality_part, name_token)
        rows = get_rows(search_sql, max_count)
    return rows


def get_zip_results(query_params, name_token, smart_autocomplete, max_count=10):
    if smart_autocomplete:
        where_clause = get_sql_where_clause(
            query_params, {"Locality": u"nazev_obce", "LocalityPart": u"nazev_casti_obce"}, False)
    else:
        where_clause = ""
    search_sql = "select {0}, {1} from {2} where {3} {0} like '{4}%' group by {0}, {1} order by {0}, {1}".format(
        'psc', 'nazev_obce', AC_PSC, where_clause, name_token)
    rows = get_autocomplete_rows(search_sql, 0, max_count)
    return rows


def get_id_results(query_params, name_token, smart_autocomplete, max_count=10):
    logging.debug('get_id_results(query_params={0}, name_token={1}, smart_autocomplete={2}, max_count={3})'.format(
        str(query_params), str(name_token), str(smart_autocomplete), str(max_count)))
    search_sql = "select cast({0} as text), {1} from {2} where cast({0} as text) like '{3}%'".format(
        'gid', 'address', 'ac_gids', name_token)
    rows = get_autocomplete_rows(search_sql, 0, max_count)
    return rows


def get_house_number_autocomplete_results(query_params, name_token, max_count=10):
    where_clause = get_sql_where_clause(
        query_params, {"Locality": u"nazev_obce", "LocalityPart": u"nazev_casti_obce", "Street": "nazev_ulice"}, False)
    if where_clause == "":
        return []
    else:
        search_sql = "select {0} from {1} where {2} cast({0} as text) like '{3}%' order by {0}".format(
            'cislo_domovni', ADDRESSPOINTS_TABLENAME, where_clause, name_token)
    rows = get_autocomplete_rows(search_sql, 0, max_count)
    return rows


def get_full_text_autocomplete_results(query_params, name_token, result_format, max_count=10):
    has_number, search_sql = parse_full_text_token(query_params, name_token)
    rows = []
    if search_sql != "":
        search_sql += " limit " + str(max_count)
        cursor = _execute_sql(search_sql)
        if cursor is None:
            raise DatabaseRuianError(module=__name__, message=search_sql)
        row_count = 0
        for row in cursor:
            row_count += 1
            html_items = []
            row_label = None
            for i in range(len(row)):
                html_items.append(row[i])
                row_label = None
            if has_number:
                (street, house_number, locality, zip_code, orientation_number,
                 orientation_number_character, locality_part, typ_so, nazev_mop) = row
                house_number, record_number = analyse_row(typ_so, house_number)
                district_number = extract_dictrict_number(nazev_mop)
                row_label = compile_address.compile_address(
                    builder,
                    street, house_number, record_number, orientation_number, orientation_number_character,
                    zip_code, locality, locality_part, district_number)
                if result_format.lower() == "addressparts":
                    id_value = item_to_str(street) + "," + item_to_str(house_number) + "," + item_to_str(
                        record_number) + "," + item_to_str(orientation_number) + "," + \
                               item_to_str(orientation_number_character) + "," + item_to_str(zip_code) + "," + \
                               item_to_str(locality) + "," + item_to_str(locality_part) + "," + item_to_str(
                        district_number)
                else:
                    id_value = row_label[row_label.find(", ") + 2:]
            else:
                id_value = row[0] + ", " + row[1]

            if row_label is None:
                row_label = ", ".join(html_items)

            row_value = row_label

            value = '{"id":"' + id_value + '","label":"' + row_label + '","value":"' + row_value + '"}'

            rows.append(value)

            if row_count >= max_count:
                break

    return rows


def get_autocomplete_results(query_params, ruian_type, name_token, result_format, smart_autocomplete, max_count=10):
    if ruian_type == "":
        ruian_type = "town"
    name_token = name_token.lower()

    if ruian_type == "townpart":
        return get_town_part_results(query_params, name_token, smart_autocomplete, max_count)
    elif ruian_type == "town":
        return get_town_autocomplete_results(query_params, name_token, smart_autocomplete, max_count)
    elif ruian_type == "house_number":
        return get_house_number_autocomplete_results(query_params, name_token, max_count)
    elif ruian_type == ID_VALUE:
        return get_id_results(query_params, name_token, smart_autocomplete, max_count)
    elif ruian_type == "zip":
        return get_zip_results(query_params, name_token, smart_autocomplete, max_count)
    elif ruian_type == "street":
        return get_street_results(query_params, name_token, smart_autocomplete, max_count)
    else:
        return get_full_text_autocomplete_results(query_params, name_token, result_format, max_count)


def __old_ge_data_list_response(search_sql, max_count=0):
    result = ""
    if search_sql != "":
        if max_count != 0:
            search_sql += " limit " + str(max_count)

        try:
            db = PostGISDatabase()
            cursor = db.conection.cursor()
            cursor.execute(search_sql)
        except psycopg2.Error as e:
            import sys
            return [sys.exc_info()[0], str(e)]
            # TODO ošetřit výjimku

        result_list = []
        row_count = 0
        for row in cursor:
            row_count += 1
            result_list.append(str(row[0]))
            if max_count != 0 and row_count >= max_count:
                break
        result = ",".join(result_list)

    return result


def sort_number_list_and_leave_empty(alist):
    alist = list(set(alist))
    found_empty = False
    result = []
    for item in alist:
        if item == "":
            if not found_empty:
                found_empty = True
        elif item not in result:
            result.append(item)
    result.sort(key=int)
    if found_empty:
        result.insert(0, "")
    return result


def get_number_values(field_name, where_clause, max_count, none_value=None):
    result = []
    search_sql = "select {0} from {1} where {2} group by {3}".format(
        field_name, ADDRESSPOINTS_TABLENAME, where_clause, field_name)
    if max_count != 0:
        search_sql += " limit " + str(max_count)
    cursor = _execute_sql(search_sql)
    if cursor is None:
        raise DatabaseRuianError(module=__name__, message=search_sql)
    row_count = 0
    for row in cursor:
        row_count += 1
        if row[0] is None:
            if none_value is None:
                result.append(none_value)
        else:
            result.append(str(row[0]))
        if max_count != 0 and row_count >= max_count:
            break
    return result


def get_data_list_values(query_params, max_count=50):
    result = '###'
    where_clause = get_sql_where_clause(
        query_params, {"Locality": u"nazev_obce", "LocalityPart": u"nazev_casti_obce", "Street": "nazev_ulice"}, False)
    where_clause = where_clause[:where_clause.rfind(" and")]
    if where_clause != "":
        house_number_list = get_number_values("cislo_domovni", where_clause + " and typ_so='č.p.' ", max_count)
        record_number_list = get_number_values("cislo_domovni", where_clause + " and typ_so<>'č.p.' ", max_count)
        orientation_number_list = get_number_values("cislo_orientacni", where_clause, max_count)
        orientation_number_character_list = get_number_values("znak_cisla_orientacniho", where_clause, max_count, "&nbsp;")
        house_number_list = sort_number_list_and_leave_empty(house_number_list)
        record_number_list = sort_number_list_and_leave_empty(record_number_list)
        orientation_number_list = sort_number_list_and_leave_empty(orientation_number_list)
        orientation_number_character_list = list(set(orientation_number_character_list))
        orientation_number_character_list.sort()
        if orientation_number_character_list == ["&nbsp;"]:
            orientation_number_character_list = []
        result = ",".join(house_number_list) + "#"
        result += ",".join(record_number_list) + "#"
        result += ",".join(orientation_number_list) + "#"
        result += ",".join(orientation_number_character_list)
    return result


def get_mop_list(sql_query):
    try:
        cursor = _execute_sql(sql_query)
        if cursor is None:
            raise DatabaseRuianError(module=__name__, message=sql_query)
        result_list = {}
        for row in cursor:
            key = row[0]
            if key in result_list:
                result_list[key].append(row[1])
            else:
                result_list[key] = [row[1]]
        small_list = []
        for key in result_list:
            small_list.append('\t\t"{0}" : "{1}"'.format(key, ",".join(result_list[key])))
        result = '{\n{0}\n}'.format(",\n".join(small_list))
    except (psycopg2.Error, DatabaseRuianError) as e:
        logging.error(str(e))
        return [sys.exc_info()[0], str(e)]
    return result


def get_district_mo_ps():
    sql = "select {0}, {1} from {2} where {1} <> '' group by {1}, {0} order by {1}, {0}".format(
        'nazev_casti_obce', 'nazev_mop', 'address_points')
    return get_mop_list(sql)


def get_mop_districts():
    sql = "select {0}, {1} from {2} where {0} <> '' group by {1}, {0} order by {0}, {1}".format(
        'nazev_mop', 'nazev_casti_obce', 'address_points'
    )
    return get_mop_list(sql)


def _execute_sql(sql):
    try:
        db = PostGISDatabase()
        cursor = db.conection.cursor()
        cursor.execute(sql)
        return cursor
    except psycopg2.Error as e:
        logging.error(str(e))
        # import sys
        # return [sys.exc_info()[0], str(e)]
        # TODO ošetřit výjimku
        return None


def main():
    # print(getAutocompleteResults("zip", "16"))
    # print(getAutocompleteResults("street", "Mrkvičkova 13"))
    # print(getAutocompleteResults("street", "Budovatelů 6"))
    print(get_district_mo_ps())
    # print(getMOPDistricts())
    pass


if __name__ == '__main__':
    import sys

    main()
