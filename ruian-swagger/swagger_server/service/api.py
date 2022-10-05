from settings import who_am_i, LOG
from swagger_server.models import NearbyAddress
from swagger_server.service.conversion import string_wgs_to_jtsk
from swagger_server.service.geolocation_reverse import get_ku, get_maplist, get_nearby, get_parcela, get_zsj, get_povodi
from swagger_server.service.models import CoordinatesInternal
from swagger_server.service.querying import compile_address


def compile_adr(adr):
    __name__ = who_am_i()
    out = None
    if adr is not None:
        work = compile_address(
            text_format='obj',
            zip_code=adr.zip_code,
            locality=adr.locality,
            locality_part=adr.locality_part,
            house_number=adr.house_number,
            record_number=adr.record_number,
            district_number=adr.district_number,
            district_name=adr.district_number,
            orientation_number=adr.orientation_number,
            orientation_number_character=adr.orientation_number_character,
            street=adr.street,
            do_validate=True,
            with_ruian_id=True
        )
        out = work
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Input address is missing'))
    return out


def convert_point_jtsk(lat, lon):
    __name__ = who_am_i()
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = CoordinatesInternal(x=jtsk.x, y=jtsk.y)
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def ku(x, y):
    __name__ = who_am_i()
    out = None
    if x is not None and y is not None:
        out = get_ku(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
        else:
            LOG.logger.error('{}: {} x={}, y={}'.format(__name__, 'No data found for: ', x, y))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def ku_wgs(lat, lon):
    __name__ = who_am_i()
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        out = ku(x=jtsk.x, y=jtsk.y)
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def mapy50(x, y):
    __name__ = who_am_i()
    out = None
    if x is not None and y is not None:
        out = get_maplist(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def mapy50_wgs(lat, lon):
    __name__ = who_am_i()
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        out = mapy50(x=jtsk.x, y=jtsk.y)
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def nearby_address(x, y):
    __name__ = who_am_i()
    out_list = None
    if x is not None and y is not None:
        work_list = get_nearby(y=y, x=x)
        if work_list is None:
            return None
        out_list = []
        for work in work_list:
            out = NearbyAddress(
                order=work['order'], distance=work['distance'], address=work['address'].to_swagger
            )
            out_list.append(out)
        LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out_list


def nearby_address_wgs(lat, lon):
    __name__ = who_am_i()
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        out = nearby_address(x=jtsk.x, y=jtsk.y)
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def parcela(x, y):
    __name__ = who_am_i()
    out = None
    if x is not None and y is not None:
        out = get_parcela(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def parcela_wgs(lat, lon):
    __name__ = who_am_i()
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        out = parcela(x=jtsk.x, y=jtsk.y)
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def _to_jtsk(lat, lon):
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            return jtsk
    return None


def zsj(x, y):
    __name__ = who_am_i()
    out = None
    if x is not None and y is not None:
        out = get_zsj(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def zsj_wgs(lat, lon):
    __name__ = who_am_i()
    out = None
    jtsk = _to_jtsk(lat=lat, lon=lon)
    if jtsk is not None:
        out = zsj(x=jtsk.x, y=jtsk.y)
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def povodi(x, y):
    __name__ = who_am_i()
    out = None
    if x is not None and y is not None:
        out = get_povodi(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def povodi_wgs(lat, lon):
    __name__ = who_am_i()
    out = None
    jtsk = _to_jtsk(lat=lat, lon=lon)
    if jtsk is not None:
        out = povodi(x=jtsk.x, y=jtsk.y)
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


COUNTER = {
    'info_api': 0,
    'compile_address_api': 0,
    'compile_address_ft_api': 0,
    'compile_address_id_api': 0,
    'convert_point_jtsk_api': 0,
    'convert_point_jtsk_post_api': 0,
    'convert_point_wgs_api': 0,
    'convert_point_wgs_post_api': 0,
    'convert_polygon_jtsk_api': 0,
    'convert_polygon_wgs_api': 0,
    'get_address_id_api': 0,
    'get_ku_id_api': 0,
    'get_zsj_id_api': 0,
    'ku_api': 0,
    'ku_post_api': 0,
    'ku_wgs_api': 0,
    'ku_wgs_post_api': 0,
    'mapy50_api': 0,
    'mapy50_post_api': 0,
    'mapy50_wgs_api': 0,
    'mapy50_wgs_post_api': 0,
    'nearby_address_api': 0,
    'nearby_address_post_api': 0,
    'nearby_address_wgs_api': 0,
    'nearby_address_wgs_post_api': 0,
    'parcela_api': 0,
    'parcela_post_api': 0,
    'parcela_wgs_api': 0,
    'parcela_wgs_post_api': 0,
    'povodi_api': 0,
    'povodi_post_api': 0,
    'povodi_wgs_api': 0,
    'povodi_wgs_post_api': 0,
    'search_address_api': 0,
    'search_address_ft_api': 0,
    'search_address_id_api': 0,
    'validate_address_id_api': 0,
    'zsj_api': 0,
    'zsj_post_api': 0,
    'zsj_wgs_api': 0,
    'zsj_wgs_post_api': 0
}
