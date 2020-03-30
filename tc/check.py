from tc.inner.checkers import checkers_dict

def check(template, value) -> bool:
    """Test a value against a template"""
    template_type = type(template)
    if template_type in checkers_dict:
        return checkers_dict[template_type](template, value, check)

    for ty, checker in checkers_dict.items():
        if isinstance(template, ty):
            return checker(template, value, check)

    return False