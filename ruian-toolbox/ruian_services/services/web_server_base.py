# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

# =============================================================================
import cgi
import cgitb
import os

import web

from ruian_services.services.config import SERVICES_WEB_PATH, SERVER_HTTP
from ruian_services.services.http_shared import HTTPResponse

"""
Knihovna pro zabalení funkcionality serveru.

Př.

import webserverbase

def processRequest(page, servicePathInfo, pathInfos, queryParams, response):
    response.htmlData = "<html><body>Empty</body></html>"
    response.handled = True
    return response

webserverbase.processRequestProc = processRequest

if __name__ == "__main__":
    webserverbase.mainProcess(processRequest)

"""
#  =============================================================================

path = SERVICES_WEB_PATH.split("/")
serverPathDepth = 0

for item in path:
    if item != "":
        serverPathDepth = serverPathDepth + 1

SERVER_PATH_DEPTH = serverPathDepth
EMPTY_HTML_DATA = "<html><body>Empty</body></html>"


def _parsed_process_request_proc(page, service_path_info, path_infos, query_params, response):
    print(str(page), str(service_path_info), str(path_infos), str(query_params))
    # TODO
    response.html_data = EMPTY_HTML_DATA
    response.handled = True
    return response


process_request_proc = _parsed_process_request_proc


def _process_request_proc(page, query_params, response):
    if page in ["/", ""]:
        response.html_data = EMPTY_HTML_DATA
        response.handled = True
    elif page.find(".") >= 0:
        if os.path.exists(SERVICES_WEB_PATH + page):
            f = open(SERVICES_WEB_PATH + page)
            response.html_data = f.read()  # TODO Implementovat vracení binárních souborů
            f.close()
            response.handled = True
        else:
            response.html_data = EMPTY_HTML_DATA
            response.handled = True
    else:
        full_path_list = page.split("/")  # REST parametry
        if SERVER_PATH_DEPTH != 0:
            full_path_list = full_path_list[SERVER_PATH_DEPTH:]
        # TODO PathInfo by mělo být až za adresou serveru - zkontolovat jak je to na Apache
        if len(full_path_list) > 0:
            service_path_info = "/" + full_path_list[0]  # první rest parametr
        else:
            service_path_info = "/"

        path_infos = full_path_list[1:]  # ostatní
        response = process_request_proc(page, service_path_info, path_infos, query_params, response)

    return response


urls = ('/(.*)', 'handler')


class ServerApplication(web.application):
    def run(self, port, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (SERVER_HTTP, port))


class Favicon:
    def get(self):
        pass


def do_process_request(page):
    response = _process_request_proc(page, web.input(), HTTPResponse(False))
    if response.handled:
        web.header("Content-Type", response.mimeFormat + ";charset=utf-8")
        return response.htmlData
    else:
        return "doProcessRequest Error"


def get(page):
    return do_process_request(page)


def post(page):
    return do_process_request(page)


def main_process(a_process_request_proc):
    global process_request_proc
    process_request_proc = a_process_request_proc
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
        for item_value in item_list:
            query[item_value.name] = item_value.value

        response = _process_request_proc(path_info, query, HTTPResponse(False))
        if response.handled:
            print("Content-Type: {0};charset=utf-8".format(response.mimeFormat))  # HTML is following
            print()  # blank line, end of headers
            print(response.htmlData.encode('utf-8'))
        else:
            print("MAIN Error")
    else:
        app = ServerApplication(urls, globals())
        app.run(port=4567)  # PORT_NUMBER)
