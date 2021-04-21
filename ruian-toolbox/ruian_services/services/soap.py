# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        soap.py
# Purpose:     Implements soap interface to implemented functionality.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------
import cgi
import cgitb
import os
import sys

import web

# import address_web_services
# from config import SERVICES_WEB_PATH
# from config import config
# from http_shared import *
from ruian_services.services import address_web_services
from ruian_services.services.config import SERVICES_WEB_PATH, config
from ruian_services.services.http_shared import HTTPResponse

path = SERVICES_WEB_PATH.split("/")
server_path_depth = 0
for item in path:
    if item != "":
        server_path_depth = server_path_depth + 1


def get_html_path():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/html/"


def get_wsdl_path():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/soap/"


def get_file_content(file_name):
    if os.path.exists(file_name):
        f = open(file_name, "rb")
        s = f.read()
        f.close()
        return s
    else:
        return "File {0} not found.".format(file_name)


def process_request(page, query_params, reply):
    print(str(page), str(query_params))
    address_web_services.console.clear()
    reply.html_data = get_file_content(
        get_wsdl_path() + "Euradin_sluzby.wsdl")  # TODO Implementovat vracení binárních souborů
    reply.mime_format = "text/xml"
    reply.handled = True
    return reply


urls = ('/favicon.ico', 'favicon', '/(.*)', 'handler')


class MyApplication(web.application):
    def run(self, port=config.noCGIAppPortNumber, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (config.noCGIAppServerHTTP, port))


class Favicon:
    def get(self):
        pass


def do_process_request(page):
    reply = process_request(page, web.input(), HTTPResponse(False))
    if reply.handled:
        web.header("Content-Type", reply.mime_format + ";charset=utf-8")
        return reply.html_data
    else:
        return "do_process_request Error"


def get(page):
    return do_process_request(page)


def post(page):
    return do_process_request(page)


if __name__ == "__main__":
    server_path_depth = 0
    if 'SERVER_SOFTWARE' in os.environ:
        cgitb.enable()

        form = cgi.FieldStorage()
        if 'PATH_INFO' in os.environ:
            path_info = os.environ['PATH_INFO']
        else:
            path_info = ""
        if path_info[:1] == "/":
            path_info = path_info[1:]

        query = {}
        item_list = form.list
        for item in item_list:
            query[item.name] = item.value

        response = process_request(path_info, query, HTTPResponse(False))
        if response.handled:
            print("Content-Type: " + response.mime_format + ";charset=utf-8")  # HTML is following
            print()  # blank line, end of headers
            # print response.htmlData.encode('utf-8')
            sys.stdout.write(response.html_data.encode('utf-8'))
        else:
            print("SOAP Error")

    else:
        config.serverHTTP = config.noCGIAppServerHTTP
        SERVER_HTTP = config.noCGIAppServerHTTP
        config.portNumber = config.noCGIAppPortNumber
        PORT_NUMBER = config.noCGIAppPortNumber

        app = MyApplication(urls, globals())
        app.run(port=config.noCGIAppPortNumber)
