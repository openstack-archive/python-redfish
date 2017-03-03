# coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

import unittest
import mock
import redfish
import tortilla


from redfish.tests.fakes import system_fakes
from redfish.tests.fakes import connection_fakes


class TestSystems(unittest.TestCase):

    def setUp(self):
        mock_init = mock.Mock()
        mock_init.return_value = None
        self.patches = {
            "redfish.standard.Systems.__init__": mock_init,
        }
        for patch, data in self.patches.items():
            mock.patch(patch, data).start()

        self.instance = redfish.standard.Systems()
        self.instance.data = tortilla.utils.Bunch(
            system_fakes.fake_system_data())
        self.instance.api_url = mock.Mock()
        self.instance.api_url.url.return_value = 'http://127.0.0.1:8000'
        self.instance.connection_parameters = connection_fakes.\
            fake_connection_parameters()

    def tearDown(self):
        mock.patch.stopall()

    def test_get_power(self):
        systems = system_fakes.fake_system_data()
        expected = systems.get('PowerState')
        power = self.instance.get_power()
        self.assertEqual(power, expected)

    @mock.patch('requests.post')
    def test_reset_system_with_available_action(self, mock_post):

        fake_url = 'http://127.0.0.1:8000'
        self.instance.api_url.url.return_value = fake_url

        self.instance.reset_system(u'ForceOff')
        self.instance.api_url.url.assert_called()

        systems = system_fakes.fake_system_data()
        target = systems['Actions'][u'#ComputerSystem.Reset']['target']
        expected_url = fake_url + target
        expected_action = '{"ResetType": "ForceOff"}'
        expected_headers = {'OData-Version': '4.0',
                            'Content-type': 'application/json',
                            'Accept': 'application/json',
                            'Origin': fake_url,
                            'User-Agent': 'python-redfish'}
        mock_post.assert_called_once_with(
            expected_url,
            verify=self.instance.connection_parameters.verify_cert,
            headers=expected_headers,
            data=expected_action)
