import connexion

from settings import LOG, who_am_i
from swagger_server.models import PolygonWgs, PolygonJtsk
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
from swagger_server.service.api import compile_adr, convert_point_jtsk, ku, ku_wgs, mapy50, mapy50_wgs, nearby_address, \
    nearby_address_wgs, parcela, parcela_wgs, zsj, zsj_wgs, povodi, povodi_wgs, COUNTER
from swagger_server.service.common import compile_address_as_obj
from swagger_server.service.conversion import point2wgs, polygon2wgs, polygon2jtsk, get_full_address, get_full_cadaster, \
    get_full_settlement
from swagger_server.service.querying import full_text_search_address_object, search_address
from swagger_server.service.ruian_connection import find_address


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
        LOG.logger.error('compile_address_api: {}'.format('Missing input data'))
    out = compile_adr(body)
    if out is not None:
        LOG.logger.info('compile_address_api: {}'.format('Address compiled'))
    else:
        LOG.logger.warning('compile_address_api: {}'.format('Address cannot be compiled'))
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
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input query'))
        return None
    adr_list = full_text_search_address_object(query)
    if adr_list is None:
        LOG.logger.info('{}: {}'.format(__name__, 'Nothing found'))
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
    LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
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
        LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
        return querying.compile_address_id(id_)
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing identifier'))
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
    return convert_point_jtsk(lat=lat, lon=lon)


def convert_point_jtsk_post_api(body=None):  # noqa: E501
    """converts one point from WGS-84 to JTSK

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: PointJtsk
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
        out = convert_point_jtsk(lat=str(body.lat), lon=str(body.lon))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input data'))
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
        LOG.logger.info('{0}: {1}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input coordinates'))
    return out


def convert_point_wgs_post_api(body=None):  # noqa: E501
    """converts one point from JTSK to WGS-84

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: PointWgs
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
        if (body.x is not None) and (body.y is not None):
            out = point2wgs(y=str(body.y), x=str(body.x))
            LOG.logger.info('{0}: {1}'.format(__name__, 'Result returned'))
        else:
            LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
    return out


def convert_polygon_jtsk_api(body=None):  # noqa: E501
    """converts polygon from WGS84 to JTSK

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: PolygonJtsk
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PolygonWgs.from_dict(connexion.request.get_json())  # noqa: E501
        if body.polygon is not None:
            out = polygon2jtsk(body.polygon)
            LOG.logger.info('{0}: {1}'.format(__name__, 'Result returned'))
        else:
            LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input polygon'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
    return out


def convert_polygon_wgs_api(body=None):  # noqa: E501
    """converts polygon from JTSK to WGS84

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: PolygonWgs
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PolygonJtsk.from_dict(connexion.request.get_json())  # noqa: E501
        if body.polygon is not None:
            out = polygon2wgs(body.polygon)
            LOG.logger.info('{0}: {1}'.format(__name__, 'Result returned'))
        else:
            LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input polygon'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
    return out


def get_address_id_api(id_):  # noqa: E501
    """get addres point full info by identifier

    By passing in the appropriate options, you can obtain addres point  # noqa: E501

    :param id_: Address point identifier
    :type id_: int

    :rtype: FullAddress
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    print('{0} - ID: {1}'.format(__name__, str(id_)))
    out = None
    if id_ is not None:
        out = get_full_address(identifier=id_)
        LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
    return out


def get_ku_id_api(id_):  # noqa: E501
    """get cadastral territory full info by identifier

    By passing in the appropriate options, you can obtain cadastral territory  # noqa: E501

    :param id_: cadastral territory identifier
    :type id_: int

    :rtype: FullCadaster
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    print('{0} - ID: {1}'.format(__name__, str(id_)))
    out = None
    if id_ is not None:
        out = get_full_cadaster(identifier=id_)
        LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
    return out


def get_zsj_id_api(id_):  # noqa: E501
    """get basic settlement unit full info by identifier

    By passing in the appropriate options, you can obtain basic settlement unit  # noqa: E501

    :param id_: basic settlement unit identifier
    :type id_: int

    :rtype: FullSettlement
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    print('{0} - ID: {1}'.format(__name__, str(id_)))
    out = None
    if id_ is not None:
        out = get_full_settlement(identifier=id_)
        LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
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
    return ku(x=x, y=y)


def ku_post_api(body=None):  # noqa: E501
    """find cadastral territory by coordinates

    By passing in the appropriate options, you can search for the cadastral territory  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: KatastralniUzemi
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
        out = ku(x=body.x, y=body.y)
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
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
    return ku_wgs(lat=lat, lon=lon)


def ku_wgs_post_api(body=None):  # noqa: E501
    """find cadastral territory by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: KatastralniUzemi
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = ku_wgs(lat=str(body.lat), lon=str(body.lon))
        else:
            LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
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
    return mapy50(x=x, y=y)


def mapy50_post_api(body=None):  # noqa: E501
    """find map sheets layout by coordinates

    By passing in the appropriate options, you can search for the map sheets layout  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: MapovyList50
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = mapy50(x=body.x, y=body.y)
        else:
            LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
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
    return mapy50_wgs(lat=lat, lon=lon)


def mapy50_wgs_post_api(body=None):  # noqa: E501
    """find map sheets layout by coordinates

    By passing in the appropriate options, you can search for the map sheets layout  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: MapovyList50
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = mapy50_wgs(lat=str(body.lat), lon=str(body.lon))
        else:
            LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
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
    return nearby_address(x=x, y=y)


def nearby_address_post_api(body=None):  # noqa: E501
    """find nearby adresses by coordinates

    By passing in the appropriate options, you can search for the nearby adresses  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: List[NearbyAddress]
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = nearby_address(x=body.x, y=body.y)
        else:
            LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
    return out


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
    return nearby_address_wgs(lat=lat, lon=lon)


def nearby_address_wgs_post_api(body=None):  # noqa: E501
    """find nearby adresses by coordinates

    By passing in the appropriate options, you can search for the nearby adresses  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: List[NearbyAddress]
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = nearby_address_wgs(lat=str(body.lat), lon=str(body.lat))
        else:
            LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{0}: {1}'.format(__name__, 'Missing input data'))
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
    return parcela(x=x, y=y)


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
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = Jtsk.from_dict(connexion.request.get_json())  # noqa: E501
        out = parcela(x=body.x, y=body.y)
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
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
    return parcela_wgs(lat=lat, lon=lon)


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
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = Wgs.from_dict(connexion.request.get_json())  # noqa: E501
        if (body.lat is not None) and (body.lon is not None):
            out = parcela_wgs(lat=body.lat, lon=body.lon)
        else:
            LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input data'))
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
    return povodi(x=x, y=y)


def povodi_post_api(body=None):  # noqa: E501
    """find basin info by coordinates

    By passing in the appropriate options, you can search for the basin info  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: Povodi
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = povodi(x=body.x, y=body.y)
        else:
            LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input data'))
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
    return povodi_wgs(lat=lat, lon=lon)


def povodi_wgs_post_api(body=None):  # noqa: E501
    """find basin info by coordinates

    By passing in the appropriate options, you can search for the basin info  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: Povodi
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = povodi_wgs(lat=str(body.lat), lon=str(body.lat))
        else:
            LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input data'))
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
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
        if body is None:
            LOG.logger.error('{}: {}'.format(__name__, 'Missing input JSON data'))
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
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input data'))
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
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input query'))
        return None
    adr_list = full_text_search_address_object(query)
    if adr_list is None:
        return None
    out_list = []
    for adr in adr_list:
        out_list.append(adr.to_swagger)
    LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
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
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
            return adr.to_swagger
        else:
            LOG.logger.error('{}: Address point {} not found'.format(__name__, id_))
            return None
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing identifier'))
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
            LOG.logger.info('{}: {}'.format(__name__, 'Result returned'))
            return True
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing identifier'))
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
    return zsj(x=x, y=y)


def zsj_post_api(body=None):  # noqa: E501
    """find basic settlement unit by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: Zsj
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = zsj(x=body.x, y=body.y)
        else:
            LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input data'))
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
    return zsj_wgs(lat=lat, lon=lon)


def zsj_wgs_post_api(body=None):  # noqa: E501
    """find basic settlement unit by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: Zsj
    """
    __name__ = who_am_i()
    COUNTER[__name__] += 1
    out = None
    if body is not None:
        print('BODY: {0}'.format(str(body)))
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
        if body is not None:
            out = zsj_wgs(lat=str(body.lat), lon=str(body.lon))
        else:
            LOG.logger.error('{}: {}'.format(__name__, 'Missing input coordinates'))
    else:
        LOG.logger.error('{}: {}'.format(__name__, 'Missing input data'))
    return out
