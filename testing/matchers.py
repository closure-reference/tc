from .add_matcher import _


@_
def default(s, *, it, i, e):
    return {
        "title": it,
        "expected": e,
        "actual": s(*i)
    }


@_
def plain(s, *, it, i, e):
    return {
        "title": it,
        "expected": e,
        "actual": i
    }


@_
def compare(s, *, it, e):
    return {
        "title": it,
        "expected": e,
        "actual": s
    }


@_
def error(s, *, it, i, e):
    try:
        result = s(*i)
    except Exception as exc:
        return {
            "title" : it,
            "expected": e,
            "actual": type(exc)
        }
    else:
        return {
            "title": it,
            "expected": e,
            "actual": ["no error", result]
        }

@_
def plainerror(s, *, it, i, e):
    try:
        result = i()
    except Exception as exc:
        return {
            "title" : it,
            "expected": e,
            "actual": type(exc)
        }
    else:
        return {
            "title": it,
            "expected": e,
            "actual": ["no error", result]
        }
