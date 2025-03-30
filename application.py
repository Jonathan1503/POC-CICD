from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from database import db
from api import BlacklistResource

# Inicializar aplicación Flask
application = Flask(__name__)
application.config.from_object("config")

# Configurar base de datos

db.init_app(application)

# Configurar JWT
jwt = JWTManager(application)

# Configurar API
api = Api(application)
api.add_resource(BlacklistResource, "/blacklists", "/blacklists/<string:email>")


# Crear tablas en la primera ejecución
with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(debug=True)
