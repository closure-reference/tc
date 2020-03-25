"Template checking"

from functools import wraps

from inspect import getfullargspec as arg_spec

try:
    from checkers import checkers, Either, Record, Suprecord, Extend, DictOf, MessageWrapper, Product
except ImportError:
    from .checkers import checkers, Either, Record, Suprecord, Extend, DictOf, MessageWrapper, Product

def product(*components):
    return Product(components)

def either(*options):
    return Either(options)

def dict_of(*options):
    return DictOf(options)

def msg(base, on_fail):
    if isinstance(base, MessageWrapper):
        return MessageWrapper(base.base, on_fail)
    else:
        return MessageWrapper(base, on_fail)

def extend(base, f):
    if isinstance(base, MessageWrapper):
        return MessageWrapper(Extend(base.base, f), base.on_fail)
    else:
        return Extend(base, f)


def check_value(template, value) -> bool:
    "Test a value against a template"
    for ty, checker in checkers.items():
        if isinstance(template, ty) and checker(template, value, check_value):
                return True
    return False
             


def tc(func):
    "Add template checking behaviour to a function"
    spec = arg_spec(func)
    arg_names = spec.args
    templates = {**{arg: object for arg in arg_names}, **spec.annotations}

    @wraps(func)
    def new_fn(*args, **kwargs):
        full_kwargs = {**{name: arg
                          for name, arg in zip(arg_names, args)},
                       **kwargs}

        for name, arg in full_kwargs.items():
            template = templates[name]
            if not check_value(template, arg):
                raise CheckFailed(template, arg)

        return func(*args, **kwargs)

    return new_fn



class CheckFailed(TypeError):
    def __init__(self, template, value):
        if isinstance(template, MessageWrapper):
            self.fail_message = template.on_fail(value)
        else:
            self.fail_message = template
        self.value = value

    def __str__(self):
        return f"{self.fail_message}: {repr(self.value)}"

    def __repr__(self):
        return "CheckFailed(" + repr(self.fail_message) + ", " + repr(self.value) + ")"
