# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        config
# Purpose:     Implements services config class.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------
# from shared_tools import shared
from shared_tools import shared
from shared_tools.configuration import Configuration, ruian_importer_config

shared.setup_paths(depth=2)

servicesConfigAttrs = {
    "serverHTTP": 'ruian.sysnet.cz',
    "portNumber": 80,
    "servicesWebPath": "ruian/services/rest.py/",
    "databaseHost": "postgis",
    "databasePort": "5432",
    "databaseName": "ruian",
    "databaseUserName": "docker",
    "databasePassword": "docker",
    "noCGIAppServerHTTP": "0.0.0.0",
    "noCGIAppPortNumber": 5689,
    "issueNumber": "",
    "issueShortDescription": "",
    "ruianVersionDate": "",
    "disableGUISwitch": "false"
}


def convert_services_cfg(config_value):
    if config_value is None:
        return

    if config_value.portNumber == "":
        config_value.portNumber = 80
    else:
        config_value.portNumber = int(config_value.portNumber)
    pass

    config_value.noCGIAppPortNumber = int(config_value.noCGIAppPortNumber)

    # noCGIAppServerHTTP nemůže být prázdné
    if config_value.noCGIAppServerHTTP == "":
        config_value.noCGIAppServerHTTP = "localhost"

    # servicesWebPath nemá mít lomítko na konci
    if config_value.servicesWebPath[len(config_value.servicesWebPath) - 1:] == "/":
        config_value.servicesWebPath = config_value.servicesWebPath[:len(config_value.servicesWebPath) - 1]

    config_value.disableGUISwitch = config_value.disableGUISwitch.lower() == "true"

    config_value.issueNumber = "2.0.00"
    config_value.issueShortDescription = ''
    '''
    # u""", 
    <a href="https://github.com/vugtk21/RUIANToolbox/issues?q=milestone%3A%22Konzultace+5.1.2014%22">
    podrobnosti na GitHub
    </a>."""
    '''
    importer_attrs_mapper = {
        "databaseHost": "host",
        "databasePort": "port",
        "databaseName": "dbname",
        "databaseUserName": "user",
        "databasePassword": "password"
    }
    importer_config = ruian_importer_config()
    for servicesAttr in importer_attrs_mapper:
        if config_value.attrs[servicesAttr] == servicesConfigAttrs[servicesAttr]:
            config_value.set_attr(servicesAttr, importer_config.attrs[importer_attrs_mapper[servicesAttr]])


config = Configuration("ruian_services.cfg", servicesConfigAttrs, convert_services_cfg, module_file=__file__)


def get_port_specification():
    if config.portNumber == 80:
        return ""
    else:
        return ":" + str(config.portNumber)


SERVER_HTTP = config.serverHTTP
PORT_NUMBER = config.portNumber
SERVICES_WEB_PATH = config.servicesWebPath
HTMLDATA_URL = "html/"

_isFirstCall = True


def setup_variables():
    global _isFirstCall
    global SERVER_HTTP
    global PORT_NUMBER
    global SERVICES_WEB_PATH
    global HTMLDATA_URL

    if _isFirstCall and not shared.isCGIApplication:
        SERVER_HTTP = config.noCGIAppServerHTTP
        PORT_NUMBER = config.noCGIAppPortNumber
        SERVICES_WEB_PATH = ""
        HTMLDATA_URL = "html/"

    _isFirstCall = False


def get_cgi_path():
    server_items = "/".split(SERVER_HTTP)
    return "/".join(server_items[:len(server_items) - 1])


def get_html_data_url():
    result = get_services_url()
    if HTMLDATA_URL != "":
        result = result + "/" + HTMLDATA_URL
    return result


def get_services_url():
    setup_variables()
    result = 'http:' + '//' + SERVER_HTTP + get_port_specification()
    if SERVICES_WEB_PATH != "":
        result = result + "/" + SERVICES_WEB_PATH
    return result


def get_services_path():
    result = get_services_url().split("/")
    result = result[:len(result) - 1]
    return "/".join(result)
