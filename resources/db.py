import pymongo

myclient = pymongo.MongoClient('mongodb://derek:450412@192.168.1.7:27017/lovers')
db = myclient.lovers