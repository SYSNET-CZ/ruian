# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        shared
# Purpose:
#
# Author:      Administrator
#
# Created:     08/10/2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------
import os
import os.path
import sys


first_call = True
ruian_tool_box_path = ""
isCGIApplication = True


def module_exists(module_name):
    return os.path.exists(ruian_tool_box_path + os.sep + module_name)


def setup_paths(depth=1):
    # ####################################
    # Setup path to RUIANToolbox
    # ####################################
    global first_call
    if first_call:
        path_parts = os.path.dirname(__file__).split(os.sep)
        base_path = os.sep.join(path_parts[:len(path_parts) - depth])

        global ruian_tool_box_path
        ruian_tool_box_path = base_path

        if base_path not in sys.path:
            sys.path.append(base_path)
        first_call = False


def init_app(path_depth=1):
    setup_paths(path_depth)
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
