from libcdmi.connection import Connection

def open(endpoint, credentials=None):
    return Connection(endpoint, credentials=credentials)
