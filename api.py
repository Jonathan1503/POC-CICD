from flask import request, jsonify
from flask_restful import Resource
from models import Blacklist
from database import db
from schemas.blacklist_schema import blacklist_schema
from flask_jwt_extended import jwt_required

class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        email = data.get("email")
        app_uuid = data.get("app_uuid")
        blocked_reason = data.get("blocked_reason", "")

        if not email or not app_uuid:
            return {"message": "Email and app_uuid are required"}, 400

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
