#!/usr/bin/env python3
# import os

# import connexion
# from environs import Env
# from flask import render_template
# from swagger_server import encoder

# SERVICE_ENVIRONMENT = os.getenv("SERVICE_ENVIRONMENT", "development")
# debug = True
# if SERVICE_ENVIRONMENT == 'production':
#    debug = False


#app = connexion.App(__name__, specification_dir='./swagger/')
#app.app.json_encoder = encoder.JSONEncoder
#app.add_api('swagger.yaml', arguments={'title': 'SYSNET RUIAN services API'}, pythonic_params=True)

#env = Env()
#env.read_env()

# @app.route('/')
# def home():
#     return render_template('home.html', message='Hello World, we are running RUIAN Service')
from app import app, debug

if __name__ == '__main__':
    app.run(port=8080, debug=debug)
