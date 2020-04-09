from fxq.commons.marshalling import DictMarshal

from kodiak.server import comments_dao
from kodiak.server.gql.utils import build_executable_schema
from kodiak.server.gql.utils import build_executable_schema, get_schema_def


def get_comments(value, info, **args):
    return [DictMarshal.to_dict(c) for c in comments_dao.get_comments()]


resolvers = {
    'RootQuery': {
        'getComments': get_comments
    }
}

schema = build_executable_schema(get_schema_def(), resolvers)
