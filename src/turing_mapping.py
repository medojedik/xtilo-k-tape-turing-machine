from collections import defaultdict

from src.config import B


# --- Helper Classes ---
class Tape:
    def __init__(self, input_str: list[str] = []):
        self.symbols: dict[int, str] = defaultdict(lambda: B, dict(enumerate(input_str)))


class Head:
    pass


class Action:
    pass


class Rule:
    pass


# --- Main TM Class ---
class TuringMachine:
    pass
