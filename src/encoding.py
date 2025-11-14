from src.config import Direction, Q_End, Q_Start
from src.helpers import Rule


def create_encoding_mappings(rules: list[Rule]) -> dict[str, dict]:
    """
    Create encoding mappings for states, symbols, and directions from a list of rules.
    """
    valid_rules = [r for r in rules if r is not None]
    return {
        "states": _create_states_mapping(valid_rules),
        "symbols": _create_symbols_mapping(valid_rules),
        "directions": _create_directions_mapping(),
    }


def _create_states_mapping(rules: list[Rule]) -> dict[str, int]:
    """
    Create integer mapping for state names.
    """
    states: set[str] = set()
    for r in rules:
        states.add(r.current_state.name)
        states.add(r.next_state.name)
    inner_states = sorted(s for s in states if s not in {Q_Start.name, Q_End.name})
    return {
        **{Q_Start.name: 1},
        **{name: idx for idx, name in enumerate(inner_states, start=2)},
        **{Q_End.name: len(inner_states) + 2},
    }


def _create_symbols_mapping(rules: list[Rule]) -> dict[str, int]:
    """
    Create integer mapping for tape symbols.
    """
    all_symbols = set()
    for rule in rules:
        all_symbols.update(rule.read_symbols)
        all_symbols.update(rule.write_symbols)
    sorted_symbols = sorted(all_symbols)
    return {symbol: idx + 1 for idx, symbol in enumerate(sorted_symbols)}


def _create_directions_mapping() -> dict[Direction, int]:
    """
    Create integer mapping for Direction enum values.
    """
    return {
        Direction.R: 1,
        Direction.L: 2,
        Direction.S: 3,
    }


def encode_rules_to_binary(rules: list[Rule | None]) -> str:
    """
    Encode rules into a binary string representation using unary encoding.
    """
    valid_rules = [r for r in rules if r is not None]
    if not valid_rules:
        return ""

    mappings = create_encoding_mappings(valid_rules)

    def seg(kind: str, key: str, m: int = 1) -> str:
        return _encode_0_1(mappings[kind][key], m)

    def encode_rule(rule: Rule, is_last: bool) -> str:
        term_m = 3 if is_last else 2
        parts: list[str] = [seg("states", rule.current_state.name)]
        parts.extend(seg("symbols", s) for s in rule.read_symbols)
        parts.append(seg("states", rule.next_state.name))
        if rule.write_symbols:
            *middle, last = rule.write_symbols
            parts.extend(seg("symbols", s) for s in middle)
            parts.append(seg("symbols", last, term_m))
        return "".join(parts)

    out: list[str] = ["111"]
    last_idx = len(valid_rules) - 1
    for i, rule in enumerate(valid_rules):
        out.append(encode_rule(rule, is_last=(i == last_idx)))
        if i == last_idx - 1 and last_idx > 0:
            out.append("111")

    return "".join(out)


def _encode_0_1(n: int, m: int = 1) -> str:
    """
    Encode a number in unary format: n zeros followed by m ones.
    """
    return "0" * n + "1" * m
