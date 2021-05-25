# coding: utf-8

from __future__ import absolute_import

from swagger_server.test import BaseTestCase


class TestDevelopersController(BaseTestCase):
    """DevelopersController integration test stubs"""

    def test_info_api(self):
        """Test case for info_api

        get service info
        """
        response = self.client.open(
            '/sysnetcz/RUIAN/1.0.0-oas3/info',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
