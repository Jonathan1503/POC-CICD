from models import Blacklist
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, ValidationError
import uuid

ma = Marshmallow()

def validate_uuid(val):
    try:
        uuid.UUID(val)
    except ValueError:
        raise ValidationError("Invalid UUID format")

class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist

blacklist_schema = BlacklistSchema()

class BlacklistInputSchema(SQLAlchemyAutoSchema):
    email = fields.Email(required=True)
    app_uuid = fields.String(required=True, validate=validate_uuid)
    blocked_reason = fields.String(required=False, allow_none=True, validate=validate.Length(max=255))

    class Meta:
        model = Blacklist
        exclude = ("id", "created_at", "ip_address")

blacklist_input_schema = BlacklistInputSchema()
