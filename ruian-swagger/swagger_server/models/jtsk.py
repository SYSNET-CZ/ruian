# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Jtsk(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, x: float = None, y: float = None):  # noqa: E501
        """Jtsk - a model defined in Swagger

        :param x: The x of this Jtsk.  # noqa: E501
        :type x: float
        :param y: The y of this Jtsk.  # noqa: E501
        :type y: float
        """
        self.swagger_types = {
            'x': float,
            'y': float
        }

        self.attribute_map = {
            'x': 'x',
            'y': 'y'
        }
        self._x = x
        self._y = y

    @classmethod
    def from_dict(cls, dikt) -> 'Jtsk':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Jtsk of this Jtsk.  # noqa: E501
        :rtype: Jtsk
        """
        return util.deserialize_model(dikt, cls)

    @property
    def x(self) -> float:
        """Gets the x of this Jtsk.


        :return: The x of this Jtsk.
        :rtype: float
        """
        return self._x

    @x.setter
    def x(self, x: float):
        """Sets the x of this Jtsk.


        :param x: The x of this Jtsk.
        :type x: float
        """

        self._x = x

    @property
    def y(self) -> float:
        """Gets the y of this Jtsk.


        :return: The y of this Jtsk.
        :rtype: float
        """
        return self._y

    @y.setter
    def y(self, y: float):
        """Sets the y of this Jtsk.


        :param y: The y of this Jtsk.
        :type y: float
        """

        self._y = y
