from arango_db import connect_to_db, find_or_create_collection

db = connect_to_db('social_graph_db')
people = find_or_create_collection(db, 'people')

for person in people:
    print(f"Person {person['_key']}: {person['first_name']} "
          f"{person['last_name']}")
