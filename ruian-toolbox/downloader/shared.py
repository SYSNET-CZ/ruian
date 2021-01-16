# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        shared
# Purpose:     Module shared procedures.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------

first_call = True
ruian_tool_box_path = ""


def setup_paths(depth=1):
    # ####################################
    # Setup path to RUIANToolbox
    # ####################################
    global ruian_tool_box_path
    global first_call

    if first_call:
        import os.path
        import sys

        pathParts = os.path.dirname(__file__).split(os.sep)
        base_path = os.sep.join(pathParts[:len(pathParts) - depth])

        ruian_tool_box_path = base_path

        if base_path not in sys.path:
            sys.path.append(base_path)
        first_call = False
