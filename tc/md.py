"Multiple dispatch with templates"

import inspect
from functools import wraps

class MultipleDispatch:
    def __init__(self, name, fallback):
        self.functions = []
        self.name = name
        self.fallback = fallback

    def __call__(self, *args, **kwargs):
        fallback, fn = self.get(args, kwargs)
        return fn(*args, __do_check=fallback, **kwargs)

    def get(self, args, kwargs):
        for func in reversed(self.functions):
            if not func.failing_value(args, kwargs):
                return (False, func)
        return (True, self.fallback)

    def add(self, func):
        self.functions.append(func)

    def __repr__(self):
        return f"md::{self.name}"


def multiple_dispatch(parent=None):
    frame = inspect.getouterframes(inspect.currentframe())[2]
    names = {**frame.frame.f_globals, **frame.frame.f_locals}
    def _(fn):
        nonlocal parent
        if parent is None:
            if fn.__name__ in names:
                parent = names[fn.__name__]
            else:
                return MultipleDispatch(fn.__name__, fn)
        parent.add(fn)
        return parent
    return _


