from arango_db import *
from vk_api import get_friends

db = connect_to_db('social_graph_db')
graph = find_or_create_graph(db, 'vk')
users = find_or_create_vertex_collection(graph, 'users')
friends = find_or_create_edge_definition(graph, 'friends', 'users')


def main(start_vk_id, goal_vk_id):
    result = bfs(start_vk_id, goal_vk_id)
    print(result)


def bfs(start_vk_id, goal_vk_id):
    level = 0
    prev_parent = None
    queue = [[prev_parent, start_vk_id]]
    insert_user(start_vk_id)

    while queue and level < 4:
        current = queue.pop(0)
        print(current)
        id = current[1]
        parent = current[0]
        insert_user(id)

        if parent:
            insert_friend(parent, id)
        if id == goal_vk_id:
            return True
        friends_list = get_friends(id)
        print(friends_list)
        queue += [[id, friend] for friend in friends_list]
        if prev_parent != parent:
            level += 1
        prev_parent = parent

    return False


def insert_user(vk_id):
    if not users.has(str(vk_id)):
        users.insert({'_key': str(vk_id)})


def insert_friend(first_vk_id, last_vk_id):
    if not (friends.has(f'{first_vk_id}-{last_vk_id}') or
            friends.has(f'{last_vk_id}-{first_vk_id}')):
        friends.insert({
            '_key': f'{first_vk_id}-{last_vk_id}',
            '_from': f'users/{first_vk_id}',
            '_to': f'users/{last_vk_id}'
        })


def traverse(start_vertex):
    graph.traverse(
        start_vertex=start_vertex,
        direction='outbound',
        strategy='bfs',
        edge_uniqueness='global',
        vertex_uniqueness='global',
    )


main(1000, 1001)
