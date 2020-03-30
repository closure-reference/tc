from tc.inner.checkers import Either, Record, Suprecord, Extend, DictOf, MessageWrapper, Product, Not, Exact
from tc.check import check
from tc.template_check import template_check
from tc.md import multiple_dispatch

def overload(parent=None):
    return lambda fn: multiple_dispatch(parent)(template_check(fn))

def record(**spec): #V
    return Record(spec)

def suprecord(**spec): #V
    return Suprecord(spec)

def product(*components): #V
    return Product(components)

def either(*options): #V
    return Either(options)

def dict_of(*options):
    return DictOf(options)

def exact(base): #V
    return Exact(base)

def extend(base, f): #V
    return wrap_base(base, lambda b: Extend(b, f))

def complement(base): #V
    return wrap_base(base, Not)



@overload()
def wrap_base(base, f):
    return f(base)

@overload()
def wrap_base(base: MessageWrapper, f):
    return MessageWrapper(f(base.base), base.on_fail)



@overload()
def msg(base, on_fail):
    return MessageWrapper(base, on_fail)

@overload()
def msg(base: MessageWrapper, on_fail):
    return MessageWrapper(base.base, on_fail)



@overload()
def match(spec: [tuple, list], fallback=None):
    def select(arg):
        for template, value in spec:
            if check(template, arg):
                return value
        else:
            return fallback
    return select

@overload()
def match(spec: dict, fallback=None):
    return match(spec.items(), fallback)



def container(*args, **kwargs):
    return args, kwargs


def apply(fn, container_result, *extra_args, **extra_kwargs):
    args, kwargs = container_result
    return fn(*args, *extra_args, **kwargs, **extra_kwargs)



@overload()
def dichotomy(base): #V
    return base, complement(base)

@overload()
def dichotomy(base, criterion): #V
    true = extend(base, criterion)
    false = extend(base, lambda x: not criterion(x))
    return true, false