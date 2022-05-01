import datetime, json
import this
from flask import request, Response, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from util.db import db

appCode_bp = Blueprint('appCode', __name__)

@appCode_bp.route('/', methods=['GET'])
@jwt_required()
def getAppCode(): 
    try:
        output = {}
        response = {}

        for data in db.app_code.find():
            for item in data:            
                if item != '_id': 
                    if isinstance(data[item], datetime.datetime):                    
                        response[item] = data[item].strftime('%d/%m/%Y')
                    else:
                        response[item] = data[item]

        user_id = get_jwt_identity()
        filter = {}
        filter["user_id"] = user_id
        result = db.users.find_one(filter)
        if "user_name" in result:
            response['user_name'] = result['user_name']
        else:
            response['user_name'] = ''
        response['user_id'] = result['user_id']

        output['success'] = True
        output['response'] = response
        
    except Exception as e:
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output), mimetype='application/json', status=200)
