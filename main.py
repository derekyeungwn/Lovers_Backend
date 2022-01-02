import datetime, time, json
from flask import Flask, jsonify, make_response, request, Response, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

#Mongo Setting
app.config['MONGO_URI'] = 'mongodb://derek:450412@192.168.1.7:27017/lovers'
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('./index.html')

@app.route('/api/v1/datings/', methods=['GET'])
def get_all_datings():
    output = []    
    for data in mongo.db.datings.find():
        thisdict = {}
        for item in data:            
            if item != '_id': 
                if isinstance(data[item], datetime.datetime):                    
                    thisdict[item] = data[item].strftime('%d/%m/%Y')
                else:
                    thisdict[item] = data[item]
        output.append(thisdict)
    return Response(json.dumps({'data' : output}), mimetype='application/json', status=200)

@app.route('/api/v1/datings/', methods=['POST'])
def add_dating():
    #print(json.dumps(request.json['data'], indent = 3))
    mongo.db.datings.insert_one(request.json['data'])
    return Response(json.dumps({'Status' : 'Succesfully Inserted'}), mimetype='application/json', status=200)

@app.route('/api/v1/datings/<id>', methods=['DELETE'])
def delete_dating(id):
    filter = {}
    filter['id'] = int(id)
    mongo.db.datings.delete_one(filter)
    return Response(json.dumps({'Status' : 'Succesfully Deleted'}), mimetype='application/json', status=200)

@app.route('/api/v1/datings/<id>', methods=['PUT'])
def update_dating(id):
    filter = {}
    filter['id'] = int(id)
    updated_data = {'$set' : request.json['data']}
    mongo.db.datings.update_one(filter, updated_data)
    return Response(json.dumps({'Status' : 'Succesfully Updated'}), mimetype='application/json', status=200)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8888')