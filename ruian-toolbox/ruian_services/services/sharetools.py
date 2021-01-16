# -*- coding: utf-8 -*-
__author__ = 'Augustyn'


def get_key_value(dict_with_values, key, default_value=""):
    if dict_with_values is None or key not in dict_with_values:
        return default_value
    else:
        return dict_with_values[key]
