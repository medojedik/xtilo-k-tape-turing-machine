from src.config import B
from src.helpers import Tape


class TestTape:
    """Test Tape class functionality"""

    def test_tape_initialization_with_input(self):
        """Test that Tape initializes correctly with input string"""
        tape = Tape(["1", "0", "1"])

        assert tape.symbols[0] == "1"
        assert tape.symbols[1] == "0"
        assert tape.symbols[2] == "1"

    def test_tape_returns_blank_for_uninitialized_positions(self):
        """Test that Tape returns blank symbol for positions not in input"""
        tape = Tape()

        assert tape.symbols[5] == B
        assert tape.symbols[0] == B
        assert tape.symbols[-1] == B
