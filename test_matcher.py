import matcher

def test_simple_match():
    matches = matcher.GetMatches("I like to use [[bulbasaur]]")
    assert matches == ["[[bulbasaur]]"]

    matches = matcher.GetMatches("I like to use [[bulbasaur]] and [[charizard ex]]")
    assert matches == ["[[bulbasaur]]", "[[charizard ex]]"]

def test_matcher_with_filters():
    matches = matcher.GetMatches("I use [[oricorio+type=lightning]]")
    assert matches == ["[[oricorio+type=lightning]]"]

    matches = matcher.GetMatches("I use [[oricorio+type={L}}]]")
    assert matches == ["[[oricorio+type={L}}]]"]

    matches = matcher.GetMatches("I use [[oricorio+set=A3+type={P}]]")
    assert matches == ["[[oricorio+set=A3+type={P}]]"]
