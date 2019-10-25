import json
from os.path import join, dirname


def _get_absolute_filepath(folder, filename):
    relative_path = join(folder, filename)
    absolute_path = join(dirname(__file__), relative_path)
    return absolute_path


def save_data_as_json_file(responce, filename):
    absolute_path = _get_absolute_filepath('result', filename)

    f = open(absolute_path, 'w')
    data = responce.get_json()
    f.write(json.dumps(data))
