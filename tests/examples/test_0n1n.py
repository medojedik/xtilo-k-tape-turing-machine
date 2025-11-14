"""
Test for recognizing language L = {0^n 1^n | n >= 0}

This Turing machine recognizes strings with equal numbers of 0s and 1s,
where all 0s come before all 1s.
Valid: "", "01", "0011", "000111"
Invalid: "0", "1", "00110", "00111", "1100"
"""

import pytest

import src.actions as act
from src.config import Q_End, Q_Start, State
from src.turing_mapping import Head, Rule, Tape, TuringMachine


class Test0n1n:
    """Test Turing machine for language 0^n 1^n"""

    @pytest.fixture
    def turing_machine_rules(self):
        """Define the rules for 0^n 1^n recognition"""
        # State definitions
        q1 = State("q1")  # Looking for first 1
        q2 = State("q2")  # Going back to find next 0
        q3 = State("q3")  # Checking if tape is empty (accept state)

        # Rule groups for clarity
        find_first_0 = [
            Rule(Q_Start, q1, [act.R0X]),  # mark first 0 as X, move right
            Rule(Q_Start, q3, [act.RYY]),  # no more 0s, check if done
        ]

        find_left_most_1 = [
            Rule(q1, q1, [act.R00]),  # skip unmarked 0s
            Rule(q1, q1, [act.RYY]),  # skip marked 1s (Y)
            Rule(q1, q2, [act.L1Y]),  # found 1, mark as Y, go back
        ]

        find_left_most_0 = [
            Rule(q2, q2, [act.LYY]),  # move left over marked 1s
            Rule(q2, q2, [act.L00]),  # move left over unmarked 0s
            Rule(q2, Q_Start, [act.RXX]),  # found marked 0, start next iteration
        ]

        find_end_of_tape = [
            Rule(q3, q3, [act.RYY]),  # skip all marked symbols
            Rule(q3, Q_End, [act.SBB]),  # reached blank, accept
        ]

        return find_first_0 + find_left_most_1 + find_left_most_0 + find_end_of_tape

    @pytest.mark.parametrize(
        "input_string, should_accept",
        [
            ("", False),  # Empty string is not valid
            ("01", True),  # Basic valid case
            ("0011", True),  # Two pairs
            ("000111", True),  # Three pairs
            ("0", False),  # Only 0s
            ("1", False),  # Only 1s
            ("00110", False),  # Extra 0 at the end
            ("00111", False),  # Unequal count
            ("1100", False),  # Wrong order
        ],
    )
    def test_0n1n_recognition(self, turing_machine_rules, input_string, should_accept):
        """Test that the TM correctly recognizes or rejects strings"""
        print("\n\n")
        tape = Tape(list(input_string))
        head = Head()
        tm = TuringMachine(rules=turing_machine_rules, tapes=[tape], heads=[head])

        result = tm.run()
        if should_accept:
            assert result["accepted"], f"Expected '{input_string}' to be accepted"
        else:
            assert not result["accepted"], f"Expected '{input_string}' to be rejected"
