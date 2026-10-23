import random
import csv
from datetime import date, timedelta
from faker import Faker

random.seed(42)
fake = Faker()
Faker.seed(42)

ROW_COUNT = 2000

COUNTRY_VARIANTS = {
    "United States": ["USA", "usa", "United States", "U.S.A.", "United States of America"],
    "Canada": ["Canada", "CANADA", "canada"],
    "Spain": ["Spain", "spain", "SPAIN"],
    "China": ["China", "china", "CHINA"],
    "Egypt": ["Egypt", "egypt", "EGYPT"],
    "Ireland": ["Ireland", "ireland", "IRELAND"],
    "Germany": ["Germany", "germany", "GERMANY"],
    "India": ["India", "india", "INDIA"],
    "Brazil": ["Brazil", "brazil", "BRAZIL"],
    "Australia": ["Australia", "australia", "AUSTRALIA"],
}

DATE_FORMATS = ["%m/%d/%Y", "%d-%m-%Y", "%m/%d/%y", "%Y-%m-%d", "%d/%m/%Y"]

def random_date():
    start = date(2022, 1, 1)
    end = date(2024, 12, 31)
    d = start + timedelta(days=random.randint(0, (end - start).days))
    return d.strftime(random.choice(DATE_FORMATS))

def messy_case(text, chance=0.35):
    r = random.random()
    if r < chance / 2:
        return text.upper()
    elif r < chance:
        return text.lower()
    return text

def random_phone():
    return f"555-{random.randint(1000,9999)}" if random.random() > 0.5 else f"555{random.randint(1000,9999)}"

rows = []
customer_id = 1000

for i in range(ROW_COUNT):
    customer_id += 1
    name = fake.name()
    email = f"{name.lower().replace(' ', '.')}@email.com"
    country_key = random.choice(list(COUNTRY_VARIANTS.keys()))
    country = random.choice(COUNTRY_VARIANTS[country_key])
    spend = round(random.uniform(50, 5000), 2)

    if random.random() < 0.05:
        spend = ""
    elif random.random() < 0.02:
        spend = -abs(spend)

    if random.random() < 0.04:
        name = ""

    phone = random_phone()
    if random.random() < 0.05:
        phone = ""

    row = {
        "CustomerID": customer_id,
        "Name": messy_case(name) if name else "",
        "Email": messy_case(email, chance=0.3) if name else email,
        "SignupDate": random_date(),
        "Country": country,
        "AnnualSpend": spend,
        "Phone": phone,
    }
    rows.append(row)

    if random.random() < 0.03:
        customer_id += 1
        dup = row.copy()
        dup["CustomerID"] = customer_id
        rows.append(dup)

with open("raw_customer_data_large.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["CustomerID", "Name", "Email", "SignupDate", "Country", "AnnualSpend", "Phone"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> raw_customer_data_large.csv")
