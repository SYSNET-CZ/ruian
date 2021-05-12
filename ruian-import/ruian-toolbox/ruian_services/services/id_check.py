from ruian_services.services import ruian_connection, compile_address
from shared_tools import shared


def id_check_service_handler(query_params, response, builder):
    response.mime_format = builder.get_mime_format()
    address = ruian_connection.find_address(shared.get_key_value(query_params, "AddressPlaceId"))
    response.handled = True
    if address:
        html = compile_address.compile_address(
            builder, address.street, address.house_number, address.record_number,
            address.orientation_number, address.orientationNumberCharacter,
            address.zip_code, address.locality, address.locality_part,
            address.district_number)
        response.html_data = builder.list_to_response_text([html])

    return response
