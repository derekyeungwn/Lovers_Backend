import datetime, json

from flask import request, Response, Blueprint
from flask_jwt_extended import create_access_token
import datetime
import hashlib

from util.db import db

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['PUT'])
def login():
    try:
        output = {}
        response = {}

        email = request.json.get('email', None)
        password = request.json.get('password', None)        

        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        hashValue = m.hexdigest()

        filter = {}
        filter['email'] = email
        filter['password'] = hashValue
        result = db.users.find_one(filter)

        if not result:
            output['success'] = False
            output['error_message'] = 'Wrong email or password'
            return Response(json.dumps(output), mimetype='application/json', status=400)

        expires = datetime.timedelta(days=365)
        access_token = create_access_token(identity=result['user_id'], expires_delta=expires)
        output['success'] = True
        response['access_token'] = access_token
        output['response'] = response

        print(access_token)

    except Exception as e:
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output), mimetype='application/json', status=200)