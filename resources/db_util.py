from .db import db

def getNextSequenceValue(sequenceName):
    ret = db.sequences.find_and_modify({'collection': sequenceName}, {'$inc': {'id': 1}}, new = True)
    return ret['id']
