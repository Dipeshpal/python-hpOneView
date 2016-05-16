# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

import mock
import unittest

from hpOneView.connection import connection
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.resource import ResourceClient


class FcNetworksTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._fc_networks = FcNetworks(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._fc_networks.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        options = {
            'name': 'OneViewSDK Test FC Network',
            'autoLoginRedistribution': False,
            'type': 'fc-networkV2',
            'linkStabilityTime': 30,
            'fabricType': None,
        }
        mock_create.return_value = {}

        self._fc_networks.create(options, False)
        mock_create.assert_called_once_with(options, False)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_default_values(self, mock_create):
        options = {
            'name': 'OneViewSDK Test FC Network',
        }
        options_with_defaults = {
            'name': 'OneViewSDK Test FC Network',
            'autoLoginRedistribution': False,
            'type': 'fc-networkV2',
            'linkStabilityTime': 30,
            'fabricType': 'FabricAttach',
        }
        mock_create.return_value = {}

        self._fc_networks.create(options)

        mock_create.assert_called_once_with(options_with_defaults, True)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
        options = {
            'name': 'OneViewSDK Test FC Network',
            'autoLoginRedistribution': False,
            'type': 'fc-networkV2',
            'linkStabilityTime': 30,
            'fabricType': None,
            'uri': 'a_uri',
        }
        mock_update.return_value = {}

        self._fc_networks.update(options, False)
        mock_update.assert_called_once_with(options, False)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_default_values(self, mock_update):
        options = {
            'name': 'OneViewSDK Test FC Network',
            'uri': 'a_uri',
        }
        options_with_defaults = {
            'name': 'OneViewSDK Test FC Network',
            'autoLoginRedistribution': False,
            'type': 'fc-networkV2',
            'linkStabilityTime': 30,
            'fabricType': 'FabricAttach',
            'uri': 'a_uri',
        }
        mock_update.return_value = {}

        self._fc_networks.update(options)

        mock_update.assert_called_once_with(options_with_defaults, True)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._fc_networks.delete(id, force=False, blocking=True)

        mock_delete.assert_called_once_with(id, force=False, blocking=True)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._fc_networks.get_by('name', 'MyFibreNetwork')

        mock_get_by.assert_called_once_with('name', 'MyFibreNetwork')
