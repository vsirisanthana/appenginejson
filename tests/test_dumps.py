from datetime import datetime

import unittest2
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import testbed

from appenginejson import dumps


class BaseTestHandler(unittest2.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_dumps_string(self):
        json = dumps('Hello')
        self.assertEqual(json, '"Hello"')

    def test_dumps_datetime(self):
        self.assertEqual(dumps(datetime(2012, 1, 1)), '"2012-01-01 00:00:00"')

    def test_dumps_dict(self):
        self.assertEqual(dumps({'created': datetime(2012, 1, 2)}), '{"created": "2012-01-02 00:00:00"}')

    def test_dumps_model(self):
        class Dummy(db.Model):
            name = db.StringProperty()
            created = db.DateTimeProperty()
        dummy = Dummy(name='Lemur is not dumb.', created=datetime(2012, 10, 31, 12, 15))
        dummy.put()
        dummy = Dummy.get(dummy.key())

        self.assertEqual(dumps(dummy, sort_keys=True), '{"created": "2012-10-31 12:15:00", '
                                                       '"key": "%s", '
                                                       '"name": "Lemur is not dumb."}' % str(dummy.key()))

    def test_dumps_user(self):
        user = users.User('ring-tailed@lemur.com')
        self.assertEqual(dumps(user, sort_keys=True), '{"email": "ring-tailed@lemur.com", '
                                                      '"federated_identity": null, '
                                                      '"federated_provider": null, '
                                                      '"nickname": "ring-tailed@lemur.com", '
                                                      '"user_id": null}')