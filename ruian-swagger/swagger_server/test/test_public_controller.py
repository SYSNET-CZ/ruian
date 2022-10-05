# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.address import Address  # noqa: E501
from swagger_server.models.full_address import FullAddress  # noqa: E501
from swagger_server.models.full_cadaster import FullCadaster  # noqa: E501
from swagger_server.models.full_settlement import FullSettlement  # noqa: E501
from swagger_server.models.jtsk import Jtsk  # noqa: E501
from swagger_server.models.katastralni_uzemi import KatastralniUzemi  # noqa: E501
from swagger_server.models.mapovy_list50 import MapovyList50  # noqa: E501
from swagger_server.models.nearby_address import NearbyAddress  # noqa: E501
from swagger_server.models.parcela import Parcela  # noqa: E501
from swagger_server.models.point_jtsk import PointJtsk  # noqa: E501
from swagger_server.models.point_wgs import PointWgs  # noqa: E501
from swagger_server.models.polygon_jtsk import PolygonJtsk  # noqa: E501
from swagger_server.models.polygon_wgs import PolygonWgs  # noqa: E501
from swagger_server.models.povodi import Povodi  # noqa: E501
from swagger_server.models.wgs import Wgs  # noqa: E501
from swagger_server.models.zsj import Zsj  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPublicController(BaseTestCase):
    """PublicController integration test stubs"""

    def test_compile_address_api(self):
        """Test case for compile_address_api

        compile adresses by query
        """
        body = Address()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/compile/address',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_compile_address_ft_api(self):
        """Test case for compile_address_ft_api

        compile adresses by query
        """
        query_string = [('query', 'query_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/compile/address',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_compile_address_id_api(self):
        """Test case for compile_address_id_api

        compile adresses by identifier
        """
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/compile/address/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_convert_point_jtsk_api(self):
        """Test case for convert_point_jtsk_api

        converts one point from WGS-84 to JTSK
        """
        query_string = [('lat', 'lat_example'),
                        ('lon', 'lon_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/convert/point/jtsk',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_convert_point_jtsk_post_api(self):
        """Test case for convert_point_jtsk_post_api

        converts one point from WGS-84 to JTSK
        """
        body = PointWgs()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/convert/point/jtsk',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_convert_point_wgs_api(self):
        """Test case for convert_point_wgs_api

        converts one point from JTSK to WGS-84
        """
        query_string = [('x', 1.2),
                        ('y', 1.2)]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/convert/point/wgs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_convert_point_wgs_post_api(self):
        """Test case for convert_point_wgs_post_api

        converts one point from JTSK to WGS-84
        """
        body = PointJtsk()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/convert/point/wgs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_convert_polygon_jtsk_api(self):
        """Test case for convert_polygon_jtsk_api

        converts polygon from WGS84 to JTSK
        """
        body = PolygonWgs()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/convert/polygon/jtsk',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_convert_polygon_wgs_api(self):
        """Test case for convert_polygon_wgs_api

        converts polygon from JTSK to WGS84
        """
        body = PolygonJtsk()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/convert/polygon/wgs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_address_id_api(self):
        """Test case for get_address_id_api

        get addres point full info by identifier
        """
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/address/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_ku_id_api(self):
        """Test case for get_ku_id_api

        get cadastral territory full info by identifier
        """
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/cadaster/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_zsj_id_api(self):
        """Test case for get_zsj_id_api

        get basic settlement unit full info by identifier
        """
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/settlement/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_ku_api(self):
        """Test case for ku_api

        find cadastral territory by coordinates
        """
        query_string = [('x', 1.2),
                        ('y', 1.2)]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/cadaster/jtsk',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_ku_post_api(self):
        """Test case for ku_post_api

        find cadastral territory by coordinates
        """
        body = PointJtsk()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/cadaster/jtsk',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_ku_wgs_api(self):
        """Test case for ku_wgs_api

        find cadastral territory by coordinates
        """
        query_string = [('lat', 'lat_example'),
                        ('lon', 'lon_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/cadaster/wgs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_ku_wgs_post_api(self):
        """Test case for ku_wgs_post_api

        find cadastral territory by coordinates
        """
        body = PointWgs()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/cadaster/wgs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mapy50_api(self):
        """Test case for mapy50_api

        find map sheets layout by coordinates
        """
        query_string = [('x', 1.2),
                        ('y', 1.2)]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/sheet50/jtsk',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mapy50_post_api(self):
        """Test case for mapy50_post_api

        find map sheets layout by coordinates
        """
        body = PointJtsk()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/sheet50/jtsk',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mapy50_wgs_api(self):
        """Test case for mapy50_wgs_api

        find map sheets layout by coordinates
        """
        query_string = [('lat', 'lat_example'),
                        ('lon', 'lon_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/sheet50/wgs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mapy50_wgs_post_api(self):
        """Test case for mapy50_wgs_post_api

        find map sheets layout by coordinates
        """
        body = PointWgs()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/sheet50/wgs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_nearby_address_api(self):
        """Test case for nearby_address_api

        find nearby adresses by coordinates
        """
        query_string = [('x', 1.2),
                        ('y', 1.2)]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/nearby/jtsk',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_nearby_address_post_api(self):
        """Test case for nearby_address_post_api

        find nearby adresses by coordinates
        """
        body = PointJtsk()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/nearby/jtsk',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_nearby_address_wgs_api(self):
        """Test case for nearby_address_wgs_api

        find nearby adresses by coordinates
        """
        query_string = [('lat', 'lat_example'),
                        ('lon', 'lon_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/nearby/wgs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_nearby_address_wgs_post_api(self):
        """Test case for nearby_address_wgs_post_api

        find nearby adresses by coordinates
        """
        body = PointWgs()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/nearby/wgs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_parcela_api(self):
        """Test case for parcela_api

        find land parcel by coordinates
        """
        query_string = [('x', 1.2),
                        ('y', 1.2)]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/parcel/jtsk',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_parcela_post_api(self):
        """Test case for parcela_post_api

        find plot (of land) by coordinates
        """
        body = Jtsk()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/parcel/jtsk',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_parcela_wgs_api(self):
        """Test case for parcela_wgs_api

        find land parcel by coordinates
        """
        query_string = [('lat', 'lat_example'),
                        ('lon', 'lon_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/parcel/wgs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_parcela_wgs_post_api(self):
        """Test case for parcela_wgs_post_api

        find plot (of land) by coordinates
        """
        body = Wgs()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/parcel/wgs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_povodi_api(self):
        """Test case for povodi_api

        find basin info by coordinates
        """
        query_string = [('x', 1.2),
                        ('y', 1.2)]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/basin/jtsk',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_povodi_post_api(self):
        """Test case for povodi_post_api

        find basin info by coordinates
        """
        body = PointJtsk()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/basin/jtsk',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_povodi_wgs_api(self):
        """Test case for povodi_wgs_api

        find basin info by coordinates
        """
        query_string = [('lat', 'lat_example'),
                        ('lon', 'lon_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/basin/wgs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_povodi_wgs_post_api(self):
        """Test case for povodi_wgs_post_api

        find basin info by coordinates
        """
        body = PointWgs()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/basin/wgs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_address_api(self):
        """Test case for search_address_api

        search adresses by structured query
        """
        body = Address()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/search/address',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_address_ft_api(self):
        """Test case for search_address_ft_api

        search adresses by query
        """
        query_string = [('query', 'query_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/search/address',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_address_id_api(self):
        """Test case for search_address_id_api

        seach address by identifier
        """
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/search/address/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_validate_address_id_api(self):
        """Test case for validate_address_id_api

        validate adresses by identifier
        """
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/validate/address/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_zsj_api(self):
        """Test case for zsj_api

        find basic settlement unit by coordinates
        """
        query_string = [('x', 1.2),
                        ('y', 1.2)]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/settlement/jtsk',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_zsj_post_api(self):
        """Test case for zsj_post_api

        find basic settlement unit by coordinates
        """
        body = PointJtsk()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/settlement/jtsk',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_zsj_wgs_api(self):
        """Test case for zsj_wgs_api

        find basic settlement unit by coordinates
        """
        query_string = [('lat', 'lat_example'),
                        ('lon', 'lon_example')]
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/settlement/wgs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_zsj_wgs_post_api(self):
        """Test case for zsj_wgs_post_api

        find basic settlement unit by coordinates
        """
        body = PointWgs()
        response = self.client.open(
            '/SYSNET/RUIAN/1.0.2/reverse/settlement/wgs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
