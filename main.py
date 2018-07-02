from arango_db import *
from vk_api import *


class SocialGraph:

    def __init__(self, start_vk_id, goal_vk_id, stop_level=6):
        self.start_vk_id = start_vk_id
        self.goal_vk_id = goal_vk_id
        self.stop_level = stop_level
        self.connection = ArangoDb('social_graph_db')
        self.graph = self.connection.find_or_create_graph('vk')
        self.users = ArangoDb.find_or_create_vertex_collection(
            self.graph, 'users'
        )
        self.friends = ArangoDb.find_or_create_edge_definition(
            self.graph, 'friends', 'users'
        )

    def bfs(self):
        vk_api = VkApi()
        level = 0
        stop_condition = False
        queue = [[None, self.start_vk_id, level]]
        self._private_insert_user(self.start_vk_id)

        while queue:
            current = queue.pop(0)
            print(f'Текущий: {current}')
            id = current[1]
            parent = current[0]
            level = current[2] + 1
            if level > self.stop_level:
                break
            self._private_insert_user(id)

            if parent:
                self._private_insert_friend(parent, id)
            if id == self.goal_vk_id:
                return True

            if not stop_condition:
                friends_list = vk_api.get_friends(id)
                stop_condition = self.goal_vk_id in friends_list
                if stop_condition:
                    queue = [[id, self.goal_vk_id, level]]
                else:
                    ids_in_queue = [elem[1] for elem in queue]
                    queue.extend(
                        [[id, friend, level] for friend in friends_list
                            if friend not in ids_in_queue]
                    )

            print(f'Очередь: {len(queue)}')
            print('')

        return False

    def _private_insert_user(self, vk_id):
        if not self.users.has(str(vk_id)):
            self.users.insert({'_key': str(vk_id)})

    def _private_insert_friend(self, first_vk_id, last_vk_id):
        if not (self.friends.has(f'{first_vk_id}-{last_vk_id}') or
                self.friends.has(f'{last_vk_id}-{first_vk_id}')):
            self.friends.insert({
                '_key': f'{first_vk_id}-{last_vk_id}',
                '_from': f'users/{first_vk_id}',
                '_to': f'users/{last_vk_id}'
            })


if __name__ == '__main__':
    social_graph = SocialGraph(1861235, 11821, 5)
    result = social_graph.bfs()
    print(result)
