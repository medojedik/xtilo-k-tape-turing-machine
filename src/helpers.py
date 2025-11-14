from collections import defaultdict

from src.actions import Action
from src.config import B, State


# --- Helper Classes ---
class Tape:
    def __init__(self, input_str: list[str] = []) -> None:
        self.symbols: dict[int, str] = defaultdict(lambda: B, dict(enumerate(input_str)))


class Head:
    def __init__(self):
        self.position: int = 0


class Rule:
    def __init__(
        self,
        current_state: State,
        next_state: State,
        actions: list[Action],
    ) -> None:
        self.current_state = current_state
        self.next_state = next_state
        self.actions = actions
        self.write_symbols = [a.write_symbol for a in self.actions]
        self.operation = [a.operation for a in self.actions]
        self.read_symbols = [a.read_symbol for a in self.actions]

    def matches(self, state: State, symbols: list[str]) -> bool:
        """Check if this rule matches the given state and symbols"""
        if state != self.current_state:
            return False

        return all(action.matches(symbol) for action, symbol in zip(self.actions, symbols))
