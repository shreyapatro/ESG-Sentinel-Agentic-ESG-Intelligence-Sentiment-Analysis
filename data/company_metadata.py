import csv
from pathlib import Path

COMPANY_LIST_PATH = Path("data/company_list.csv")


def load_company_by_ticker(ticker: str) -> dict:
    normalized_ticker = ticker.upper()

    if not COMPANY_LIST_PATH.exists():
        raise FileNotFoundError(f"Company list not found: {COMPANY_LIST_PATH}")

    with COMPANY_LIST_PATH.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["ticker"].upper() == normalized_ticker:
                return row

    raise ValueError(f"Ticker not found in company list: {ticker}")

def load_companies() -> list[dict]:
    if not COMPANY_LIST_PATH.exists():
        raise FileNotFoundError(f"Company list not found: {COMPANY_LIST_PATH}")

    with COMPANY_LIST_PATH.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)