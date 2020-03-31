"""This module explains overload --- the most important function in this module"""

import tc

"""
tc.overload(): () ⟼ f(*, **) ⟼ f(*, **)
tc.overload(parent): parent ⟼ f(*, **) ⟼ f(*, **) 

(it actually returns a `MultipleDispatch` object,
but from a logical point of view it returns a function)

This function (also used as a decorator) allows you to
write different function implementations for different
argument configurations. 
"""

def error(func, args, ty):
    try: func(args); return False
    except BaseException as e: return isinstance(e, ty)

if "supports variable argument count":
    @tc.overload()
    def add(x):
        return x

    @tc.overload()
    def add(x, y):
        return x + y

    assert add(7) == 7
    assert add(7, 2) == 9

    del add # this is only required here because I'll define another `add` later


if "supports different template signatures via type hints":
    @tc.overload()
    def type_of(x: int):
        return "integer"

    @tc.overload()
    def type_of(x: str):
        return "string"

    assert type_of(5) == "integer"
    assert type_of("abc") == "string"
    assert error(type_of, (3.14,), tc.CheckFailed)

    del type_of


if "supports a combination of those":
    @tc.overload()
    def add(x: (int, int)):
        return x[0] + x[1]

    @tc.overload()
    def add(x: int, y: int):
        return x + y

    assert add((7, 2)) == 9
    assert add(7, 2) == 9
    assert error(add, ("a", "b"), tc.CheckFailed)

    del add


if "supports all the complex templates that other functions support":
    UID = tc.extend(int, lambda x: x > 0)
    User = tc.record(uid=UID, name=str)
    alice = {"uid": 1, "name": "alice"}
    bob = {"uid": 2, "name": "bob"}
    database = {1: alice, 2: bob}


    def get_users_by_name(name):
        return filter(
            lambda user: user["name"] == name,
            database.values()
        )

    if "version 1":
        @tc.overload()
        def get_user(user: User):
            return user

        @tc.overload()
        def get_user(uid: UID):
            if uid in database:
                return database[uid]
            else:
                return None

        @tc.overload()
        def get_user(name: str):
            matching = list(get_users_by_name(name))
            if matching:
                return matching[0]
            else:
                return None

        assert get_user(1) is alice
        assert get_user(2) is bob

        assert get_user("alice") is alice
        assert get_user("bob") is bob

        assert get_user(alice) is alice
        assert get_user(bob) is bob

        assert get_user(25) is None
        assert get_user("admin") is None
        assert error(get_user, (123, 456), tc.CheckFailed)

        del get_user


    if "version 2":
        # Version 1 still uses an explicit if. We can change that.
        ExistingUID, MissingUID = \
            tc.dichotomy(
                UID,
                lambda name: name in database
            )

        ExistingName, MissingName = \
            tc.dichotomy(
                str,
                lambda name: any(get_users_by_name(name))
            )


        @tc.overload()
        def get_user(user: User):
            return user

        @tc.overload()
        def get_user(uid: MissingUID):
            return None

        @tc.overload()
        def get_user(uid: ExistingUID):
            return database[uid]

        @tc.overload()
        def get_user(name: MissingName):
            return None

        @tc.overload()
        def get_user(name: ExistingName):
            return next(get_users_by_name(name))


        assert get_user(1) is alice
        assert get_user(2) is bob

        assert get_user("alice") is alice
        assert get_user("bob") is bob

        assert get_user(alice) is alice
        assert get_user(bob) is bob

        assert get_user(25) is None
        assert get_user("admin") is None
        assert error(get_user, (123, 456), tc.CheckFailed)

        del get_user


    if "version 3":
        # However, in this case, `match` would probably be better.
        # `overload` is more useful if:
        #   1) a single case doesn't or can't fit inside a lambda
        #   2) you only have 2 or 3 options
        #   3) you want to dynamically overload a function [I never used this yet]

        def get_user(user):
            return tc.match([
                (User,         lambda u: user),
                (ExistingName, lambda u: next(get_users_by_name(u))),
                (MissingName,  lambda u: None),
                (ExistingUID,  lambda u: database[u]),
                (MissingUID,  lambda u: None),
            ],      fallback=  lambda u: None
            )(user)(user)


        assert get_user(1) is alice
        assert get_user(2) is bob

        assert get_user("alice") is alice
        assert get_user("bob") is bob

        assert get_user(alice) is alice
        assert get_user(bob) is bob

        assert get_user(25) is None
        assert get_user("admin") is None

        del get_user


    if "example 2":
        # This is a bit naive, but still good usage of overload
        import os, re, requests

        def Regexp(regexp):
            return tc.extend(str, re.compile(regexp).fullmatch)

        URLExternal =\
            Regexp(
                r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
            )

        URLLocal =\
            Regexp(
                r"^(?!http[s]?://)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
            )

        @tc.overload()
        def file_contents(url: URLExternal):
            return requests.get(url).text

        @tc.overload()
        def file_contents(url: URLLocal):
            with open(os.path.join("server/", url)) as file:
                return file.read()