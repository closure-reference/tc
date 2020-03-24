def test(t, m):
    Either = m["Either"]
    Record = m["Record"]
    DictOf = m["DictOf"]

    with t("works for any type as template: T"):
        T = type(...)
        t(
            it= "detects ints",
            i= [int, 42],
            e= True
        )(
            it= "ignores non-ints",
            i= [int, "string"],
            e= False
        )(
            it= "beware: bool ⊂ int",
            i= [int, True],
            e= True
        )(
            it= "beware: namedtuple ⊂ tuple",
            i= [tuple, Either([int, str])],
            e= True
        )(
            it= "detects ellipsis..es?",
            i= [T, ...],
            e= True
        )(
            it= "ignores non-ellipsis..es?",
            i= [T, "not an ellipsis"],
            e= False
        )

    with t("works for tuple templates: (T1, T2, ...)"):
        t(
            it= "detects tuples (str, int)",
            i= [(str, int), ("hello", 42)],
            e= True
        )(
            it= "ignores tuples which aren't (str, int)",
            i= [(str, int), (123, 456)],
            e= False
        )(
            it= "ignores non-tuples",
            i= [(str, int), 1],
            e= False
        )(
            it= "also works with nested templates",
            i= [(str, (int, int)), ("point", (0, 5))],
            e= True
        )

    with t("works for Either templates: (Either([...]), v)"):
        t(
            it= "detects ints with Either((int, str))",
            i= [Either((int, str)), 42],
            e= True
        )(
            it= "detects strs with Either((int, str))",
            i= [Either((int, str)), "string"],
            e= True
        )(
            it= "ignores other types with Either((int, str))",
            i= [Either((int, str)), [1, "hi"]],
            e= False
        )

    with t("works for list templates: [T] || [T1, T2, ...]"):
        t(
            it= "detects lists of ints: [int]",
            i= [[int], [1, 2, 3, 4]],
            e= True
        )(
            it= "ignores lists where not everything is int: [int]",
            i= [[int], [1, 2, 3.1416, 4]],
            e= False
        )(
            it= "ignores non-lists",
            i= [[str], ...],
            e= False
        )(
            it= "also works with nested templates: [(str, int)]",
            i= [[(str, int)], [("hello", 1), ("world", 2), ("aaa", 666)]],
            e= True
        )(
            it= "multiple elements mean 'either': [int, float]",
            i= [[int, float], [1, 2.718, 3.1416, 4]],
            e= True
        )

    with t("works for Record templates: Record({key1: T, key2: T, ...})"):
        t(
            it= "detects dicts that look like: {1: str, 'yeah': [int]}",
            i= [
                Record({1: str, 'yeah': [int]}),
                {1: "hello", "yeah": [1, 2, 3]}
               ],
            e= True
        )(
            it= "ignores dicts that have extra keys",
            i= [
                Record({1: str, 'yeah': [int]}),
                {1: "hello", "yeah": [1, 2, 3], "ok": True}
               ],
            e= False
        )(
            it= "ignores dicts that are missing some keys",
            i= [
                Record({1: str, 'yeah': [int]}),
                {1: "hello"}
               ],
            e= False
        )(
            it= "ignores dicts with wrong value types",
            i= [
                Record({1: str, 'yeah': [int]}),
                {1: [[[[[]]]]], "yeah": (1, 2, 3)}
               ],
            e= False
        )(
            it= "ignores non-dicts",
            i= [Record({int: str}), (12345, "abracadabra")],
            e= False
        )

    with t("works with dict templates: {KT1: VT1, KT2: VT2, ...}"):
        t(
            it= "detects dicts that have {str: int} pairs: {str: int}",
            i= [{str: int}, {"hello": 123, "world": 456}],
            e= True
        )(
            it= "ignores dicts that have a non-{str: int} pair: {str: int}",
            i= [{str: int}, {"hello": 123, "world": 456, 789: "WRONG"}],
            e= False
        )(
            it= "as with lists, many pair means 'either': {str: int, int: str}",
            i= [{str: int, int: str}, {"hello": 123, "world": 456, 789: "ok"}],
            e= True
        )

    with t("works with DictOf templates: DictOf([(KT1, VT1), (KT2, VT2), ...])"):
        t(
            it= "DictOf is needed in case you have overlapping keys\n"
                "and you don't want to use Either: "
                "DictOf([(str, int), (str, float)])",
            i= [DictOf([(str, int), (str, float)]),
                {"hello": 123, "world": 3.14}],
            e= True
        )