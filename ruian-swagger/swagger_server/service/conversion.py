# -*- coding: utf-8 -*-

from swagger_server.service.querying import _convert_point_to_jtsk, _convert_point_to_wgs, _convert_str_wgs_to_jtsk

point2wgs = _convert_point_to_wgs
point2jtsk = _convert_point_to_jtsk
string_wgs_to_jtsk = _convert_str_wgs_to_jtsk
