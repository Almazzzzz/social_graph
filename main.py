from graph import *
from vk_api import *


graph = Graph('social_graph_db', 'vk')
users = graph.find_or_create_vertex_collection('users')
friends = graph.find_or_create_edge_definition('friends', 'users')
vk_api = VkApi()


def bfs(start_vk_id, goal_vk_id, stop_level=6):
    level = 0
    stop_condition = False
    queue = [[None, start_vk_id, level]]
    insert_user(start_vk_id)

    while queue:
        current = queue.pop(0)
        print(f'Текущий: {current}')
        id = current[1]
        parent = current[0]
        level = current[2] + 1
        if level > stop_level:
            break
        insert_user(id)
        if parent:
            insert_friend(parent, id)

        if id == goal_vk_id:
            return True

        if not stop_condition:
            friends_list = vk_api.get_friends(id)
            stop_condition = goal_vk_id in friends_list
            if stop_condition:
                queue = [[id, goal_vk_id, level]]
            else:
                ids_in_queue = [elem[1] for elem in queue]
                queue.extend(
                    [[id, friend, level] for friend in friends_list
                        if friend not in ids_in_queue]
                )

        print(f'Очередь: {len(queue)}')
        print('')

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


if __name__ == '__main__':
    result = bfs(1861235, 11821, 5)
    print(result)
