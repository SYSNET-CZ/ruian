import connexion
import six

from swagger_server.models.address import Address  # noqa: E501
from swagger_server.models.full_address import FullAddress  # noqa: E501
from swagger_server.models.full_cadaster import FullCadaster  # noqa: E501
from swagger_server.models.full_settlement import FullSettlement  # noqa: E501
from swagger_server.models.jtsk import Jtsk  # noqa: E501
from swagger_server.models.katastralni_uzemi import KatastralniUzemi  # noqa: E501
from swagger_server.models.mapovy_list50 import MapovyList50  # noqa: E501
from swagger_server.models.nearby_address import NearbyAddress  # noqa: E501
from swagger_server.models.parcela import Parcela  # noqa: E501
from swagger_server.models.point_jtsk import PointJtsk  # noqa: E501
from swagger_server.models.point_wgs import PointWgs  # noqa: E501
from swagger_server.models.polygon_jtsk import PolygonJtsk  # noqa: E501
from swagger_server.models.polygon_wgs import PolygonWgs  # noqa: E501
from swagger_server.models.povodi import Povodi  # noqa: E501
from swagger_server.models.wgs import Wgs  # noqa: E501
from swagger_server.models.zsj import Zsj  # noqa: E501
from swagger_server import util


def compile_address_api(body=None):  # noqa: E501
    """compile adresses by query

    By passing in the appropriate options, you can obtain formatted addreses  # noqa: E501

    :param body: query by form
    :type body: dict | bytes

    :rtype: List[str]
    """
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def compile_address_ft_api(query):  # noqa: E501
    """compile adresses by query

    By passing in the appropriate options, you can obtain formatted addreses  # noqa: E501

    :param query: Search query
    :type query: str

    :rtype: List[str]
    """
    return 'do some magic!'


def compile_address_id_api(id):  # noqa: E501
    """compile adresses by identifier

    By passing in the appropriate options, you can obtain formatted addres  # noqa: E501

    :param id: Address point identifier
    :type id: int

    :rtype: str
    """
    return 'do some magic!'


def convert_point_jtsk_api(lat, lon):  # noqa: E501
    """converts one point from WGS-84 to JTSK

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: PointJtsk
    """
    return 'do some magic!'


def convert_point_jtsk_post_api(body=None):  # noqa: E501
    """converts one point from WGS-84 to JTSK

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: PointJtsk
    """
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def convert_point_wgs_api(x, y):  # noqa: E501
    """converts one point from JTSK to WGS-84

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: PointWgs
    """
    return 'do some magic!'


def convert_point_wgs_post_api(body=None):  # noqa: E501
    """converts one point from JTSK to WGS-84

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: PointWgs
    """
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def convert_polygon_jtsk_api(body=None):  # noqa: E501
    """converts polygon from WGS84 to JTSK

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: PolygonJtsk
    """
    if connexion.request.is_json:
        body = PolygonWgs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def convert_polygon_wgs_api(body=None):  # noqa: E501
    """converts polygon from JTSK to WGS84

    By passing in the appropriate options, you can obtain converted value  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: PolygonWgs
    """
    if connexion.request.is_json:
        body = PolygonJtsk.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_address_id_api(id):  # noqa: E501
    """get addres point full info by identifier

    By passing in the appropriate options, you can obtain addres point  # noqa: E501

    :param id: Address point identifier
    :type id: int

    :rtype: FullAddress
    """
    return 'do some magic!'


def get_ku_id_api(id):  # noqa: E501
    """get cadastral territory full info by identifier

    By passing in the appropriate options, you can obtain cadastral territory  # noqa: E501

    :param id: cadastral territory identifier
    :type id: int

    :rtype: FullCadaster
    """
    return 'do some magic!'


def get_zsj_id_api(id):  # noqa: E501
    """get basic settlement unit full info by identifier

    By passing in the appropriate options, you can obtain basic settlement unit  # noqa: E501

    :param id: basic settlement unit identifier
    :type id: int

    :rtype: FullSettlement
    """
    return 'do some magic!'


def ku_api(x, y):  # noqa: E501
    """find cadastral territory by coordinates

    By passing in the appropriate options, you can search for the cadastral territory  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: KatastralniUzemi
    """
    return 'do some magic!'


def ku_post_api(body=None):  # noqa: E501
    """find cadastral territory by coordinates

    By passing in the appropriate options, you can search for the cadastral territory  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: KatastralniUzemi
    """
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def ku_wgs_api(lat, lon):  # noqa: E501
    """find cadastral territory by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: KatastralniUzemi
    """
    return 'do some magic!'


def ku_wgs_post_api(body=None):  # noqa: E501
    """find cadastral territory by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: KatastralniUzemi
    """
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def mapy50_api(x, y):  # noqa: E501
    """find map sheets layout by coordinates

    By passing in the appropriate options, you can search for the map sheets layout  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: MapovyList50
    """
    return 'do some magic!'


def mapy50_post_api(body=None):  # noqa: E501
    """find map sheets layout by coordinates

    By passing in the appropriate options, you can search for the map sheets layout  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: MapovyList50
    """
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def mapy50_wgs_api(lat, lon):  # noqa: E501
    """find map sheets layout by coordinates

    By passing in the appropriate options, you can search for the map sheets layout  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: MapovyList50
    """
    return 'do some magic!'


def mapy50_wgs_post_api(body=None):  # noqa: E501
    """find map sheets layout by coordinates

    By passing in the appropriate options, you can search for the map sheets layout  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: MapovyList50
    """
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def nearby_address_api(x, y):  # noqa: E501
    """find nearby adresses by coordinates

    By passing in the appropriate options, you can search for the nearby adresses  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: List[NearbyAddress]
    """
    return 'do some magic!'


def nearby_address_post_api(body=None):  # noqa: E501
    """find nearby adresses by coordinates

    By passing in the appropriate options, you can search for the nearby adresses  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[NearbyAddress]
    """
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def nearby_address_wgs_api(lat, lon):  # noqa: E501
    """find nearby adresses by coordinates

    By passing in the appropriate options, you can search for the nearby adresses  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: List[NearbyAddress]
    """
    return 'do some magic!'


def nearby_address_wgs_post_api(body=None):  # noqa: E501
    """find nearby adresses by coordinates

    By passing in the appropriate options, you can search for the nearby adresses  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[NearbyAddress]
    """
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def parcela_api(x, y):  # noqa: E501
    """find land parcel by coordinates

    By passing in the appropriate options, you can search for the plot of land  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: Parcela
    """
    return 'do some magic!'


def parcela_post_api(body=None):  # noqa: E501
    """find plot (of land) by coordinates

    By passing in the appropriate options, you can search for the plot of land  # noqa: E501

    :param body: JTSK coordinates
    :type body: dict | bytes

    :rtype: Parcela
    """
    if connexion.request.is_json:
        body = Jtsk.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def parcela_wgs_api(lat, lon):  # noqa: E501
    """find land parcel by coordinates

    By passing in the appropriate options, you can search for the plot of land  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: Parcela
    """
    return 'do some magic!'


def parcela_wgs_post_api(body=None):  # noqa: E501
    """find plot (of land) by coordinates

    By passing in the appropriate options, you can search for the plot of land  # noqa: E501

    :param body: WGS coordinates
    :type body: dict | bytes

    :rtype: Parcela
    """
    if connexion.request.is_json:
        body = Wgs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def povodi_api(x, y):  # noqa: E501
    """find basin info by coordinates

    By passing in the appropriate options, you can search for the basin info  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: Povodi
    """
    return 'do some magic!'


def povodi_post_api(body=None):  # noqa: E501
    """find basin info by coordinates

    By passing in the appropriate options, you can search for the basin info  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Povodi
    """
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def povodi_wgs_api(lat, lon):  # noqa: E501
    """find basin info by coordinates

    By passing in the appropriate options, you can search for the basin info  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: Povodi
    """
    return 'do some magic!'


def povodi_wgs_post_api(body=None):  # noqa: E501
    """find basin info by coordinates

    By passing in the appropriate options, you can search for the basin info  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Povodi
    """
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def search_address_api(body=None):  # noqa: E501
    """search adresses by structured query

    By passing in the appropriate options, you can obtain search results  # noqa: E501

    :param body: query by form
    :type body: dict | bytes

    :rtype: List[Address]
    """
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def search_address_ft_api(query):  # noqa: E501
    """search adresses by query

    By passing in the appropriate options, you can obtain search results  # noqa: E501

    :param query: Search query
    :type query: str

    :rtype: List[Address]
    """
    return 'do some magic!'


def search_address_id_api(id):  # noqa: E501
    """seach address by identifier

    By passing in the appropriate options, you can obtain addres point  # noqa: E501

    :param id: Address point identifier
    :type id: int

    :rtype: Address
    """
    return 'do some magic!'


def validate_address_id_api(id):  # noqa: E501
    """validate adresses by identifier

    By passing in the appropriate options, you can validate address point  # noqa: E501

    :param id: Address point identifier
    :type id: int

    :rtype: bool
    """
    return 'do some magic!'


def zsj_api(x, y):  # noqa: E501
    """find basic settlement unit by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param x: JTSK x coordinate
    :type x: float
    :param y: JTSK y coordinate
    :type y: float

    :rtype: Zsj
    """
    return 'do some magic!'


def zsj_post_api(body=None):  # noqa: E501
    """find basic settlement unit by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Zsj
    """
    if connexion.request.is_json:
        body = PointJtsk.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def zsj_wgs_api(lat, lon):  # noqa: E501
    """find basic settlement unit by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param lat: WGS-84 lat coordinate
    :type lat: str
    :param lon: WGS-84 lon coordinate
    :type lon: str

    :rtype: Zsj
    """
    return 'do some magic!'


def zsj_wgs_post_api(body=None):  # noqa: E501
    """find basic settlement unit by coordinates

    By passing in the appropriate options, you can search for the basic settlement unit  # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Zsj
    """
    if connexion.request.is_json:
        body = PointWgs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
