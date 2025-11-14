from src.actions import Action
from src.config import B, L, R, S, State
from src.turing_mapping import Rule


class TestRuleInitialization:
    """Test Rule class initialization"""

    def test_rule_basic_initialization(self):
        """Test creating a Rule with basic parameters"""
        q0 = State("q0")
        q1 = State("q1")
        actions = Action(read_symbol="0", write_symbol="1", operation=R)

        rule = Rule(current_state=q0, next_state=q1, actions=[actions])

        assert rule.current_state == q0
        assert rule.next_state == q1
        assert rule.actions == [actions]
        assert rule.write_symbols == ["1"]
        assert rule.operation == [R]
        assert rule.read_symbols == ["0"]

    def test_rule_with_multiple_actions(self):
        """Test Rule with multiple actions for k-tape machine"""
        q0 = State("q0")
        q1 = State("q1")
        actions = [
            Action(read_symbol="0", write_symbol="1", operation=R),
            Action(read_symbol="1", write_symbol="0", operation=L),
            Action(read_symbol="X", write_symbol="Y", operation=S),
        ]

        rule = Rule(current_state=q0, next_state=q1, actions=actions)

        assert len(rule.actions) == 3
        assert rule.write_symbols == ["1", "0", "Y"]
        assert rule.operation == [R, L, S]
        assert rule.operation == [1, -1, 0]
        assert rule.read_symbols == ["0", "1", "X"]


class TestRuleMatches:
    """Test Rule.matches() method"""

    def test_matches_exact_state_and_symbols(self):
        """Test rule matches when state and symbols are exact"""
        q0 = State("q0")
        q1 = State("q1")
        actions = [
            Action(read_symbol="0", write_symbol="1", operation=R),
            Action(read_symbol="1", write_symbol="0", operation=L),
        ]
        rule = Rule(current_state=q0, next_state=q1, actions=actions)

        assert rule.matches(q0, ["0", "1"]) is True

    def test_does_not_match_wrong_state(self):
        """Test rule does not match when state is different"""
        q0 = State("q0")
        q1 = State("q1")
        actions = [Action(read_symbol="0", write_symbol="1", operation=R)]
        rule = Rule(current_state=q0, next_state=q1, actions=actions)

        assert rule.matches(q1, ["0"]) is False

    def test_does_not_match_wrong_symbols(self):
        """Test rule does not match when symbols are different"""
        q0 = State("q0")
        q1 = State("q1")
        actions = [
            Action(read_symbol="0", write_symbol="1", operation=R),
            Action(read_symbol="1", write_symbol="0", operation=L),
        ]
        rule = Rule(current_state=q0, next_state=q1, actions=actions)

        # Wrong symbols
        assert rule.matches(q0, ["1", "0"]) is False
        assert rule.matches(q0, ["0", "0"]) is False

    def test_matches_with_wildcard(self):
        """Test rule matches when using wildcard symbols"""
        q0 = State("q0")
        q1 = State("q1")
        actions = [
            Action(read_symbol="*", write_symbol="1", operation=R),
            Action(read_symbol="1", write_symbol="0", operation=L),
        ]
        rule = Rule(current_state=q0, next_state=q1, actions=actions)

        # Wildcard should match any symbol in first position
        assert rule.matches(q0, ["0", "1"]) is True
        assert rule.matches(q0, ["X", "1"]) is True
        assert rule.matches(q0, [B, "1"]) is True
        # But second position must still be "1"
        assert rule.matches(q0, ["0", "0"]) is False
