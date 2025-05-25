import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from database import db
from api import BlacklistResource
import newrelic.agent
import logging
newrelic.agent.initialize()

# Set up logging
logger = logging.getLogger("Basic Logger")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)




application = Flask(__name__)
application.config.from_object("config")


db.init_app(application)

jwt = JWTManager(application)

api = Api(application)
api.add_resource(BlacklistResource, "/blacklists", "/blacklists/<string:email>")

# Endpoint de Healthcheck
@application.route("/")
def index():
    return jsonify(status="ok"), 200

with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 5000, debug = True)
