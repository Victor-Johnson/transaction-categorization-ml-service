import random
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

CATEGORIES = {
    "Groceries": ["Milk", "Bread", "Eggs", "Rice", "Chicken", "Vegetables", "Fruit", "Cereal"],
    "Utilities": ["Electricity Bill", "Water Bill", "Gas Bill", "Internet Bill", "Phone Bill"],
    "Transportation": ["Uber Ride", "Train Ticket", "Bus Pass", "Fuel", "Car Maintenance"],
    "Dining": ["Restaurant", "Fast Food", "Food Delivery", "Cafe"],
    "Subscriptions": ["Netflix", "Spotify", "Gym Membership", "iCloud", "Prime Membership"],
    "Housing": ["Rent", "Mortgage", "Landlord Payment"],
    "Other": ["Online Purchase", "Misc Expense", "Pharmacy", "Gift", "Electronics"]
}

# Target distribution to avoid imbalances on randomization 
WEIGHTS = {
    "Groceries": 0.25,
    "Utilities": 0.15,
    "Transportation": 0.15,
    "Dining": 0.20,
    "Subscriptions": 0.10,
    "Housing": 0.10,
    "Other": 0.05,
}

def random_date(start="2023-01-01", end="2024-12-31"):
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).date().isoformat()

def gen_amount(category: str) -> float:
    if category == "Housing":
        return round(random.uniform(650, 2200), 2)
    if category == "Utilities":
        return round(random.uniform(25, 260), 2)
    if category == "Subscriptions":
        return round(random.uniform(4, 45), 2)
    if category == "Transportation":
        return round(random.uniform(2, 140), 2)
    if category == "Dining":
        return round(random.uniform(5, 160), 2)
    if category == "Groceries":
        return round(random.uniform(5, 200), 2)
    return round(random.uniform(3, 250), 2)

def main(out="data/retail_10k.csv", n=10000):
    Path("data").mkdir(exist_ok=True)

    cats = list(CATEGORIES.keys())
    weights = [WEIGHTS[c] for c in cats]

    rows = []
    for _ in range(n):
        category = random.choices(cats, weights=weights, k=1)[0]
        item = random.choice(CATEGORIES[category])
        amount = gen_amount(category)

        rows.append({
            "Category": category,
            "Item": item,
            "Total Spent": amount,
            "Transaction Date": random_date()
        })

    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)

    print(f"!! generated {len(df)} rows → {out}")
    print(df["Category"].value_counts(normalize=True).round(3))
    print(df.head(5))

if __name__ == "__main__":
    main()