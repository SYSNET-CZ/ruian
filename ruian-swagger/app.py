#!/usr/bin/env python3
import os
from logging.config import dictConfig

import connexion
from environs import Env
from flask_cors import CORS

from swagger_server import encoder

COUNTER = {
    'info_api': 0,
    'compile_address_api': 0,
    'compile_address_ft_api': 0,
    'compile_address_id_api': 0,
    'convert_point_jtsk_api': 0,
    'convert_point_wgs_api': 0,
    'ku_api': 0,
    'ku_wgs_api': 0,
    'mapy50_api': 0,
    'mapy50_wgs_api': 0,
    'nearby_address_api': 0,
    'nearby_address_wgs_api': 0,
    'parcela_api': 0,
    'parcela_post_api': 0,
    'parcela_wgs_api': 0,
    'parcela_wgs_post_api': 0,
    'povodi_api': 0,
    'povodi_wgs_api': 0,
    'search_address_api': 0,
    'search_address_ft_api': 0,
    'search_address_id_api': 0,
    'validate_address_id_api': 0,
    'zsj_api': 0,
    'zsj_wgs_api': 0
}

SERVICE_ENVIRONMENT = os.getenv("SERVICE_ENVIRONMENT", "development")
debug = True
if SERVICE_ENVIRONMENT == 'production':
    debug = False

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = connexion.App(__name__, specification_dir='swagger_server/swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.app.logger.info("The logger configured!")
app.add_api('swagger.yaml', arguments={'title': 'SYSNET RUIAN services API'}, pythonic_params=True)
CORS(app.app)
env = Env()
env.read_env()


if __name__ == '__main__':
    app.run(port=8080, debug=debug)
