# -*- coding: utf-8 -*-
import cgitb

# *****************************************************************************
# Tento CGI skript vrací hodnoty pro Autocomplete
# *****************************************************************************

from ruian_services.services import jquery_autocomplete_postgis, web_server_base

cgitb.enable()


def get_query_value(query_params, id_value, default_value):
    # Vrací hodnotu URL Query parametruy id, pokud neexistuje, vrací hodnotu defValue
    if id_value is query_params:
        return query_params[id_value]
    else:
        return default_value


def process_request(page, service_path_info, path_infos, query_params, response):
    print(str(service_path_info), str(path_infos))
    if page.lower().startswith("mopdistricts"):
        response.html_data = jquery_autocomplete_postgis.get_mop_districts()
    elif page.lower().startswith("districtmops"):
        response.html_data = jquery_autocomplete_postgis.get_district_mo_ps()
    elif query_params:
        max_matches = int(get_query_value(query_params, 'max_matches', 40))
        if page.lower().startswith("fill"):
            response.html_data = jquery_autocomplete_postgis.get_fill_results(query_params)
        elif page.lower().startswith("datalists"):
            data_lists_limit = int(get_query_value(query_params, 'max_matches', 150))
            response.html_data = jquery_autocomplete_postgis.get_data_list_values(query_params, data_lists_limit)
        else:
            token = get_query_value(query_params, 'term', "")
            ruian_type = get_query_value(query_params, 'RUIANType', "zip")
            result_format = get_query_value(query_params, 'ResultFormat', "")
            smart_autocomplete = get_query_value(query_params, 'SmartAutocomplete', "False").lower() == "true"
            result_array = jquery_autocomplete_postgis.get_autocomplete_results(
                query_params, ruian_type, token, result_format,
                smart_autocomplete, max_matches)
            response.html_data = "[\n\t" + ",\n\t".join(result_array) + "\n]"
    else:
        response.html_data = "[  ]"

    response.mime_format = "text/javascript"
    response.handled = True
    return response


if __name__ == '__main__':
    # Spuštění serveru
    web_server_base.main_process(process_request)
