import json
from flask import Response, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from util.db import db

XXX_bp = Blueprint('XXX', __name__)

@XXX_bp.route('/', methods=['GET'])
@jwt_required()
def func(): 
    try:
        output = {}
        response = {}

        output['success'] = True
        output['response'] = response
        
    except Exception as e:
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output), mimetype='application/json', status=200)
