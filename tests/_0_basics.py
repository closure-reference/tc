"""This module shows some trivial use cases of the tc.check function"""

"""
tc.check(template, value) -> bool

Returns whether the value fits the template.
"""

import tc

# First of all, types can be templates
assert tc.check(int, 1)
assert tc.check(tuple, ())

"""
From a mathematical point of view, types represent sets,
that is, collections of elements that satisfy a certain criterion.
In OOP (usually) type ≡ class, so to avoid confusion,
I will call these things "templates".
    
A template describes a set of values.
For instance:
    all integers greater than 0: 
        tc.extend(int, lambda x: x > 0)
        
    all objects that are either an int or a string:
        tc.either(int, str)
        
    all objects which are not integers:
        tc.complement(int)
        
    all objects which are Female and Admin:
        tc.product(Female, Admin)
        
    all either floating or complex numbers different from zero
        tc.extend(
            either(float, complex),
            lambda x: x != 0
        )
        
    all objects which are both an int and not an int (hint: there are no such objects, thus is's an empty set):
        tc.product(
            int,
            complement(int)
        )
        


/-----Template syntax (in this case -- a type)
V
T ≡ {x | x ∈ T}
      ^
      \---Set builder notation:
            all x's which satisfy condition: x ∈ T (x belongs to T) 
Together, this notation means:
    a template notation which is: (T), where T is a 
    describes all 

Conventions:
    T, U, V --- templates
    a, b, c --- ordinary values  
    
"""


# `None` is a template as well
assert tc.check(None, None)
"""
None ≡ {None}
        ^------Set enumeration notation
                (e. g. {1, 2, 3} ≡ {x | (x = 1) or (x = 2) or (x = 3)})
"""


# tc.exact checks for the exact value
assert tc.check(tc.exact(42), 42)
assert tc.check(tc.exact(int), int)
"""
exact(v) = {x | x == v}
"""

