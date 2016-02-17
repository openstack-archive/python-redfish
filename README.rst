python-redfish
==============

This repository will be used to house the Redfish python library, a reference
implementation to enable Python developers to communicate with the Redfish API
(http://www.dmtf.org/standards/redfish).

NOTE::

    DRAFT - WORK IN PROGRESS

    The current Redfish specification revision is 1.0.0 - Note that the mockup 
    is still at version 0.99.0a and may not reflect what the standard provides 
    fully


Project Structure
-------------------

This project follows the same convention as OpenStack projects, eg. using pbr
for build and test automation::

    doc/            # Documentation
    doc/source      # The doc source files live here
    doc/build/html  # Output of building any docs will go here
    dmtf            # Reference documents and mockup provided by the DMTF
    examples/       # Any sample code using this library, eg. for education
                    # should be put here
    pbconf          # Project builder file to build rpm/deb packages for
                    # distributions
    redfish/        # The redfish library itself
    redfish/tests/  # Python redfish unit test suite
    redfish-client  # Client tool to manage redfish devices

Requirements
------------

To use the enclosed examples, you will need Python 2.7
(https://www.python.org/downloads/).  Note that Python 2.7.9 enforces greater
SSL verification requiring server certificates be installed. Parameters to
relax the requirements are available in the library, but these configurations
are discouraged due to security.

Python requirements are listed in requirements.txt; additional requirements for
running the unit test suite are listed in test-requirements.txt.

Get the sources
---------------

The sources are available on github and can be retrieved using::

    git clone https://github.com/uggla/python-redfish

As python redefish is currently in heavy development we recommend to checkout the devel branch using::

    cd python-redfish
    git checkout devel

Installation
------------

Please refer to the following link.

http://pythonhosted.org/python-redfish/installation.html

Contacts
--------

Distribution list: python-redfish@mondorescue.org

Further References
------------------

Please look at `dmtf/README.rst <further_ref.html>`_ file.
