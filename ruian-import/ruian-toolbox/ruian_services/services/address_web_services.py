#!C:/Python27/python.exe
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        addresswebservices
# Purpose:
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------
import codecs
import os.path

from ruian_services.services import compile_address, ft_search, geocode, nearby_addresses, ruian_connection, validate, \
    validate_address_id
from ruian_services.services.config import config, SERVER_HTTP, SERVICES_WEB_PATH
from ruian_services.services.http_shared import services

USE_DATA_LISTS = True
SERVICES_PATH = ''  # 'services'
ROTATING_CIRCLE = '{0}://jqueryui.com/resources/demos/autocomplete/images/ui-anim_basic_16x16.gif'.format('http')


def get_address_tab_name(item_name):
    address_tab_names = {
        "vstup": ["FillAddressButton", "Locality", "LocalityPart", "DistrictNumber", "Street", "HouseNumber",
                  "RecordNumber", "OrientationNumber", "OrientationNumberCharacter", "ZIPCode"],
        "id": ["AddressPlaceId"],
        "adresa": ["SearchText"]
    }
    for key in address_tab_names:
        if item_name in address_tab_names[key]:
            return key
    return ""


def get_page_template():
    f = codecs.open("..//HTML//RestPageTemplate.htm", "r", "utf-8")
    result = f.read()
    f.close()

    # convert windows line breaks to linux, so firebug places breakpoint properly
    result = result.replace("\r\n", "\n")
    return result


class Console:
    consoleLines = ""
    infoLines = ""
    debugMode = False

    def add_msg(self, msg):
        msg = '<div class="ui-widget">' \
              '<div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">' \
              '<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>' \
              '<strong>Chyba: </strong>' + msg + '</p></div></div>'
        self.consoleLines += msg + "\n"

    def add_info(self, msg):
        if not self.debugMode:
            return

        msg = '<div class="ui-widget">' \
              '<div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">' \
              '<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>' \
              '<strong>Info: </strong>' + msg + '</p></div></div>'
        self.infoLines += msg + "\n"

    def clear(self):
        self.consoleLines = ''
        self.infoLines = ""


console = Console()


def get_no_address_available_html(form_name):
    result = u"""
<div class="ui-widget NOADDRESSHINTDIV" id="#FORMNAME#_NoAddressHintDiv" isvisible="false" tabname="vstup">
    <div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">
        <p>
            <span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>
            Adresa v této kombinaci prvků nebyla nenalezena
        </p>
    </div>
</div>"""
    result = result.replace("#FORMNAME#", form_name)
    return result


def get_issue_html():
    if config.issueShortDescription == "":
        return ""
    else:
        result = u'<div class="ui-widget">' \
                 u'<div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">' \
                 u'<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>' \
                 u'<strong>Návrh řešení ' + config.issueNumber + u'</strong>'
        result += config.issueShortDescription
        result += u'</div></div>'

        return result


def normalize_query_params(query_params):
    """ Parametry odesílané v URL requestu do query z HTML fomulářů musí být použity bez jména formuláře,
    tj. 'form_2_/AddressPlaceId' se spráně jmenuje 'AddressPlaceId'.
    """
    result = {}
    for key in query_params:
        result[key[key.find("/") + 1:]] = query_params[key]
    return result


class ServicesHTMLPageBuilder:
    def __init__(self):
        self.dataListHTML = ""

    def table_property_row(self, param, form_name, param_type_str, query_params, on_change_proc_code, has_address_tabs):
        key_name = param.name[1:]
        print(param_type_str)
        if key_name in query_params:
            value_str = 'value = "' + query_params[key_name] + '"'
        else:
            value_str = ""

        if param.disabled:
            visibility_str = ' style="display:none" '
        else:
            visibility_str = ''

        if has_address_tabs:
            tags_str = ' isvisible="true" '
            tab_name = get_address_tab_name(param.name)
            if tab_name:
                tags_str += ' tabname="%s" ' % tab_name
        else:
            tags_str = ''

        result = '<tr id="%s_row_%s"%s%s>' % (form_name, param.name, visibility_str, tags_str)

        if param.name == 'FillAddressButton':
            result += '<td align="right" colspan = "2">'
        else:
            result += '<td align="right">' + param.caption + ' </td><td>'

        if param.name == '/Format':
            build_rotating_circle = False
            select_html = '<select input name="' + form_name + '_' + param.name + '" title="' + \
                          param.short_desc + '" onchange="updateServiceSpan(\'%s\')' % form_name + '">' + \
                          '<option value="text">text</option>' + \
                          '<option value="textToOneRow">text do řádku</option>' + \
                          '<option value="xml">xml</option>' + \
                          '<option value="html">html</option>' + \
                          '<option value="htmlToOneRow">html do řádku</option>' + \
                          '<option value="json">json</option>' + \
                          '</select>'
            if build_rotating_circle:
                result += '<span>{0}</span>'.format(select_html)
                result += '<span id="{0}_WaitCursorSpan" class="WAITCURSORSPAN" '.format(form_name)
                result += 'style="width:100%%;text-align:right;">'
                result += '<img src="{0}" />'.format(ROTATING_CIRCLE)
                result += '</span>'
            else:
                result += select_html
        elif param.name == "DistrictNumber":
            id_value = "%s_%s" % (form_name, param.name)
            result += '<select id="{0}" name="{0}" title="{1}" onchange="districtNumberChanged(\'{2}\')">'.format(
                id_value, param.short_desc, form_name)
            result += '<option value=""></option>' + \
                      '<option value="1">Praha 1</option>' + \
                      '<option value="2">Praha 2</option>' + \
                      '<option value="3">Praha 3</option>' + \
                      '<option value="4">Praha 4</option>' + \
                      '<option value="5">Praha 5</option>' + \
                      '<option value="6">Praha 6</option>' + \
                      '<option value="7">Praha 7</option>' + \
                      '<option value="8">Praha 8</option>' + \
                      '<option value="9">Praha 9</option>' + \
                      '<option value="10">Praha 10</option>' + \
                      '</select>'
        elif param.name == 'ExtraInformation':
            if form_name == "form_1":
                address_option = '<option value="address">přidat adresu</option>'
            elif form_name == "form_5":
                address_option = '<option value="distance">přidat vzdálenost</option>'
            else:
                address_option = ""

            result += '<select name="{0}_{1}" title="{2}" onchange="updateServiceSpan(\'{0}\')" >'.format(
                form_name, param.name, param.short_desc)
            result += '<option value="standard">žádné</option>'
            result += '<option value="id">přidat ID</option>'
            result += address_option
            result += '</select>'

        elif param.name == 'FillAddressButton':
            result += '<span class="SMARTAUTOCOMPLETECB">'
            result += '<input type="checkbox" id="{0}_SmartAutocompleteCB" checked '.format(form_name)
            result += 'onchange="setupInputs(\'{0}\')" '.format(form_name)
            result += 'title="Našeptávače budou reagovat na již vložené hodnoty">'
            result += 'Chytré našeptávače</span>'
            result += '&nbsp;&nbsp;<input type="button" value="Doplň adresu" id="{0}_FillAddressButton'.format(
                form_name)
            result += '" title="{0}"  onclick="findAddress(\'{1}\')">'.format(param.short_desc, form_name)
        else:
            disabled_str = ''  # disabled_str = ' disabled="disabled" '
            elem_id = form_name + '_' + param.name
            if param.name == 'LocalityPart':
                on_change_proc_code = on_change_proc_code.replace("onChangeProc(", "localityPartChanged(")

            data_list_ref = ""
            if USE_DATA_LISTS and param.name in \
                    ["HouseNumber", "OrientationNumber", "RecordNumber", "OrientationNumberCharacter", "LocalityPart"]:
                data_list_id = "%s_%s_DataList" % (form_name, param.name)
                if param.name == 'LocalityPart':
                    data_list_change_proc_code = ' onchange="%s"' % on_change_proc_code
                    # data_list_change_proc_code = ' onchange="alert(\'ahoj\')"'
                else:
                    data_list_change_proc_code = ""

                self.dataListHTML += '<datalist id="%s" class="DATALIST_CLASS" %s>\n</datalist>\n' % (
                    data_list_id, data_list_change_proc_code)
                data_list_ref = ' list="%s"' % data_list_id

            result += '<input name="' + elem_id + '" ' + value_str.decode('utf8') + 'title="' + \
                      param.short_desc + '" onchange="' + on_change_proc_code + '" ' + disabled_str + param.html_tags + \
                      ' id="' + elem_id + '"' + data_list_ref + ' />'
        result += '</tr>\n'
        return result

    def get_services_html_page(self, script_name, path_info, query_params):
        script_name = os.path.basename(script_name)
        self.dataListHTML = ""
        result = get_page_template().replace("#PAGETITLE#", u"Webové služby RÚIAN")
        services_url = 'http' + '://' + SERVER_HTTP + config.getPortSpecification() + "/" + SERVICES_WEB_PATH
        result = result.replace("<#SERVICES_URL>", services_url)

        result = result.replace("#HTMLDATA_URL#", config.getHTMLDataURL())
        result = result.replace("#VERSIONNUMBER#", config.issueNumber)
        result = result.replace("#SERVICES_URL_PATH#", config.getServicesPath())

        if config.ruianVersionDate == "":
            version_date = ruian_connection.get_ruian_version_date()
            config.databaseIsOK = not version_date.upper().startswith("ERROR:")
            if version_date.upper().startswith("ERROR:"):
                version_date = u"Nepřipojeno"
                ruian_version_code = u"<b>!!! Data RÚIAN nejsou připojena !!!</b>"
                console.add_msg(u"Data RÚIAN nejsou připojena, obraťte se na správce webového serveru.")
            else:
                ruian_version_code = '<a href="%s/downloaded/Import.html">%s</a>' % (services_url, version_date)

            config.ruianVersionDate = version_date
            config.ruianVersionCode = ruian_version_code

        result = result.replace("#RUIANVERSIONDATE#", config.ruianVersionCode)

        query_params = normalize_query_params(query_params)

        tab_captions = ""
        tab_divs = ""

        i = 1
        tab_index = 0
        for service in services:
            tab_captions += '<li><a href="#tabs-' + str(i) + '">' + service.caption + '</a></li>\n'
            tab_divs += '<div id="tabs-' + str(i) + '">   <h2>' + service.short_desc + '</h2>\n'
            tab_divs += service.html_desc
            tab_divs += u'<p class = "enhancedGUI">Adresa služby:' + service.path_name + '</p>\n'
            form_name = "form_" + str(i)
            url_span_name = form_name + "_urlSpan"
            on_change_proc_code = 'onChangeProc(' + form_name + ', true)'
            display_result_proc_code = "runOrHookDisplayResult('" + form_name + "', '" + service.path_name + "')"
            if service.path_name == path_info:
                tab_index = i

            rest_py_url = 'http' + '://' + SERVER_HTTP + config.getPortSpecification() + "/" + SERVICES_WEB_PATH + "/"
            tab_divs += u'<span name="' + url_span_name + '" class = "enhancedGUI" id="' + url_span_name + '" >' + \
                        'http' + '://' + SERVER_HTTP + config.getPortSpecification() + "/" + SERVICES_WEB_PATH + "/" + \
                        service.path_name[1:] + "</span>\n"  # service.getServicePath() + "</span>\n"
            has_address_tabs = service.path_name == "/CompileAddress" or service.path_name == "/Geocode"
            if has_address_tabs:
                update_service_span_code = ' onclick="updateServiceSpan(\'%s\')"' % form_name
                tab_divs += u"""
                <br><br>
                <input type="radio" name= "radio%s" value="adresa"   id="%s_AddressRB" checked %s>Adresa
                <input type="radio" name= "radio%s" value="vstup" id="%s_AddressItemsRB" %s>Prvky adresy
                <input type="radio" name= "radio%s" value="id"  id="%s_RuianIdRB" %s>Identifikátor RÚIAN
                """ % (
                    service.path_name, form_name, update_service_span_code, service.path_name, form_name,
                    update_service_span_code,
                    service.path_name, form_name, update_service_span_code)

            tab_divs += "<br><br>"
            tab_divs += "<table><tr valign=\"top\"><td>"
            tab_divs += '<form id="' + form_name + '" name="' + form_name + '" action="' + SERVICES_PATH + \
                        service.path_name + '" method="get" SearchForAddress="false">\n'

            # Parameters list
            tab_divs += '<div class="warning">\n'
            tab_divs += '<table id="' + form_name + '_ParamsTable">\n'
            for param in service.restPathParams:
                tab_divs += self.table_property_row(param, form_name, u"REST", query_params, on_change_proc_code,
                                                    has_address_tabs)

            for param in service.queryParams:
                tab_divs += self.table_property_row(param, form_name, u"Query", query_params, on_change_proc_code,
                                                    has_address_tabs)

            tab_divs += '</table>\n'
            tab_divs += '</div>\n'

            tab_divs += '<br>'
            tab_divs += '<input style="float: right;" type="button" value="Nové zadání" ' + \
                        'onclick="clearInputs(\'%s\')">\n' % form_name
            tab_divs += '<input style="float: right;" type="button" ' + \
                        'value="%s" onclick="%s">\n' % (service.sendButtonCaption, display_result_proc_code)
            tab_divs += '</form>\n'
            tab_divs += "</td>"
            tab_divs += '<td>'
            tab_divs += '<div id="%s_addressesDiv" class="AddressesDiv" ' % form_name + \
                        'title="Vyber adresu" isvisible="false" tabname="vstup"></div>'
            tab_divs += get_no_address_available_html(form_name)
            tab_divs += '<div id="%s_addressDiv" class="AddressDiv" ' % form_name + \
                        'isvisible="false" tabname="vstup"></div>'
            tab_divs += '<textarea id=' + form_name + \
                        '_textArea rows ="12" cols="50" class="RESULTTEXTAREA"></textarea></td>'
            tab_divs += "</tr></table>"
            tab_divs += "<a class = 'enhancedGUI' href='" + rest_py_url + "testing" + \
                        service.path_name + ".html'>Výsledky testů</a>"
            url = config.getHTMLDataURL() + service.path_name[1:] + ".png"
            tab_divs += '<p>\n<center><img width="80%" class="enhancedGUI" src="' + url + '"></center></p>\n'
            tab_divs += '</div>\n'
            i = i + 1

        if config.databaseIsOK:
            separate_str = ""
            in_str = ""
        else:
            separate_str = "{ disabled: [1, 2, 3, 4, 5, 6] }"
            in_str = ", disabled: [1, 2, 3, 4, 5, 6]"

        if tab_index == 0:
            new_str = separate_str
        else:
            new_str = '{ active: %s %s }' % (str(tab_index), in_str)

        result = result.replace("#TABSOPTIONS#", new_str)

        result = result.replace("#CONSOLELINES#", console.consoleLines + "\n" + console.infoLines)
        result = result.replace("#ISSUELINES#", get_issue_html() + "\n")
        result = result.replace("<#TABCAPTIONS#/>", tab_captions)
        result = result.replace("<#TABCAPTIONS#/>", tab_captions)
        result = result.replace("<#TABDIVS#/>", tab_divs)
        result = result.replace("#USE_DATA_LISTS#", str(USE_DATA_LISTS).lower())
        result = result.replace("#SCRIPT_NAME#", script_name)
        result = result.replace("#DISABLEGUISWITCH#", str(config.disableGUISwitch).lower())

        result = result.replace("</body>", self.dataListHTML + "</body>")

        return result


def create_services():
    geocode.create_service_handlers()
    ft_search.create_service_handlers()
    compile_address.create_service_handlers()
    validate.create_service_handlers()
    nearby_addresses.create_service_handlers()
    validate_address_id.create_service_handlers()
    #    IDCheck.createServiceHandlers()
    pass


create_services()


def main():
    # Build HTML page with service description
    page_builder = ServicesHTMLPageBuilder()
    page_content = page_builder.get_services_html_page(__file__, "", {})

    # Write result into file
    file = codecs.open("..//html//WebServices.html", "w", "utf-8")
    file.write(page_content)
    file.close()
    pass


if __name__ == '__main__':
    main()
