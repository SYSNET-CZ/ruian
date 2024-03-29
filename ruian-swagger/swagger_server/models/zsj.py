# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.administrative_division import AdministrativeDivision  # noqa: F401,E501
from swagger_server.models.settlement import Settlement  # noqa: F401,E501
from swagger_server import util


class Zsj(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, settlement: Settlement=None, administrative_division: AdministrativeDivision=None):  # noqa: E501
        """Zsj - a model defined in Swagger

        :param settlement: The settlement of this Zsj.  # noqa: E501
        :type settlement: Settlement
        :param administrative_division: The administrative_division of this Zsj.  # noqa: E501
        :type administrative_division: AdministrativeDivision
        """
        self.swagger_types = {
            'settlement': Settlement,
            'administrative_division': AdministrativeDivision
        }

        self.attribute_map = {
            'settlement': 'settlement',
            'administrative_division': 'administrative_division'
        }
        self._settlement = settlement
        self._administrative_division = administrative_division

    @classmethod
    def from_dict(cls, dikt) -> 'Zsj':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Zsj of this Zsj.  # noqa: E501
        :rtype: Zsj
        """
        return util.deserialize_model(dikt, cls)

    @property
    def settlement(self) -> Settlement:
        """Gets the settlement of this Zsj.


        :return: The settlement of this Zsj.
        :rtype: Settlement
        """
        return self._settlement

    @settlement.setter
    def settlement(self, settlement: Settlement):
        """Sets the settlement of this Zsj.


        :param settlement: The settlement of this Zsj.
        :type settlement: Settlement
        """

        self._settlement = settlement

    @property
    def administrative_division(self) -> AdministrativeDivision:
        """Gets the administrative_division of this Zsj.


        :return: The administrative_division of this Zsj.
        :rtype: AdministrativeDivision
        """
        return self._administrative_division

    @administrative_division.setter
    def administrative_division(self, administrative_division: AdministrativeDivision):
        """Sets the administrative_division of this Zsj.


        :param administrative_division: The administrative_division of this Zsj.
        :type administrative_division: AdministrativeDivision
        """

        self._administrative_division = administrative_division
