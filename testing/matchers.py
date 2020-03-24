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
