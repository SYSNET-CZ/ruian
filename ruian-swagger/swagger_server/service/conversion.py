# -*- coding: utf-8 -*-

from swagger_server.service.querying import _convert_point_to_jtsk, _convert_point_to_wgs, _convert_str_wgs_to_jtsk, \
    _convert_polygon_to_wgs, _convert_polygon_to_jtsk, _get_full_address, _get_full_cadaster, _get_full_settlement

point2wgs = _convert_point_to_wgs
point2jtsk = _convert_point_to_jtsk
string_wgs_to_jtsk = _convert_str_wgs_to_jtsk
polygon2wgs = _convert_polygon_to_wgs
polygon2jtsk = _convert_polygon_to_jtsk
get_full_address = _get_full_address
get_full_cadaster = _get_full_cadaster
get_full_settlement = _get_full_settlement


