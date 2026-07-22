# Allergen Data Integrity Validator

> Checks that a dish's **declared allergens match the allergens implied by its ingredients**
> (FALCPA Big-9 / EU FIC). An allergen in the pot but not on the label is a safety error.
>
> Part of the **Technika11y** suite · *Root access for everyone.* · complements `menu-a11y-engine`

[![ci](https://github.com/technika11y/allergen-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/technika11y/allergen-validator/actions/workflows/ci.yml)
![status](https://img.shields.io/badge/status-pre--alpha-orange)
![license](https://img.shields.io/badge/license-Apache--2.0-blue)
![python](https://img.shields.io/badge/python-3.10%2B-informational)

---

## Quick start

```bash
git clone https://github.com/technika11y/allergen-validator && cd allergen-validator
PYTHONPATH=src python3 -m allergen.cli examples/dish.json
```

## Status — read this first

**Pre-alpha (`v0.1.0a0`). Honest state of the code:**

| Capability | State |
|---|---|
| Derive allergens from ingredients; flag **undeclared** ones (error) | ✅ works, tested |
| Multi-allergen ingredients (e.g. soy sauce → soybeans + wheat) | ✅ works, tested |
| Warn on declared labels not in the regime's official list | ✅ works, tested |
| Warn on unknown ingredients (can't verify → manual review) | ✅ works, tested |
| US Big-9 regime | ✅ works, tested |
| EU FIC regime | ⚠️ partial — only the `wheat→gluten`, `shellfish→crustaceans` bridges; extend before EU use |
| Ingredient knowledge base | ⚠️ small starter map — extend for production |

The ingredient map and EU mapping are deliberately small and **stated as partial** — this catches
the common, dangerous mistakes, not every case. Never treat a clean result as a substitute for a
proper allergen program.

## Why it exists

`menu-a11y-engine` makes sure the allergen line is *present and readable*; this makes sure it's
*true*. Together they close the loop: a menu that both announces allergens to a screen reader and
doesn't lie about them.

## Usage

```bash
PYTHONPATH=src python -m allergen.cli examples/dish.json
```

```jsonc
// drop the "milk" declaration and butter gives it away:
{ "ingredients": ["sourdough","sardine","butter"], "declared_allergens": ["fish","wheat"] }
// ERROR undeclared-allergen  "milk" is introduced by butter but is not declared — a diner would not be warned
```

## Roadmap

- [ ] Full ingredient knowledge base + fuzzy matching
- [ ] Complete EU FIC (14) + label localisation
- [ ] "May contain" / cross-contact modelling
- [ ] Ingest recipes from POS/menu formats (pairs with `menu-a11y-engine`)
- [ ] SARIF output + the shared Technika11y CI gate

## License

[Apache-2.0](LICENSE). See [`SECURITY.md`](SECURITY.md).

---

**Part of the [Technika11y](https://github.com/technika11y) suite** · [technika11y.github.io](https://technika11y.github.io/) · security, compliance, and accessibility as one discipline.
