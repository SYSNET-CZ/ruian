# from typing import List

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
import logging

import connexion.exceptions

from swagger_server.config import X_API_KEY


def check_apiKey(api_key, required_scopes):
    __name__ = check_apiKey.__name__
    if api_key is None:
        logging.error('{0}: missing api key'.format(__name__))
        raise connexion.exceptions.Unauthorized('missing api key')
    if api_key not in X_API_KEY.keys():
        logging.error('{0}: invalid api key'.format(__name__))
        raise connexion.exceptions.Unauthorized('invalid api key')
    description = X_API_KEY.get(api_key)
    out = {'x-api-key': api_key, 'description': description}
    logging.info('{}: x-api-key={}'.format(__name__, description))
    return out
