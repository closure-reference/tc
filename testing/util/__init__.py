def exported(module):
    return {name: getattr(module, name)
            for name in dir(module)
            if not name.startswith("_")}
