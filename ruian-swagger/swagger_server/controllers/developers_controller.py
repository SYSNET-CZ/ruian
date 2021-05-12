from app import COUNTER, app
from swagger_server.service import database
from swagger_server.util import who_am_i


def info_api():  # noqa: E501
    """get service info

    Returns service info - status, technology versions, etc.  # noqa: E501


    :rtype: str
    """
    __name__ = who_am_i()
    COUNTER['info_api'] += 1
    postgis = database.get_row('ruian', "SELECT PostGIS_Full_Version();")
    ruian_version = database.get_ruian_version()
    out = {
        'status': 'OK',
        'ruian': ruian_version,
        'postgis': postgis[0].replace('"', ''),
        'counter': COUNTER
    }
    app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    return out
