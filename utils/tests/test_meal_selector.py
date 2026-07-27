import re
from core.food.meal_selector import select_meals

def test_meal_selector_output_format():
    result = select_meals(2, "simple")

    # Basic structure checks
    assert "Selected meals for 2 days" in result
    assert "Day 1:" in result
    assert "Day 2:" in result

    # Ensure breakfast/lunch/dinner lines exist
    assert re.search(r"- Breakfast:", result)
    assert re.search(r"- Lunch:", result)
    assert re.search(r"- Dinner:", result)
