"""Allergen reference data. Small and honest — a real deployment extends the ingredient map.

Labels use US ("Big-9") vocabulary; a partial US->EU bridge is applied at check time for the two
labels that differ most commonly (wheat->gluten, shellfish->crustaceans).
"""

# FDA FALCPA "Big-9" (sesame added 2023).
US_BIG9 = {"milk", "eggs", "fish", "shellfish", "tree nuts", "peanuts", "wheat", "soybeans", "sesame"}

# EU FIC Annex II — the 14 declarable allergens.
EU_FIC_14 = {
    "gluten", "crustaceans", "eggs", "fish", "peanuts", "soybeans", "milk", "tree nuts",
    "celery", "mustard", "sesame", "sulphites", "lupin", "molluscs",
}

# Common ingredient (lowercase) -> allergens it introduces (US labels).
INGREDIENT_ALLERGENS = {
    "wheat flour": {"wheat"}, "flour": {"wheat"}, "bread": {"wheat"}, "sourdough": {"wheat"},
    "butter": {"milk"}, "cream": {"milk"}, "cheese": {"milk"}, "milk": {"milk"}, "yogurt": {"milk"},
    "egg": {"eggs"}, "eggs": {"eggs"}, "mayonnaise": {"eggs"},
    "soy sauce": {"soybeans", "wheat"}, "tofu": {"soybeans"}, "edamame": {"soybeans"},
    "almond": {"tree nuts"}, "almonds": {"tree nuts"}, "walnut": {"tree nuts"}, "cashew": {"tree nuts"},
    "peanut": {"peanuts"}, "peanuts": {"peanuts"}, "peanut oil": {"peanuts"},
    "shrimp": {"shellfish"}, "prawn": {"shellfish"}, "crab": {"shellfish"}, "lobster": {"shellfish"},
    "sardine": {"fish"}, "salmon": {"fish"}, "tuna": {"fish"}, "anchovy": {"fish"},
    "sesame oil": {"sesame"}, "sesame seeds": {"sesame"}, "tahini": {"sesame"},
}

# Partial bridge from US labels to EU FIC labels (extend as needed).
US_TO_EU = {"wheat": "gluten", "shellfish": "crustaceans"}
