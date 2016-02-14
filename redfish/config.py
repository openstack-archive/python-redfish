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
REDFISH_LOGFILE = "/var/log/python-redfish/python-redfish.log"
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
    try:
        file_handler = RotatingFileHandler(REDFISH_LOGFILE, 'a', 1000000, 1)
    except IOError:
        print('ERROR: {} does not exist or is not writeable.\n'.format(REDFISH_LOGFILE))
        print('1- Try to create directory {}'.format(os.path.dirname(REDFISH_LOGFILE)))
        print('   using: sudo mkdir -p {}'.format(os.path.dirname(REDFISH_LOGFILE)))
        print('2- Try to get the {} ownership'.format(os.path.dirname(REDFISH_LOGFILE)))
        print('   using: sudo chown {} {}'.format(getpass.getuser(), os.path.dirname(REDFISH_LOGFILE)))
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
