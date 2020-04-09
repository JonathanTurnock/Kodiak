from pathlib import Path

import graphql

from bootstrap import resources_root


def get_schema_def():
    schema_graphqls_path = Path(resources_root, 'schema.graphqls').absolute()

    with open(str(schema_graphqls_path), 'r') as f:
        return f.read()


def build_executable_schema(schema_definition, resolvers):
    ast = graphql.parse(schema_definition)
    schema = graphql.build_ast_schema(ast)

    for type_name in resolvers:
        field_type = schema.get_type(type_name)

        for fieldName in resolvers[type_name]:
            if field_type is graphql.GraphQLScalarType:
                field_type.fields[fieldName].resolver = resolvers[type_name][fieldName]
                continue

            field = field_type.fields[fieldName]
            field.resolver = resolvers[type_name][fieldName]

        if not field_type.fields:
            continue

        for remaining in field_type.fields:
            if not field_type.fields[remaining].resolver:
                field_type.fields[remaining].resolver = lambda value, info, _r=remaining, **args: value[_r]

    return schema
