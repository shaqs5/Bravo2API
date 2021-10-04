from flask import Flask, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import avatars
from flask_marshmallow import Marshmallow
# from sqlalchemy import func
# import psycopg2
# import psycopg2.extras
import os
from dotenv import load_dotenv
load_dotenv()

# from sqlalchemy import func
# data = db.session.query(func.your_schema.your_function_name()).all()

app = Flask(__name__)
api = Api(app)
CORS(app)

CONN_HOST = os.environ['CONN_HOST']
CONN_DBNAME = os.environ['CONN_DBNAME']
CONN_USER = os.environ['CONN_USER']
CONN_PASS = os.environ['CONN_PASS']

# conn = psycopg2.connect(f"host='{CONN_HOST}' dbname='{CONN_DBNAME}' user='{CONN_USER}' password='{CONN_PASS}'")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{CONN_USER}:{CONN_PASS}@localhost:5432/{CONN_DBNAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.init_app(app)

SWAGGER_URL = os.environ["SWAGGER_URL"]
API_URL = os.environ["API_URL"]
SWAGGER_APP_NAME = os.environ["SWAGGER_APP_NAME"]


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': SWAGGER_APP_NAME
    },
)

app.register_blueprint(swaggerui_blueprint)

ma = Marshmallow(app)

# Moved Model Avatars


class AvatarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


avatar_schema = AvatarSchema()
avatars_schema = AvatarSchema(many=True)


# Create Avatar
@app.route('/api/avatars', methods=['POST'])
def add_avatar():
    name = request.json['name']
    description = request.json['description']

    new_avatar = avatars.Avatars(name, description)

    db.session.add(new_avatar)
    db.session.commit()

    return avatar_schema.jsonify(new_avatar)


# Update Avatar
@app.route('/api/avatars/<id>', methods=['PUT'])
def update_avatar(id):
    avatar = avatars.Avatars.query.get(id)

    name = request.json['name']
    description = request.json['description']

    avatar.name = name
    avatar.description = description

    db.session.commit()

    return avatar_schema.jsonify(avatar)


# Get All Avatars
@app.route('/api/avatars', methods=['get'])
def get_avatars():
    # data = db.session.query(func.public.get_avatars()).all()
    all_avatars = avatars.Avatars.query.all()
    result = avatars_schema.dump(all_avatars)
    # result = data
    # print(result)
    return jsonify(result)


# Get Avatar by ID
@app.route('/api/avatars/<id>', methods=['get'])
def get_avatar(id):
    avatar = avatars.Avatars.query.get(id)
    return avatar_schema.jsonify(avatar)


# @app.route("/api")
# def root_main():
#     return "Working with from FastCGI via IIS!"

# @app.route('/api/unprotected')
# def unprotected():
#     return 'This is unprotected route, and requires no authentication.'

# @app.route('/api/superheros', methods=["GET"])
# def get_superheros():
#     superheros = SuperHeros.query.all()
#     result_set = superheros_schema.dump(superheros)
#     return jsonify(results_set)


# class Avatars(Resource):
#     def get(self):
#         cols = ['id', 'name', 'description', 'properties']
#         # query = 'SELECT a_id, a_name, a_description, a_properties  FROM public.get_avatars();'
#         query = "SELECT a_id, a_name, a_description, (case when a_properties IS NULL then 'N/A' else a_properties end) as a_properties  FROM public.get_avatars();"
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cur.execute(query)
#         result = [dict(zip(tuple(cols), i)) for i in cur.fetchall()]
#         cur.close()
#         return jsonify(result)
#
#
# # Routes
# api.add_resource(Avatars, '/api/avatars')


if __name__ == '__main__':
    app.run(debug=True)


# Browser > localhost:5000/api/docs/
