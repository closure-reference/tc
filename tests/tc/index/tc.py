def test(t, m):

    tc = m["tc"]
    CheckFailed = m["CheckFailed"]
    either = m["either"]
    Record = m["Record"]


    with t("given an annotationless function f(x, y, z)"):
        @tc
        def f(x, y, z):
            return x + y + z
        t(
            matcher= "plain",
            it= "don't change its behaviour",
            i= f(1, 2, 3),
            e=6
        )

    with t("use annotations as templates (type hints)"):
        with t("works with simple types"):
            with t("add_ints(x: int, y: int, z: int)"):
                @tc
                def add_ints(x: int, y: int, z: int):
                    return x + y + z
                t(
                    matcher= "plain",
                    it= "add_ints(1, 2, 3) is 6",
                    i= add_ints(1, 2, 3),
                    e= 6
                )(
                    matcher= "plainerror",
                    it= "add_ints('a', 'b', 'c') raises CheckFailed",
                    i= lambda: add_ints('a', 'b', 'c'),
                    e= CheckFailed
                )

            with t("answer(r: ())"):
                @tc
                def answer(r: ()):
                    return 42
                t(
                    matcher= "plain",
                    it= "answer( () ) is 42",
                    i= answer( () ),
                    e= 42
                )(
                    matcher= "plainerror",
                    it= "answer( 'question' ) raises CheckFailed",
                    i= lambda: answer( 'question' ),
                    e= CheckFailed
                )

        with t("works with compound types"):
            with t("mul_string(s: str, number: either(int, float))"):
                @tc
                def mul_string(s: str, number: either(int, float)):
                    from math import floor
                    return s * floor(number)
                t(
                    matcher= "plain",
                    it= "mul_string('hi', 4) is 'hihihihi'",
                    i= mul_string('hi', 4),
                    e= 'hihihihi'
                )(
                    matcher= "plain",
                    it= "mul_string('hello', 3.14) is 'hihihi'",
                    i= mul_string('hi', 3.14),
                    e= 'hihihi'
                )(
                    matcher= "plainerror",
                    it= "mul_string('hi', 'five') raises CheckFailed",
                    i= lambda: mul_string('hi', 'five'),
                    e= CheckFailed
                )
            with t("get_age(person: Record({'name': str, 'age': either(int, (float, float))}))"):
                @tc
                def get_age(person: Record({
                                            "name": str,
                                            "age": either(int, (float, float))
                                            })):
                    if isinstance(person["age"], int):
                        return person["age"]
                    else:
                        return complex(*person["age"])
                    
                t(
                    matcher= "plain",
                    it= "get_age({'name': 'John', 'age': 666}) is 666",
                    i= get_age({'name': 'John', 'age': 666}),
                    e= 666
                )(
                    matcher= "plain",
                    it= "get_age({'age': 666, 'name': 'John'}) is 666",
                    i= get_age({'name': 'John', 'age': 666}),
                    e= 666
                )(
                    matcher= "plain",
                    it= "get_age({'name': 'John', 'age': (1.0, 5.3)}) is 1.0+5.3j",
                    i= get_age({'name': 'John', 'age': (1.0, 5.3)}),
                    e= 1.0+5.3j
                )(
                    matcher= "plainerror",
                    it= "get_age({'name': 'John', 'age': 'nine'}) raises CheckFailed",
                    i= lambda: get_age({'name': 'John', 'age': 'nine'}),
                    e= CheckFailed
                )(
                    matcher= "plainerror",
                    it= "get_age({'name': 'John', 'age': 9, 'job': 'programmer'}) raises CheckFailed",
                    i= lambda: get_age({'name': 'John', 'age': 9, 'job': 'programmer'}),
                    e= CheckFailed
                )(
                    matcher= "plainerror",
                    it= "get_age({'name': 'John'}) raises CheckFailed",
                    i= lambda: get_age({'name': 'John'}),
                    e= CheckFailed
                )
