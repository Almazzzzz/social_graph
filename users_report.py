from arango_db import db_find_or_create, collection_find_or_create


db = db_find_or_create('social_graph_db')
users_collection = collection_find_or_create(db, 'users')

users = users_collection.fetchAll()
for user in users:
    print(f"User {user['first_name']} {user['last_name']}")
