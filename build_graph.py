from arango_db import *

db = connect_to_db('social_graph_db')
graph = find_or_create_graph(db, 'vk')
users = find_or_create_vertex_collection(graph, 'users')
friends = find_or_create_edge_definition(graph, 'friends', 'users')

for i in range(50):
    if not users.has({'_key': str(i)}):
        user = {
            '_key': str(i), 'first_name': f'Name {i}',
            'last_name': f'Surname {i}'
        }
        users.insert(user)

for i in range(0,21):
    if not friends.has(f'0-{i}'):
        friends.insert({
            '_key': f'0-{i}',
            '_from': 'users/0',
            '_to': f'users/{i}'
        })

graph.traverse(
    start_vertex='users/0',
    direction='outbound',
    strategy='bfs',
    edge_uniqueness='global',
    vertex_uniqueness='global',
)
