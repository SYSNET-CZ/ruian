# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        log
# Purpose:     This module creates standard logger for whole application.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------
import logging

from shared_tools import create_dir_for_file

logger = logging.getLogger(__name__)


def clear_log_file(log_file_name):
    """ This procedure creates empty log file with file name LOG_FILENAME """
    f = open(log_file_name, 'w')
    f.close()


def create_logger(log_file_name):
    global logger

    # create logger
    if logger is not None:
        if not logger.handlers:
            logger = None       # logger nebyl vytvořen pomocí této funkce

    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s %(message)s', datefmt="%H:%M:%S")

        # Create and setup console log parameters
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s %(message)s', "%H:%M:%S"))
        logger.addHandler(ch)

        # Create and setup log file parameters
        create_dir_for_file(log_file_name)
        file_handler = logging.FileHandler(log_file_name)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        print("\nLogger created")
    else:
        print("\nLogger already exists")


if __name__ == '__main__':
    logger.info("Logger test info")
    logger.debug("Logger test debug")
    logger.error("Logger test error")
    logger.critical("Logger test critical")
