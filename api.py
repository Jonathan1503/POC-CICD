import traceback
from flask import request
from flask_restful import Resource
from models import Blacklist
from database import db
from schemas.blacklist_schema import blacklist_schema, blacklist_input_schema
from flask_jwt_extended import jwt_required

class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            validated_data = blacklist_input_schema.load(data)
        except Exception as e:
            print(str(e))
            print(str(traceback.print_exc()))
            return {"message": str(e)}, 400

        email = validated_data.get("email") 
        app_uuid = validated_data.get("app_uuid")
        blocked_reason = validated_data.get("blocked_reason", "")

        if Blacklist.query.filter_by(email=email, app_uuid=app_uuid).first():
            return {"message": "Email already blacklisted for this app"}, 400

        ip_address = request.remote_addr
        new_entry = Blacklist(email=email, app_uuid=app_uuid, ip_address=ip_address, blocked_reason=blocked_reason)

        db.session.add(new_entry)
        db.session.commit()

        return blacklist_schema.dump(new_entry), 201

    @jwt_required()
    def get(self, email):
        entry = Blacklist.query.filter_by(email=email).first()
        if entry:
            return {"is_blacklisted": True, "blocked_reason": entry.blocked_reason}, 200
        return {"is_blacklisted": False}, 200
