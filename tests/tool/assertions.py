import json
from os.path import join, dirname, abspath
from jsonschema import validate


def assert_valid_schema(responce, schema_file):
    """ Checks whether the given data matches the schema """
    data = responce.get_json()
    schema = _load_json_schema(schema_file)
    return validate(data, schema)


def _load_json_schema(filename):
    """ Loads the given schema file """

    relative_path = join('schemas', filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as schema_file:
        return json.loads(schema_file.read())
