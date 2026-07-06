import unittest

from allergen.validate import validate, has_errors


def dish(ingredients, declared, regime="US", name="Test"):
    return {"name": name, "regime": regime, "ingredients": ingredients, "declared_allergens": declared}


def rules(d):
    return [f["rule"] for f in validate(d)]


class ValidateTests(unittest.TestCase):
    def test_undeclared_allergen_is_error(self):
        findings = validate(dish(["butter"], []))  # butter -> milk, not declared
        self.assertTrue(any(f["rule"] == "undeclared-allergen" and f["severity"] == "error" for f in findings))

    def test_declared_allergen_passes(self):
        self.assertFalse(has_errors(validate(dish(["butter"], ["milk"]))))

    def test_multi_allergen_ingredient(self):
        # soy sauce -> soybeans + wheat; only soybeans declared -> wheat undeclared
        findings = validate(dish(["soy sauce"], ["soybeans"]))
        msgs = " ".join(f["message"] for f in findings if f["rule"] == "undeclared-allergen")
        self.assertIn("wheat", msgs)

    def test_unknown_ingredient_warns(self):
        self.assertIn("unknown-ingredient", rules(dish(["capers"], [])))

    def test_declared_token_not_in_regime_warns(self):
        # "gluten" is not a US Big-9 label (US uses "wheat")
        self.assertIn("allergen-not-in-regime", rules(dish(["salmon"], ["fish", "gluten"])))

    def test_eu_bridge_wheat_to_gluten(self):
        # under EU, wheat flour should require a "gluten" declaration
        findings = validate(dish(["wheat flour"], [], regime="EU"))
        self.assertTrue(any(f["rule"] == "undeclared-allergen" and "gluten" in f["message"] for f in findings))

    def test_eu_gluten_declared_passes(self):
        self.assertFalse(has_errors(validate(dish(["wheat flour"], ["gluten"], regime="EU"))))


if __name__ == "__main__":
    unittest.main()
