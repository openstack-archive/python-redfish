# Copyright 2017 Hewlett Packard Enterprise Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
import pytest

import redfish
from redfish import exception
from redfish import main
from redfish import types


@mock.patch.object(types.config, 'logger', autospec=True)
@mock.patch.object(main, 'ConnectionParameters', autospec=True)
def test_redfish(connection_parameters_mock, logger_mock):
    print('Still a fake test...')
    with pytest.raises(exception.InvalidRedfishContentException) as e:
        redfish.standard.Systems('http://127.0.0.1:8000',
                                 connection_parameters_mock())
    assert 'Ivalid content' in str(e.value.message)
