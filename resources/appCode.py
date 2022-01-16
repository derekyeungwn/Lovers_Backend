import datetime, json
from flask import request, Response, Blueprint
from .db import db

appCode_bp = Blueprint('appCode', __name__)

@appCode_bp.route('/', methods=['GET'])
def getAppCode():
    output = []    
    for data in db.app_code.find():
        thisdict = {}
        for item in data:            
            if item != '_id': 
                if isinstance(data[item], datetime.datetime):                    
                    thisdict[item] = data[item].strftime('%d/%m/%Y')
                else:
                    thisdict[item] = data[item]
        output.append(thisdict)
    return Response(json.dumps({'data' : output}), mimetype='application/json', status=200)
