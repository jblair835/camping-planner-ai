def generate_grocery_list(meal_plan: str, num_people: int) -> str:
    """Generate a grocery list based on a text meal plan and number of people."""

    ingredients_by_meal = {
        "Oatmeal": ["Oatmeal packets", "Brown sugar", "Dried fruit"],
        "Eggs & tortillas": ["Eggs", "Tortillas", "Cheese"],
        "Fruit & granola": ["Granola", "Apples", "Bananas"],
        "Sandwiches": ["Bread", "Lunch meat", "Cheese", "Mustard"],
        "Wraps": ["Tortillas", "Lettuce", "Chicken", "Ranch"],
        "Trail mix + jerky": ["Trail mix", "Jerky"],
        "Foil packet veggies + sausage": ["Sausage", "Bell peppers", "Onions", "Foil"],
        "Grilled chicken + rice": ["Chicken", "Rice", "Seasoning"],
        "Chili + cornbread": ["Canned chili", "Cornbread mix"],
        "Pancakes": ["Pancake mix", "Syrup"],
        "Breakfast burritos": ["Eggs", "Tortillas", "Salsa"],
        "French toast": ["Bread", "Eggs", "Cinnamon"],
        "Chicken salad wraps": ["Chicken", "Tortillas", "Mayo"],
        "Charcuterie board": ["Crackers", "Cheese", "Salami"],
        "Veggie hummus sandwiches": ["Bread", "Hummus", "Veggies"],
        "Dutch oven stew": ["Stew meat", "Potatoes", "Carrots"],
        "Campfire fajitas": ["Chicken", "Bell peppers", "Tortillas"],
        "BBQ ribs + potatoes": ["Ribs", "Potatoes", "BBQ sauce"],
        "Instant oatmeal": ["Instant oatmeal", "Dried fruit"],
        "Protein bars": ["Protein bars"],
        "Tuna packets + crackers": ["Tuna packets", "Crackers"],
        "Freeze-dried meals": ["Freeze-dried meals"],
        "Instant ramen + dehydrated veggies": ["Ramen", "Dehydrated veggies"],
    }

    grocery = {}

    for line in meal_plan.splitlines():
        for meal_name, items in ingredients_by_meal.items():
            if meal_name in line:
                for item in items:
                    grocery[item] = grocery.get(item, 0) + num_people

    lines = ["Grocery List:"]
    for item, qty in sorted(grocery.items()):
        lines.append(f"- {item}: {qty}")

    return "\n".join(lines)
