import unittest

from allergen.validate import validate, has_errors


def dish(ingredients, declared, regime="US", name="Test", **extra):
    d = {"name": name, "regime": regime, "ingredients": ingredients, "declared_allergens": declared}
    d.update(extra)
    return d


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

    def test_facility_cross_contact_warns(self):
        # peanuts aren't an ingredient, but the shared facility handles them and there's no advisory
        findings = validate(dish(["salmon"], ["fish"], facility_allergens=["peanuts"]))
        self.assertTrue(any(f["rule"] == "facility-cross-contact" and f["severity"] == "warn" for f in findings))

    def test_facility_allergen_with_may_contain_is_ok(self):
        r = rules(dish(["salmon"], ["fish"], facility_allergens=["peanuts"], may_contain=["peanuts"]))
        self.assertNotIn("facility-cross-contact", r)

    def test_facility_allergen_that_is_an_ingredient_is_not_cross_contact(self):
        # butter -> milk is a real ingredient; declaring it means no cross-contact warning for milk
        r = rules(dish(["butter"], ["milk"], facility_allergens=["milk"]))
        self.assertNotIn("facility-cross-contact", r)

    def test_facility_cross_contact_is_not_an_error(self):
        self.assertFalse(has_errors(validate(dish(["salmon"], ["fish"], facility_allergens=["peanuts"]))))

    def test_may_contain_typo_warns(self):
        self.assertIn("may-contain-not-in-regime", rules(dish(["salmon"], ["fish"], may_contain=["peanutz"])))


if __name__ == "__main__":
    unittest.main()
