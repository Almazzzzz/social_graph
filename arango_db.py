from pyArango.connection import *
import settings

conn = Connection(username=settings.arangodb_user,
                  password=settings.arangodb_password)


def db_find_or_create(db_name):
    if conn.hasDatabase(db_name):
        return conn[db_name]
    else:
        return conn.createDatabase(name=db_name)

def collection_find_or_create(db, collection_name):
    if db.hasCollection(collection_name):
        return db.collections[collection_name]
    else:
        return db.createCollection(name=collection_name)
