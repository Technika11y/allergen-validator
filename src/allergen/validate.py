"""Validate a dish's declared allergens against the allergens implied by its ingredients.

Pure functions — unit-testable, no I/O. The headline check is safety-critical: an allergen present
in the ingredients but missing from the declaration is an ERROR, because a diner would not be warned.
"""
from .knowledge import US_BIG9, EU_FIC_14, INGREDIENT_ALLERGENS, US_TO_EU


def _f(rule, severity, message):
    return {"rule": rule, "severity": severity, "message": message}


def _regime_set(regime):
    return EU_FIC_14 if regime == "EU" else US_BIG9


def _to_regime(allergen, regime):
    return US_TO_EU.get(allergen, allergen) if regime == "EU" else allergen


def derive_allergens(ingredients):
    """Return ({allergen: [source ingredients]}, [unknown ingredients])."""
    found, unknown = {}, []
    for ing in ingredients:
        key = str(ing).strip().lower()
        if key in INGREDIENT_ALLERGENS:
            for a in INGREDIENT_ALLERGENS[key]:
                found.setdefault(a, []).append(ing)
        else:
            unknown.append(ing)
    return found, unknown


def validate(dish):
    regime = dish.get("regime", "US")
    regime_allergens = _regime_set(regime)
    declared = {str(a).strip().lower() for a in dish.get("declared_allergens", [])}

    derived_us, unknown = derive_allergens(dish.get("ingredients", []))
    derived = {}
    for a, sources in derived_us.items():
        derived.setdefault(_to_regime(a, regime), []).extend(sources)

    findings = []

    # 1. allergen present in ingredients but not declared — the safety error
    for a, sources in derived.items():
        if a in regime_allergens and a not in declared:
            findings.append(_f("undeclared-allergen", "error",
                f'"{a}" is introduced by {", ".join(sorted(set(sources)))} but is not declared — '
                f'a diner would not be warned'))

    # 2. declared token not in the active regime's official list
    for a in declared:
        if a not in regime_allergens:
            findings.append(_f("allergen-not-in-regime", "warn",
                f'declared allergen "{a}" is not in the {regime} major-allergen list — typo or non-standard label'))

    # 3. declared but not traceable to a known ingredient (possible cross-contact)
    for a in declared:
        if a in regime_allergens and a not in derived:
            findings.append(_f("declared-not-derived", "info",
                f'"{a}" is declared but not traced to a known ingredient (cross-contact? verify)'))

    # 4. ingredient we cannot reason about
    for ing in unknown:
        findings.append(_f("unknown-ingredient", "warn",
            f'ingredient "{ing}" is not in the allergen knowledge base — verify its allergens manually'))

    # 5. precautionary allergen labelling (PAL): the shared facility handles an allergen that is
    #    not an ingredient here and carries no "may contain" advisory. Cross-contact is a real
    #    hazard for sensitive diners, so surface it.
    facility = {str(a).strip().lower() for a in dish.get("facility_allergens", [])}
    may_contain = {str(a).strip().lower() for a in dish.get("may_contain", [])}
    for a in facility:
        if a in regime_allergens and a not in derived and a not in declared and a not in may_contain:
            findings.append(_f("facility-cross-contact", "warn",
                f'the facility also handles "{a}", which is not an ingredient here and has no '
                f'"may contain" advisory — consider precautionary labelling'))

    # 6. a "may contain" advisory that isn't a recognised allergen label
    for a in may_contain:
        if a not in regime_allergens:
            findings.append(_f("may-contain-not-in-regime", "warn",
                f'"may contain {a}" is not a {regime} major-allergen label — typo or non-standard'))

    return findings


def has_errors(findings):
    return any(x["severity"] == "error" for x in findings)
