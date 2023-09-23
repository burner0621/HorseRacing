from bson import ObjectId
from datetime import datetime
import json

class JSONEncoder(json.JSONEncoder):
    def encode(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, dict):
            return {k: v for k, v in o.items()}
        return json.JSONEncoder.default(self, o)