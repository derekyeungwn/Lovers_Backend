import datetime, json
from flask import request, Response, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import db

dating_bp = Blueprint('datings', __name__)

@dating_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_datings():
    user_id = get_jwt_identity()
    filter = {}
    filter["user_id"] = user_id
    output = []    
    for data in db.datings.find(filter):        
        thisdict = {}
        for item in data:               
            if item != '_id':
                if isinstance(data[item], datetime.datetime):                    
                    thisdict[item] = data[item].strftime('%d/%m/%Y')
                else:
                    thisdict[item] = data[item]
        output.append(thisdict)
    return Response(json.dumps({'data' : output}), mimetype='application/json', status=200)

@dating_bp.route('/', methods=['POST'])
@jwt_required()
def add_dating(): 
    db.datings.insert_one(request.json['data'])
    return Response(json.dumps({'Status' : 'Succesfully Inserted'}), mimetype='application/json', status=200)

@dating_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_dating(id):
    filter = {}
    filter['id'] = int(id)
    db.datings.delete_one(filter)
    return Response(json.dumps({'Status' : 'Succesfully Deleted'}), mimetype='application/json', status=200)

@dating_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_dating(id):
    filter = {}
    filter['id'] = int(id)
    updated_data = {'$set' : request.json['data']}
    db.datings.update_one(filter, updated_data)
    return Response(json.dumps({'Status' : 'Succesfully Updated'}), mimetype='application/json', status=200)