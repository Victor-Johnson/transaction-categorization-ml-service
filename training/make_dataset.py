import pandas as pd
import random
import re
from pathlib import Path

random.seed(42)

MAP = {
    "Groceries": "groceries",
    "Dining": "dining",
    "Friend Activities": "dining",
    "Transportation": "transportation",
    "Utilities": "utilities",
    "Housing": "housing",
    "Subscriptions": "subscriptions",
    "Fitness": "subscriptions",
    "Gifts": "other",
    "Other": "other",
}

# UK Major merchants/providers by label
UK_ENTITIES = {
    "groceries": ["TESCO", "SAINSBURYS", "ASDA", "LIDL", "ALDI", "WAITROSE", "MORRISONS", "ICELAND"],
    "dining": ["PRET", "NANDO'S", "MCDONALDS", "KFC", "GREGGS", "COSTA", "STARBUCKS", "DELIVEROO", "JUST EAT", "UBER EATS"],
    "transportation": ["TFL", "TRAINLINE", "NATIONAL RAIL", "UBER", "BOLT", "SHELL", "BP", "ESSO"],
    "utilities": ["BRITISH GAS", "OCTOPUS ENERGY", "E.ON", "SCOTTISHPOWER", "THAMES WATER", "SEVERN TRENT", "VODAFONE", "O2", "EE", "BT", "SKY"],
    "housing": ["RENT", "LANDLORD", "LETTING AGENT", "MORTGAGE"],
    "subscriptions": ["NETFLIX", "SPOTIFY", "DISNEY+", "AMAZON PRIME", "APPLE.COM/BILL", "GOOGLE *SERVICES", "GYM GROUP", "PUREGYM"],
    "other": ["AMAZON", "EBAY", "ARGOS", "CURRYS", "BOOTS", "SUPERDRUG", "HMRC", "NHS"],
}

PAYMENT_PREFIXES = [
    "VISA", "MASTERCARD", "CARD", "POS", "CONTACTLESS", "DIRECT DEBIT", "BACS", "FPS", "SO", "STO"
]
# Bank-style templates by label
TEMPLATES = {
    "groceries": [
        "POS {entity} {item}",
        "CARD PAYMENT {entity} {item}",
        "CONTACTLESS {entity} {item}",
    ],
    "dining": [
        "CARD PAYMENT {entity} {item}",
        "RESTAURANT {entity} {item}",
        "FOOD DELIVERY {entity} {item}",
    ],
    "transportation": [
        "TRANSPORT {entity} {item}",
        "CARD PAYMENT {entity} {item}",
        "FUEL {entity} {item}",
    ],
    "utilities": [
        "DIRECT DEBIT {entity}",
        "BILL PAYMENT {entity}",
        "UTILITY BILL {entity}",
    ],
    "housing": [
        "RENT PAYMENT {entity}",
        "MORTGAGE PAYMENT {entity}",
        "BACS {entity} RENT",
    ],
    "subscriptions": [
        "SUBSCRIPTION {entity}",
        "DIRECT DEBIT {entity}",
        "CARD PAYMENT {entity}",
    ],
    "other": [
        "CARD PAYMENT {entity} {item}",
        "POS PURCHASE {entity} {item}",
        "ONLINE PURCHASE {entity} {item}",
    ],
}



def noiseify(text: str) -> str:
    t = re.sub(r"\s+", " ", text).strip()

    # abbreviations
    t = re.sub(r"\bPAYMENT\b", random.choice(["PAYMENT", "PMT"]), t, flags=re.IGNORECASE)

    # sometimes add a prefix
    if random.random() < 0.25:
        t = f"{random.choice(PAYMENT_PREFIXES)} {t}"

    # casing noise
    r = random.random()
    if r < 0.3:
        t = t.upper()
    elif r < 0.6:
        t = t.lower()
    else:
        t = " ".join(w.capitalize() for w in t.split())

    # separators + reference id
    if random.random() < 0.35:
        t = t.replace(" ", random.choice([" ", "/", "-", "*"]))
    if random.random() < 0.70:
        t += f" {random.randint(1000, 999999)}"

    # occasional truncation
    if random.random() < 0.08 and len(t) > 20:
        t = t[:-random.randint(2, 8)]

    return t.strip()

def map_cat(cat: str) -> str:
    return MAP.get(str(cat).strip(), "other")

def make_desc(label: str, item: str) -> str:
    entity = random.choice(UK_ENTITIES.get(label, UK_ENTITIES["other"]))
    template = random.choice(TEMPLATES.get(label, TEMPLATES["other"]))
    base = template.format(entity=entity, item=str(item))
    return noiseify(base)

# def main(inp="data/retail_10k.csv", out="data/transactions_v2.csv"):
#     p = Path(inp)
#     if not p.exists() or p.stat().st_size == 0:
#         raise ValueError(f"Missing/empty input file: {p.resolve()}")


def main(inp="data/retail_10k.csv", out="data/transactions_v2.csv"):
    # Always resolve output relative to project root (parent of training/)
    project_root = Path(__file__).resolve().parent.parent
    inp_path = (project_root / inp).resolve() if not Path(inp).is_absolute() else Path(inp).resolve()
    out_path = (project_root / out).resolve() if not Path(out).is_absolute() else Path(out).resolve()

    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not inp_path.exists() or inp_path.stat().st_size == 0:
        raise ValueError(f"Missing/empty input file: {inp_path}")


    df = pd.read_csv(inp)

    # column flexibility
    col_alias = {
        "Category": ["Category", "category"],
        "Item": ["Item", "item"],
        "Total Spent": ["Total Spent", "TotalSpent", "total_spent", "Total"],
        "Transaction Date": ["Transaction Date", "TransactionDate", "date", "Transaction_Date"],
    }

    def pick_col(options):
        for c in options:
            if c in df.columns:
                return c
        return None

    cat_col = pick_col(col_alias["Category"])
    item_col = pick_col(col_alias["Item"])
    amt_col = pick_col(col_alias["Total Spent"])
    date_col = pick_col(col_alias["Transaction Date"])

    missing = [name for name, col in [("Category", cat_col), ("Item", item_col), ("Total Spent", amt_col), ("Transaction Date", date_col)] if col is None]
    if missing:
        raise ValueError(f"Missing columns {missing}. Found: {list(df.columns)}")

    labels = df[cat_col].apply(map_cat)
    descriptions = [make_desc(lbl, it) for lbl, it in zip(labels, df[item_col])]

    out_df = pd.DataFrame({
        "date": pd.to_datetime(df[date_col], errors="coerce").dt.date.astype(str),
        "description": descriptions,
        "amount": pd.to_numeric(df[amt_col], errors="coerce"),
        "label": labels,
        "source": "simulated_bank_transactions_uk",
    }).dropna(subset=["date", "description", "amount", "label"])

    out_df.to_csv(out, index=False)
    print(f" writing {len(out_df)} rows -> {out}")
    print(out_df["label"].value_counts())
    print(out_df.head(5))

if __name__ == "__main__":
    main()