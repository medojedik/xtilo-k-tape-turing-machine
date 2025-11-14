from src.config import WILDCARD, Direction, Q_Start
from src.helpers import Head, Rule, Tape


# --- Main TM Class ---
class TuringMachine:
    def __init__(self, rules: list[Rule], tapes: list[Tape], heads: list[Head]) -> None:
        self.rules = rules  # (q0, [0, 1, B]) -> (q1, [1, 1, B], [R, R, R])
        self.tapes = tapes  # [[#, 0, #], [#, 1, #], [#, #, #]]
        self.heads = heads  # [0, 0, 0]

    def read_tape(self) -> list[str]:
        return [tape.symbols[head.position] for tape, head in zip(self.tapes, self.heads)]

    def write_tape(self, write_symbols: list[str]) -> None:
        for tape, head, symbol in zip(self.tapes, self.heads, write_symbols):
            tape.symbols[head.position] = symbol

    def move_head(self, operations: list[Direction]) -> None:
        for head, operation in zip(self.heads, operations):
            head.position += operation

    def read_rule(self) -> Rule | None:
        current_tape_symbols = self.read_tape()
        for rule in self.rules:
            if rule.matches(self.current_state, current_tape_symbols):
                return rule
        return None

    def run_rule(self, rule: Rule) -> None:
        current_symbols = self.read_tape()
        write_symbols = []
        for action, current_symbol in zip(rule.actions, current_symbols):
            if action.read_symbol == WILDCARD:
                write_symbols.append(current_symbol)
            else:
                write_symbols.append(action.write_symbol)

        self.write_tape(write_symbols)
        self.move_head([action.operation for action in rule.actions])
        self.current_state = rule.next_state

    def run(self, max_steps: int = 100_000):
        steps = 0
        self.current_state = Q_Start
        rules = []
        rules_strings = []
        while steps < max_steps:
            rule = self.read_rule()
            rules.append(rule)
            rules_strings.append(str(rule))
            if rule is None or self.current_state.end:
                break
            self.print_tape()
            self.run_rule(rule)
            steps += 1
        if self.current_state.end:
            print(f"Accepted in {steps} steps")
            return {
                "accepted": True,
                "final_return_content": str(self.tapes[-1]),
                "endoded_rules_world": ""
            }
        else:
            print(f"Rejected in {steps} steps")
            return {
                "accepted": False,
                "final_return_content": str(self.tapes[-1]),
                "endoded_rules_world": ""
            }
        
    def print_tape(self):
        for i, (tape, head) in enumerate(zip(self.tapes, self.heads)):
            symbols = [tape.symbols[j] for j in range(-10, 15)]
            head_idx = head.position + 10
            if 0 <= head_idx < len(symbols):
                symbols[head_idx] = f"[{symbols[head_idx]}]"
            tape_str = "".join(symbols)
            print(f"Tape {i}: {tape_str}")

    def encode_rules(self) -> str:
        """Encode the rules into a string representation (placeholder)"""

        return "Encoded rules placeholder"
