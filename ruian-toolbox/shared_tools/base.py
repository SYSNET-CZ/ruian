# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        base
# Purpose:     Library shared procedures.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------

import codecs
import os
import sys

RUNS_ON_WINDOWS = sys.platform.lower().startswith('win')
RUNS_ON_LINUX = not RUNS_ON_WINDOWS
COMMAND_FILE_EXTENSION = [".bat", ".sh"][RUNS_ON_LINUX]


def extract_file_name(file_name):
    lastDel = file_name.rfind(os.sep)
    return file_name[lastDel + 1:]


def get_file_extension(file_name):
    """ Returns fileName extension part dot including (.txt,.png etc.)"""
    return file_name[file_name.rfind("."):]


def path_with_last_slash(path):
    assert isinstance(path, basestring)

    path = normalize_path_sep(path)
    if path != "" and path[len(path) - 1:] != os.sep:
        path = path + os.sep

    return path


def create_dir_for_file(file_name):
    safe_mk_dir(os.path.dirname(file_name))


def safe_mk_dir(path):
    assert isinstance(path, basestring)

    if path == "" or os.path.exists(path):
        return

    pathParts = path.split(os.sep)
    actPathList = []
    for pathItem in pathParts:
        actPathList.append(pathItem)
        actPathStr = os.sep.join(actPathList)
        if actPathStr and not os.path.exists(actPathStr):
            os.mkdir(actPathStr)


def extract_file_name2(path):
    head, tail = os.path.split(path)
    return tail


def get_python_modules():
    return sys.modules.keys()


def setup_utf():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')


def normalize_path_sep(path):
    assert isinstance(path, basestring)
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path


def get_file_content(file_name, char_set="utf-8"):
    assert isinstance(file_name, basestring)
    assert isinstance(char_set, basestring)

    if os.path.exists(file_name):
        inFile = codecs.open(file_name, "r", char_set)
        result = inFile.read()
        inFile.close()
    else:
        result = ""

    return result
