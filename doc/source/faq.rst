===
FAQ
===

- Q1 : error in setup command: Invalid environment marker: (python_version < '3')

    This error is caused by old setuptools revisions that do not understant "python_version < '3'".
    Upgrade setuptools using::

        pip install --upgrade setuptools

