"""This module demonstrates what templates there are in tc"""

import tc


if "Python types":
    assert tc.check(int, 1)
    assert tc.check(tuple, ())


if "None":
    assert tc.check(None, None)
    """
    None ≡ {None}
    """


if "tuple":
    assert tc.check((int, str), (4, "string"))
    assert tc.check((), ())
    """
    (T1, T2, ...) ≡ {(x1, x2, ...) | x(i) ∈ T(i)}
    """


if "list":
    assert tc.check([int], [1, 2, 3, 4])
    assert tc.check([int, float], [1, 2.5, 3.14, 4])
    assert tc.check([(int, float)], [(1, 2.5), (3, 4.14), (5, 0.5)])
    assert tc.check([], [])
    """
    [T1, T2, ...] ≡ {[x1, x2...] | x(i) ∈ either(T(j))}
    """


if "dict":
    assert tc.check({str: int}, {"a": 1, "b": 2})
    assert tc.check({str: int, (str, str): int}, {"a": 1, "b": 2, ("c", "d"): 3})
    assert tc.check({}, {})
    """
    {K(i): V(i)} ≡ {{k1: v1, k2: v2, ...) | (k(i), v(i)) ∈ either((K(j), V(j) }
    """


if "tc.exact":
    assert tc.check(tc.exact(42), 42)
    assert tc.check(tc.exact(int), int)
    """
    exact(v) ≡ {x | x == v}
    """


if "tc.either":
    Number = tc.either(int, float, complex)
    assert tc.check(Number, 10)
    assert tc.check(Number, 10.5)
    assert tc.check(Number, 1+2j)
    """
    either(T1, T2, ...) ≡ T1 ∪ T2 ∪ ... 
    """


if "tc.product":
    EqualToOne = tc.exact(1)
    Real = tc.either(int, float)
    RealOne = tc.product(EqualToOne, Real)
    assert tc.check(RealOne, 1)
    assert tc.check(RealOne, 1.0)
    assert not tc.check(RealOne, 1+0j)
    """
    product(T1, T2, ...) ≡ T1 ∩ T2 ∩ ...
    """


if "tc.extend":
    PositiveInt = tc.extend(int, lambda x: x > 0)
    assert tc.check(PositiveInt, 100)
    assert not tc.check(PositiveInt, 0)
    assert not tc.check(PositiveInt, -100)
    assert not tc.check(PositiveInt, "not an int")
    """
    extend(T, f: (T ⟹ bool)) ≡ {x ∈ T | f(x)}
    """


if "tc.complement":
    NotNumbers = tc.complement(int)
    assert tc.check(NotNumbers, "string")
    assert not tc.check(NotNumbers, 255)

    ProperInt = tc.product(int, tc.complement(bool))
    assert tc.check([int], [True, False])
    assert tc.check([int], [1, 2, 3])

    assert not tc.check([ProperInt], [True, False])
    assert tc.check([ProperInt], [1, 2, 3])
    r"""
    complement(T) ≡ object \ T
    """


if "tc.record":
    user = tc.record(
        username= str,
        age= int
    )
    assert tc.check(user, {"username": "bob", "age": 23})
    assert not tc.check(user, {"username": "bob"})
    assert not tc.check(user, {"username": "bob", "age": 23, "status": "inactive"})
    """
    record(K(i)=T(i)) ≡ {x | x[K(i)] ∈ T(i) and x.keys = K }
    """


if "tc.suprecord":
    with_coordinates = tc.suprecord(
        x= int,
        y= int
    )
    assert tc.check(with_coordinates, {"x": 4, "y": 5})
    assert not tc.check(with_coordinates, {"x": 4})
    assert tc.check(with_coordinates, {"x": 1, "y": 2, "z": 3})
    """
    suprecord(K(i)=T(i)) ≡ {x | x[K(i)] ∈ T(i) and x.keys ⊆ K }
    """


if "tc.dichotomy/1":
    String, NonString = tc.dichotomy(str)

    assert tc.check(String, "aaa")
    assert tc.check(NonString, 123)

    """
    dichotomy(T) ≡ (T, complement(T))
    """


if "tc.dichotomy/2":
    PositiveInt, NonPositiveInt =\
        tc.dichotomy(
            int,
            lambda x: x > 0
        )

    assert tc.check(PositiveInt, 4)
    assert not tc.check(PositiveInt, 0)

    assert tc.check(NonPositiveInt, -4)
    assert tc.check(NonPositiveInt, 0)

    """
    dichotomy(T, f) ≡ ( extend(T, f), extend(T, x ⟼ ¬f(x)) )
    dichotomy(T, f) ≡ ( extend(T, f), T \ extend(T, f) )
    """


