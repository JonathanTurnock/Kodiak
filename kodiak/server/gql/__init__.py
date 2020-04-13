from pathlib import Path

from bootstrap import resources_root
from kodiak.server.gql.resolvers import resolver_map
from kodiak.server.gql.schema_adapter import to_gql_schema
from kodiak.utils.gql import build_executable_schema


def get_schema_def():
    schema_graphqls_path = Path(resources_root, 'schema.graphql').absolute()

    with open(str(schema_graphqls_path), 'r') as f:
        return f.read()


schema = build_executable_schema(get_schema_def(), resolver_map)
