from tc.check import check

def template_filter(template, iterable):
    for i in iterable:
        if check(template, i):
            yield i
