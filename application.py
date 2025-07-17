import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from database import db
from api import BlacklistResource




application = Flask(__name__)
application.config.from_object("config")


db.init_app(application)

jwt = JWTManager(application)

api = Api(application)
api.add_resource(BlacklistResource, "/blacklists", "/blacklists/<string:email>")

# Endpoint de Healthcheck
@application.route("/")
def index():
    return jsonify(status="test2"), 200

with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 5000, debug = True)
