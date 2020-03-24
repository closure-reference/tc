import inspect


def _(f):
    matcher_name = f.__qualname__
    params = inspect.getfullargspec(f).kwonlyargs

    def new_f(subject, test):
        test = {k: test[k] for k in test if k != "matcher"}
        return f(subject, **test)

    def detect(test):
        return (
            test.get("matcher", "default") == matcher_name
            and all((param in test) for param in params)
        )

    return {
        "f": new_f,
        "detect": detect
    }
