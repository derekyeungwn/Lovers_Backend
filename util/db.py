import pymongo

myclient = pymongo.MongoClient('mongodb://derek:450412@192.168.1.7:27017/lovers')
db = myclient.lovers

def getNextSequenceValue(sequenceName):
    ret = db.sequences.find_and_modify({'collection': sequenceName}, {'$inc': {'id': 1}}, new = True)
    return ret['id']