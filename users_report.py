from arango_db import connect_to_db, find_or_create_collection

db = connect_to_db('social_graph_db')
users = find_or_create_collection(db, 'users')

for user in users:
    print(f"User {user['_key']}: {user['first_name']} {user['last_name']}")
