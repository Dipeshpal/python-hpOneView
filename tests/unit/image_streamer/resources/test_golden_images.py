# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.image_streamer.resources.golden_images import GoldenImages
from hpOneView.resources.resource import ResourceClient


class GoldenImagesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = GoldenImages(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._client.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('name', 'GoldenImage')

        mock_get_by.assert_called_once_with(
            'name', 'GoldenImage')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        information = {
            "type": "GoldenImage",
            "description": "Description of this Golden Image",
        }
        mock_create.return_value = {}

        self._client.create(information)
        mock_create.assert_called_once_with(information.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        information = {
            "type": "GoldenImage",
            "description": "Description of this Golden Image",
        }
        mock_update.return_value = {}

        self._client.update(information)
        mock_update.assert_called_once_with(information.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with(
            '3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/plan-scripts/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._client.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.delete(id, force=False)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_force(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.delete(id, force=True)

        mock_delete.assert_called_once_with(id, force=True, timeout=-1)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload_post_multipart_called_once(self, mock_upload):
        information = {
            "name": "GoldenImageName",
            "description": "Description of this Golden Image",
        }
        filepath = "test/SPPgen9snap6.2015_0405.81.iso"

        self._client.upload(filepath, information)

        expected_uri = '/rest/golden-images?name=GoldenImageName&description=Description%20of%20this%20Golden%20Image'

        mock_upload.assert_called_once_with(filepath, expected_uri)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload_without_description(self, mock_upload):
        information = {
            "name": "GoldenImageName",
        }

        filepath = "test/SPPgen9snap6.2015_0405.81.iso"

        self._client.upload(filepath, information)

        expected_uri = '/rest/golden-images?name=GoldenImageName&description='

        mock_upload.assert_called_once_with(filepath, expected_uri)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload_with_empty_information(self, mock_upload):
        information = {}
        filepath = "test/SPPgen9snap6.2015_0405.81.iso"

        self._client.upload(filepath, information)

        expected_uri = '/rest/golden-images?name=&description='

        mock_upload.assert_called_once_with(filepath, expected_uri)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_archive_called_once_with_id(self, mock_download):
        id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        file_path = "~/archive.log"

        self._client.download_archive(id, file_path)

        mock_download.assert_called_once_with('/rest/golden-images/archive/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              file_path)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_archive_called_once_with_uri(self, mock_download):
        uri = '/rest/golden-images/3518be0e-17c1-4189-8f81-83f3724f6155'
        file_path = "~/archive.log"

        self._client.download_archive(uri, file_path)

        mock_download.assert_called_once_with('/rest/golden-images/archive/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              file_path)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_called_once_with_uri(self, mock_download):
        uri = '/rest/golden-images/3518be0e-17c1-4189-8f81-83f3724f6155'
        file_path = "~/archive.log"

        self._client.download(uri, file_path)

        mock_download.assert_called_once_with('/rest/golden-images/download/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              file_path)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_called_once_with_id(self, mock_download):
        id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        file_path = "~/archive.log"

        self._client.download(id, file_path)

        mock_download.assert_called_once_with('/rest/golden-images/download/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              file_path)
