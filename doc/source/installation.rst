============
Installation
============

Using pip
---------
Use::

    sudo pip install python-redfish

Pip will install :

1. The library and all dependencies into prefix/lib/pythonX.Y/site-packages directory
2. Redfish client master conf file into prefix/etc/redfish_client.conf
   Unless if prefix = '/usr', in that case force configuration file to be in /etc

3. Data file (templates) into prefix/share/redfish-client/templates

Point 2 and 3 above need root access to your system. If you don't have root
access on your system, please follow `Using pip and virtualenv`_ section.


Using pip and virtualenv
------------------------

1. Install virtualenv and virtualenvwrapper:

 Fedora 22::

    dnf install python-virtualenv python-virtualenvwrapper

 Ubuntu 15.04::

    apt-get install python-virtualenv virtualenvwrapper

2. Source virtualenvwrapper.sh::

    . /usr/bin/virtualenvwrapper.sh

 or::

    . /usr/share/virtualenvwrapper/virtualenvwrapper.sh

3. Create a redfish virtual environement::

    mkvirtualenv redfish

4. Install using pip::

    pip install python-virtualenv

 All files are installed under your virtualenv.

Using the sources
-----------------

#. Follow `get the sources <http://pythonhosted.org/python-redfish/readme.html#get-the-sources>`_ section to retrieve the sources.
#. Install from the source using::

    python setup.py install --prefix="/usr/local"


Using rpm package
-----------------

There is currently no oficial packages for distributions.
However part of the sources there is a mechanism to buil rpm or deb packages for distributions.

The mechanism is based on `project builder <http://www.project-builder.org/>`_ tool.

#. Follow `get the sources <http://pythonhosted.org/python-redfish/readme.html#get-the-sources>`_ section to retrieve the sources.
#. Download project builder for your distribution from ftp://ftp.project-builder.org.
#. Clone the project to your own github account.
#. Create a .pbrc with the following content, replace "/wokspace/python/redfish" and "uggla" with your own directory and account::

    [uggla@ugglalaptop ~]$ cat .pbrc
    pbdefdir python-redfish = $ENV{'HOME'}/workspace
    pbconfdir python-redfish = $ENV{'HOME'}/workspace/python-redfish/pbconf
    pbconfurl python-redfish = git+ssh://git@github.com:uggla/python-redfish.git
    pburl python-redfish = git+ssh://git@github.com:uggla/python-redfish.git
#. Build the project::

    pb -p python-redfish sbx2pkg

 or::

    pb -p python-redfish sbx2pkg2ins

#. All packages (srpm/rpm) should be available into the build directory, then install the package using rpm::

    rpm -Uvh python-redfish/build/RPMS/python-redfish-devel20160213182552.rpm


#. Follow `get the sources <http://pythonhosted.org/python-redfish/readme.html#get-the-sources>`_ section to retrieve the sources.

Using deb package
-----------------

This installation in not yet possible due to missing deb package dependencies. We are working on it.

In the meantime we recommend to use `Using pip`_ or `Using pip and virtualenv`_.

=====================================
Host configuration file configuration
=====================================

#. Verify redfish-client is working correclty::

    redfish-client -h

#. Create a default entry to use the mockup::

    redfish-client config add default default http://localhost:8000/redfish/v1

#. Verify the entry is correctly registered::

    redfish-client config showall

===================
Mockup installation
===================

#. Follow `get the sources <http://pythonhosted.org/python-redfish/readme.html#get-the-sources>`_ section to retrieve the sources.
#. Install docker using your distribution packages or the docker `procedure <https://docs.docker.com/engine/installation/>`_ (docker provide more recent packages for ubuntu)::

    dnf install docker
    systemctl enable docker.service
    systemctl start docker.service
    systemctl status docker.service

#. Jump into the dmtf directory.
#. Run ./buildImage.sh and ./run-redfish-simulator.sh
#. Check that a container is running and listening on port 8000::

    (pypi)[uggla@ugglalaptop dmtf]$ docker ps
    CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                  NAMES
    9943ff1d4d93        redfish-simulator:latest   "/bin/sh -c /tmp/redf"   3 weeks ago         Up 2 days           0.0.0.0:8000->80/tcp   redfish-simulator
#. Try to connect using a navigator to http://localhost:8000 the following screen should apear.

   .. image:: images/simulator.jpg

Note : in the above screenshot, firefox JSON-handle extension is used. If you want the same presentation install the extension and refresh the page.

==========================
Testing against the mockup
==========================

#. Follow `Host configuration file configuration`_ and `Mockup installation`_ section.
#. Run the following command::

    redfish-client manager getinfo

The result should be like this::

    (pypi)[uggla@ugglalaptop dmtf]$ redfish-client manager getinfo
    Gathering data from manager, please wait...

    Redfish API version :  1.00
    Root Service

    Managers information :
    ======================

    Manager id 1:
    UUID : 00000000-0000-0000-0000-000000000000
    Type : BMC
    Firmware version : 1.00
    State : Enabled
    Ethernet Interface :
        This manager has no ethernet interface
    Managed Chassis :
        1
    Managed System :
        1
    ----------------------------

    Manager id 2:
    UUID : 00000000-0000-0000-0000-000000000000
    Type : EnclosureManager
    Firmware version : Not available
    State : Enabled
    Ethernet Interface :
        This manager has no ethernet interface
    Managed Chassis :
        Enc1
    Managed System :
        2
    ----------------------------

    Manager id 3:
    UUID : 00000000-0000-0000-0000-000000000000
    Type : EnclosureManager
    Firmware version : Not available
    State : Enabled
    Ethernet Interface :
        This manager has no ethernet interface
    Managed Chassis :
        Enc1
    Managed System :
        2
    ----------------------------



============================
Building local documentation
============================

Building the html documentation locally


#. Follow `get the sources <http://pythonhosted.org/python-redfish/readme.html#get-the-sources>`_ section to retrieve the sources.
#. Jump in the doc directory::

    cd doc
#. Build the html documentation::

    make html


If you want to build the documentation in pdf.

#. Get texlive full distribution, ex on Fedora::

    dnf install texlive-scheme-full
#. Build the documentation::

    make latexpdf

