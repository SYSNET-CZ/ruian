# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.administrative_division import AdministrativeDivision  # noqa: F401,E501
from swagger_server.models.mapovy_list50 import MapovyList50  # noqa: F401,E501
from swagger_server.models.povodi import Povodi  # noqa: F401,E501
from swagger_server.models.settlement import Settlement  # noqa: F401,E501
from swagger_server import util


class FullSettlement(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, settlement: Settlement = None, administrative_division: AdministrativeDivision = None,
                 basin: Povodi = None, map50_sheet: MapovyList50 = None):  # noqa: E501
        """FullSettlement - a model defined in Swagger

        :param settlement: The settlement of this FullSettlement.  # noqa: E501
        :type settlement: Settlement
        :param administrative_division: The administrative_division of this FullSettlement.  # noqa: E501
        :type administrative_division: AdministrativeDivision
        :param basin: The basin of this FullSettlement.  # noqa: E501
        :type basin: Povodi
        :param map50_sheet: The map50_sheet of this FullSettlement.  # noqa: E501
        :type map50_sheet: MapovyList50
        """
        self.swagger_types = {
            'settlement': Settlement,
            'administrative_division': AdministrativeDivision,
            'basin': Povodi,
            'map50_sheet': MapovyList50
        }

        self.attribute_map = {
            'settlement': 'settlement',
            'administrative_division': 'administrative_division',
            'basin': 'basin',
            'map50_sheet': 'map50_sheet'
        }
        self._settlement = settlement
        self._administrative_division = administrative_division
        self._basin = basin
        self._map50_sheet = map50_sheet

    @classmethod
    def from_dict(cls, dikt) -> 'FullSettlement':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FullSettlement of this FullSettlement.  # noqa: E501
        :rtype: FullSettlement
        """
        return util.deserialize_model(dikt, cls)

    @property
    def settlement(self) -> Settlement:
        """Gets the settlement of this FullSettlement.


        :return: The settlement of this FullSettlement.
        :rtype: Settlement
        """
        return self._settlement

    @settlement.setter
    def settlement(self, settlement: Settlement):
        """Sets the settlement of this FullSettlement.


        :param settlement: The settlement of this FullSettlement.
        :type settlement: Settlement
        """

        self._settlement = settlement

    @property
    def administrative_division(self) -> AdministrativeDivision:
        """Gets the administrative_division of this FullSettlement.


        :return: The administrative_division of this FullSettlement.
        :rtype: AdministrativeDivision
        """
        return self._administrative_division

    @administrative_division.setter
    def administrative_division(self, administrative_division: AdministrativeDivision):
        """Sets the administrative_division of this FullSettlement.


        :param administrative_division: The administrative_division of this FullSettlement.
        :type administrative_division: AdministrativeDivision
        """

        self._administrative_division = administrative_division

    @property
    def basin(self) -> Povodi:
        """Gets the basin of this FullSettlement.


        :return: The basin of this FullSettlement.
        :rtype: Povodi
        """
        return self._basin

    @basin.setter
    def basin(self, basin: Povodi):
        """Sets the basin of this FullSettlement.


        :param basin: The basin of this FullSettlement.
        :type basin: Povodi
        """

        self._basin = basin

    @property
    def map50_sheet(self) -> MapovyList50:
        """Gets the map50_sheet of this FullSettlement.


        :return: The map50_sheet of this FullSettlement.
        :rtype: MapovyList50
        """
        return self._map50_sheet

    @map50_sheet.setter
    def map50_sheet(self, map50_sheet: MapovyList50):
        """Sets the map50_sheet of this FullSettlement.


        :param map50_sheet: The map50_sheet of this FullSettlement.
        :type map50_sheet: MapovyList50
        """

        self._map50_sheet = map50_sheet
