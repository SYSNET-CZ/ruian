# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Settlement(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, nazev: str=None):  # noqa: E501
        """Settlement - a model defined in Swagger

        :param id: The id of this Settlement.  # noqa: E501
        :type id: int
        :param nazev: The nazev of this Settlement.  # noqa: E501
        :type nazev: str
        """
        self.swagger_types = {
            'id': int,
            'nazev': str
        }

        self.attribute_map = {
            'id': 'id',
            'nazev': 'nazev'
        }
        self._id = id
        self._nazev = nazev

    @classmethod
    def from_dict(cls, dikt) -> 'Settlement':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Settlement of this Settlement.  # noqa: E501
        :rtype: Settlement
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Settlement.


        :return: The id of this Settlement.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Settlement.


        :param id: The id of this Settlement.
        :type id: int
        """

        self._id = id

    @property
    def nazev(self) -> str:
        """Gets the nazev of this Settlement.


        :return: The nazev of this Settlement.
        :rtype: str
        """
        return self._nazev

    @nazev.setter
    def nazev(self, nazev: str):
        """Sets the nazev of this Settlement.


        :param nazev: The nazev of this Settlement.
        :type nazev: str
        """

        self._nazev = nazev
