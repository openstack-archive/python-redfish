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
from logging.handlers import RotatingFileHandler
import redfish


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

    def initialize_logger(redfish_logfile, logger_level):
        '''Initialize a global loggeer to track application behaviour

        :param redfish_logfile: log file name
        :type str
        :param logger_level: log level (logging.DEBUG, logging.ERROR, ...)
        :type logging constant
        :returns:  True

        '''
        global logger
        logger = logging.getLogger()

        logger.setLevel(logger_level)
        formatter = logging.Formatter(
            '%(asctime)s :: %(levelname)s :: %(message)s'
            )
        file_handler = RotatingFileHandler(redfish_logfile, 'a', 1000000, 1)

        # First logger to file
        file_handler.setLevel(logger_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Second logger to console
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logger_level)
        logger.addHandler(steam_handler)
        return True

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
        remote_mgmt = redfish.connect(connection_parameters['url'],
                                      connection_parameters['login'],
                                      connection_parameters['password'],
                                      verify_cert=check_SSL
                                      )

        print ('Redfish API version : %s \n' % remote_mgmt.get_api_version())

    # Initialize logger
    logger = None
    initialize_logger('redfish-client.log', logging.DEBUG)

    # Get $HOME environment.
    HOME = os.getenv('HOME')

    if HOME == '':
        print('$HOME environment variable not set, please check your system')
        sys.exit(1)

    # Parse and manage arguments
    arguments = docopt.docopt(__doc__, version='redfish-client 0.1')
    logger.debug(arguments)

    arguments['--conf_file'] = arguments['--conf_file'].replace('~', HOME)

    conf_file = ConfigFile(arguments['--conf_file'])

    if arguments['config'] is True:
        if arguments['show'] is True:
            show_manager()
        elif arguments['showall'] is True:
            show_manager(True)
        elif arguments['add'] is True:
            conf_file.add_manager(arguments['<manager_name>'],
                                  arguments['<manager_url>'],
                                  arguments['<login>'],
                                  arguments['password'])
            logger.debug(pprint.pprint(conf_file.data))
            conf_file.save()
        elif arguments['del'] is True:
            conf_file.delete_manager(arguments['<manager_name>'])
            logger.debug(pprint.pprint(conf_file.data))
            conf_file.save()
        elif arguments['modify'] is True:
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
        if arguments['getinfo'] is True:
            # If manager is not defined set it to 'default'
            if not arguments['<manager_name>']:
                manager_name = 'default'
                # Check if the default section is available in our conf file
                conf_file.check_manager(manager_name)
            if arguments['--insecure'] is True:
                get_manager_info(manager_name, False)
            else:
                get_manager_info(manager_name, True)

    sys.exit(0)
