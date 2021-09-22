from pymongo import MongoClient

DEBUG = True
client = MongoClient('mongodb://%s:%s@127.0.0.1' % ('root', 'root'))
DATABASE = client['restfulapi']