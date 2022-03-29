import json
from datetime import datetime
from flask import request, Response, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import db

dating_bp = Blueprint('datings', __name__)

@dating_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_datings():
    try:
        output = {}

        user_id = get_jwt_identity()
        filter = {}
        filter["user_id"] = user_id
        datings = []
        for data in db.datings.find(filter,{'_id': 0}):        
            datings.append(data)

        output['success'] = True
        output['response'] = datings

    except Exception as e:
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output, default=str), mimetype='application/json', status=200)

@dating_bp.route('/', methods=['POST'])
@jwt_required()
def add_dating(): 
    try:
        output = {} 

        data = request.json['data']
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d')

        db.datings.insert_one(data)

        output['success'] = True
        
    except Exception as e:
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output), mimetype='application/json', status=200)

@dating_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_dating(id):
    try:
        output = {}
    
        filter = {}
        filter['id'] = int(id)
        db.datings.delete_one(filter)

        output['success'] = True

    except Exception as e:
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output), mimetype='application/json', status=200)

@dating_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_dating(id):
    try:    
        output = {}

        data = request.json['data']
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d')
    
        filter = {}
        filter['id'] = int(id)
        updated_data = {'$set' : data}
        db.datings.update_one(filter, updated_data)

        output['success'] = True

    except Exception as e:
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output), mimetype='application/json', status=200)