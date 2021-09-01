# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.address import Address  # noqa: F401,E501
from swagger_server import util


class NearbyAddress(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, order: int = None, distance: float = None, address: Address = None):  # noqa: E501
        """NearbyAddress - a model defined in Swagger

        :param order: The order of this NearbyAddress.  # noqa: E501
        :type order: int
        :param distance: The distance of this NearbyAddress.  # noqa: E501
        :type distance: float
        :param address: The address of this NearbyAddress.  # noqa: E501
        :type address: Address
        """
        self.swagger_types = {
            'order': int,
            'distance': float,
            'address': Address
        }

        self.attribute_map = {
            'order': 'order',
            'distance': 'distance',
            'address': 'address'
        }
        self._order = order
        self._distance = distance
        self._address = address

    @classmethod
    def from_dict(cls, dikt) -> 'NearbyAddress':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NearbyAddress of this NearbyAddress.  # noqa: E501
        :rtype: NearbyAddress
        """
        return util.deserialize_model(dikt, cls)

    @property
    def order(self) -> int:
        """Gets the order of this NearbyAddress.


        :return: The order of this NearbyAddress.
        :rtype: int
        """
        return self._order

    @order.setter
    def order(self, order: int):
        """Sets the order of this NearbyAddress.


        :param order: The order of this NearbyAddress.
        :type order: int
        """

        self._order = order

    @property
    def distance(self) -> float:
        """Gets the distance of this NearbyAddress.


        :return: The distance of this NearbyAddress.
        :rtype: float
        """
        return self._distance

    @distance.setter
    def distance(self, distance: float):
        """Sets the distance of this NearbyAddress.


        :param distance: The distance of this NearbyAddress.
        :type distance: float
        """

        self._distance = distance

    @property
    def address(self) -> Address:
        """Gets the address of this NearbyAddress.


        :return: The address of this NearbyAddress.
        :rtype: Address
        """
        return self._address

    @address.setter
    def address(self, address: Address):
        """Sets the address of this NearbyAddress.


        :param address: The address of this NearbyAddress.
        :type address: Address
        """

        self._address = address