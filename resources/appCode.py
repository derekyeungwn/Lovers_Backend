import datetime, json
from flask import request, Response, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import db

appCode_bp = Blueprint('appCode', __name__)

@appCode_bp.route('/', methods=['GET'])
@jwt_required()
def getAppCode(): 
    output = []
    thisdict = {}
    for data in db.app_code.find():
        for item in data:            
            if item != '_id': 
                if isinstance(data[item], datetime.datetime):                    
                    thisdict[item] = data[item].strftime('%d/%m/%Y')
                else:
                    thisdict[item] = data[item]

    user_id = get_jwt_identity()
    filter = {}
    filter["user_id"] = user_id
    result = db.users.find_one(filter)
    thisdict['user_name'] = result['user_name']
    thisdict['user_id'] = result['user_id']

    output.append(thisdict)

    return Response(json.dumps({'data' : output}), mimetype='application/json', status=200)
