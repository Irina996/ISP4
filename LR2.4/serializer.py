import json_serializer
import json_deserializer
import toml_serializer
import yaml_serializer


def _get_serializer(type):
    if type == "json":
        return json_serializer.dumps
    elif type == "toml":
        return toml_serializer.dumps
    elif type == "yaml":
        return yaml_serializer.dumps
    else:
        raise ValueError(type)


def dumps(obj, type):
    _dumps = _get_serializer(type)
    return _dumps(obj)


def dump(obj, type, fp):
    string = dumps(obj, type)
    try:
        with open(fp, "w") as file:
            file.write(string)
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")

    
def _get_deserializer(type):
    if type == "json":
        return json_deserializer.loads
    elif type == "toml":
        return toml_serializer.loads
    elif type == "yaml":
        return yaml_serializer.loads
    else:
        raise ValueError(type)


def loads(str, type):
    _loads = _get_deserializer(type)
    return _loads(str)


def load(fp, type):
    try:
        with open(fp, "r") as file:
            str = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")
    return loads(str)