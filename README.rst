python-redfish
==============

This repository will be used to house the Redfish python library, a reference
implementation to enable Python developers to communicate with the Redfish API
(http://www.redfishspecification.org/).

.. sidebar:: NOTE - DRAFT - WORK IN PROGRESS

    The current Redfish specification revsion is 0.91 - anything and everything
    in this library is subject to change until the DMTF ratifies the Redfish API
    standard v1.0.

Project Structure
-------------------

This project follows the same convention as OpenStack projects, eg. using pbr
for build and test automation::

    doc/            # documentation
    doc/source      # the doc source files live here
    doc/build/html  # output of building any docs will go here
    examples/       # any sample code using this library, eg. for education
                    # should be put here
    redfish/        # the redfish library
    redfish/tests/  # python unit test suite

Requirements
------------

To use the enclosed examples, you will need Python 2.7
(https://www.python.org/downloads/).  Note that Python 2.7.9 enforces greater
SSL verification requiring server certificates be installed.  Parameters to
relax the requirements are available in the library, but these configurations
are discouraged due to security concerns.

Project python dependencies are listed in "requirements.txt".

Any test-specific requirements are listed in "test-requirements.txt".

Further References
------------------

The data model documentation can be found here:
  http://www.redfishspecification.org/redfish-data-model-and-schema/

The overall protocol documentation can be found here:
  http://www.redfishspecification.org/