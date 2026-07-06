"""allergen-validator <dish.json> — check that declared allergens match the ingredients.

Exit 1 if any allergen present in the ingredients is undeclared (safety error)."""
import argparse
import json
import sys

from .validate import validate, has_errors

_ORDER = {"error": 0, "warn": 1, "info": 2}


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="allergen-validator")
    parser.add_argument("dish", help="dish JSON: {name, regime, ingredients[], declared_allergens[]}")
    args = parser.parse_args(argv)

    with open(args.dish) as fh:
        dish = json.load(fh)

    findings = validate(dish)
    for f in sorted(findings, key=lambda x: _ORDER.get(x["severity"], 9)):
        print(f"{f['severity'].upper():5} {f['rule']}  {f['message']}", file=sys.stderr)
    if not findings:
        print("OK — declared allergens match the ingredients", file=sys.stderr)

    return 1 if has_errors(findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
