import base64
import requests

try:
    import json
except ImportError:
    import simplejson as json

from libcdmi.common import CDMI_OBJECT, CDMI_CONTAINER


class ObjectProxy(object):
    pass


class Container(ObjectProxy):
    headers = {}
    mime_type = CDMI_CONTAINER


class Blob(ObjectProxy):
    headers = {}
    mime_type = CDMI_OBJECT


class Connection(object):

    credentials = None
    endpoint = None

    def __init__(self, endpoint, credentials=None):
        self.endpoint = endpoint
        self.credentials = credentials

    def head(self, resource):
        """Get meta-information about a blob. Returns JSON-encoded metadata."""
        headers = {'Accept': CDMI_OBJECT}
        response = requests.head(self.endpoint + resource,
                                 auth=self.credentials,
                                 headers=headers)
        return response.headers

    def get(self, resource):
        """Read contents of a blob."""
        # put relevant headers
        headers = {'Accept': CDMI_OBJECT}
        response = requests.get(self.endpoint + resource,
                                auth=self.credentials,
                                headers=headers)

        return response.json()

    def create_container(self, resource, metadata={}):
        """Create a new container"""
        op = Container()
        op.headers = {'Accept': op.mime_type,
                      'Content-Type': op.mime_type}

        op.data = {'metadata': metadata}

        res = requests.put(self.endpoint + resource,
                           json.dumps(op.data),
                           auth=self.credentials,
                           headers=op.headers)
        return res.json()

    update_container = create_container

    def create_blob(self, resource, local_filename, mimetype='text/plain',
                    metadata={}):
        op = Blob()
        op.headers = {'Accept': op.mime_type,
                      'Content-Type': op.mime_type}

        op.data = {'mimetype': mimetype,
                   'metadata': metadata}

        with open(local_filename, 'rb') as input_file:
            try:
                content = input_file.read()
                unicode(content, 'utf-8')
                op.data['valuetransferencoding'] = 'utf-8'
            except UnicodeDecodeError:
                input_file.seek(0)
                content = base64.b64encode(input_file.read())
                op.data['valuetransferencoding'] = 'base64'

        op.data['value'] = content

        res = requests.put(self.endpoint + resource,
                           json.dumps(op.data),
                           auth=self.credentials,
                           headers=op.headers)
        return res.json()

    update_blob = create_blob

    def delete(self, remoteblob):
        """Delete specified blob"""
        requests.delete(self.endpoint + remoteblob, auth=self.credentials)
