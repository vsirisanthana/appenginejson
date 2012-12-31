import datetime
from json import (dump, dumps as dumps_orig, load, loads, JSONDecoder, JSONEncoder)

from google.appengine.api import users
from google.appengine.ext import db


class ExtEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return unicode(obj)
        elif isinstance(obj, users.User):
            return {
                'nickname': obj.nickname(),
                'email': obj.email(),
                'user_id': obj.user_id(),
                'federated_identity': obj.federated_identity(),
                'federated_provider': obj.federated_provider(),
            }
        elif isinstance(obj, db.Model):
            output = {'key': str(obj.key())}
            for key, prop in obj.properties().iteritems():
                value = getattr(obj, key)
                output[key] = value
            return output
        elif isinstance(obj, db.Key):
            model_instance = db.get(obj)
            return self.default(model_instance)
        else:
            return JSONEncoder.default(self, obj)


def dumps(obj, *args, **kwargs):
    return dumps_orig(obj, cls=ExtEncoder, *args, **kwargs)