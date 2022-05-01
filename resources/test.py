import json
from flask import Response, Blueprint

import requests

test_bp = Blueprint('test', __name__)

@test_bp.route('/', methods=['GET'])
def func(): 
    try:
        output = {}
        response = {}

        #Make API request
        """
        timeout = 3
        url = 'https://api.avgle.com/v1/categories'
        r = requests.get(url, timeout=timeout)
        json = r.json()
        print(r.elapsed.total_seconds())
        print(r.headers)
        """

        output['success'] = True
        output['response'] = response
        
    except Exception as e:
        print(e)
        output['success'] = False
        output['error_message'] = 'Internal Server Error'
        return Response(json.dumps(output), mimetype='application/json', status=500)
    return Response(json.dumps(output), mimetype='application/json', status=200)
