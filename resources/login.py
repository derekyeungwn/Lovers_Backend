import datetime, json
from flask import request, Response, Blueprint
from flask_jwt_extended import create_access_token
import datetime
from .db import db

login_bp = Blueprint('login', __name__)

JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)

@login_bp.route('/', methods=['PUT'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    filter = {}
    filter['email'] = email
    filter['password'] = password
    result = db.users.find_one(filter)

    if not result:
        return Response(json.dumps({'msg' : 'Bad username or password'}), mimetype='application/json', status=401)
    
    output = {}

    access_token = create_access_token(identity=result['user_id'])
    output['access_token'] = access_token
    output['user_name'] = result['user_name']
    output['user_id'] = result['user_id']

    return Response(json.dumps(output), mimetype='application/json', status=200)