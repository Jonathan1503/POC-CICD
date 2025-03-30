from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


# Inicializar aplicación Flask
application = Flask(__name__)
application.config.from_object("config")

# Configurar base de datos
db = SQLAlchemy()
db.init_app(application)

# Configurar JWT
jwt = JWTManager(application)

# Configurar API
api = Api(application)


# Crear tablas en la primera ejecución
with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(debug=True)
