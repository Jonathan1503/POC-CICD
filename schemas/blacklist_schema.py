from models import Blacklist
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
ma = Marshmallow()

class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist

blacklist_schema = BlacklistSchema()
