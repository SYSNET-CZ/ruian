# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.administrative_division import AdministrativeDivision  # noqa: F401,E501
from swagger_server import util


class Parcela(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, kmenovecislo: int=None, pododdelenicisla: int=None, vymeraparcely: float=None, administrative_division: AdministrativeDivision=None):  # noqa: E501
        """Parcela - a model defined in Swagger

        :param id: The id of this Parcela.  # noqa: E501
        :type id: int
        :param kmenovecislo: The kmenovecislo of this Parcela.  # noqa: E501
        :type kmenovecislo: int
        :param pododdelenicisla: The pododdelenicisla of this Parcela.  # noqa: E501
        :type pododdelenicisla: int
        :param vymeraparcely: The vymeraparcely of this Parcela.  # noqa: E501
        :type vymeraparcely: float
        :param administrative_division: The administrative_division of this Parcela.  # noqa: E501
        :type administrative_division: AdministrativeDivision
        """
        self.swagger_types = {
            'id': int,
            'kmenovecislo': int,
            'pododdelenicisla': int,
            'vymeraparcely': float,
            'administrative_division': AdministrativeDivision
        }

        self.attribute_map = {
            'id': 'id',
            'kmenovecislo': 'kmenovecislo',
            'pododdelenicisla': 'pododdelenicisla',
            'vymeraparcely': 'vymeraparcely',
            'administrative_division': 'administrative_division'
        }
        self._id = id
        self._kmenovecislo = kmenovecislo
        self._pododdelenicisla = pododdelenicisla
        self._vymeraparcely = vymeraparcely
        self._administrative_division = administrative_division

    @classmethod
    def from_dict(cls, dikt) -> 'Parcela':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Parcela of this Parcela.  # noqa: E501
        :rtype: Parcela
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Parcela.


        :return: The id of this Parcela.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Parcela.


        :param id: The id of this Parcela.
        :type id: int
        """

        self._id = id

    @property
    def kmenovecislo(self) -> int:
        """Gets the kmenovecislo of this Parcela.


        :return: The kmenovecislo of this Parcela.
        :rtype: int
        """
        return self._kmenovecislo

    @kmenovecislo.setter
    def kmenovecislo(self, kmenovecislo: int):
        """Sets the kmenovecislo of this Parcela.


        :param kmenovecislo: The kmenovecislo of this Parcela.
        :type kmenovecislo: int
        """

        self._kmenovecislo = kmenovecislo

    @property
    def pododdelenicisla(self) -> int:
        """Gets the pododdelenicisla of this Parcela.


        :return: The pododdelenicisla of this Parcela.
        :rtype: int
        """
        return self._pododdelenicisla

    @pododdelenicisla.setter
    def pododdelenicisla(self, pododdelenicisla: int):
        """Sets the pododdelenicisla of this Parcela.


        :param pododdelenicisla: The pododdelenicisla of this Parcela.
        :type pododdelenicisla: int
        """

        self._pododdelenicisla = pododdelenicisla

    @property
    def vymeraparcely(self) -> float:
        """Gets the vymeraparcely of this Parcela.


        :return: The vymeraparcely of this Parcela.
        :rtype: float
        """
        return self._vymeraparcely

    @vymeraparcely.setter
    def vymeraparcely(self, vymeraparcely: float):
        """Sets the vymeraparcely of this Parcela.


        :param vymeraparcely: The vymeraparcely of this Parcela.
        :type vymeraparcely: float
        """

        self._vymeraparcely = vymeraparcely

    @property
    def administrative_division(self) -> AdministrativeDivision:
        """Gets the administrative_division of this Parcela.


        :return: The administrative_division of this Parcela.
        :rtype: AdministrativeDivision
        """
        return self._administrative_division

    @administrative_division.setter
    def administrative_division(self, administrative_division: AdministrativeDivision):
        """Sets the administrative_division of this Parcela.


        :param administrative_division: The administrative_division of this Parcela.
        :type administrative_division: AdministrativeDivision
        """

        self._administrative_division = administrative_division
