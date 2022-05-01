import datetime, json
from flask import request, Response, Blueprint
from flask_jwt_extended import create_access_token
import hashlib

from util.db import db
from util.db import getNextSequenceValue

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['POST'])
def add_user():
    try:
        output = {}
        response = {}

        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if db.users.find_one({'email': email}, {'_id': 1}) is not None:
            output['success'] = False
            output['error_message'] = '這個電郵巳被註冊了' 
            return Response(json.dumps(output), mimetype='application/json', status=400)
        
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        hashValue = m.hexdigest()

        data = {}
        data['email'] = email
        data['password'] = hashValue
        data['user_id'] = str(getNextSequenceValue('users'))
        db.users.insert_one(data)

        expires = datetime.timedelta(days=365)
        access_token = create_access_token(identity=data['user_id'], expires_delta=expires)
        output['success'] = True
        response['access_token'] = access_token
        response['user_id'] = str(data['user_id'])
        output['response'] = response
        
    except Exception as e:
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output), mimetype='application/json', status=200)