from flask_marshmallow import Marshmallow
import app

ma = Marshmallow(app)

class AvatarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')
