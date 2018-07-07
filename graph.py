from arango_db import *


class Graph:
    def __init__(self, db_name, graph_name):
        self.db = ArangoDb(db_name).db
        self.graph = self.find_or_create_graph(graph_name)

    def find_or_create_graph(self, graph_name):
        if self.db.has_graph(graph_name):
            return self.db.graph(graph_name)
        else:
            return self.db.create_graph(graph_name)

    def find_or_create_vertex_collection(self, collection_name):
        if self.graph.has_vertex_collection(collection_name):
            return self.graph.vertex_collection(collection_name)
        else:
            return self.graph.create_vertex_collection(collection_name)

    def find_or_create_edge_definition(self, definition_name,
                                       vertex_collection_name):
        if self.graph.has_edge_definition(definition_name):
            return self.graph.edge_collection(definition_name)
        else:
            return self.graph.create_edge_definition(
                edge_collection=definition_name,
                from_vertex_collections=[vertex_collection_name],
                to_vertex_collections=[vertex_collection_name]
            )
