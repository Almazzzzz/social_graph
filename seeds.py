from arango_db import db_find_or_create, collection_find_or_create


db = db_find_or_create('social_graph_db')
users_collection = collection_find_or_create(db, 'users')

for i in range(10):
    doc = users_collection.createDocument()
    data = {
        'vk_id': i, 'first_name': f'Name {i}', 'last_name': f'Surname {i}'
    }
    doc.set(data)
    doc.save()
