import libcdmi
import os
import tempfile
import unittest

from mock import MagicMock


class TestBasic(unittest.TestCase):
    _endpoint = 'http://localhost:8080'
    _mock_up_marker = object()

    def setUp(self):
        self._cleanup = []
        fh, self._filename = tempfile.mkstemp(prefix='libcdmi-test-')
        os.close(fh) # allow opening by the library

    def tearDown(self):
        os.unlink(self._filename)

        for method, args, kwargs in self._cleanup:
            method(*args, **kwargs)

    def addToCleanup(self, method, *args, **kw):
        self._cleanup.append((method, args, kw))

    def mockUp(self, container, object_name, new_value=_mock_up_marker):
        if new_value is self._mock_up_marker:
            new_value = MagicMock()
        old_value = getattr(container, object_name)
        setattr(container, object_name, new_value)
        self.addToCleanup(setattr, container, object_name, old_value)
        return new_value

    def test_container_and_blob_create_and_delete_mock_requests(self):
        c = libcdmi.open(self._endpoint)

        requests_put = self.mockUp(libcdmi.connection.requests, 'put')

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

        c.create_object('/container/blob', self._filename)
        requests_put.assert_called_with(
            self._endpoint + '/container/blob',
            expected_metadata,
            headers={'Content-Type': 'application/cdmi-object',
                     'Accept': 'application/cdmi-object',
                     'X-CDMI-Specification-Version': '1.0.2'}, auth=None)

        requests_delete = self.mockUp(libcdmi.connection.requests, 'delete')
        c.delete('/container/blob')
        requests_delete.assert_called_once_with(self._endpoint + '/container/blob', auth=None)

    def test_open_connection(self):
        c = libcdmi.open(self._endpoint)
        self.assertTrue(c, 'Could not create a connection with %s!' % self._endpoint)
        self.assertEqual(type(c), libcdmi.connection.Connection)
        self.assertEqual(c.endpoint, self._endpoint)

    def test_get_container_mock_requests(self):
        c = libcdmi.open(self._endpoint)
        requests_get = self.mockUp(libcdmi.connection.requests, 'get')
        self.mockUp(libcdmi.connection.requests, 'put')
        c.create_container('/container/')
        c.get('/container/', accept=libcdmi.common.CDMI_CONTAINER)
        requests_get.assert_called_once_with(self._endpoint + '/container/',
                                             headers={'Accept': 'application/cdmi-container',
                                                      'X-CDMI-Specification-Version': '1.0.2'},
                                             auth=None)

    def test_get_object_mock_requests(self):
        c = libcdmi.open(self._endpoint)
        requests_get = self.mockUp(libcdmi.connection.requests, 'get')
        self.mockUp(libcdmi.connection.requests, 'put')

        c.create_object('/container/blob', self._filename)

        c.get('/container/blob')
        requests_get.assert_called_once_with(self._endpoint + '/container/blob',
                                             headers={'Accept': 'application/cdmi-object',
                                                      'X-CDMI-Specification-Version': '1.0.2'},
                                             auth=None)

    def test_raises_error_on_bad_status_code(self):
        c = libcdmi.open(self._endpoint)
        requests_get = self.mockUp(libcdmi.connection.requests, 'get')
        requests_get.return_value = MagicMock()
        response = requests_get.return_value
        self.mockUp(libcdmi.connection.requests, 'put')
        c.create_container('/container/')
        response.raise_on_status.assert_called_once_with()
