from dataclasses import dataclass
from typing import cast

from src.config import WILDCARD, B, Direction


# --- Define Action class ---
class Action:
    def __init__(self, read_symbol: str, write_symbol: str, operation: Direction) -> None:
        self.read_symbol = read_symbol
        self.write_symbol = write_symbol
        self.operation = operation

    def matches(self, symbol: str) -> bool:
        """Check if this action matches the given symbol, supporting wildcards"""
        return (
            (self.read_symbol == WILDCARD) or (symbol == WILDCARD) or (self.read_symbol == symbol)
        )


# --- Define common moves ---
@dataclass(frozen=True)
class Moves:
    R: Action
    L: Action
    S: Action


# --- Helper Functions ---
def make_moves(read_sym: str, write_sym: str) -> Moves:
    return Moves(
        R=Action(read_sym, write_sym, Direction.R),
        L=Action(read_sym, write_sym, Direction.L),
        S=Action(read_sym, write_sym, Direction.S),
    )


def normalize_symbol(sym: str) -> str:
    mapping = {B: "B", WILDCARD: "W"}
    return mapping.get(sym, sym)


# --- Global dictionary to hold rewrites ---
rewrites: dict = {}


def register_rewrites(read_sym: str, write_targets: list[str]) -> None:
    rewrites.setdefault(read_sym, {})
    for w in write_targets:
        moves = make_moves(read_sym, w)
        rewrites[read_sym][w] = moves

        # create shortcut names like RXY, LXY, SXY
        base = f"{normalize_symbol(read_sym)}{normalize_symbol(w)}"

        # Set the actual values
        globals()[f"R{base}"] = moves.R
        globals()[f"L{base}"] = moves.L
        globals()[f"S{base}"] = moves.S


# --- Register common shortcuts ---
register_rewrites(read_sym="1", write_targets=["1", "0", B, "X", "Y"])
register_rewrites(read_sym="0", write_targets=["1", "0", B, "X", "Y"])
register_rewrites(read_sym="X", write_targets=["1", "0", B, "X", "Y"])
register_rewrites(read_sym="Y", write_targets=["1", "0", B, "X", "Y"])
register_rewrites(read_sym=B, write_targets=["1", "0", B, "X", "Y"])
register_rewrites(read_sym=WILDCARD, write_targets=[WILDCARD])


# --- Module-level __getattr__ for type checking ---
def __getattr__(name: str) -> Action:
    """
    Allow mypy to recognize dynamically created shortcut attributes.
    At runtime, shortcuts are already in globals() from register_rewrites.
    """
    if name in globals():
        return cast(Action, globals()[name])
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
