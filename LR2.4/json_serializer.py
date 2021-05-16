import inspect
import types

f_found = {}


def dumps_list(obj):
    if not len(obj):
        return "[]"
    res = "[\n"
    for i in range(len(obj) - 1):
        res += (_dumps(obj[i]) + ",\n")
    res += (_dumps(obj[-1]) + "\n]")
    return res


def dumps_dict(obj):
    if not len(obj):
        return "{}"
    res = "{\n"
    keys = list(obj)
    for i in keys[:-1]:
        res += (
                '"'
                + str(i)
                + '"'
                + ": "
                + _dumps(obj[i])
                + ",\n"
        )
    res += (
            '"'
            + str(keys[-1])
            + '"'
            + ": "
            + _dumps(obj[keys[-1]])
            + "\n}"
    )
    return res


def is_instance(obj):
    if not hasattr(obj, "__dict__"):
        return False
    if inspect.isroutine(obj):
        return False
    if inspect.isclass(obj):
        return False
    else:
        return True

def class_to_dict(cls):
    dpns = ()
    if len(cls.__bases__) != 0:
        for i in cls.__bases__:
            if i.__name__ != "object":
                dpns += (class_to_dict(i),)
    args = {}
    st_args = dict(cls.__dict__)
    if len(st_args) != 0:
        for i in st_args:
            if inspect.isclass(st_args[i]):
                args[i] = class_to_dict(st_args[i])
            elif inspect.isfunction(st_args[i]):
                if st_args[i] not in f_found:
                    args[i] = function_to_dict(st_args[i])
            elif isinstance(st_args[i], staticmethod):
                if st_args[i].__func__ not in f_found:
                    args[i] = smethod_to_dict(st_args[i])
            elif isinstance(st_args[i], classmethod):
                if st_args[i].__func__ not in f_found:
                    args[i] = cmethod_to_dict(st_args[i])
            elif inspect.ismodule(st_args[i]):
                args[i] = module_to_dict(st_args[i])
            elif is_instance(st_args[i]):
                args[i] = object_to_dict(st_args[i])
            elif isinstance(
                    st_args[i],
                    (
                            set,
                            dict,
                            list,
                            int,
                            float,
                            bool,
                            type(None),
                            tuple,
                    ),
            ):
                args[i] = st_args[i]
    return {"class_type": {"name": cls.__name__, "bases": dpns, "dict": args}}


def object_to_dict(obj):
    return {
        "instance_type": {
            "class": class_to_dict(obj.__class__),
            "vars": obj.__dict__,
        }
    }


def module_to_dict(obj):
    return {"module_type": obj.__name__}


def gather_gls(obj, obj_code):
    global f_found
    f_found[obj] = True
    gls = {}
    for i in obj_code.co_names:
        try:
            if inspect.isclass(obj.__globals__[i]):
                gls[i] = class_to_dict(obj.__globals__[i])
            elif inspect.isfunction(obj.__globals__[i]):
                if obj.__globals__[i] not in f_found:
                    gls[i] = function_to_dict(obj.__globals__[i])
            elif isinstance(obj.__globals__[i], staticmethod):
                if obj.__globals__[i].__func__ not in f_found:
                    gls[i] = smethod_to_dict(obj.__globals__[i])
            elif isinstance(obj.__globals__[i], classmethod):
                if obj.__globals__[i].__func__ not in f_found:
                    gls[i] = cmethod_to_dict(obj.__globals__[i])
            elif inspect.ismodule(obj.__globals__[i]):
                gls[i] = module_to_dict(obj.__globals__[i])
            elif is_instance(obj.__globals__[i]):
                gls[i] = object_to_dict(obj.__globals__[i])
            elif isinstance(
                    obj.__globals__[i],
                    (set, dict, list, int, float, bool, type(None), tuple, str),
            ):
                gls[i] = obj.__globals__[i]
        except KeyError:
            pass
    for i in obj_code.co_consts:
        if isinstance(i, types.CodeType):
            gls.update(gather_gls(obj, i))
    return gls


def smethod_to_dict(obj):
    return {"static_method_type": function_to_dict(obj.__func__)}


def cmethod_to_dict(obj):
    return {"class_method_type": function_to_dict(obj.__func__)}


def function_to_dict(obj):
    gls = gather_gls(obj, obj.__code__)

    return {
        "function_type": {
            "__globals__": gls,
            "__name__": obj.__name__,
            "__code__": code_to_dict(obj.__code__),
            "__defaults__": obj.__defaults__,
            "__closure__": obj.__closure__,
        }
    }


def cell_to_dict(obj):
    return {"cell_type": obj.cell_contents}


def set_to_dict(obj):
    return {"set_type": list(obj)}


def frozenset_to_dict(obj):
    return {"frozenset_type": list(obj)}


def tuple_to_dict(obj):
    return {"tuple_type": list(obj)}


def code_to_dict(obj):
    return {
        "code_type": {
            "co_argcount": obj.co_argcount,
            "co_posonlyargcount": obj.co_posonlyargcount,
            "co_kwonlyargcount": obj.co_kwonlyargcount,
            "co_nlocals": obj.co_nlocals,
            "co_stacksize": obj.co_stacksize,
            "co_flags": obj.co_flags,
            "co_code": obj.co_code,
            "co_consts": obj.co_consts,
            "co_names": obj.co_names,
            "co_varnames": obj.co_varnames,
            "co_filename": obj.co_filename,
            "co_name": obj.co_name,
            "co_firstlineno": obj.co_firstlineno,
            "co_lnotab": obj.co_lnotab,
            "co_freevars": obj.co_freevars,
            "co_cellvars": obj.co_cellvars,
        }
    }


def _dumps(obj):
    global f_found
    if obj is None:
        return "null"
    elif obj is True:
        return "true"
    elif obj is False:
        return "false"
    elif obj is float("Inf"):
        return "Infinity"
    elif obj is float("-Inf"):
        return "-Infinity"
    elif obj is float("NaN"):
        return "NaN"
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, bytes):
        return '"' + str(list(bytearray(obj))) + '"'
    elif isinstance(obj, str):
        return '"' + obj.replace("\\", "\\\\").replace('"', '\\"') + '"'
    elif isinstance(obj, set):
        return dumps_dict(set_to_dict(obj))
    elif isinstance(obj, frozenset):
        return dumps_dict(frozenset_to_dict(obj))
    elif isinstance(obj, tuple):
        return dumps_dict(tuple_to_dict(obj))
    elif isinstance(obj, list):
        return dumps_list(obj)
    elif isinstance(obj, dict):
        return dumps_dict(obj)
    elif inspect.isfunction(obj):
        res = dumps_dict(function_to_dict(obj))
        f_found = {}
        return res
    elif isinstance(obj, staticmethod):
        res = dumps_dict(smethod_to_dict(obj))
        f_found = {}
        return res
    elif isinstance(obj, classmethod):
        res = dumps_dict(cmethod_to_dict(obj))
        f_found = {}
        return res
    elif inspect.ismodule(obj):
        return dumps_dict(module_to_dict(obj))
    elif inspect.isclass(obj):
        return dumps_dict(class_to_dict(obj))
    elif is_instance(obj):
        return dumps_dict(object_to_dict(obj))
    elif isinstance(obj, types.CodeType):
        return dumps_dict(code_to_dict(obj))
    elif isinstance(obj, types.CellType):
        return dumps_dict(cell_to_dict(obj))
    else:
        raise TypeError()


def dumps(obj):
    res = _dumps(obj).replace("\n", "")
    res = res.replace('"[', '[')
    res = res.replace(']"', ']')
    return res


def dump(obj, fp):
    string = dumps(obj)
    try:
        with open(fp, "w") as file:
            file.write(string)
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")