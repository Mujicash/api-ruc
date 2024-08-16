import logging

from flask import Flask
from flask_cors import CORS

from .ruc_details.infrastructure.api_ruc_details import ruc_details

logger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", datefmt='%m/%d/%Y %I:%M:%S')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
fileHandler = logging.FileHandler('app.log')
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

app = Flask(__name__)

CORS(app)

app.register_blueprint(ruc_details)
