from libcdmi.connection import Connection
from libcdmi import cli

from requests.exceptions import HTTPError

def open(endpoint, credentials=None, keystone_token=None):
    return Connection(endpoint, credentials=credentials, keystone_token=keystone_token)
