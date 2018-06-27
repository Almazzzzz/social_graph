from arango import ArangoClient
import settings


def connect_to_db(db_name):
    client = ArangoClient()
    sys_db = client.db('_system', username='root',
                       password=settings.arangodb_root_password)

    create_database(sys_db, db_name)

    db = client.db(db_name, username=settings.arangodb_user,
                   password=settings.arangodb_user_password)

    return db


def create_database(sys_db, db_name):
    if not sys_db.has_database(db_name):
        sys_db.create_database(
            name=db_name,
            users=[
                {'username': settings.arangodb_user,
                 'password': settings.arangodb_user_password,
                 'active': True}
            ]
        )


def find_or_create_collection(db, collection_name):
    if db.has_collection(collection_name):
        return db.collection(collection_name)
    else:
        return db.create_collection(collection_name)


def find_or_create_graph(db, graph_name):
    if db.has_graph(graph_name):
        return db.graph(graph_name)
    else:
        return db.create_graph(graph_name)


def find_or_create_vertex_collection(graph, collection_name):
    if graph.has_vertex_collection(collection_name):
        return graph.vertex_collection(collection_name)
    else:
        return graph.create_vertex_collection(collection_name)


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
