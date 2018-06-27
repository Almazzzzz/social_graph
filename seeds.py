from arango_db import connect_to_db, find_or_create_collection

db = connect_to_db('social_graph_db')
users = find_or_create_collection(db, 'users')

for i in range(10):
    if not users.get({'_key': str(i)}):
        data = {
            '_key': str(i), 'first_name': f'Name {i}',
            'last_name': f'Surname {i}'
        }
        users.insert(data)
