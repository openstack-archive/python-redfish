# coding=utf-8
import os
import stat
import subprocess
import re
from docker import Client
from path import Path


class DockerTest():
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
        return(response)


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
    search = re.search(r"removing '(\S+)'", output)
    filename = Path('dist/' + search.group(1) + '.tar.gz')
    filename.copy('redfish-client/tests/python-redfish.src.tar.gz')
    assert Path('redfish-client/tests/python-redfish.src.tar.gz').isfile()


def test_dockerbuild():
    docker = DockerTest()
    dockerfiles = ('redfish-client/tests/Dockerfile.ubuntu',
                   'redfish-client/tests/Dockerfile.debian',
                   'redfish-client/tests/Dockerfile.fedora',
                   'redfish-client/tests/Dockerfile.fedorapip')
    for dockerfile in dockerfiles:
        print('Testing : {}'.format(dockerfile))
        response = docker.build(dockerfile)
        status = response.pop()
        assert 'Successfully built' in status


def test_install():
    docker = DockerTest()
    images = ('rfubuntu', 'rfdebian', 'rffedora', 'rffedorapip')
    for img in images:
        print('Testing : {}'.format(img))
        response = docker.run(img, 'redfish-client config showall')
        print(response)
        assert ('Managers configured' in response and 'None' in response)


def test_versionformat():
    docker = DockerTest()
    images = ('rfubuntu', 'rfdebian', 'rffedora', 'rffedorapip')
    for img in images:
        print('Testing : {}'.format(img))
        response = docker.run(img, 'redfish-client --version')
        print(response)
        assert (re.match('redfish-client \d+\.\d+', response))

