# coding=utf-8

from redfish.main import ConnectionParameters

def fake_connection_parameters():
        connection_parameters = ConnectionParameters()
        connection_parameters.rooturl = u'http://127.0.0.1:8000/redfish/v1/'
        connection_parameters.user_name = u''
        connection_parameters.password = u''
        connection_parameters.enforceSSL = False
        connection_parameters.verify_cert = False
        connection_parameters.auth_token = None
        connection_parameters.user_uri = None

        return connection_parameters
