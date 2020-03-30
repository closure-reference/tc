from inspect import getfullargspec as arg_spec
from tc import check
from tc.inner.check_failed import CheckFailed
from functools import wraps


def template_check(func):
    """Add template checking behaviour to a function"""
    spec = arg_spec(func)
    arg_names = spec.args
    default_args = {name: arg for name, arg in zip(arg_names[len(spec.defaults or ()):], spec.defaults or ())}
    templates = {**{arg: object for arg in arg_names}, **spec.annotations}

    def failing_value(args, kwargs):
        full_kwargs = {**default_args,
                       **{name: arg
                          for name, arg in zip(arg_names, args)},
                       **kwargs}

        if len(full_kwargs) != len(spec.args):
             return ("Incorrect number of arguments", (args, kwargs))

        for name, arg in full_kwargs.items():
            template = templates[name]
            if not check(template, arg):
                return (template, arg)
        return None

    @wraps(func)
    def new_fn(*args, __do_check=True, **kwargs):
        failing = __do_check and failing_value(args, kwargs)
        if not failing:
            return func(*args, **kwargs)
        else:
            raise CheckFailed(*failing)

    new_fn.failing_value = failing_value

    return new_fn
