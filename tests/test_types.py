from utlz.types import SimpleEnum, EnumeratedEnum, Enum


def test_simple_enum():
    states = SimpleEnum(STATE_0=0, STATE_1=1, STATE_2=2, STATE_3=3,
                        STATE_123=123)

    assert isinstance(states, object)
    assert str(states) == "<class 'utlz.types.SimpleEnum'>"

    assert states.STATE_1 == 1
    assert states.STATE_2 == 2
    assert states.STATE_3 == 3
    assert states.STATE_123 == 123


def test_enumerated_enum():
    states = EnumeratedEnum('STATE_0', 'STATE_1', 'STATE_2', 'STATE_3',
                            STATE_123=123)

    assert isinstance(states, object)
    assert str(states) == "<class 'utlz.types.EnumeratedEnum'>"

    assert states.STATE_0 == 0
    assert states.STATE_1 == 1
    assert states.STATE_2 == 2
    assert states.STATE_3 == 3
    assert states.STATE_123 == 123


def test_named_enum():
    states = Enum('STATE_0', 'STATE_1', 'STATE_2', 'STATE_3', STATE_123=123)

    assert isinstance(states, object)
    assert str(states) == "<class 'utlz.types.Enum'>"

    assert states.STATE_0 == 0
    assert states.STATE_1 == 1
    assert states.STATE_2 == 2
    assert states.STATE_3 == 3
    assert states.STATE_123 == 123

    assert states.reverse == {
        0: 'STATE_0',
        1: 'STATE_1',
        2: 'STATE_2',
        3: 'STATE_3',
        123: 'STATE_123',
    }
