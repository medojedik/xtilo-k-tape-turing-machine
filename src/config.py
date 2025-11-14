from enum import IntEnum

# --- Global Constants ---
B = "#"
WILDCARD = "*"  # New wildcard symbol


# --- Direction Enum ---
class Direction(IntEnum):
    """Direction for head movement: R (right), L (left), S (stay)"""

    R = 1
    L = -1
    S = 0

    def __str__(self) -> str:
        """Return the name of the direction (R, L, or S)"""
        return self.name


# --- State Definition ---
class State:
    def __init__(self, name: str, start: bool = False, end: bool = False) -> None:
        self.name = name
        self.start = start
        self.end = end

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False
        return all([self.name == other.name, self.start == other.start, self.end == other.end])

    def __str__(self) -> str:
        return self.name


# --- Fixed States ---
Q_Start = State("q_start", start=True)
Q_End = State("q_end", end=True)
