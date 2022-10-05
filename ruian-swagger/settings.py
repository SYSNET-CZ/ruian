import logging
import os
import sys
import traceback

DEBUG = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')
TZ = os.getenv('TZ', 'Europe/Prague')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s in %(module)s: %(message)s')
LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%d.%m.%Y %H:%M:%S')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
LOG_DIR = os.getenv('LOG_DIR', os.path.join(ROOT_DIR, 'logs'))
CONFIG_DIR = os.getenv('CONFIG_DIRECTORY', os.path.join(ROOT_DIR, 'conf'))
CONFIG_FILE_NAME = os.getenv('CONFIG_FILE_NAME', 'ruian.yml')
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE_NAME)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Log(object, metaclass=Singleton):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler(sys.stdout)
        if DEBUG:
            self.logger.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
            handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        handler.setFormatter(formatter)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(handler)
        self.logger.propagate = False
        self.logger.info('LOG created')


def set_ext_logger(ext_logger):
    if ext_logger is not None:
        LOG.logger = ext_logger


def who_am_i():
    stack = traceback.extract_stack()
    file_name, code_line, func_name, text = stack[-2]
    return func_name


LOG = Log()

