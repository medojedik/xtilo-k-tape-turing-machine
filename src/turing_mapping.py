from src.config import WILDCARD, Direction, Q_Start
from src.encoding import create_encoding_mappings, encode_rules_to_binary
from src.helpers import Head, Rule, Tape


# --- Main TM Class ---
class TuringMachine:
    def __init__(self, rules: list[Rule], tapes: list[Tape], heads: list[Head]) -> None:
        self.rules = rules
        self.tapes = tapes
        self.heads = heads

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

        result = {
            "accepted": self.current_state.end,
            "steps": steps,
            "final_return_content": self.tapes[-1].stripped(),
            "initial_input": self.tapes[0].input_str,
            "encoded_rules_mappings": self.encode_rules(rules) if rules else {},
            "encoded_rules_binary": encode_rules_to_binary(rules),
        }

        self._print_summary(result)

        return result

    def print_tape(self) -> None:
        for i, (tape, head) in enumerate(zip(self.tapes, self.heads)):
            tape_str = str(tape) if str(tape) else "#"
            pos = head.position
            if pos >= 0:
                tape_str = "##" + tape_str[:pos] + f"[{tape_str[pos]}]" + tape_str[pos + 1 :] + "##"
            else:
                tape_str = "##" + tape_str[:pos] + f"[{tape_str[pos]}]" + "##"
            print(f"Tape {i}: {tape_str}")

    def encode_rules(self, rules: list[Rule | None]) -> dict[str, dict]:
        """
        Return encoding mappings for provided rules including possible None entries.
        """
        filtered: list[Rule] = [r for r in rules if r is not None]
        return create_encoding_mappings(filtered)

    def _print_summary(self, result: dict) -> None:
        print("\n" + "=" * 80)
        if result["accepted"]:
            print(f"✓ ACCEPTED in {result['steps']} steps")
        else:
            print(f"✗ REJECTED in {result['steps']} steps")
        print("=" * 80)

        print(f"\nInitial Input: {result['initial_input']}")
        print(f"Final Output:  {result['final_return_content']}")

        print("\n--- All Tape Contents and Head Positions ---")
        self.print_tape()

        print("\n--- Encoding Information ---")
        print("State Mappings:", result["encoded_rules_mappings"]["states"])
        print("Symbol Mappings:", result["encoded_rules_mappings"]["symbols"])
        print("Direction Mappings:", result["encoded_rules_mappings"]["directions"])

        print("\n--- Binary Encoded Rules ---")
        print(result["encoded_rules_binary"])
        print("=" * 80 + "\n")
