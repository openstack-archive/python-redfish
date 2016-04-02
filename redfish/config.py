# coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import logging
import sys
import os
import getpass
from logging.handlers import RotatingFileHandler

# Global variable definition

logger = None
TORTILLADEBUG = True
HOME = os.getenv('HOME')
if HOME == '':
    print("$HOME environment variable not set, please check your system")
    sys.exit(1)

REDFISH_HOME = HOME + "/.redfish"
if not os.path.exists(REDFISH_HOME):
    try:
        os.mkdir(REDFISH_HOME)
    except IOError:
        print('ERROR: can\'t create {}.\n'.format(REDFISH_HOME))
        print('       Try to create directory {}'.format(os.path.dirname(REDFISH_LOGFILE)))
        print('       using: mkdir -p {}'.format(os.path.dirname(REDFISH_LOGFILE)))
        sys.exit(1)

REDFISH_LOGFILE = REDFISH_HOME + "/python-redfish.log"
CONSOLE_LOGGER_LEVEL = logging.DEBUG
FILE_LOGGER_LEVEL = logging.DEBUG


def initialize_logger(REDFISH_LOGFILE,
                      CONSOLE_LOGGER_LEVEL,
                      FILE_LOGGER_LEVEL,
                      logger_name=None):
    '''Initialize a global logger to track application behaviour

    :param redfish_logfile: Log filename
    :type redfish_logfile: str
    :param screen_logger_level: Console log level
                                (logging.DEBUG, logging.ERROR, ..) or nolog
    :type screen_logger_level: logging constant or string
    :param file_logger_level: File log level
    :type file_logger_level: logging constant
    :returns:  logging object

    '''

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(message)s'
        )
    f = open(os.path.expandvars(REDFISH_LOGFILE), 'w')
    f.close()

    try:
        file_handler = RotatingFileHandler(os.path.expandvars(REDFISH_LOGFILE), 'a', 1000000, 1)
    except IOError:
        print('ERROR: {} does not exist or is not writeable.\n'.format(REDFISH_LOGFILE))
        sys.exit(1)

    # First logger to file
    file_handler.setLevel(FILE_LOGGER_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Second logger to console
    if CONSOLE_LOGGER_LEVEL != "nolog":
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(CONSOLE_LOGGER_LEVEL)
        logger.addHandler(steam_handler)
    return logger
