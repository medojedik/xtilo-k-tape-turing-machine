from src.config import State, Q_Start, Q_End


def test_state_equality():
    """
    Test the equality operator for State class.
    """
    state1 = State("q1", start=True)
    state2 = State("q1", start=True)
    state3 = State("q1", start=False)
    state4 = State("q2", start=True)
    state5 = State("q1", start=True, end=True)

    assert state1 == state2, "States with same name and attributes should be equal"
    assert state1 != state3, "States with same name but different attributes should not be equal"
    assert state1 != state4, "States with different names should not be equal"
    assert state1 != state5, "States with same name but different end attribute should not be equal"


def test_fixed_states():
    """
    Test the fixed states Q_Start and Q_End.
    """
    assert Q_Start.name == "q_start", "Q_Start should have the name 'q_start'"
    assert Q_Start.start is True, "Q_Start should be a start state"
    assert Q_Start.end is False, "Q_Start should not be an end state"

    assert Q_End.name == "q_end", "Q_End should have the name 'q_end'"
    assert Q_End.start is False, "Q_End should not be a start state"
    assert Q_End.end is True, "Q_End should be an end state"


def test_state_str():
    """
    Test the string representation of State class.
    """
    state = State("q_test", start=True, end=False)
    assert str(state) == "q_test", "String representation of State should return its name"