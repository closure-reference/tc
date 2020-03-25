from collections import namedtuple


Either = namedtuple("Either", ["options"])
Product = namedtuple("Product", ["components"])
Record = namedtuple("Record", ["obj"])
Suprecord = namedtuple("Suprecord", ["obj"])
DictOf = namedtuple("DictOf", ["kv_pairs"])
Extend = namedtuple("Extend", ["base", "ensure"])
MessageWrapper = namedtuple("MessageWrapper", ["base", "on_fail"])

checkers = {}

def checker(ty, check_for_type=True):
    if check_for_type is True:
        type_checker = lambda v: isinstance(v, ty)
    elif isinstance(check_for_type, type):
        type_checker = lambda v: isinstance(v, check_for_type)
    else:
        type_checker = lambda v: True
        
    def _(fn):
        checkers[ty] = (lambda template, value, check_value:
                            fn(template, value, check_value)
                            if type_checker(value)
                            else False
                        )
    return _


@checker(type, check_for_type=False)
def _(template, value, check_value):
    return isinstance(value, template)


@checker(tuple)
def _(template, value, check_value):
    return all(
        check_value(subtemp, subvalue)
        for subtemp, subvalue in zip(template, value)
    )


@checker(list)
def _(template, value, check_value):
    template = Either(template)
    return all(
        check_value(template, subvalue)
        for subvalue in value
    )


@checker(dict)
def _(template, value, check_value):
    return check_value(DictOf((*template.items(),)), value)


@checker(Either, check_for_type=False)
def _(template, value, check_value):
    return any(
        check_value(subtemp, value)
        for subtemp in template.options
    )


@checker(Product, check_for_type=False)
def _(template, value, check_value):
    return all(
        check_value(subtemp, value)
        for subtemp in template.components
    )


@checker(Record, check_for_type=dict)
def _(template, value, check_value):
    if template.obj.keys() != value.keys():
        return False
    else:
        return all(
            check_value(template.obj[key], value[key])
            for key in template.obj
        )    


@checker(Suprecord, check_for_type=dict)
def _(template, value, check_value):
    if any((key not in value) for key in template.obj):
        return False
    else:
        return all(
            check_value(template.obj[key], value[key])
            for key in template.obj
        )        


@checker(DictOf, check_for_type=dict)
def _(template, value, check_value):
    kv_pair_template = Either(template.kv_pairs)
    return all(
        check_value(kv_pair_template, (key, subvalue))
        for key, subvalue in value.items()
    )


@checker(Extend, check_for_type=False)
def _(template, value, check_value):
    return check_value(template.base, value) and template.ensure(value)


@checker(MessageWrapper, check_for_type=False)
def _(template, value, check_value):
    template = template.base
    return check_value(template, value)


@checker(object, check_for_type=False)
def _(template, value, check_value):
    return (value == template)