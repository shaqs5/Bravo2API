from app import db


class Avatars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, name, description):
        # self.id = id
        self.name = name
        self.description = description