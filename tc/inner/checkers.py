from collections import namedtuple

Either = namedtuple("Either", ["options"])
Record = namedtuple("Record", ["obj"])
Product = namedtuple("Product", ["components"])
Suprecord = namedtuple("Suprecord", ["obj"])
DictOf = namedtuple("DictOf", ["kv_pairs"])
Extend = namedtuple("Extend", ["base", "ensure"])
MessageWrapper = namedtuple("MessageWrapper", ["base", "on_fail"])
Not = namedtuple("Not", ["base"])
Exact = namedtuple("Exact", ["base"])

checkers_dict = {}

def checker(ty):
    def _(fn):
        checkers_dict[ty] = fn
    return _


@checker(type(None))
def checker_type(template, value, check_value):
    return (value is None)


@checker(type)
def checker_type(template, value, check_value):
    return isinstance(value, template)


@checker(tuple)
def checker_tuple(template, value, check_value):
    return (
        isinstance(value, tuple)
        and all(
                check_value(subtemp, subvalue)
                for subtemp, subvalue in zip(template, value)
            )
    )


@checker(list)
def checker_list(template, value, check_value):
    template = Either(template)
    return (
        isinstance(value, list)
        and all(
            check_value(template, subvalue)
            for subvalue in value
        )
    )


@checker(dict)
def checker_dict(template, value, check_value):
    return (
        isinstance(value, dict)
        and check_value(DictOf((*template.items(),)), value)
    )


@checker(Not)
def checker_complement(template, value, check_value):
    template = template.base
    return (not check_value(template, value))


@checker(Either)
def checker_either(template, value, check_value):
    return any(
        check_value(subtemp, value)
        for subtemp in template.options
    )


@checker(Product)
def checker_product(template, value, check_value):
    return all(
        check_value(subtemp, value)
        for subtemp in template.components
    )


@checker(Record)
def checker_record(template, value, check_value):
    if not isinstance(value, dict):
        return False
    elif template.obj.keys() != value.keys():
        return False
    else:
        return all(
            check_value(template.obj[key], value[key])
            for key in template.obj
        )


@checker(Suprecord)
def checker_suprecord(template, value, check_value):
    if not isinstance(value, dict):
        return False
    elif any((key not in value) for key in template.obj):
        return False
    else:
        return all(
            check_value(template.obj[key], value[key])
            for key in template.obj
        )


@checker(DictOf)
def checker_dictof(template, value, check_value):
    if not isinstance(value, dict):
        return False
    else:
        kv_pair_template = Either(template.kv_pairs)
        return all(
            check_value(kv_pair_template, (key, subvalue))
            for key, subvalue in value.items()
        )


@checker(Extend)
def checker_extend(template, value, check_value):
    return check_value(template.base, value) and template.ensure(value)


@checker(MessageWrapper)
def checker_message_wrapper(template, value, check_value):
    template = template.base
    return check_value(template, value)

@checker(Exact)
def checker_exact(template, value, check_value):
    template = template.base
    return (template == value)
