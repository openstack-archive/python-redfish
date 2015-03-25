
 # Copyright 2014 Hewlett-Packard Development Company, L.P.
 #
 # Licensed under the Apache License, Version 2.0 (the "License"); you may
 # not use this file except in compliance with the License. You may obtain
 # a copy of the License at
 #
 #      http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 # License for the specific language governing permissions and limitations
 # under the License.


"""

Provides functions for using the Redfish RESTful API.

"""

import json
import sys
from redfish import connection

class RedfishOperation(object):

    def __init__(self, host, user_name, password):
        super(RedFishOperation, self).__init__()
        # XXX add members, we're going to have to cache
        conn = RedfishConnection(host, user_name, password)

    # noinspection PyPep8Naming
    def reset_server():
        print('Reset a server')
    
        # for each system in the systems collection at /rest/v1/Systems
        for status, headers, system, memberuri in collection(host, '/rest/v1/Systems', None, user_name, password):
    
            # verify expected type
            # hint:  don't limit to version 0 here as we will rev to 1.0 at some point hopefully with minimal changes
            assert(conn.get_type(system) == 'ComputerSystem.0' or conn.get_type(system) == 'ComputerSystem.1')
    
            # verify it supports POST
            assert(conn.operation_allowed(headers, 'POST'))
    
            action = dict()
            action['Action'] = 'Reset'
            action['ResetType'] = 'ForceRestart'
    
            # perform the POST action
            print('POST ' + json.dumps(action) + ' to ' + memberuri)
            status, headers, response = conn.rest_post(host, memberuri, None, action, user_name, password)
            print('POST response = ' + str(status))
            conn.print_extended_error(response)
    
            # point made...quit
            break
