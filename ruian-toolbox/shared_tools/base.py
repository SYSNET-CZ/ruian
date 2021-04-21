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
COMMAND_FILE_EXTENSION = ['.bat', '.sh'][RUNS_ON_LINUX]


def extract_file_name(file_name):
    last_del = file_name.rfind(os.sep)
    return file_name[last_del + 1:]


def get_file_extension(file_name):
    """ Returns fileName extension part dot including (.txt,.png etc.)"""
    return file_name[file_name.rfind('.'):]


def path_with_last_slash(path):
    assert isinstance(path, (str, bytes))
    path = normalize_path_sep(path)
    if path != '' and path[len(path) - 1:] != os.sep:
        path = path + os.sep
    return path


def create_dir_for_file(file_name):
    safe_mk_dir(os.path.dirname(file_name))


def safe_mk_dir(path):
    assert isinstance(path, (str, bytes))

    if path == '' or os.path.exists(path):
        return

    path_parts = path.split(os.sep)
    act_path_list = []
    for pathItem in path_parts:
        act_path_list.append(pathItem)
        act_path_str = os.sep.join(act_path_list)
        if act_path_str and not os.path.exists(act_path_str):
            os.mkdir(act_path_str)


def extract_file_name2(path):
    head, tail = os.path.split(path)
    return tail


def get_python_modules():
    return sys.modules.keys()


def setup_utf():
    pass


def normalize_path_sep(path):
    assert isinstance(path, (str, bytes))
    path = path.replace('/', os.sep)
    path = path.replace('\\', os.sep)
    return path


def get_file_content(file_name, char_set='utf-8'):
    assert isinstance(file_name, (str, bytes))
    assert isinstance(char_set, (str, bytes))

    if os.path.exists(file_name):
        in_file = codecs.open(file_name, 'r', char_set)
        result = in_file.read()
        in_file.close()
    else:
        result = ''

    return result
