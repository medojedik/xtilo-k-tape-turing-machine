# xtilo-k-tape-turing-machine

Semestrální projekt do předmětu XTILO.

Implementace K‑páskového Turingova stroje schopného:
- zpracovat libovolnou množinu pravidel (přechodových funkcí),
- simulovat běh nad více páskami současně,
- vracet zakódovanou binární/unární reprezentaci použitých pravidel.

---
## 1. Požadavky

- Python ≥ 3.10 (doporučeno 3.11+)
- `make` (macOS / Linux; na Windows lze použít WSL nebo přepis příkazů do PowerShellu)

---
## 2. Vytvoření virtuálního prostředí a instalace balíčku

Z kořenového adresáře projektu:

```bash
# Vytvoření a aktivace prostředí
make venv
source .venv/bin/activate  # macOS / Linux

# Instalace pouze produkčních závislostí (editable mód)
make install

# Instalace vývojových závislostí (lint, mypy, pytest)
make install-dev
```

Alternativně přímo přes `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

---
## 3. Lintování, formátování a typová kontrola

Projekt používá Black, Isort a Mypy.

```bash
# Automatické formátování
make lint

# Kontrola formátu bez úprav
make lint-check

# Typová kontrola (mypy)
make type-check

# Kombinace kontrol (lint + mypy)
make check

# Kompletní sekvence (clean + lint + type-check + test)
make all
```

---
## 4. Spuštění testů

Jednotkové testy:
```bash
make test        # tests/
```

Testovací příklady (examples) se zapnutým výpisem `print` (pomocí `-s`):
```bash
make test-examples          # běh tests/examples/ s -s
```

---
## 5. Spuštění demonstračních příkladů s logováním

Demonstrační skripty (např. více‑páskový součet binárních čísel) jsou v adresáři `examples/`.

```bash
source .venv/bin/activate
python tests/examples/test_sum.py      # ukázka s verbose výstupem
python tests/examples/test_0n1n.py     # rozpoznání jazyka 0^n 1^n
```

Ve výstupu uvidíte:
- stav přijetí/odmítnutí,
- obsah všech pásek s označením pozice hlavy,
- mapování stavů / symbolů / směrů,
- kódování pravidel.

---
## 6. Struktura projektu

```
src/                # Implementace k-páskového turingova stroje, akcí, pomocných tříd a kódování
tests/              # Jednotkové testy + příklady jako testovací scénáře
tests/examples/     # Spustitelné demo skripty
Makefile            # Zkrácené příkazy pro běžné úkony
pyproject.toml      # Definice balíčku a závislostí
```

Klíčové soubory:
- `src/turing_mapping.py` – hlavní třída `TuringMachine` (běh, tisk pásek, sumarizace)
- `src/helpers.py` – `Tape`, `Head`, `Rule`
- `src/actions.py` – definice akcí (čtení/zápis + pohyb)
- `src/encoding.py` – funkce pro mapování a unární/binarizované kódování pravidel

---
## 7. Kódování pravidel (stručně)

Každý prvek (stav, symbol) je mapován na celé číslo. Číslo `n` se v unárním kódování zapisuje jako `n` nul následovaných jednou nebo více jedničkami:

- běžný segment: `0^n 1`
- terminace pravidla: `0^n 11`
- terminace streamu: `0^n 111`

Implementace: viz `encode_rules_to_binary()` v `src/encoding.py`.

---
## 9. Rychlý přehled příkazů

```bash
make venv                       # vytvoří virtuální prostředí
make install-dev                # instalace vývoj závislostí
make lint                       # formátování
make type-check                 # mypy
make test                       # jednotkové testy
make test-examples              # příklady s výstupem
python examples/demo_sum.py     # spuštění demo skriptu
```

---
## 10. Zadání projektu

**Zadání:**

V libovolném programovacím jazyce realizujte program, který bude simulovat deterministický k‑páskový Turingův stroj tak, aby bylo možno ve vašem programu definovat:

1. konečnou množinu stavů,
2. koncové stavy,
3. počáteční stav,
4. konečnou abecedu obsahující prázdný symbol,
5. přechodové funkce,

a aby poskytl zakódovanou podobu simulovaného stroje.

**Požadavky na výstup:**
- Program má pro každý krok simulace zobrazit stav všech pásek.
- Na závěr má vrátit kód zakódovaného Turingova stroje (viz kódování v části 7).

**Inicializace:**
- Na začátku simulace je pozice čtecí/zapisovací hlavy na prvním neprázdném symbolu vstupní pásky.
- Pozice hlavy po skončení simulace není podstatná.

**Demonstrační úloha (funkce `fun`):**
- Vytvořte Turingův stroj realizující funkci `fun`.
- Vstupem `fun` je entita (sekvence) čísel \(x_i\) kódovaných v binární soustavě.
- Jednotlivé objekty vstupní sekvence jsou odděleny prázdným symbolem (např. `#`).

V projektu je tato část demonstrována skriptem `examples/demo_sum.py`, který sčítá binární čísla oddělená prázdným symbolem a výsledný součet ukládá na výstupní pásku.

---
## 11. Zdroje a reference

Primární studijní a konzultační materiály použité při tvorbě projektu:

- GeeksforGeeks – Turing Machine (teorie a příklady): https://www.geeksforgeeks.org/theory-of-computation/turing-machine-in-toc
- turingmachine.io – Interaktivní simulátor Turingova stroje (vizualizace a ověřování jednoduchých konfigurací): https://turingmachine.io/
- Přednášky z předmětu XTILO (oficiální materiály k teorii výpočtu, stavům, jazykům a Turingovým strojům)
- Konzultace a asistence velkých jazykových modelů (LLMs) pro refaktorizaci kódu a návrh kódování: Gemini Flash 2.5, GPT-5 (ChatGPT-5)

Poznámka: Uvedené online zdroje sloužily k rychlému ověření definic a formátů; finální implementace byla přizpůsobena požadavkům zadání projektu.

