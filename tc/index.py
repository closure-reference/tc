"Template checking"

from functools import wraps

from inspect import getfullargspec as arg_spec

try:
    from checkers import checkers, Either, Record, DictOf
except ImportError:
    from .checkers import checkers, Either, Record, DictOf


def either(*options):
    return Either(options)

def dict_of(*options):
    return DictOf(options)


def check_value(template, value):
    for ty, checker in checkers.items():
        if isinstance(template, ty) and checker(template, value, check_value):
                return True
    return False
             


def tc(func):
    spec = arg_spec(func)
    arg_names = spec.args
    templates = {**{arg: object for arg in arg_names}, **spec.annotations}

    @wraps(func)
    def new_fn(*args, **kwargs):
        full_kwargs = {**{name: arg
                          for name, arg in zip(arg_names, args)},
                       **kwargs}

        for name, arg in full_kwargs.items():
            if not check_value(templates[name], arg):
                raise CheckFailed

        return func(*args, **kwargs)

    return new_fn



class CheckFailed(TypeError):
    pass
