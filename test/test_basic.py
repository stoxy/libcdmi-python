import libcdmi
import os
import tempfile
import unittest

from mock import MagicMock


class TestBasic(unittest.TestCase):
    _endpoint = 'http://localhost:8080'

    def setUp(self):
        fh, self._filename = tempfile.mkstemp(prefix='libcdmi-test-')
        os.close(fh) # allow opening by the library

    def tearDown(self):
        os.unlink(self._filename)

    def addToCleanup(self, method, *args, **kw):
        self._cleanup.append((method, args, kw))

    def test_container_and_blob_create_and_delete_mock_requests(self):
        c = libcdmi.open(self._endpoint)
        self.assertTrue(c), 'Could not create connection %s' % self._endpoint

        requests_put = libcdmi.connection.requests.put = MagicMock()

        c.create_container('/container/')

        expected_metadata = ('{"metadata": {}}')

        requests_put.assert_called_once_with(self._endpoint + '/container/',
                         expected_metadata,
                         headers={'Content-Type': 'application/cdmi-container',
                                  'Accept': 'application/cdmi-container',
                                  'X-CDMI-Specification-Version': '1.0.2'},
                                             auth=None)

        expected_metadata = ('{"mimetype": "text/plain", '
                             '"valuetransferencoding": "utf-8", '
                             '"value": "", "metadata": {}}')

        c.create_blob('/container/blob', self._filename)
        requests_put.assert_called_with(
            self._endpoint + '/container/blob',
            expected_metadata,
            headers={'Content-Type': 'application/cdmi-object',
                     'Accept': 'application/cdmi-object',
                     'X-CDMI-Specification-Version': '1.0.2'}, auth=None)
