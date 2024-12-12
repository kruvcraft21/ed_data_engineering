from json import JSONEncoder
from bson.objectid import ObjectId
from datetime import datetime


class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return JSONEncoder.default(obj, **kwargs)

def rename_key_nested(list_of_dict, old_key, new_key):
    for dictionary in list_of_dict:
        if old_key in dictionary:
            dictionary[new_key] = dictionary.pop(old_key)