"""This module explains the match function"""

import tc

"""
tc.match( {T(i): v(i)}, fallback=None ): spec ⟼ (input ⟼ output)
tc.match( [(T(i), v(i))], fallback=None ): spec ⟼ (input ⟼ output)
"""

"""
tc.match will iterate over the (template, choice) pairs
and choose the appropriate output.

This is analogous to `case` in Erlang/Elixir.
"""

if "simple example":
    TypeIdentifier = tc.match([
                        (int, "integer"),
                        (str, "string"),
                     ])
    assert TypeIdentifier(4) == "integer"
    assert TypeIdentifier("hello") == "string"
    assert TypeIdentifier([[[]]]) is None


if "example with fallback":
    TypeIdentifierFallback = tc.match(
                                [
                                    (int, "integer"),
                                    (str, "string"),
                                ],
                                "unknown"
                             )
    assert TypeIdentifierFallback(4) == "integer"
    assert TypeIdentifierFallback("hello") == "string"
    assert TypeIdentifierFallback([[[]]]) == "unknown"


if "complex example":
    User =\
        tc.record(
            uid= int,
            is_admin= bool
        )

    Admin, NonAdmin =\
        tc.dichotomy(
            User,
            lambda user: user["is_admin"]
        )

    Page =\
        tc.record(
            uid= int,
            who_can_view= tc.either(tc.exact("anyone"), [int])
        )

    PublicPage, PrivatePage =\
        tc.dichotomy(
            Page,
            lambda page: page["who_can_view"] == "anyone"
         )


    def PrivatePageViewableBy(user):
        return tc.extend(
                    PrivatePage,
                    lambda page: user["uid"] in page["who_can_view"]
                )

    def can_user_view_page(user, page):
        return tc.match([
                [(Admin, Page), True],
                [(NonAdmin, PublicPage), True],
                [(NonAdmin, PrivatePageViewableBy(user)), True]
            ],  False
            )(
                (user, page)
            )

    alice = {"uid": 3, "is_admin": False}
    bob = {"uid": 4, "is_admin": False}
    charlie = {"uid": 5, "is_admin": False}
    admin = {"uid": 6, "is_admin": True}

    page_for_everyone =\
        {"uid": 1, "who_can_view": "anyone"}
    page_for_alice =\
        {"uid": 2, "who_can_view": [ alice["uid"] ]}
    page_for_alice_and_bob =\
        {"uid": 4, "who_can_view": [ alice["uid"], bob["uid"] ]}
    page_for_admin =\
        {"uid": 5, "who_can_view": [] }

    assert can_user_view_page(alice, page_for_everyone)
    assert can_user_view_page(bob, page_for_everyone)
    assert can_user_view_page(charlie, page_for_everyone)
    assert can_user_view_page(admin, page_for_everyone)

    assert can_user_view_page(alice, page_for_alice)
    assert not can_user_view_page(bob, page_for_alice)
    assert not can_user_view_page(charlie, page_for_alice)
    assert can_user_view_page(admin, page_for_alice)

    assert can_user_view_page(alice, page_for_alice_and_bob)
    assert can_user_view_page(bob, page_for_alice_and_bob)
    assert not can_user_view_page(charlie, page_for_alice_and_bob)
    assert can_user_view_page(admin, page_for_alice_and_bob)

    assert not can_user_view_page(alice, page_for_admin)
    assert not can_user_view_page(bob, page_for_admin)
    assert not can_user_view_page(charlie, page_for_admin)
    assert can_user_view_page(admin, page_for_admin)

    """
    These template declarations are quite verbose.
    But keep in mind that you can and you should reuse them.
    Now you can easily answer "can" and "is" questions
    without using conditionals.
    
    Pattern-matching arrays convey meaning very clearly and declaratively:
    
        admins can view anything:
            [(Admin, Page), True],
            
        non-admins can view public pages:
            [(NonAdmin, PublicPage), True],
            
        ...or private pages they're allowed to see: 
            [(NonAdmin, PrivatePageViewableBy(user)), True]
            
        otherwise,
            False
    """