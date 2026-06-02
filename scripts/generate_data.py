import csv
import os
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "sample")

os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_ORDERS = 20000
MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 4

STATES = [
    ("CA", "United States"),
    ("TX", "United States"),
    ("NY", "United States"),
    ("VA", "United States"),
    ("FL", "United States"),
    ("IL", "United States"),
    ("WA", "United States"),
]

CITIES_BY_STATE = {
    "CA": ["Los Angeles", "San Diego", "San Jose", "San Francisco"],
    "TX": ["Houston", "Dallas", "Austin", "San Antonio"],
    "NY": ["New York", "Buffalo", "Albany", "Rochester"],
    "VA": ["Richmond", "Virginia Beach", "Norfolk", "Alexandria"],
    "FL": ["Miami", "Orlando", "Tampa", "Jacksonville"],
    "IL": ["Chicago", "Springfield", "Naperville", "Peoria"],
    "WA": ["Seattle", "Tacoma", "Spokane", "Bellevue"],
}

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael",
    "Linda", "William", "Elizabeth", "David", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Nancy"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]

CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Small Business"]

CATEGORIES = {
    "Electronics": ["Headphones", "Keyboard", "Mouse", "Monitor", "Speaker"],
    "Home": ["Chair", "Lamp", "Vacuum", "Blender", "Storage Box"],
    "Sports": ["Yoga Mat", "Dumbbell", "Bottle", "Resistance Band", "Ball"],
    "Fashion": ["T-Shirt", "Jeans", "Sneakers", "Jacket", "Backpack"],
    "Beauty": ["Moisturizer", "Shampoo", "Cleanser", "Serum", "Perfume"],
}

BRANDS = [
    "NovaTech", "UrbanLine", "PeakFit", "HomeNest", "GlowCare",
    "AeroWave", "BrightKart", "ZenStyle", "CoreMax", "PrimeEdge"
]

PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Apple Pay"]
ORDER_STATUSES = ["Delivered", "Shipped", "Processing", "Cancelled"]
WAREHOUSES = ["WH-001", "WH-002", "WH-003", "WH-004"]


def random_date(start_date: datetime, end_date: datetime) -> datetime:
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86399)
    return start_date + timedelta(days=random_days, seconds=random_seconds)


def maybe_dirty(value: str, probability: float = 0.01) -> str:
    """Inject a few dirty values for cleaning practice."""
    if random.random() < probability:
        return ""
    return value


def generate_customers():
    customers = []
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 3, 31)

    for i in range(1, NUM_CUSTOMERS + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        state, country = random.choice(STATES)
        city = random.choice(CITIES_BY_STATE[state])
        signup_dt = random_date(start_date, end_date)

        customer_id = f"CUST{i:05d}"
        email = f"{first.lower()}.{last.lower()}{i}@example.com"
        phone = f"804-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        segment = random.choice(CUSTOMER_SEGMENTS)

        customers.append([
            customer_id,
            first,
            last,
            maybe_dirty(email, 0.005),
            maybe_dirty(phone, 0.005),
            city,
            state,
            country,
            signup_dt.strftime("%Y-%m-%d"),
            segment,
        ])

    return customers


def generate_products():
    products = []
    created_start = datetime(2021, 1, 1)
    created_end = datetime(2024, 12, 31)

    product_id_counter = 1
    for category, names in CATEGORIES.items():
        for _ in range(NUM_PRODUCTS // len(CATEGORIES)):
            base_name = random.choice(names)
            brand = random.choice(BRANDS)
            product_name = f"{brand} {base_name}"

            cost_price = round(random.uniform(5, 300), 2)
            markup = random.uniform(1.15, 1.8)
            unit_price = round(cost_price * markup, 2)
            is_active = random.choice(["true"] * 9 + ["false"])
            created_date = random_date(created_start, created_end).strftime("%Y-%m-%d")

            products.append([
                f"PROD{product_id_counter:05d}",
                product_name,
                category,
                brand,
                unit_price,
                cost_price,
                is_active,
                created_date,
            ])
            product_id_counter += 1

    return products[:NUM_PRODUCTS]


def weighted_status():
    return random.choices(
        ORDER_STATUSES,
        weights=[65, 20, 10, 5],
        k=1
    )[0]


def generate_orders(customers):
    orders = []
    order_items = []

    order_start = datetime(2024, 1, 1)
    order_end = datetime(2025, 3, 31)
    product_ids = [f"PROD{i:05d}" for i in range(1, NUM_PRODUCTS + 1)]

    for i in range(1, NUM_ORDERS + 1):
        order_id = f"ORD{i:06d}"
        customer = random.choice(customers)
        customer_id = customer[0]
        shipping_city = customer[5]
        shipping_state = customer[6]
        shipping_country = customer[7]

        order_date = random_date(order_start, order_end).strftime("%Y-%m-%d %H:%M:%S")
        order_status = weighted_status()
        payment_method = random.choice(PAYMENT_METHODS)

        orders.append([
            order_id,
            customer_id,
            order_date,
            order_status,
            payment_method,
            shipping_city,
            shipping_state,
            shipping_country,
        ])

        num_items = random.randint(MIN_ITEMS_PER_ORDER, MAX_ITEMS_PER_ORDER)
        used_products = random.sample(product_ids, k=num_items)

        for item_num, product_id in enumerate(used_products, start=1):
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(10, 500), 2)
            discount_amount = round(random.choice([0, 0, 0, 5, 10, 15, 20]), 2)

            order_items.append([
                f"ITEM-{order_id}-{item_num}",
                order_id,
                product_id,
                quantity,
                unit_price,
                discount_amount,
            ])

    return orders, order_items


def generate_inventory():
    inventory = []
    inventory_id_counter = 1
    last_updated_start = datetime(2025, 1, 1)
    last_updated_end = datetime(2025, 4, 15)

    for i in range(1, NUM_PRODUCTS + 1):
        inventory.append([
            f"INV{inventory_id_counter:05d}",
            f"PROD{i:05d}",
            random.choice(WAREHOUSES),
            random.randint(0, 500),
            random.randint(10, 80),
            random_date(last_updated_start, last_updated_end).strftime("%Y-%m-%d %H:%M:%S"),
        ])
        inventory_id_counter += 1

    return inventory


def write_csv(file_name, header, rows):
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Wrote {file_name}: {len(rows)} rows")


def main():
    customers = generate_customers()
    products = generate_products()
    orders, order_items = generate_orders(customers)
    inventory = generate_inventory()

    write_csv(
        "customers.csv",
        [
            "customer_id", "first_name", "last_name", "email", "phone",
            "city", "state", "country", "signup_date", "customer_segment"
        ],
        customers,
    )

    write_csv(
        "products.csv",
        [
            "product_id", "product_name", "category", "brand", "unit_price",
            "cost_price", "is_active", "created_date"
        ],
        products,
    )

    write_csv(
        "orders.csv",
        [
            "order_id", "customer_id", "order_date", "order_status",
            "payment_method", "shipping_city", "shipping_state", "shipping_country"
        ],
        orders,
    )

    write_csv(
        "order_items.csv",
        [
            "order_item_id", "order_id", "product_id", "quantity",
            "unit_price", "discount_amount"
        ],
        order_items,
    )

    write_csv(
        "inventory.csv",
        [
            "inventory_id", "product_id", "warehouse_id", "stock_quantity",
            "reorder_level", "last_updated"
        ],
        inventory,
    )

    print(f"\nAll files generated in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()