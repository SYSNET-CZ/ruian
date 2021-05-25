import connexion

from app import app, COUNTER
from swagger_server.models import NearbyAddress
from swagger_server.models.address import Address  # noqa: E501
from swagger_server.models.jtsk import Jtsk  # noqa: E501
from swagger_server.models.katastralni_uzemi import KatastralniUzemi  # noqa: E501
from swagger_server.models.mapovy_list50 import MapovyList50  # noqa: E501
# from swagger_server.models.nearby_address import NearbyAddress  # noqa: E501
from swagger_server.models.parcela import Parcela  # noqa: E501
from swagger_server.models.point_jtsk import PointJtsk  # noqa: E501
from swagger_server.models.point_wgs import PointWgs  # noqa: E501
from swagger_server.models.povodi import Povodi  # noqa: E501
from swagger_server.models.wgs import Wgs  # noqa: E501
from swagger_server.models.zsj import Zsj  # noqa: E501
from swagger_server.service import querying
from swagger_server.service.common import compile_address_as_obj
from swagger_server.service.conversion import string_wgs_to_jtsk, point2wgs
from swagger_server.service.geolocation_reverse import get_ku, get_maplist, get_parcela, get_povodi, get_zsj, get_nearby
from swagger_server.service.models import CoordinatesInternal
from swagger_server.service.querying import full_text_search_address_object, compile_address, search_address
from swagger_server.service.ruian_connection import find_address
from swagger_server.util import who_am_i


def _compile_adr(adr):
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
        app.app.logger.error('{}: {}'.format(__name__, 'Input address is missing'))
    return out


def compile_address_api(body=None):  # noqa: E501
    """compile adresses by query

    By passing in the appropriate options, you can obtain formatted addreses  # noqa: E501

    :param body: query by form
    :type body: dict | bytes

    :rtype: List[str]
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        app.app.logger.error('compile_address_api: {}'.format('Missing input data'))
    out = _compile_adr(body)
    if out is not None:
        app.app.logger.info('compile_address_api: {}'.format('Address compiled'))
    else:
        app.app.logger.warning('compile_address_api: {}'.format('Address cannot be compiled'))
    return out


def compile_address_ft_api(query):  # noqa: E501
    """compile adresses by query

    By passing in the appropriate options, you can obtain formatted addreses  # noqa: E501

    :param query: Search query
    :type query: str

    :rtype: List[str]
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    if query is None:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input query'))
        return None
    adr_list = full_text_search_address_object(query)
    if adr_list is None:
        app.app.logger.info('{}: {}'.format(__name__, 'Nothing found'))
        return None
    out_list = []
    for adr in adr_list:
        out = compile_address_as_obj(
            street=adr.street,
            orientation_number_character=adr.orientation_number_character,
            orientation_number=adr.orientation_number,
            house_number=adr.house_number,
            record_number=adr.record_number,
            district_number=adr.district_number,
            locality=adr.locality,
            locality_part=adr.locality_part,
            zip_code=adr.zip_code,
            ruian_id=adr.ruian_id
        )
        out_list.append(out)
    app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    return out_list


def compile_address_id_api(id_):  # noqa: E501
    """compile adresses by identifier

    By passing in the appropriate options, you can obtain formatted addres  # noqa: E501

    :param id_: Address point identifier
    :type id_: int

    :rtype: str
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    if id_ is not None:
        app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
        return querying.compile_address_id(id_)
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing identifier'))
    return None


def convert_point_jtsk_api(lat, lon):  # noqa: E501
    """converts one point from WGS-84 to JTSK

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: PointJtsk
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = CoordinatesInternal(x=jtsk.x, y=jtsk.y)
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def convert_point_wgs_api(x, y):  # noqa: E501
    """converts one point from JTSK to WGS-84

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: PointWgs
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if x is not None and y is not None:
        out = point2wgs(y=y, x=x)
        app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def ku_api(x, y):  # noqa: E501
    """find cadastral territory by coordinates

    By passing in the appropriate options, you can search for the cadastral territory  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: KatastralniUzemi
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if x is not None and y is not None:
        out = get_ku(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
        else:
            app.app.logger.error('{}: {} x={}, y={}'.format(__name__, 'No data found for: ', x, y))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def ku_wgs_api(lat, lon):  # noqa: E501
    """find cadastral territory by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: KatastralniUzemi
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = get_ku(y=jtsk.y, x=jtsk.x)
            if out is not None:
                out = out.to_swagger
                app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def mapy50_api(x, y):  # noqa: E501
    """find map sheets layout by coordinates

    By passing in the appropriate options, you can search for the map sheets layout  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: MapovyList50
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if x is not None and y is not None:
        out = get_maplist(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def mapy50_wgs_api(lat, lon):  # noqa: E501
    """find map sheets layout by coordinates

    By passing in the appropriate options, you can search for the map sheets layout  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: MapovyList50
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = get_maplist(y=jtsk.y, x=jtsk.x)
            if out is not None:
                out = out.to_swagger
                app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def nearby_address_api(x, y):  # noqa: E501
    """find nearby adresses by coordinates

    By passing in the appropriate options, you can search for the nearby adresses  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: List[NearbyAddress]
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
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
        app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out_list


def nearby_address_wgs_api(lat, lon):  # noqa: E501
    """find nearby adresses by coordinates

    By passing in the appropriate options, you can search for the nearby adresses  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: List[NearbyAddress]
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = nearby_address_api(y=jtsk.y, x=jtsk.x)
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def parcela_api(x, y):  # noqa: E501
    """find plot (of land) by coordinates

    By passing in the appropriate options, you can search for the plot of land  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: Parcela
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if x is not None and y is not None:
        out = get_parcela(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def parcela_post_api(body=None):  # noqa: E501
    """find plot (of land) by coordinates

    By passing in the appropriate options, you can search for the plot of land  # noqa: E501

    :param body: JTSK coordinates
    :type body: dict | bytes

    :rtype: Parcela
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if connexion.request.is_json:
        body = Jtsk.from_dict(connexion.request.get_json())  # noqa: E501
        if body.x is not None and body.y is not None:
            out = get_parcela(y=body.y, x=body.x)
            if out is not None:
                out = out.to_swagger
                app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def parcela_wgs_api(lat, lon):  # noqa: E501
    """find plot (of land) by coordinates

    By passing in the appropriate options, you can search for the plot of land  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: Parcela
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = get_parcela(y=jtsk.y, x=jtsk.x)
            if out is not None:
                out = out.to_swagger
                app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def parcela_wgs_post_api(body=None):  # noqa: E501
    """find plot (of land) by coordinates

    By passing in the appropriate options, you can search for the plot of land  # noqa: E501

    :param body: WGS coordinates
    :type body: dict | bytes

    :rtype: Parcela
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if connexion.request.is_json:
        body = Wgs.from_dict(connexion.request.get_json())  # noqa: E501
        if (body.lat is not None) and (body.lon is not None):
            s = body.lat + ', ' + body.lon
            jtsk = string_wgs_to_jtsk(s)
            if jtsk is not None:
                out = get_parcela(y=jtsk.y, x=jtsk.x)
                if out is not None:
                    out = out.to_swagger
                    app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
        else:
            app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input data'))
    return out


def povodi_api(x, y):  # noqa: E501
    """find basin info by coordinates

    By passing in the appropriate options, you can search for the basin info  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: Povodi
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if x is not None and y is not None:
        out = get_povodi(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def povodi_wgs_api(lat, lon):  # noqa: E501
    """find basin info by coordinates

    By passing in the appropriate options, you can search for the basin info  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: Povodi
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = get_povodi(y=jtsk.y, x=jtsk.x)
            if out is not None:
                out = out.to_swagger
                app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def search_address_api(body=None):  # noqa: E501
    """search adresses by query

    By passing in the appropriate options, you can obtain search results  # noqa: E501

    :param body: query by form
    :type body: dict | bytes

    :rtype: List[Address]
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out_list = None
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
        if body is None:
            app.app.logger.error('{}: {}'.format(__name__, 'Missing input JSON data'))
            return None
        work_list = search_address(
            street=body.street, locality_part=body.locality_part, locality=body.locality, zip_code=body.zip_code,
            orientation_number_character=body.orientation_number_character, house_number=body.house_number,
            record_number=body.record_number, district_number=body.district_number,
            orientation_number=body.orientation_number, district_name=body.district
        )
        if work_list is not None:
            out_list = []
            for work in work_list:
                out_list.append(work.to_swagger)
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input data'))
    return out_list


def search_address_ft_api(query):  # noqa: E501
    """search adresses by query

    By passing in the appropriate options, you can obtain search results  # noqa: E501

    :param query: Search query
    :type query: str

    :rtype: List[Address]
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    if query is None:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input query'))
        return None
    adr_list = full_text_search_address_object(query)
    if adr_list is None:
        return None
    out_list = []
    for adr in adr_list:
        out_list.append(adr.to_swagger)
    app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    return out_list


def search_address_id_api(id_):  # noqa: E501
    """seach address by identifier

    By passing in the appropriate options, you can obtain addres point  # noqa: E501

    :param id_: Address point identifier
    :type id_: int

    :rtype: Address
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    if id_ is not None:
        adr = find_address(id_)
        if adr is not None:
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
            return adr.to_swagger
        else:
            app.app.logger.error('{}: Address point {} not found'.format(__name__, id_))
            return None
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing identifier'))
    return None


def validate_address_id_api(id_):  # noqa: E501
    """compile adresses by identifier

    By passing in the appropriate options, you can validate address point  # noqa: E501

    :param id_: Address point identifier
    :type id_: int

    :rtype: bool
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    if id_ is not None:
        out = find_address(identifier=id_)
        if out is not None:
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
            return True
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing identifier'))
    return False


def zsj_api(x, y):  # noqa: E501
    """find basic settlement unit by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: Zsj
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if x is not None and y is not None:
        out = get_zsj(y=y, x=x)
        if out is not None:
            out = out.to_swagger
            app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out


def zsj_wgs_api(lat, lon):  # noqa: E501
    """find basic settlement unit by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: Zsj
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if (lat is not None) and (lon is not None):
        s = lat + ', ' + lon
        jtsk = string_wgs_to_jtsk(s)
        if jtsk is not None:
            out = get_zsj(y=jtsk.y, x=jtsk.x)
            if out is not None:
                out = out.to_swagger
                app.app.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        app.app.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    return out
