#!/usr/bin/python

# coding=utf-8

'''
redfish-client

Usage:
  redfish-client.py [options] config add <manager_name> <manager_url> [<login>] [<password>]
  redfish-client.py [options] config del <manager_name>
  redfish-client.py [options] config modify <manager_name> (manager_name | url | login | password) <changed_value>
  redfish-client.py [options] config show
  redfish-client.py [options] config showall
  redfish-client.py [options] manager getinfo [<manager_name>]
  redfish-client.py (-h | --help)
  redfish-client.py --version


Options:
  -h --help     Show this screen.
  --version     Show version.
  --conf_file FILE      Configuration file [default: ~/.redfish.conf].
  --insecure    Check SSL certificats


config commands : manage the configuration file.
manager commands : manage the manager (Ligh out management). If <manager_name>
                   is not provided use the 'default' entry
'''

import os
import sys
import json
import pprint
import docopt
import logging
import redfish
import requests.packages.urllib3


class ConfigFile(object):
    '''redfisht-client configuration file management'''
    def __init__(self, config_file):
        '''Initialize the configuration file

        Open and load configuration file data.
        If the file does not exist create an empty one ready to receive data

        :param config_file: File name of the configuration file
                            default: ~/.redfish.conf
        :type str
        :returns: Nothing

        '''
        self._config_file = config_file
        # read json file
        try:
            with open(self._config_file) as json_data:
                self.data = json.load(json_data)
                json_data.close()
        except (ValueError, IOError):
            self.data = {'Managers': {}}

    def save(self):
        '''Save the configuration file data'''
        try:
            with open(self._config_file, 'w') as json_data:
                json.dump(self.data, json_data)
                json_data.close()
        except IOError as e:
            print(e.msg)
            sys.exit(1)

    def manager_incorect(self, exception):
        ''' Log and exit if manager name is incorect'''
        logger.error('Incorect manager name : %s' % exception.args)
        sys.exit(1)

    def check_manager(self, manager_name):
        '''Check if the manager exists in configuration file

        :param manager_name: Name of the manager
        :type str

        '''
        try:
            if manager_name not in self.get_managers():
                raise KeyError(manager_name)
        except KeyError as e:
            self.manager_incorect(e)

    def add_manager(self, manager_name, url, login, password):
        '''Add a manager to the configuration file

        :param manager_name: Name of the manager
        :type str
        :param url: Url of the manager
        :type str
        :param login: Login of the manager
        :type str
        :param password: Password of the manager
        :type str

        '''

        self.data['Managers'][manager_name] = {}
        self.data['Managers'][manager_name]['url'] = url
        if login is not None:
            self.data['Managers'][manager_name]['login'] = login
        if password is not None:
            self.data['Managers'][manager_name]['password'] = password

    def modify_manager(self, manager_name, parameter, parameter_value):
        '''Modify the manager settings

        :param manager name: Name of the manager
        :type str
        :param parameter: url | login | password
        :type str
        :param parameter_value: Value of the parameter
        :type str
        :returns: Nothing

        '''

        if parameter == 'url':
            try:
                self.data['Managers'][manager_name]['url'] = parameter_value
            except KeyError as e:
                self.manager_incorect(e)
        elif parameter == 'login':
            try:
                self.data['Managers'][manager_name]['login'] = parameter_value
            except KeyError as e:
                self.manager_incorect(e)
        elif parameter == 'password':
            try:
                self.data['Managers'][manager_name]['password'] = parameter_value
            except KeyError as e:
                self.manager_incorect(e)
        elif parameter == 'manager_name':
            # Create a new entry with the new name
            self.add_manager(parameter_value,
                             self.data['Managers'][manager_name]['url'],
                             self.data['Managers'][manager_name]['login'],
                             self.data['Managers'][manager_name]['password'],
                             )
            # Remove the previous one
            self.delete_manager(manager_name)

    def delete_manager(self, manager_name):
        '''Delete manager

        :param manager name: Name of the manager
        :type str
        :returns: Nothing

        '''

        try:
            del self.data['Managers'][manager_name]
        except KeyError as e:
            self.manager_incorect(e)

    def get_managers(self):
        '''Get manager configured

        :returns: Managers
        :type list

        '''
        managers = []
        for manager in self.data['Managers']:
            managers += [manager]
        return(managers)

    def get_manager_info(self, manager):
        '''Show manager info (url, login, password)

        :param manager: Name of the manager
        :type str
        :returns: info containing url, login, password
        :type dict

        '''
        info = {}
        url = self.data['Managers'][manager]['url']
        login = self.data['Managers'][manager]['login']
        password = self.data['Managers'][manager]['password']
        info = {'url': url, 'login': login, 'password': password}
        return(info)


class RedfishClientException(Exception):

    '''Base class for redfish client exceptions'''

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        self.message = message


if __name__ == '__main__':
    '''Main application redfish-client'''
    # Functions

    def show_manager(all=False):
        '''Display manager info

        :param all: Add login and password info
        :type bool
        :returns: Nothing

        '''
        print('Managers configured :')
        for manager in conf_file.get_managers():
            print(manager)
            if all is True:
                info = conf_file.get_manager_info(manager)
                print('\tUrl : {}'.format(info['url']))
                print('\tLogin : {}'.format(info['login']))
                print('\tPassword : {}'.format(info['password']))

    def get_manager_info(manager_name, check_SSL):
        connection_parameters = conf_file.get_manager_info(manager_name)
        if not connection_parameters['login']:
            simulator = True
            enforceSSL = False
        else:
            simulator = False
            enforceSSL = True
        remote_mgmt = redfish.connect(connection_parameters['url'],
                                      connection_parameters['login'],
                                      connection_parameters['password'],
                                      verify_cert=check_SSL,
                                      simulator=simulator,
                                      enforceSSL=enforceSSL
                                      )

        print ('Redfish API version : %s \n' % remote_mgmt.get_api_version())

    # Main program
    redfishclient_version = "redfish-client 0.1"

    # Parse and manage arguments
    arguments = docopt.docopt(__doc__, version=redfishclient_version)

    # Initialize logger
    logger = None
    logger = redfish.config.initialize_logger('redfish-client.log',
                                              "nolog",
                                              logging.DEBUG,
                                              __name__)
    redfish.config.TORTILLADEBUG = False
    redfish.config.CONSOLE_LOGGER_LEVEL = "nolog"
    # Avoid warning messages from request / urllib3
    # SecurityWarning: Certificate has no `subjectAltName`, falling back
    # to check for a `commonName` for now. This feature is being removed
    # by major browsers and deprecated by RFC 2818.
    # (See https://github.com/shazow/urllib3/issues/497 for details.)
    requests.packages.urllib3.disable_warnings()

    logger.info("*** Starting %s ***" % redfishclient_version)
    logger.info("Arguments parsed")
    logger.debug(arguments)

    # Get $HOME environment.
    HOME = os.getenv('HOME')

    if not HOME:
        print('$HOME environment variable not set, please check your system')
        logger.error('$HOME environment variable not set')
        sys.exit(1)
    logger.debug("Home directory : %s" % HOME)

    arguments['--conf_file'] = arguments['--conf_file'].replace('~', HOME)
    conf_file = ConfigFile(arguments['--conf_file'])

    if arguments['config'] is True:
        logger.debug("Config commands")
        if arguments['show'] is True:
            logger.debug('show command')
            show_manager()
        elif arguments['showall'] is True:
            logger.debug('showall command')
            show_manager(True)
        elif arguments['add'] is True:
            logger.debug('add command')
            conf_file.add_manager(arguments['<manager_name>'],
                                  arguments['<manager_url>'],
                                  arguments['<login>'],
                                  arguments['<password>'])
            logger.debug(pprint.pprint(conf_file.data))
            conf_file.save()
        elif arguments['del'] is True:
            logger.debug('del command')
            conf_file.delete_manager(arguments['<manager_name>'])
            logger.debug(pprint.pprint(conf_file.data))
            conf_file.save()
        elif arguments['modify'] is True:
            logger.debug('modify command')
            if arguments['url'] is not False:
                conf_file.modify_manager(arguments['<manager_name>'],
                                         'url',
                                         arguments['<changed_value>'])
            elif arguments['login'] is not False:
                conf_file.modify_manager(arguments['<manager_name>'],
                                         'login',
                                         arguments['<changed_value>'])
            elif arguments['password'] is not False:
                conf_file.modify_manager(arguments['<manager_name>'],
                                         'password',
                                         arguments['<changed_value>'])
            elif arguments['manager_name'] is not False:
                conf_file.modify_manager(arguments['<manager_name>'],
                                         'manager_name',
                                         arguments['<changed_value>'])
            logger.debug(pprint.pprint(conf_file.data))
            conf_file.save()
    if arguments['manager'] is True:
        logger.debug("Manager commands")
        if arguments['getinfo'] is True:
            logger.debug('getinfo command')
            # If manager is not defined set it to 'default'
            if not arguments['<manager_name>']:
                manager_name = 'default'
            else:
                manager_name = arguments['<manager_name>']
            # Check if the default section is available in our conf file
            conf_file.check_manager(manager_name)
            if arguments['--insecure'] is True:
                get_manager_info(manager_name, False)
            else:
                get_manager_info(manager_name, True)

    logger.info("Client session teminated")
    sys.exit(0)
