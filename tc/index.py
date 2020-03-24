"Template checking"

from functools import wraps

from inspect import getfullargspec as arg_spec

from checkers import checkers, Either, Record, DictOf


def check_value(template, value):
    for ty, checker in checkers.items():
        if isinstance(template, ty) and checker(template, value, check_value):
                return True
    return False
             


def check(func):
    templates = arg_spec(func).annotations
    @wraps(func)
    def new_fn(*args, **kwargs):
        return 


class CheckFailed(TypeError):
    pass
