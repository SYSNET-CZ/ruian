# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import List, Dict  # noqa: F401

from swagger_server import util
from swagger_server.models.base_model_ import Model
from swagger_server.models.point_jtsk import PointJtsk  # noqa: F401,E501


class PolygonJtsk(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, polygon: List[PointJtsk] = None):  # noqa: E501
        """PolygonJtsk - a model defined in Swagger

        :param polygon: The polygon of this PolygonJtsk.  # noqa: E501
        :type polygon: List[PointJtsk]
        """
        self.swagger_types = {
            'polygon': List[PointJtsk]
        }

        self.attribute_map = {
            'polygon': 'polygon'
        }
        self._polygon = polygon

    @classmethod
    def from_dict(cls, dikt) -> 'PolygonJtsk':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PolygonJtsk of this PolygonJtsk.  # noqa: E501
        :rtype: PolygonJtsk
        """
        return util.deserialize_model(dikt, cls)

    @property
    def polygon(self) -> List[PointJtsk]:
        """Gets the polygon of this PolygonJtsk.


        :return: The polygon of this PolygonJtsk.
        :rtype: List[PointJtsk]
        """
        return self._polygon

    @polygon.setter
    def polygon(self, polygon: List[PointJtsk]):
        """Sets the polygon of this PolygonJtsk.


        :param polygon: The polygon of this PolygonJtsk.
        :type polygon: List[PointJtsk]
        """

        self._polygon = polygon
