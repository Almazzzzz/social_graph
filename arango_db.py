from arango import ArangoClient
import settings


class ArangoDb:
    def __init__(self, db_name):
        self.client = ArangoClient()
        self.sys_db = self.client.db('_system', username='root',
                                     password=settings.arangodb_root_password)
        self._private_create_database(db_name)
        self.db = self.client.db(db_name, username=settings.arangodb_user,
                                 password=settings.arangodb_user_password)

    def _private_create_database(self, db_name):
        if not self.sys_db.has_database(db_name):
            self.sys_db.create_database(
                name=db_name,
                users=[
                    {'username': settings.arangodb_user,
                     'password': settings.arangodb_user_password,
                     'active': True}
                ]
            )

    def find_or_create_collection(self, collection_name):
        if self.db.has_collection(collection_name):
            return self.db.collection(collection_name)
        else:
            return self.db.create_collection(collection_name)

    def find_or_create_graph(self, graph_name):
        if self.db.has_graph(graph_name):
            return self.db.graph(graph_name)
        else:
            return self.db.create_graph(graph_name)

    @staticmethod
    def find_or_create_vertex_collection(graph, collection_name):
        if graph.has_vertex_collection(collection_name):
            return graph.vertex_collection(collection_name)
        else:
            return graph.create_vertex_collection(collection_name)

    @staticmethod
    def find_or_create_edge_definition(graph, definition_name,
                                       vertex_collection_name):
        if graph.has_edge_definition(definition_name):
            return graph.edge_collection(definition_name)
        else:
            return graph.create_edge_definition(
                edge_collection=definition_name,
                from_vertex_collections=[vertex_collection_name],
                to_vertex_collections=[vertex_collection_name]
            )

    @staticmethod
    def traverse(graph, start_vertex):
        graph.traverse(
            start_vertex=start_vertex,
            direction='outbound',
            strategy='bfs',
            edge_uniqueness='global',
            vertex_uniqueness='global',
        )
