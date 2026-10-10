import os
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

# =========================================================
# FOOD DELIVERY DATA ANALYSIS APP
# =========================================================

st.set_page_config(
    page_title="Food Delivery Data Analysis",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Keep CSV files in a data folder beside this app.py.
# Saved orders and feedback remain available after closing/reopening the app
# on the same computer, as long as this folder is not deleted.
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

ORDER_FILE = DATA_DIR / "food_delivery_orders.csv"
FEEDBACK_FILE = DATA_DIR / "customer_feedback.csv"

ORDER_COLUMNS = [
    "Customer_ID", "Food", "City", "Quantity", "Amount", "Order_Date"
]
FEEDBACK_COLUMNS = [
    "Customer_ID", "Food", "Rating", "Feedback_Type", "Comment", "Feedback_Date"
]

# Original food menu with prices. "Other / Custom Item" lets you enter
# a food name and price that are not listed here.
FOOD_PRICES = {
    "Burger": 120,
    "Cheese Burger": 150,
    "Veg Pizza": 200,
    "Chicken Pizza": 280,
    "Biryani": 180,
    "Chicken Biryani": 220,
    "Veg Fried Rice": 130,
    "Chicken Fried Rice": 170,
    "Noodles": 130,
    "Sandwich": 100,
    "Dosa": 80,
    "Idli": 50,
    "French Fries": 90,
    "Chicken Curry": 220,
    "Ice Cream": 70,
    "Coffee": 60,
    "Tea": 25,
    "Other / Custom Item": 0,
}

# =========================================================
# GLOBAL STYLE: applies to all pages
# =========================================================
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background:
          linear-gradient(135deg,
            rgba(255, 91, 35, 0.82),
            rgba(255, 174, 50, 0.78),
            rgba(255, 75, 90, 0.80)),
          url("https://images.unsplash.com/photo-1579751626657-72bc17010498");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0.08); }
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #25132d, #7c241c, #b84918);
    }
    [data-testid="stSidebar"] * { color: #fff7ed; }
    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {
        text-shadow: 0 1px 2px rgba(60, 20, 5, 0.18);
    }
    h1, h2, h3 { color: #ffffff !important; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #fff0df, #ffd166) !important;
        border: 2px solid rgba(255,255,255,0.9);
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 5px 18px rgba(75, 25, 5, 0.18);
    }
    [data-testid="stMetricLabel"] { color: #71320e !important; }
    [data-testid="stMetricValue"] { color: #a52a16 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.90);
        border-radius: 14px;
    }
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background: rgba(255,255,255,0.95);
        border-radius: 12px;
    }
    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #e94b20, #ff9f1c);
        color: white;
        border: 0;
        border-radius: 10px;
        font-weight: 700;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(90deg, #c93616, #f07b13);
        color: white;
        border: 0;
    }
    input, textarea, [data-baseweb="select"] { border-radius: 8px !important; }
    hr { border-color: rgba(255,255,255,0.5); }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# FILE HELPERS
# =========================================================
def ensure_csv(path: Path, columns: list[str]) -> None:
    if not path.exists():
        pd.DataFrame(columns=columns).to_csv(path, index=False)


def read_csv_safe(path: Path, columns: list[str]) -> pd.DataFrame:
    ensure_csv(path, columns)
    try:
        data = pd.read_csv(path)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        data = pd.DataFrame(columns=columns)

    for column in columns:
        if column not in data.columns:
            data[column] = pd.Series(dtype="object")
    return data[columns]


def append_csv_record(path: Path, record: dict, columns: list[str]) -> None:
    existing = read_csv_safe(path, columns)
    updated = pd.concat([existing, pd.DataFrame([record])], ignore_index=True)
    updated.to_csv(path, index=False)


def money(value) -> str:
    try:
        return f"₹{float(value):,.2f}".replace(".00", "")
    except (TypeError, ValueError):
        return "₹0"


def show_empty_message() -> None:
    st.info("No order data yet. Select **➕ Add Order** from the sidebar to save your first order.")


# Make sure the data files exist, then load saved data.
df = read_csv_safe(ORDER_FILE, ORDER_COLUMNS)
feedback_df = read_csv_safe(FEEDBACK_FILE, FEEDBACK_COLUMNS)

# Clean types for analysis.
if not df.empty:
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

if not feedback_df.empty:
    feedback_df["Rating"] = pd.to_numeric(feedback_df["Rating"], errors="coerce")
    feedback_df["Feedback_Date"] = pd.to_datetime(
        feedback_df["Feedback_Date"], errors="coerce"
    )

# =========================================================
# SIDEBAR NAVIGATION - 8 PAGES
# =========================================================
st.sidebar.title("🍔 Food Delivery")
st.sidebar.caption("Food Delivery Data Analysis")

pages = [
    "🏠 Dashboard",
    "➕ Add Order",
    "🍔 Food Analysis",
    "👥 Customer Analysis",
    "🏙️ City Analysis",
    "💰 Revenue Analysis",
    "⭐ Customer Feedback",
    "📋 View Data",
]
page = st.sidebar.radio("Select a page", pages, index=0)

# =========================================================
# 1. DASHBOARD
# =========================================================
if page == "🏠 Dashboard":
    st.title("🍔 Food Delivery Dashboard")
    st.write("Manage food orders, customers, cities, revenue, and customer feedback.")

    if df.empty:
        show_empty_message()
    else:
        total_orders = len(df)
        total_customers = df["Customer_ID"].astype(str).nunique()
        total_quantity = int(df["Quantity"].sum())
        total_revenue = df["Amount"].sum()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📦 Total Orders", f"{total_orders:,}")
        c2.metric("👥 Customers", f"{total_customers:,}")
        c3.metric("🍽️ Items Sold", f"{total_quantity:,}")
        c4.metric("💰 Total Revenue", money(total_revenue))

        st.divider()
        left, right = st.columns(2)
        with left:
            st.subheader("🍽️ Best-selling food")
            sold = df.groupby("Food")["Quantity"].sum().sort_values(ascending=False)
            st.bar_chart(sold)
        with right:
            st.subheader("💰 Revenue by food")
            revenue_by_food = df.groupby("Food")["Amount"].sum().sort_values(ascending=False)
            st.bar_chart(revenue_by_food)

        st.subheader("🏙️ Revenue by City")
        city_revenue = df.groupby("City")["Amount"].sum().sort_values(ascending=False)
        st.bar_chart(city_revenue)

        st.subheader("📅 Order Trends")
        dated = df.dropna(subset=["Order_Date"]).copy()
        if not dated.empty:
            dated["Date"] = dated["Order_Date"].dt.date
            st.line_chart(dated.groupby("Date").size().rename("Orders"))
        else:
            st.info("Order dates will appear here when available.")

    st.divider()
    st.subheader("🍽️ Food Menu")
    menu_cols = st.columns(3)
    for i, (item, price) in enumerate(FOOD_PRICES.items()):
        with menu_cols[i % 3]:
            emoji = "🍕" if "Pizza" in item else ("🍔" if "Burger" in item else "🍽️")
            shown_price = "Enter your price" if item == "Other / Custom Item" else money(price)
            st.markdown(
                f"""
                <div style="background:linear-gradient(135deg,#fff0df,#ffd166);
                            padding:14px;border-radius:14px;margin-bottom:10px;
                            border:2px solid white;text-align:center;">
                  <div style="font-size:30px;">{emoji}</div>
                  <div style="font-weight:700;color:#7c2d12;">{item}</div>
                  <div style="font-size:20px;font-weight:800;color:#c2410c;">{shown_price}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()
    st.subheader("⭐ Customer Feedback Overview")
    current_feedback = read_csv_safe(FEEDBACK_FILE, FEEDBACK_COLUMNS)
    if current_feedback.empty:
        st.info("No feedback has been submitted yet.")
    else:
        current_feedback["Rating"] = pd.to_numeric(
            current_feedback["Rating"], errors="coerce"
        )
        f1, f2, f3 = st.columns(3)
        average_rating = current_feedback["Rating"].mean()
        f1.metric(
            "⭐ Average Rating",
            f"{average_rating:.1f}/5" if pd.notna(average_rating) else "N/A",
        )
        f2.metric("📝 Total Feedback", len(current_feedback))
        f3.metric(
            "😊 Positive Feedback",
            int((current_feedback["Feedback_Type"] == "Positive").sum()),
        )

# =========================================================
# 2. ADD ORDER
# =========================================================
elif page == "➕ Add Order":
    st.title("➕ Add New Food Order")
    st.write("Enter the order details below.")

    with st.form("add_order_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            customer_id = st.text_input("Customer ID")
            city = st.text_input("City")
            food = st.selectbox("Select Food Item", list(FOOD_PRICES.keys()))

        with col2:
            order_date = st.date_input("Order Date", value=date.today())
            if food == "Other / Custom Item":
                custom_food = st.text_input("Enter Food Name")
                price_per_item = st.number_input(
                    "Price per Item (₹)", min_value=1, value=100, step=10
                )
            else:
                custom_food = ""
                price_per_item = FOOD_PRICES[food]
                st.number_input(
                    "Price per Item (₹)",
                    min_value=0,
                    value=int(price_per_item),
                    step=10,
                    disabled=True,
                    key=f"price_display_{food}",
                )

            quantity = st.number_input(
                "Quantity", min_value=1, max_value=100, value=1, step=1
            )

        food_name = custom_food.strip() if food == "Other / Custom Item" else food
        total_amount = int(price_per_item) * int(quantity)

        st.markdown(
            f"""
            <div style="background:linear-gradient(90deg,#ffedd5,#fde68a);
                        padding:18px;border-radius:14px;border:2px solid white;">
              <div style="color:#7c2d12;font-size:18px;font-weight:700;">Order Summary</div>
              <div style="color:#c2410c;font-size:32px;font-weight:900;">{money(total_amount)}</div>
              <div style="color:#7c2d12;">{food_name or "Food item"} × {quantity} at {money(price_per_item)} each</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button("💾 Save Order", use_container_width=True)

    if submitted:
        if not customer_id.strip():
            st.error("Please enter Customer ID.")
        elif not city.strip():
            st.error("Please enter City.")
        elif not food_name:
            st.error("Please enter the food name.")
        else:
            record = {
                "Customer_ID": customer_id.strip(),
                "Food": food_name,
                "City": city.strip(),
                "Quantity": int(quantity),
                "Amount": float(total_amount),
                "Order_Date": str(order_date),
            }
            append_csv_record(ORDER_FILE, record, ORDER_COLUMNS)
            st.success(f"Order saved successfully! Total: {money(total_amount)}")
            st.info("Your order is saved in the data folder and will remain available when you reopen the app.")
            st.rerun()

# =========================================================
# 3. FOOD ANALYSIS
# =========================================================
elif page == "🍔 Food Analysis":
    st.title("🍔 Food Analysis")
    if df.empty:
        show_empty_message()
    else:
        summary = (
            df.groupby("Food")
            .agg(
                Orders=("Food", "size"),
                Quantity=("Quantity", "sum"),
                Revenue=("Amount", "sum"),
            )
            .sort_values("Revenue", ascending=False)
            .reset_index()
        )
        st.dataframe(summary, use_container_width=True, hide_index=True)
        a, b = st.columns(2)
        with a:
            st.subheader("Items Sold")
            st.bar_chart(summary.set_index("Food")["Quantity"])
        with b:
            st.subheader("Revenue by Item")
            st.bar_chart(summary.set_index("Food")["Revenue"])
        top = summary.iloc[0]
        st.success(f"Top item by revenue: {top['Food']} — {money(top['Revenue'])}")

# =========================================================
# 4. CUSTOMER ANALYSIS
# =========================================================
elif page == "👥 Customer Analysis":
    st.title("👥 Customer Analysis")
    if df.empty:
        show_empty_message()
    else:
        customer_summary = (
            df.groupby("Customer_ID")
            .agg(
                Orders=("Customer_ID", "size"),
                Items=("Quantity", "sum"),
                Total_Spent=("Amount", "sum"),
                Cities=("City", "nunique"),
            )
            .sort_values("Total_Spent", ascending=False)
            .reset_index()
        )
        st.dataframe(customer_summary, use_container_width=True, hide_index=True)
        a, b, c = st.columns(3)
        a.metric("Unique Customers", df["Customer_ID"].astype(str).nunique())
        b.metric("Repeat Customers", int((customer_summary["Orders"] > 1).sum()))
        c.metric("Average Order Value", money(df["Amount"].mean()))
        st.subheader("Customer Spending")
        st.bar_chart(customer_summary.set_index("Customer_ID")["Total_Spent"])

# =========================================================
# 5. CITY ANALYSIS
# =========================================================
elif page == "🏙️ City Analysis":
    st.title("🏙️ City Analysis")
    if df.empty:
        show_empty_message()
    else:
        city_summary = (
            df.groupby("City")
            .agg(
                Orders=("City", "size"),
                Customers=("Customer_ID", "nunique"),
                Items=("Quantity", "sum"),
                Revenue=("Amount", "sum"),
            )
            .sort_values("Revenue", ascending=False)
            .reset_index()
        )
        st.dataframe(city_summary, use_container_width=True, hide_index=True)
        a, b = st.columns(2)
        with a:
            st.subheader("Revenue by City")
            st.bar_chart(city_summary.set_index("City")["Revenue"])
        with b:
            st.subheader("Orders by City")
            st.bar_chart(city_summary.set_index("City")["Orders"])

# =========================================================
# 6. REVENUE ANALYSIS
# =========================================================
elif page == "💰 Revenue Analysis":
    st.title("💰 Revenue Analysis")
    if df.empty:
        show_empty_message()
    else:
        total = df["Amount"].sum()
        a, b, c = st.columns(3)
        a.metric("Total Revenue", money(total))
        b.metric("Average Order Value", money(df["Amount"].mean()))
        c.metric("Highest Order", money(df["Amount"].max()))

        st.subheader("Revenue by Food")
        st.bar_chart(df.groupby("Food")["Amount"].sum().sort_values(ascending=False))
        st.subheader("Revenue by City")
        st.bar_chart(df.groupby("City")["Amount"].sum().sort_values(ascending=False))

        dated = df.dropna(subset=["Order_Date"]).copy()
        if not dated.empty:
            dated["Date"] = dated["Order_Date"].dt.date
            daily = dated.groupby("Date")["Amount"].sum()
            st.subheader("Daily Revenue")
            st.line_chart(daily)

# =========================================================
# 7. CUSTOMER FEEDBACK
# =========================================================
elif page == "⭐ Customer Feedback":
    st.title("⭐ Customer Feedback")
    st.write("Submit a rating and comment for a food item.")

    with st.form("feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            feedback_customer = st.text_input("Customer ID")
            feedback_food_choice = st.selectbox(
                "Food Item", [item for item in FOOD_PRICES if item != "Other / Custom Item"]
                + ["Other / Custom Item"]
            )
            if feedback_food_choice == "Other / Custom Item":
                feedback_custom_food = st.text_input("Enter Food Name")
                feedback_food = feedback_custom_food.strip()
            else:
                feedback_food = feedback_food_choice
            rating = st.select_slider("Rating", options=[1, 2, 3, 4, 5], value=5)

        with col2:
            feedback_date = st.date_input("Feedback Date", value=date.today())
            feedback_type = st.selectbox(
                "Feedback Type", ["Positive", "Neutral", "Negative"]
            )

        comment = st.text_area("Comments (optional)")
        feedback_submit = st.form_submit_button(
            "⭐ Submit Feedback", use_container_width=True
        )

    if feedback_submit:
        if not feedback_customer.strip():
            st.error("Please enter Customer ID.")
        elif not feedback_food:
            st.error("Please enter the food name.")
        else:
            record = {
                "Customer_ID": feedback_customer.strip(),
                "Food": feedback_food,
                "Rating": int(rating),
                "Feedback_Type": feedback_type,
                "Comment": comment.strip(),
                "Feedback_Date": str(feedback_date),
            }
            append_csv_record(FEEDBACK_FILE, record, FEEDBACK_COLUMNS)
            st.success("Feedback saved successfully!")
            st.rerun()

    st.divider()
    st.subheader("Previously Submitted Feedback")
    saved_feedback = read_csv_safe(FEEDBACK_FILE, FEEDBACK_COLUMNS)
    if saved_feedback.empty:
        st.info("No feedback yet.")
    else:
        saved_feedback["Rating"] = pd.to_numeric(
            saved_feedback["Rating"], errors="coerce"
        )
        st.dataframe(
            saved_feedback.sort_values("Feedback_Date", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

# =========================================================
# 8. VIEW DATA
# =========================================================
elif page == "📋 View Data":
    st.title("📋 View Saved Data")

    st.subheader("🍽️ Orders")
    saved_orders = read_csv_safe(ORDER_FILE, ORDER_COLUMNS)
    if saved_orders.empty:
        st.info("No orders saved yet. Add an order first.")
    else:
        st.dataframe(saved_orders, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download Orders CSV",
            data=saved_orders.to_csv(index=False).encode("utf-8"),
            file_name="food_delivery_orders.csv",
            mime="text/csv",
        )

    st.divider()
    st.subheader("⭐ Feedback")
    saved_feedback = read_csv_safe(FEEDBACK_FILE, FEEDBACK_COLUMNS)
    if saved_feedback.empty:
        st.info("No feedback saved yet.")
    else:
        st.dataframe(saved_feedback, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download Feedback CSV",
            data=saved_feedback.to_csv(index=False).encode("utf-8"),
            file_name="customer_feedback.csv",
            mime="text/csv",
        )
