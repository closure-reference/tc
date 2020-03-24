from collections import namedtuple

Either = namedtuple("Either", ["options"])
Record = namedtuple("Record", ["obj"])
DictOf = namedtuple("DictOf", ["kv_pairs"])

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


@checker(Record, check_for_type=dict)
def _(template, value, check_value):
    if template.obj.keys() != value.keys():
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