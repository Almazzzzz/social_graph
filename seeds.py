from arango_db import connect_to_db, find_or_create_collection

db = connect_to_db('social_graph_db')
people = find_or_create_collection(db, 'people')

for i in range(10):
    if not people.has({'_key': str(i)}):
        person = {
            '_key': str(i), 'first_name': f'Name {i}',
            'last_name': f'Surname {i}'
        }
        people.insert(person)
