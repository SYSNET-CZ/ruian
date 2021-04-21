# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        rest.py
# Purpose:     Implementuje funkcionalitu služeb dle standardu REST
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

import msvcrt
import sys
from urllib import parse

import web  # pip install web.py http://webpy.org/
# from downloader.downloadruian import getDataDirFullPath

# import address_web_services
# import ruian_connection
# from http_shared import *
from ruian_services.services import address_web_services, ruian_connection
from ruian_services.services.config import SERVICES_WEB_PATH, HTMLDATA_URL, config
from ruian_services.services.http_shared import HTTPResponse
from shared_tools import shared, get_data_dir_full_path

server_path_depth = 0


def get_html_path():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/html/"


def get_testing_path():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/testing/"


DATABASE_DETAILS_PATH = "/dbdetails"
AUTOCOMPLETES_PATH = '/autocomplete'
DATA_ALIASES = {
    "/html": get_html_path,
    "/downloaded": get_data_dir_full_path,
    "/testing": get_testing_path
}


def get_file_content(file_name):
    if os.path.exists(file_name):
        if os.path.isfile(file_name):
            f = open(file_name, "rb")
            s = f.read()
            f.close()
            return s
        else:
            return file_name + " is a directory, can't be sent over http."
    else:
        return "File " + file_name + " not found."


def file_name_to_mime_format(file_name):
    known_mime_formats = {
        ".js": "text/javascript",
        ".png": "image/png",
        ".ico": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".htm": "text/html",
        ".html": "text/html",
        ".txt": "text/plain",
        ".log": "text/plain",
        ".css": "text/css"
    }
    file_ext = file_name[file_name.rfind("."):]
    if file_ext in known_mime_formats:
        return known_mime_formats[file_ext]
    else:
        return None


def process_request(full_path_list_value, query_params, response_value):
    address_web_services.console.clear()

    address_web_services.console.add_info(u"SERVICES_WEB_PATH: " + SERVICES_WEB_PATH)
    address_web_services.console.add_info(u"HTMLDATA_URL: " + HTMLDATA_URL)
    if address_web_services.console.debugMode:
        # import config as configModule
        address_web_services.console.add_info(u"configModule.getHTMLDataURL(): " + config.getHTMLDataURL())
        address_web_services.console.add_info(u"shared.isCGIApplication(): " + str(shared.isCGIApplication))
        address_web_services.console.add_info(u"configModule.HTMLDATA_URL: " + config.HTMLDATA_URL)
        address_web_services.console.add_info(u"configModule.SERVER_HTTP: " + config.SERVER_HTTP)
        address_web_services.console.add_info(
            u"configModule.getPortSpecification(): " + config.getPortSpecification())

    page_builder = address_web_services.ServicesHTMLPageBuilder()
    if full_path_list_value in [["/"], []]:
        response_value.html_data = page_builder.get_services_html_page(__file__, "", {})
        response_value.handled = True
    else:
        if not full_path_list_value:
            service_path_info = "/"
        else:
            service_path_info = "/" + full_path_list_value[0]  # první rest parametr

        if service_path_info.lower() in DATA_ALIASES:
            file_name = DATA_ALIASES[service_path_info.lower()]() + "/".join(full_path_list_value[1:])
            response_value.html_data = get_file_content(file_name)
            mime_format = file_name_to_mime_format(file_name)
            if mime_format is not None:
                response_value.mime_format = mime_format
                if mime_format == "text/plain":
                    response_value.html_data = response_value.html_data.replace("\r\n", "\n")
            response_value.handled = True
        elif service_path_info.lower().startswith(AUTOCOMPLETES_PATH):
            import jquery_autocomplete
            response_value = jquery_autocomplete.process_request("/".join(full_path_list_value[1:]), "", "",
                                                                 query_params, response_value)
        elif service_path_info.lower().startswith(DATABASE_DETAILS_PATH):
            ruian_connection.get_db_details(full_path_list_value[1:], response_value)
        else:
            path_infos = full_path_list_value[1:]  # ostatní

            for service in address_web_services.services:
                if (service.path_name == service_path_info) and (service.processHandler is not None):
                    # TODO Tohle by si asi měla dělat service sama
                    i = 0
                    for pathValue in path_infos:
                        if i < len(service.restPathParams):
                            query_params[service.restPathParams[i].path_name[
                                         1:]] = pathValue  # přidání do slovníku, přepíše hodnotu se stejným klíčem
                        else:
                            # Too many parameters
                            address_web_services.console.add_msg(
                                u"Nadbytečný REST parametr č." + str(i) + "-" + pathValue)

                        i = i + 1
                    service.processHandler(query_params, response_value)
                    break

            if not response_value.handled:
                if path_infos:
                    address_web_services.console.add_msg(u"Neznámá služba: " + service_path_info)
                response_value.html_data = page_builder.get_services_html_page(__file__, service_path_info, query_params)
                response_value.handled = True

    return response_value


urls = ('/favicon.ico', 'favicon', '/(.*)', 'handler')


class MyApplication(web.application):
    def run(self, port=config.noCGIAppPortNumber, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (config.noCGIAppServerHTTP, port))


class Favicon:
    def get(self):
        pass


def do_process_request(page):
    shared.isCGIApplication = False
    reply = process_request(page.split("/"), web.input(), HTTPResponse(False))
    if reply.handled:
        web.header("Content-Type", reply.mime_format + ";charset=utf-8")
        return reply.html_data
    else:
        return "do_process_request Error"


def get(page):
    shared.isCGIApplication = False
    return do_process_request(page)


def post(page):
    shared.isCGIApplication = False
    return do_process_request(page)


if __name__ == "__main__":
    # Nastavení znakové sady na utf-8

    import os

    if 'SERVER_SOFTWARE' in os.environ:
        # Script spuštěn jako CGI
        print("HTTP Server CGI mode")
        import cgi
        import cgitb

        cgitb.enable()

        shared.isCGIApplication = True

        path = SERVICES_WEB_PATH.split("/")
        server_path_depth = 0
        for item in path:
            if item != "":
                server_path_depth = server_path_depth + 1

        form = cgi.FieldStorage()
        if 'PATH_INFO' in os.environ:
            pathInfo = os.environ['PATH_INFO']
        else:
            pathInfo = ""
        if pathInfo[:1] == "/":
            pathInfo = pathInfo[1:]

        full_path_list = pathInfo.replace("//", "/")
        full_path_list = full_path_list.split("/")  # REST parametry

        query = {}
        list_value = form.list
        for item in list_value:
            decoded_value = parse.unquote(item.value)
            decoded_value = parse.unquote(decoded_value)
            query[item.name] = decoded_value

        response = process_request(full_path_list, query, HTTPResponse(False))
        if response.handled:
            if response.mime_format in ["text/html", "text/javascript", "text/plain"]:
                print("Content-Type: {0};charset=utf-8".format(response.mime_format))  # HTML is following
                print()  # blank line, end of headers
                sys.stdout.write(response.html_data.encode('utf-8'))
            else:
                print("Content-Type: application/octet-stream")  # response.mimeFormat
                print()  # blank line, end of headers
                if sys.platform != "win32":
                    sys.stdout.write(response.html_data)
                    sys.stdout.flush()
                else:
                    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                    sys.stdout.write(response.html_data)
                    sys.stdout.flush()
                    msvcrt.setmode(sys.stdout.fileno(), os.O_TEXT)

        else:
            print("ProcessRequest not handled")

    else:
        # Script je spuštěn jako samostatný server
        print("HTTP Server standalone mode")
        config.serverHTTP = config.noCGIAppServerHTTP
        SERVER_HTTP = config.noCGIAppServerHTTP
        # SERVICES_WEB_PATH = ""
        config.portNumber = config.noCGIAppPortNumber
        PORT_NUMBER = config.noCGIAppPortNumber

        app = MyApplication(urls, globals())
        app.run(port=config.noCGIAppPortNumber)
