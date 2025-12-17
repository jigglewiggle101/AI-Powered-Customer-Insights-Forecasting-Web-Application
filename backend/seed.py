# backend/seed.py

import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from .db import engine, Base, SessionLocal
from .models import Customer, Order, User

fake = Faker()

def seed():
    # Drop and recreate tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    # --- Seed Users with Roles ---
    users = [
        User(username="jesmine", api_key="demo-key", role="admin"),
        User(username="analyst", api_key="analyst-key", role="analyst"),
        User(username="viewer", api_key="viewer-key", role="viewer"),
    ]
    db.add_all(users)

    # --- Seed Customers ---
    segments = ["Premium", "Budget", "Loyal", "At Risk"]
    cities = ["Singapore", "Johor Bahru", "Kuala Lumpur", "Batam", "Bangkok"]
    customers = []
    for i in range(300):
        cid = f"C{100000+i}"
        c = Customer(
            customer_id=cid,
            segment=random.choice(segments),
            city=random.choice(cities),
        )
        db.add(c)
        customers.append(cid)

    # --- Seed Orders ---
    categories = ["Electronics", "Fashion", "Groceries", "Home", "Beauty"]
    channels = ["Web", "Mobile", "Store", "Marketplace"]
    start_date = datetime.utcnow() - timedelta(days=180)
    order_id_counter = 1

    for cid in customers:
        num_orders = random.randint(1, 30)
        for _ in range(num_orders):
            dt = start_date + timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))
            amount = round(random.uniform(10, 400), 2)
            o = Order(
                order_id=f"O{order_id_counter}",
                customer_id=cid,
                order_date=dt,
                amount=amount,
                product_category=random.choice(categories),
                channel=random.choice(channels),
            )
            db.add(o)
            order_id_counter += 1

    db.commit()
    db.close()
    print(f"Seeded {len(customers)} customers, {order_id_counter-1} orders, and {len(users)} users.")

if __name__ == "__main__":
    seed()