"""
Test for computing sum of binary numbers separated by blank symbols.

This 3-tape Turing machine computes the sum of multiple binary numbers.
Input format: binary numbers separated by blank symbols (e.g., "111#10#101")
Output: The sum stored on tape 3 in binary format

Algorithm:
1. Copy first number from T1 to T2
2. Copy next number from T1 to T3
3. Add T2 + T3, store result on T3
4. Copy next number from T1 to T2
5. Repeat steps 3-4 until all numbers processed
"""

import pytest

import src.actions as act
from src.config import B, Q_End, Q_Start, State
from src.turing_mapping import Head, Rule, Tape, TuringMachine


class TestBinarySum:
    """Test 3-tape Turing machine for summing binary numbers"""

    @pytest.fixture
    def sum_machine_rules(self):
        """Define rules for binary sum computation"""
        # State definitions
        q1 = State("q1")  # Copying first number to T3
        q2 = State("q2")  # Adding T2 + T3
        q3 = State("q3")  # Handling carry bit
        q4 = State("q4")  # Returning to start of T2
        q5 = State("q5")  # Check if more numbers to process
        q6 = State("q6")  # Copying next number to T2
        q7 = State("q7")  # Moving T3 to end for next addition

        # Phase 1: Copy first number from T1 to T2
        copy_first_to_t2 = [
            Rule(Q_Start, Q_Start, actions=[act.R11, act.RB1, act.SWW]),  # Read 1, write 1 to T2
            Rule(Q_Start, Q_Start, actions=[act.R00, act.RB0, act.SWW]),  # Read 0, write 0 to T2
            Rule(Q_Start, q1, actions=[act.RBB, act.LWW, act.SWW]),  # End of 1st number, mv to T3
        ]

        # Phase 2: Copy next number from T1 to T3
        copy_next_to_t3 = [
            Rule(q1, q1, actions=[act.R11, act.SWW, act.RB1]),  # Read 1, write 1 to T3
            Rule(q1, q1, actions=[act.R00, act.SWW, act.RB0]),  # Read 0, write 0 to T3
            Rule(q1, q2, actions=[act.RBB, act.SWW, act.LWW]),  # End of number, start addition
        ]

        # Phase 3: Add T2 + T3, store result on T3
        add_t2_t3 = [
            # Add without carry
            Rule(q2, q2, actions=[act.SWW, act.L0B, act.L00]),  # T2=0, T3=0: result 0
            Rule(q2, q2, actions=[act.SWW, act.L0B, act.L11]),  # T2=0, T3=1: result 1
            Rule(q2, q2, actions=[act.SWW, act.L0B, act.LB0]),  # T2=0, T3=blank: result 0
            # Add with potential carry
            Rule(q2, q2, actions=[act.SWW, act.L1B, act.L01]),  # T2=1, T3=0: result 1
            Rule(q2, q2, actions=[act.SWW, act.L1B, act.LB1]),  # T2=1, T3=blank: result 1
            Rule(q2, q3, actions=[act.SWW, act.L1B, act.L10]),  # T2=1, T3=1: result 0, carry 1
            # Handle carry propagation
            Rule(q3, q3, actions=[act.SWW, act.L10, act.SWW]),  # Carry: T3=1 becomes 0, continue
            Rule(q3, q4, actions=[act.SWW, act.R01, act.SWW]),  # Carry: T3=0 becomes 1, done
            Rule(q3, q4, actions=[act.SWW, act.RB1, act.SWW]),  # Carry: T3=blank becomes 1, done
            # Return to beginning of T2 for next digit
            Rule(q4, q4, actions=[act.SWW, act.R11, act.SWW]),  # Move right on T2 past 1s
            Rule(q4, q4, actions=[act.SWW, act.R00, act.SWW]),  # Move right on T2 past 0s
            Rule(q4, q2, actions=[act.SWW, act.LBB, act.SWW]),  # Found end of T2, continue adding
            # Finished adding current number
            Rule(q2, q5, actions=[act.SWW, act.SBB, act.RWW]),  # T2 done, check for more nmbrs
        ]

        # Phase 4: Check if more numbers and copy next to T2
        recopy_next_to_t2 = [
            Rule(q5, Q_End, actions=[act.SBB, act.LWW, act.SWW]),  # No more numbers, accept
            Rule(q5, q6, actions=[act.R11, act.RB1, act.SWW]),  # Found 1, start copying to T2
            Rule(q5, q6, actions=[act.R00, act.RB0, act.SWW]),  # Found 0, start copying to T2
            Rule(q6, q6, actions=[act.R11, act.RB1, act.SWW]),  # Continue copying 1 to T2
            Rule(q6, q6, actions=[act.R00, act.RB0, act.SWW]),  # Continue copying 0 to T2
            Rule(q6, q7, actions=[act.RBB, act.LWW, act.SWW]),  # End of number, prepare T3
        ]

        # Phase 5: Move T3 head to end for next addition
        move_t3_to_end = [
            Rule(q7, q7, actions=[act.SWW, act.SWW, act.R00]),  # Move T3 right past 0s
            Rule(q7, q7, actions=[act.SWW, act.SWW, act.R11]),  # Move T3 right past 1s
            Rule(
                q7, q2, actions=[act.SWW, act.SWW, act.LBB]
            ),  # Found end of T3, start next addition
        ]

        return copy_first_to_t2 + copy_next_to_t3 + add_t2_t3 + recopy_next_to_t2 + move_t3_to_end

    @pytest.mark.parametrize(
        "input_string,expected_sum",
        [
            ("11#10", 5),
            ("1#1", 2),
            ("10#11", 5),
            ("111#10#101", 14),
            ("1#1#1", 3),
            ("100#100", 8),
            ("111#10#101#11#1011", 28),
        ],
    )
    def test_binary_sum(self, sum_machine_rules, input_string, expected_sum):
        """Test binary addition with various inputs"""
        tape1 = Tape(list(input_string))
        tape2 = Tape()
        tape3 = Tape()

        head1 = Head()
        head2 = Head()
        head3 = Head()

        tm = TuringMachine(
            rules=sum_machine_rules,
            tapes=[tape1, tape2, tape3],
            heads=[head1, head2, head3],
        )

        result = tm.run()
        result_binary = result["final_return_content"]
        result_decimal = int(result_binary, 2)

        assert result["accepted"] == True, f"Machine should accept input '{input_string}'"
        assert (
            result_decimal == expected_sum
        ), f"Expected sum {expected_sum} (binary: {bin(expected_sum)[2:]}), got {result_decimal} (binary: {result_binary})"

    def test_complex_sum(self, sum_machine_rules):
        """Test complex multi-number addition"""
        input_string = "111#10#101#11#1011"
        tape1 = Tape(self._parse_binary_string(input_string))
        tape2 = Tape()
        tape3 = Tape()

        head1 = Head()
        head2 = Head()
        head3 = Head()

        tm = TuringMachine(
            rules=sum_machine_rules,
            tapes=[tape1, tape2, tape3],
            heads=[head1, head2, head3],
        )

        result = tm.run()
        assert result, f"Machine should accept input '{input_string}'"

        # Calculate expected: 7 + 2 + 5 + 3 + 11 = 28
        expected_sum = 7 + 2 + 5 + 3 + 11
        result_binary = result["final_return_content"]
        result_decimal = self._binary_to_decimal(result_binary)

        assert result_decimal == expected_sum
