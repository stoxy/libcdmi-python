import base64
import requests

try:
    import json
except ImportError:
    import simplejson as json

from libcdmi.common import CDMI_OBJECT, CDMI_CONTAINER, HEADER_CDMI_VERSION


class Connection(object):

    credentials = None
    endpoint = None

    def __init__(self, endpoint, credentials=None):
        self.endpoint = endpoint
        self.credentials = credentials
        self.base_headers = HEADER_CDMI_VERSION

    def _make_headers(self, headers):
        final_headers = {}
        final_headers.update(self.base_headers)
        final_headers.update(headers)
        return final_headers

    def head(self, resource):
        """Get meta-information about a blob. Returns JSON-encoded metadata."""
        headers = self._make_headers({'Accept': CDMI_OBJECT})
        response = requests.head(self.endpoint + resource,
                                 auth=self.credentials, headers=headers)
        return response.headers

    def get(self, resource):
        """Read contents of a blob."""
        # put relevant headers
        headers = self._make_headers({'Accept': CDMI_OBJECT})
        response = requests.get(self.endpoint + resource,
                                auth=self.credentials, headers=headers)
        return response.json()

    def create_container(self, resource, metadata={}):
        """Create a new container"""
        headers = self._make_headers({'Accept': CDMI_CONTAINER,
                                      'Content-Type': CDMI_CONTAINER})
        data = {'metadata': metadata}

        res = requests.put(self.endpoint + resource, json.dumps(data),
                           auth=self.credentials, headers=headers)
        return res.json()

    update_container = create_container

    def create_blob(self, resource, local_filename, mimetype='text/plain',
                    metadata={}):
        headers = self._make_headers({'Accept': CDMI_OBJECT,
                                      'Content-Type': CDMI_OBJECT})
        data = {'mimetype': mimetype,
                'metadata': metadata}

        with open(local_filename, 'rb') as input_file:
            try:
                content = input_file.read()
                unicode(content, 'utf-8')
                data['valuetransferencoding'] = 'utf-8'
            except UnicodeDecodeError:
                input_file.seek(0)
                content = base64.b64encode(input_file.read())
                data['valuetransferencoding'] = 'base64'

        data['value'] = content

        res = requests.put(self.endpoint + resource, json.dumps(data),
                           auth=self.credentials, headers=headers)
        return res.json()

    update_blob = create_blob

    def delete(self, remoteblob):
        """Delete specified blob"""
        requests.delete(self.endpoint + remoteblob, auth=self.credentials)
