import src.actions as actions_module
from src.actions import Action
from src.config import WILDCARD, B, L, R, S


class TestActionInitialization:
    """Test Action class initialization"""

    def test_action_basic_initialization(self):
        """Test creating an Action with basic parameters"""
        action = Action(read_symbol="0", write_symbol="1", operation=R)

        assert action.read_symbol == "0"
        assert action.write_symbol == "1"
        assert action.operation == R
        assert action.operation == 1

    def test_action_with_blank_symbol(self):
        """Test Action with blank symbol"""
        action = Action(read_symbol=B, write_symbol="0", operation=L)

        assert action.read_symbol == B
        assert action.write_symbol == "0"
        assert action.operation == L
        assert action.operation == -1

    def test_action_with_wildcard(self):
        """Test Action with wildcard symbol"""
        action = Action(read_symbol=WILDCARD, write_symbol=WILDCARD, operation=S)

        assert action.read_symbol == WILDCARD
        assert action.write_symbol == WILDCARD
        assert action.operation == S
        assert action.operation == 0


class TestActionMatches:
    """Test Action.matches() method"""

    def test_wildcard_input_matches_anything(self):
        """Test that wildcard input symbol matches any action read symbol"""
        action_0 = Action(read_symbol="0", write_symbol="1", operation=R)
        action_1 = Action(read_symbol="1", write_symbol="0", operation=L)

        # All actions should match wildcard input
        assert action_0.matches(WILDCARD) is True
        assert action_1.matches(WILDCARD) is True

    def test_multiple_symbols(self):
        """Test matching with different symbol combinations"""
        symbols = ["0", "1", "X", "Y", B]

        for sym in symbols:
            action = Action(read_symbol=sym, write_symbol="dummy", operation=S)
            # Should match itself
            assert action.matches(sym) is True
            # Should not match other symbols (except wildcard)
            for other_sym in symbols:
                if other_sym != sym:
                    assert action.matches(other_sym) is False
            # Should always match wildcard
            assert action.matches(WILDCARD) is True


class TestShortcutRegistration:
    """Test that shortcuts like R10 are correctly registered"""

    def test_shortcut_r10(self):
        """Test RB0: operation R, read B, write '0'"""
        shortcut = getattr(actions_module, "RB0", None)

        assert shortcut is not None, "Shortcut RB0 should be registered"
        assert isinstance(shortcut, Action)
        assert shortcut.read_symbol == B
        assert shortcut.write_symbol == "0"
        assert shortcut.operation == R
        assert shortcut.operation == 1

    def test_shortcut_l01(self):
        """Test LWW: operation L, read W, write 'W"""
        shortcut = getattr(actions_module, "LWW", None)

        assert shortcut is not None, "Shortcut LWW should be registered"
        assert isinstance(shortcut, Action)
        assert shortcut.read_symbol == WILDCARD
        assert shortcut.write_symbol == WILDCARD
        assert shortcut.operation == L
        assert shortcut.operation == -1

    def test_shortcut_s11(self):
        """Test S10: operation S, read '1', write '0'"""
        shortcut = getattr(actions_module, "S10", None)

        assert shortcut is not None, "Shortcut S10 should be registered"
        assert isinstance(shortcut, Action)
        assert shortcut.read_symbol == "1"
        assert shortcut.write_symbol == "0"
        assert shortcut.operation == S
        assert shortcut.operation == 0
