# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.administrative_division import AdministrativeDivision  # noqa: F401,E501
from swagger_server.models.cadastral_territory import CadastralTerritory  # noqa: F401,E501
from swagger_server.models.mapovy_list50 import MapovyList50  # noqa: F401,E501
from swagger_server.models.povodi import Povodi  # noqa: F401,E501
from swagger_server import util


class FullCadaster(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, cadastral_teritory: CadastralTerritory=None, administrative_division: AdministrativeDivision=None, basin: Povodi=None, map50_sheet: MapovyList50=None):  # noqa: E501
        """FullCadaster - a model defined in Swagger

        :param cadastral_teritory: The cadastral_teritory of this FullCadaster.  # noqa: E501
        :type cadastral_teritory: CadastralTerritory
        :param administrative_division: The administrative_division of this FullCadaster.  # noqa: E501
        :type administrative_division: AdministrativeDivision
        :param basin: The basin of this FullCadaster.  # noqa: E501
        :type basin: Povodi
        :param map50_sheet: The map50_sheet of this FullCadaster.  # noqa: E501
        :type map50_sheet: MapovyList50
        """
        self.swagger_types = {
            'cadastral_teritory': CadastralTerritory,
            'administrative_division': AdministrativeDivision,
            'basin': Povodi,
            'map50_sheet': MapovyList50
        }

        self.attribute_map = {
            'cadastral_teritory': 'cadastral_teritory',
            'administrative_division': 'administrative_division',
            'basin': 'basin',
            'map50_sheet': 'map50_sheet'
        }
        self._cadastral_teritory = cadastral_teritory
        self._administrative_division = administrative_division
        self._basin = basin
        self._map50_sheet = map50_sheet

    @classmethod
    def from_dict(cls, dikt) -> 'FullCadaster':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FullCadaster of this FullCadaster.  # noqa: E501
        :rtype: FullCadaster
        """
        return util.deserialize_model(dikt, cls)

    @property
    def cadastral_teritory(self) -> CadastralTerritory:
        """Gets the cadastral_teritory of this FullCadaster.


        :return: The cadastral_teritory of this FullCadaster.
        :rtype: CadastralTerritory
        """
        return self._cadastral_teritory

    @cadastral_teritory.setter
    def cadastral_teritory(self, cadastral_teritory: CadastralTerritory):
        """Sets the cadastral_teritory of this FullCadaster.


        :param cadastral_teritory: The cadastral_teritory of this FullCadaster.
        :type cadastral_teritory: CadastralTerritory
        """

        self._cadastral_teritory = cadastral_teritory

    @property
    def administrative_division(self) -> AdministrativeDivision:
        """Gets the administrative_division of this FullCadaster.


        :return: The administrative_division of this FullCadaster.
        :rtype: AdministrativeDivision
        """
        return self._administrative_division

    @administrative_division.setter
    def administrative_division(self, administrative_division: AdministrativeDivision):
        """Sets the administrative_division of this FullCadaster.


        :param administrative_division: The administrative_division of this FullCadaster.
        :type administrative_division: AdministrativeDivision
        """

        self._administrative_division = administrative_division

    @property
    def basin(self) -> Povodi:
        """Gets the basin of this FullCadaster.


        :return: The basin of this FullCadaster.
        :rtype: Povodi
        """
        return self._basin

    @basin.setter
    def basin(self, basin: Povodi):
        """Sets the basin of this FullCadaster.


        :param basin: The basin of this FullCadaster.
        :type basin: Povodi
        """

        self._basin = basin

    @property
    def map50_sheet(self) -> MapovyList50:
        """Gets the map50_sheet of this FullCadaster.


        :return: The map50_sheet of this FullCadaster.
        :rtype: MapovyList50
        """
        return self._map50_sheet

    @map50_sheet.setter
    def map50_sheet(self, map50_sheet: MapovyList50):
        """Sets the map50_sheet of this FullCadaster.


        :param map50_sheet: The map50_sheet of this FullCadaster.
        :type map50_sheet: MapovyList50
        """

        self._map50_sheet = map50_sheet
