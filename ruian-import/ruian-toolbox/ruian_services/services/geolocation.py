from ruian_services.services.postgis_db import _find_address, _get_nearby_localities, _validate_address, \
    _find_coordinates, _find_coordinates_by_address, _get_ruian_version_date, _save_ruian_version_date_today, \
    _get_table_names, _get_addresses
from ruian_services.services.ruian_reference_db import _get_db_details

find_address = _find_address
get_nearby_localities = _get_nearby_localities
validate_address = _validate_address
find_coordinates = _find_coordinates
find_coordinates_by_address = _find_coordinates_by_address
get_ruian_version_date = _get_ruian_version_date
save_ruian_version_date_today = _save_ruian_version_date_today
get_db_details = _get_db_details
get_table_names = _get_table_names
get_addresses = _get_addresses
