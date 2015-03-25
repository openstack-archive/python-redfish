python-redfish
==============

This repository will be used to house the Redfish python library.  This library
will be used to help Python developers communicate with the Redfish API
(http://www.redfishspecification.org/).

Directory Structure
-------------------

This project follows the same convention as OpenStack projects, eg. using pbr
for build and test automation.

Requirements
------------

To use the enclosed examples, you will need Python 2.7
(https://www.python.org/downloads/).  Note that Python 2.7.9 enforces greater
SSL verification requiring server certificates be installed.  Parameters to
relax the requirements are available in the library, but these configurations
are discouraged due to security concerns.
