python-redfish
==============

This repository will be used to house the Redfish python library, a reference
implementation to enable Python developers to communicate with the Redfish API
(http://www.redfishspecification.org/).

.. note:

    The current Redfish specification revsion is 0.91 - anything and everything
    in this library is subject to change until the DMTF ratifies the Redfish API
    standard.

Directory Structure
-------------------

This project follows the same convention as OpenStack projects, eg. using pbr
for build and test automation.

    examples/
    tests/


Requirements
------------

To use the enclosed examples, you will need Python 2.7
(https://www.python.org/downloads/).  Note that Python 2.7.9 enforces greater
SSL verification requiring server certificates be installed.  Parameters to
relax the requirements are available in the library, but these configurations
are discouraged due to security concerns.

Further References
------------------

The data model documentation can be found here:
  http://www.redfishspecification.org/redfish-data-model-and-schema/

The overall protocol documentation can be found here:
  http://www.redfishspecification.org/