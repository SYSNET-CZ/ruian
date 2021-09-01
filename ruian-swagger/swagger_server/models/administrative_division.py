# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class AdministrativeDivision(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, ku_kod: int = None, ku_nazev: str = None, obec_kod: int = None, obec_nazev: str = None,
                 obec_statuskod: int = None, orp_kod: int = None, orp_nazev: str = None, spravni_obec_kod: int = None,
                 spravni_obec_nazev: str = None, pou_kod: int = None, pou_nazev: str = None, okres_kod: int = None,
                 okres_nazev: str = None, vusc_kod: int = None, vusc_nazev: str = None,
                 regionsoudrznosti_kod: int = None, regionsoudrznosti_nazev: str = None, nuts_1: str = None,
                 nuts_2: str = None, nuts_3: str = None, nuts_lau1: str = None, nuts_lau2: str = None):  # noqa: E501
        """AdministrativeDivision - a model defined in Swagger

        :param ku_kod: The ku_kod of this AdministrativeDivision.  # noqa: E501
        :type ku_kod: int
        :param ku_nazev: The ku_nazev of this AdministrativeDivision.  # noqa: E501
        :type ku_nazev: str
        :param obec_kod: The obec_kod of this AdministrativeDivision.  # noqa: E501
        :type obec_kod: int
        :param obec_nazev: The obec_nazev of this AdministrativeDivision.  # noqa: E501
        :type obec_nazev: str
        :param obec_statuskod: The obec_statuskod of this AdministrativeDivision.  # noqa: E501
        :type obec_statuskod: int
        :param orp_kod: The orp_kod of this AdministrativeDivision.  # noqa: E501
        :type orp_kod: int
        :param orp_nazev: The orp_nazev of this AdministrativeDivision.  # noqa: E501
        :type orp_nazev: str
        :param spravni_obec_kod: The spravni_obec_kod of this AdministrativeDivision.  # noqa: E501
        :type spravni_obec_kod: int
        :param spravni_obec_nazev: The spravni_obec_nazev of this AdministrativeDivision.  # noqa: E501
        :type spravni_obec_nazev: str
        :param pou_kod: The pou_kod of this AdministrativeDivision.  # noqa: E501
        :type pou_kod: int
        :param pou_nazev: The pou_nazev of this AdministrativeDivision.  # noqa: E501
        :type pou_nazev: str
        :param okres_kod: The okres_kod of this AdministrativeDivision.  # noqa: E501
        :type okres_kod: int
        :param okres_nazev: The okres_nazev of this AdministrativeDivision.  # noqa: E501
        :type okres_nazev: str
        :param vusc_kod: The vusc_kod of this AdministrativeDivision.  # noqa: E501
        :type vusc_kod: int
        :param vusc_nazev: The vusc_nazev of this AdministrativeDivision.  # noqa: E501
        :type vusc_nazev: str
        :param regionsoudrznosti_kod: The regionsoudrznosti_kod of this AdministrativeDivision.  # noqa: E501
        :type regionsoudrznosti_kod: int
        :param regionsoudrznosti_nazev: The regionsoudrznosti_nazev of this AdministrativeDivision.  # noqa: E501
        :type regionsoudrznosti_nazev: str
        :param nuts_1: The nuts_1 of this AdministrativeDivision.  # noqa: E501
        :type nuts_1: str
        :param nuts_2: The nuts_2 of this AdministrativeDivision.  # noqa: E501
        :type nuts_2: str
        :param nuts_3: The nuts_3 of this AdministrativeDivision.  # noqa: E501
        :type nuts_3: str
        :param nuts_lau1: The nuts_lau1 of this AdministrativeDivision.  # noqa: E501
        :type nuts_lau1: str
        :param nuts_lau2: The nuts_lau2 of this AdministrativeDivision.  # noqa: E501
        :type nuts_lau2: str
        """
        self.swagger_types = {
            'ku_kod': int,
            'ku_nazev': str,
            'obec_kod': int,
            'obec_nazev': str,
            'obec_statuskod': int,
            'orp_kod': int,
            'orp_nazev': str,
            'spravni_obec_kod': int,
            'spravni_obec_nazev': str,
            'pou_kod': int,
            'pou_nazev': str,
            'okres_kod': int,
            'okres_nazev': str,
            'vusc_kod': int,
            'vusc_nazev': str,
            'regionsoudrznosti_kod': int,
            'regionsoudrznosti_nazev': str,
            'nuts_1': str,
            'nuts_2': str,
            'nuts_3': str,
            'nuts_lau1': str,
            'nuts_lau2': str
        }

        self.attribute_map = {
            'ku_kod': 'ku_kod',
            'ku_nazev': 'ku_nazev',
            'obec_kod': 'obec_kod',
            'obec_nazev': 'obec_nazev',
            'obec_statuskod': 'obec_statuskod',
            'orp_kod': 'orp_kod',
            'orp_nazev': 'orp_nazev',
            'spravni_obec_kod': 'spravni_obec_kod',
            'spravni_obec_nazev': 'spravni_obec_nazev',
            'pou_kod': 'pou_kod',
            'pou_nazev': 'pou_nazev',
            'okres_kod': 'okres_kod',
            'okres_nazev': 'okres_nazev',
            'vusc_kod': 'vusc_kod',
            'vusc_nazev': 'vusc_nazev',
            'regionsoudrznosti_kod': 'regionsoudrznosti_kod',
            'regionsoudrznosti_nazev': 'regionsoudrznosti_nazev',
            'nuts_1': 'nuts_1',
            'nuts_2': 'nuts_2',
            'nuts_3': 'nuts_3',
            'nuts_lau1': 'nuts_lau1',
            'nuts_lau2': 'nuts_lau2'
        }
        self._ku_kod = ku_kod
        self._ku_nazev = ku_nazev
        self._obec_kod = obec_kod
        self._obec_nazev = obec_nazev
        self._obec_statuskod = obec_statuskod
        self._orp_kod = orp_kod
        self._orp_nazev = orp_nazev
        self._spravni_obec_kod = spravni_obec_kod
        self._spravni_obec_nazev = spravni_obec_nazev
        self._pou_kod = pou_kod
        self._pou_nazev = pou_nazev
        self._okres_kod = okres_kod
        self._okres_nazev = okres_nazev
        self._vusc_kod = vusc_kod
        self._vusc_nazev = vusc_nazev
        self._regionsoudrznosti_kod = regionsoudrznosti_kod
        self._regionsoudrznosti_nazev = regionsoudrznosti_nazev
        self._nuts_1 = nuts_1
        self._nuts_2 = nuts_2
        self._nuts_3 = nuts_3
        self._nuts_lau1 = nuts_lau1
        self._nuts_lau2 = nuts_lau2

    @classmethod
    def from_dict(cls, dikt) -> 'AdministrativeDivision':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The AdministrativeDivision of this AdministrativeDivision.  # noqa: E501
        :rtype: AdministrativeDivision
        """
        return util.deserialize_model(dikt, cls)

    @property
    def ku_kod(self) -> int:
        """Gets the ku_kod of this AdministrativeDivision.


        :return: The ku_kod of this AdministrativeDivision.
        :rtype: int
        """
        return self._ku_kod

    @ku_kod.setter
    def ku_kod(self, ku_kod: int):
        """Sets the ku_kod of this AdministrativeDivision.


        :param ku_kod: The ku_kod of this AdministrativeDivision.
        :type ku_kod: int
        """

        self._ku_kod = ku_kod

    @property
    def ku_nazev(self) -> str:
        """Gets the ku_nazev of this AdministrativeDivision.


        :return: The ku_nazev of this AdministrativeDivision.
        :rtype: str
        """
        return self._ku_nazev

    @ku_nazev.setter
    def ku_nazev(self, ku_nazev: str):
        """Sets the ku_nazev of this AdministrativeDivision.


        :param ku_nazev: The ku_nazev of this AdministrativeDivision.
        :type ku_nazev: str
        """

        self._ku_nazev = ku_nazev

    @property
    def obec_kod(self) -> int:
        """Gets the obec_kod of this AdministrativeDivision.


        :return: The obec_kod of this AdministrativeDivision.
        :rtype: int
        """
        return self._obec_kod

    @obec_kod.setter
    def obec_kod(self, obec_kod: int):
        """Sets the obec_kod of this AdministrativeDivision.


        :param obec_kod: The obec_kod of this AdministrativeDivision.
        :type obec_kod: int
        """

        self._obec_kod = obec_kod

    @property
    def obec_nazev(self) -> str:
        """Gets the obec_nazev of this AdministrativeDivision.


        :return: The obec_nazev of this AdministrativeDivision.
        :rtype: str
        """
        return self._obec_nazev

    @obec_nazev.setter
    def obec_nazev(self, obec_nazev: str):
        """Sets the obec_nazev of this AdministrativeDivision.


        :param obec_nazev: The obec_nazev of this AdministrativeDivision.
        :type obec_nazev: str
        """

        self._obec_nazev = obec_nazev

    @property
    def obec_statuskod(self) -> int:
        """Gets the obec_statuskod of this AdministrativeDivision.


        :return: The obec_statuskod of this AdministrativeDivision.
        :rtype: int
        """
        return self._obec_statuskod

    @obec_statuskod.setter
    def obec_statuskod(self, obec_statuskod: int):
        """Sets the obec_statuskod of this AdministrativeDivision.


        :param obec_statuskod: The obec_statuskod of this AdministrativeDivision.
        :type obec_statuskod: int
        """

        self._obec_statuskod = obec_statuskod

    @property
    def orp_kod(self) -> int:
        """Gets the orp_kod of this AdministrativeDivision.


        :return: The orp_kod of this AdministrativeDivision.
        :rtype: int
        """
        return self._orp_kod

    @orp_kod.setter
    def orp_kod(self, orp_kod: int):
        """Sets the orp_kod of this AdministrativeDivision.


        :param orp_kod: The orp_kod of this AdministrativeDivision.
        :type orp_kod: int
        """

        self._orp_kod = orp_kod

    @property
    def orp_nazev(self) -> str:
        """Gets the orp_nazev of this AdministrativeDivision.


        :return: The orp_nazev of this AdministrativeDivision.
        :rtype: str
        """
        return self._orp_nazev

    @orp_nazev.setter
    def orp_nazev(self, orp_nazev: str):
        """Sets the orp_nazev of this AdministrativeDivision.


        :param orp_nazev: The orp_nazev of this AdministrativeDivision.
        :type orp_nazev: str
        """

        self._orp_nazev = orp_nazev

    @property
    def spravni_obec_kod(self) -> int:
        """Gets the spravni_obec_kod of this AdministrativeDivision.


        :return: The spravni_obec_kod of this AdministrativeDivision.
        :rtype: int
        """
        return self._spravni_obec_kod

    @spravni_obec_kod.setter
    def spravni_obec_kod(self, spravni_obec_kod: int):
        """Sets the spravni_obec_kod of this AdministrativeDivision.


        :param spravni_obec_kod: The spravni_obec_kod of this AdministrativeDivision.
        :type spravni_obec_kod: int
        """

        self._spravni_obec_kod = spravni_obec_kod

    @property
    def spravni_obec_nazev(self) -> str:
        """Gets the spravni_obec_nazev of this AdministrativeDivision.


        :return: The spravni_obec_nazev of this AdministrativeDivision.
        :rtype: str
        """
        return self._spravni_obec_nazev

    @spravni_obec_nazev.setter
    def spravni_obec_nazev(self, spravni_obec_nazev: str):
        """Sets the spravni_obec_nazev of this AdministrativeDivision.


        :param spravni_obec_nazev: The spravni_obec_nazev of this AdministrativeDivision.
        :type spravni_obec_nazev: str
        """

        self._spravni_obec_nazev = spravni_obec_nazev

    @property
    def pou_kod(self) -> int:
        """Gets the pou_kod of this AdministrativeDivision.


        :return: The pou_kod of this AdministrativeDivision.
        :rtype: int
        """
        return self._pou_kod

    @pou_kod.setter
    def pou_kod(self, pou_kod: int):
        """Sets the pou_kod of this AdministrativeDivision.


        :param pou_kod: The pou_kod of this AdministrativeDivision.
        :type pou_kod: int
        """

        self._pou_kod = pou_kod

    @property
    def pou_nazev(self) -> str:
        """Gets the pou_nazev of this AdministrativeDivision.


        :return: The pou_nazev of this AdministrativeDivision.
        :rtype: str
        """
        return self._pou_nazev

    @pou_nazev.setter
    def pou_nazev(self, pou_nazev: str):
        """Sets the pou_nazev of this AdministrativeDivision.


        :param pou_nazev: The pou_nazev of this AdministrativeDivision.
        :type pou_nazev: str
        """

        self._pou_nazev = pou_nazev

    @property
    def okres_kod(self) -> int:
        """Gets the okres_kod of this AdministrativeDivision.


        :return: The okres_kod of this AdministrativeDivision.
        :rtype: int
        """
        return self._okres_kod

    @okres_kod.setter
    def okres_kod(self, okres_kod: int):
        """Sets the okres_kod of this AdministrativeDivision.


        :param okres_kod: The okres_kod of this AdministrativeDivision.
        :type okres_kod: int
        """

        self._okres_kod = okres_kod

    @property
    def okres_nazev(self) -> str:
        """Gets the okres_nazev of this AdministrativeDivision.


        :return: The okres_nazev of this AdministrativeDivision.
        :rtype: str
        """
        return self._okres_nazev

    @okres_nazev.setter
    def okres_nazev(self, okres_nazev: str):
        """Sets the okres_nazev of this AdministrativeDivision.


        :param okres_nazev: The okres_nazev of this AdministrativeDivision.
        :type okres_nazev: str
        """

        self._okres_nazev = okres_nazev

    @property
    def vusc_kod(self) -> int:
        """Gets the vusc_kod of this AdministrativeDivision.


        :return: The vusc_kod of this AdministrativeDivision.
        :rtype: int
        """
        return self._vusc_kod

    @vusc_kod.setter
    def vusc_kod(self, vusc_kod: int):
        """Sets the vusc_kod of this AdministrativeDivision.


        :param vusc_kod: The vusc_kod of this AdministrativeDivision.
        :type vusc_kod: int
        """

        self._vusc_kod = vusc_kod

    @property
    def vusc_nazev(self) -> str:
        """Gets the vusc_nazev of this AdministrativeDivision.


        :return: The vusc_nazev of this AdministrativeDivision.
        :rtype: str
        """
        return self._vusc_nazev

    @vusc_nazev.setter
    def vusc_nazev(self, vusc_nazev: str):
        """Sets the vusc_nazev of this AdministrativeDivision.


        :param vusc_nazev: The vusc_nazev of this AdministrativeDivision.
        :type vusc_nazev: str
        """

        self._vusc_nazev = vusc_nazev

    @property
    def regionsoudrznosti_kod(self) -> int:
        """Gets the regionsoudrznosti_kod of this AdministrativeDivision.


        :return: The regionsoudrznosti_kod of this AdministrativeDivision.
        :rtype: int
        """
        return self._regionsoudrznosti_kod

    @regionsoudrznosti_kod.setter
    def regionsoudrznosti_kod(self, regionsoudrznosti_kod: int):
        """Sets the regionsoudrznosti_kod of this AdministrativeDivision.


        :param regionsoudrznosti_kod: The regionsoudrznosti_kod of this AdministrativeDivision.
        :type regionsoudrznosti_kod: int
        """

        self._regionsoudrznosti_kod = regionsoudrznosti_kod

    @property
    def regionsoudrznosti_nazev(self) -> str:
        """Gets the regionsoudrznosti_nazev of this AdministrativeDivision.


        :return: The regionsoudrznosti_nazev of this AdministrativeDivision.
        :rtype: str
        """
        return self._regionsoudrznosti_nazev

    @regionsoudrznosti_nazev.setter
    def regionsoudrznosti_nazev(self, regionsoudrznosti_nazev: str):
        """Sets the regionsoudrznosti_nazev of this AdministrativeDivision.


        :param regionsoudrznosti_nazev: The regionsoudrznosti_nazev of this AdministrativeDivision.
        :type regionsoudrznosti_nazev: str
        """

        self._regionsoudrznosti_nazev = regionsoudrznosti_nazev

    @property
    def nuts_1(self) -> str:
        """Gets the nuts_1 of this AdministrativeDivision.


        :return: The nuts_1 of this AdministrativeDivision.
        :rtype: str
        """
        return self._nuts_1

    @nuts_1.setter
    def nuts_1(self, nuts_1: str):
        """Sets the nuts_1 of this AdministrativeDivision.


        :param nuts_1: The nuts_1 of this AdministrativeDivision.
        :type nuts_1: str
        """

        self._nuts_1 = nuts_1

    @property
    def nuts_2(self) -> str:
        """Gets the nuts_2 of this AdministrativeDivision.


        :return: The nuts_2 of this AdministrativeDivision.
        :rtype: str
        """
        return self._nuts_2

    @nuts_2.setter
    def nuts_2(self, nuts_2: str):
        """Sets the nuts_2 of this AdministrativeDivision.


        :param nuts_2: The nuts_2 of this AdministrativeDivision.
        :type nuts_2: str
        """

        self._nuts_2 = nuts_2

    @property
    def nuts_3(self) -> str:
        """Gets the nuts_3 of this AdministrativeDivision.


        :return: The nuts_3 of this AdministrativeDivision.
        :rtype: str
        """
        return self._nuts_3

    @nuts_3.setter
    def nuts_3(self, nuts_3: str):
        """Sets the nuts_3 of this AdministrativeDivision.


        :param nuts_3: The nuts_3 of this AdministrativeDivision.
        :type nuts_3: str
        """

        self._nuts_3 = nuts_3

    @property
    def nuts_lau1(self) -> str:
        """Gets the nuts_lau1 of this AdministrativeDivision.


        :return: The nuts_lau1 of this AdministrativeDivision.
        :rtype: str
        """
        return self._nuts_lau1

    @nuts_lau1.setter
    def nuts_lau1(self, nuts_lau1: str):
        """Sets the nuts_lau1 of this AdministrativeDivision.


        :param nuts_lau1: The nuts_lau1 of this AdministrativeDivision.
        :type nuts_lau1: str
        """

        self._nuts_lau1 = nuts_lau1

    @property
    def nuts_lau2(self) -> str:
        """Gets the nuts_lau2 of this AdministrativeDivision.


        :return: The nuts_lau2 of this AdministrativeDivision.
        :rtype: str
        """
        return self._nuts_lau2

    @nuts_lau2.setter
    def nuts_lau2(self, nuts_lau2: str):
        """Sets the nuts_lau2 of this AdministrativeDivision.


        :param nuts_lau2: The nuts_lau2 of this AdministrativeDivision.
        :type nuts_lau2: str
        """

        self._nuts_lau2 = nuts_lau2