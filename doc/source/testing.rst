=============
Running tests
=============


redfish module tests
--------------------

Tests are not functional for the redfish module yet.

refish-client tests
-------------------

#. Create your development environment following `Developer setup <develsetup.html>`_.
#. Install docker using the `procedure <https://docs.docker.com/engine/installation/>`_.
#. Ensure you can use docker with your current user.
#. Jump into redfish-python directory containing the sources.
#. Install required modules for testings::

    pip install -t test-requirements.txt

#. Run the test::

    py.test redfish-client

