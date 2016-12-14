# coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from builtins import object
import os
import stat
import subprocess
import re
from docker import Client
from path import Path
standard_library.install_aliases()


class DockerTest(object):
    def __init__(self):
        self.cli = Client(base_url='unix://var/run/docker.sock')

    def build(self, dockerfile):
        dockerfile = Path(dockerfile)
        tag = 'rf' + dockerfile.basename().replace('Dockerfile.', '')
        dockerfile.copy('redfish-client/tests/Dockerfile')
        response = [line for line in self.cli.build(
            path='redfish-client/tests',
            tag=tag,
            rm=True)]
        return(response)

    def run(self, image, command):
        container = self.cli.create_container(image=image,
                                              command=command,
                                              tty=True,
                                              stdin_open=True)
        self.cli.start(container=container.get('Id'))
        self.cli.wait(container=container.get('Id'))
        response = self.cli.logs(container=container.get('Id'),
                                 stdout=True)
        self.cli.remove_container(container=container.get('Id'))
        return(response.decode('utf8'))


def test_dockersocket():
    mode = os.stat('/var/run/docker.sock').st_mode
    isSocket = stat.S_ISSOCK(mode)
    assert isSocket, 'Make sure docker services are running'


def test_docker():
    cli = Client(base_url='unix://var/run/docker.sock')
    response = cli.containers()
    assert isinstance(response, list), 'Ensure you have sufficiant' + \
                                       'credentials to use docker with' + \
                                       'your current user'


def test_sources():
    output = subprocess.check_output(["python", "setup.py", "sdist"])
    search = re.search(r"removing '(\S+)'", str(output))
    filename = Path('dist/' + search.group(1) + '.tar.gz')
    filename.copy('redfish-client/tests/python-redfish.src.tar.gz')
    assert Path('redfish-client/tests/python-redfish.src.tar.gz').isfile()


def test_dockerbuild():
    docker = DockerTest()
    # Warning :  Image tag is derived from file name, do not use uppercase !!!
    dockerfiles = ('redfish-client/tests/Dockerfile.ubuntu',
                   'redfish-client/tests/Dockerfile.debian',
                   'redfish-client/tests/Dockerfile.centos',
                   'redfish-client/tests/Dockerfile.fedora',
                   'redfish-client/tests/Dockerfile.fedorap3',
                   'redfish-client/tests/Dockerfile.fedorapip')
    for dockerfile in dockerfiles:
        print('Testing : {}'.format(dockerfile))
        response = docker.build(dockerfile)
        status = str(response.pop())
        assert 'Successfully built' in status


def test_install():
    docker = DockerTest()
    images = ('rfubuntu', 'rfdebian', 'rfcentos',
              'rffedora', 'rffedorap3', 'rffedorapip')
    for img in images:
        print('Testing : {}'.format(img))
        response = docker.run(img, 'redfish-client config showall')
        print(response)
        assert ('Managers configured' in response and 'None' in response)


def test_versionformat():
    docker = DockerTest()
    images = ('rfubuntu', 'rfdebian', 'rfcentos',
              'rffedora', 'rffedorap3', 'rffedorapip')
    for img in images:
        print('Testing : {}'.format(img))
        response = docker.run(img, 'redfish-client --version')
        print(response)
        assert (re.match(r'redfish-client \d+\.\d+', response))
