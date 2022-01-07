import datetime, json
from flask import request, Response, Blueprint
from .db import db

datings = Blueprint('datings', __name__)

@datings.route('/api/v1/datings/', methods=['GET'])
def get_all_datings():
    output = []    
    for data in db.datings.find():
        thisdict = {}
        for item in data:            
            if item != '_id': 
                if isinstance(data[item], datetime.datetime):                    
                    thisdict[item] = data[item].strftime('%d/%m/%Y')
                else:
                    thisdict[item] = data[item]
        output.append(thisdict)
    return Response(json.dumps({'data' : output}), mimetype='application/json', status=200)

@datings.route('/api/v1/datings/', methods=['POST'])
def add_dating():
    #print(json.dumps(request.json['data'], indent = 3))
    db.datings.insert_one(request.json['data'])
    return Response(json.dumps({'Status' : 'Succesfully Inserted'}), mimetype='application/json', status=200)

@datings.route('/api/v1/datings/<id>', methods=['DELETE'])
def delete_dating(id):
    filter = {}
    filter['id'] = int(id)
    db.datings.delete_one(filter)
    return Response(json.dumps({'Status' : 'Succesfully Deleted'}), mimetype='application/json', status=200)

@datings.route('/api/v1/datings/<id>', methods=['PUT'])
def update_dating(id):
    filter = {}
    filter['id'] = int(id)
    updated_data = {'$set' : request.json['data']}
    db.datings.update_one(filter, updated_data)
    return Response(json.dumps({'Status' : 'Succesfully Updated'}), mimetype='application/json', status=200)