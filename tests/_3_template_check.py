"""This module explains the template_check decorator"""

import tc

"""
tc.template_check(function): f(*, **) ⟼ f(*, **)
"""

"""
This function (mostly used as a decorator) allows you
to ensure argument types at runtime. 
"""

def error(func, args, ty):
    try:
        func(args)
        return False
    except BaseException as e:
        return isinstance(e, ty)


if "simple example":
    @tc.template_check
    def add_ints(x: int, y: int):
        return x + y


    assert add_ints(3, 5) == 8
    assert error(add_ints, ("a", "b"), tc.CheckFailed)
    assert add_ints(True, False) == 1


if "compose templates to perform checks instead of using if":
    ProperInt = tc.product(int, tc.complement(bool))

    @tc.template_check
    def add_ints(x: ProperInt, y: ProperInt):
        return x + y

    assert add_ints(3, 5) == 8
    assert error(add_ints, ("a", "b"), tc.CheckFailed)
    assert error(add_ints, (True, False), tc.CheckFailed)
    