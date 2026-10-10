import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


# ============================================
# 1. RANDOM SEED
# ============================================

np.random.seed(42)
random.seed(42)


# ============================================
# 2. BASIC DATA
# ============================================

cities = [
    "Visakhapatnam",
    "Vijayawada",
    "Hyderabad",
    "Bengaluru",
    "Chennai",
    "Kakinada"
]

restaurants = [
    "Spice Hub",
    "Food Factory",
    "Biryani House",
    "Tasty Treats",
    "Urban Kitchen",
    "Pizza Point",
    "South Flavours",
    "Cafe Corner"
]

food_categories = [
    "Indian",
    "Biryani",
    "Pizza",
    "Chinese",
    "South Indian",
    "Fast Food",
    "Desserts"
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash"
]

order_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Cancelled"
]

customers = [
    f"C{str(i).zfill(4)}"
    for i in range(1, 301)
]


# ============================================
# 3. GENERATE ORDERS
# ============================================

orders = []

start_date = datetime(2026, 1, 1)

for i in range(1, 1001):

    order_id = f"FD{str(i).zfill(5)}"

    customer_id = random.choice(customers)

    order_date = start_date + timedelta(
        days=random.randint(0, 179)
    )

    order_time_hour = random.randint(10, 22)

    order_time_minute = random.randint(0, 59)

    order_time = (
        f"{order_time_hour:02d}:"
        f"{order_time_minute:02d}"
    )

    city = random.choice(cities)

    restaurant = random.choice(restaurants)

    food_category = random.choice(
        food_categories
    )

    quantity = random.randint(1, 5)

    order_value = random.randint(
        150, 1500
    )

    delivery_fee = random.choice(
        [20, 30, 40, 50, 60]
    )

    discount = random.choice(
        [0, 20, 30, 50, 75, 100]
    )

    payment_method = random.choice(
        payment_methods
    )

    rating = random.choice(
        [3, 3.5, 4, 4, 4.5, 5]
    )

    delivery_time = random.randint(
        15, 75
    )

    distance = round(
        random.uniform(1, 15),
        1
    )

    order_status = random.choice(
        order_statuses
    )

    customer_type = random.choice(
        ["New", "Returning"]
    )

    orders.append([
        order_id,
        customer_id,
        order_date.strftime("%Y-%m-%d"),
        order_time,
        city,
        restaurant,
        food_category,
        quantity,
        order_value,
        delivery_fee,
        discount,
        payment_method,
        rating,
        delivery_time,
        distance,
        order_status,
        customer_type
    ])


# ============================================
# 4. COLUMN NAMES
# ============================================

columns = [
    "Order_ID",
    "Customer_ID",
    "Order_Date",
    "Order_Time",
    "City",
    "Restaurant",
    "Food_Category",
    "Quantity",
    "Order_Value",
    "Delivery_Fee",
    "Discount",
    "Payment_Method",
    "Rating",
    "Delivery_Time_Min",
    "Distance_KM",
    "Order_Status",
    "Customer_Type"
]


# ============================================
# 5. CREATE DATAFRAME
# ============================================

df = pd.DataFrame(
    orders,
    columns=columns
)


# ============================================
# 6. SAVE CSV FILE
# ============================================

df.to_csv(
    "data/food_delivery_data.csv",
    index=False
)


# ============================================
# 7. DISPLAY INFORMATION
# ============================================

print("\n================================")
print("FOOD DELIVERY DATASET CREATED")
print("================================")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

print("\n================================")
print("PROCESS COMPLETED SUCCESSFULLY")
print("================================")