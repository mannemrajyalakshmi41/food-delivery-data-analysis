import streamlit as st

import pandas as pd

import os

from datetime import date



# =========================================================

# PAGE CONFIGURATION

# =========================================================



st.set_page_config(

    page_title="Food Delivery Data Analysis",

    page_icon="🍔",

    layout="wide"

)



# =========================================================

# BACKGROUND AND PAGE DESIGN

# =========================================================



st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root { color-scheme: dark; }
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp {
 background: linear-gradient(rgba(5,10,20,.72), rgba(5,10,20,.82)),
 url("https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=2000&q=85") center/cover fixed;
 color: #f8fafc;
}
[data-testid="stAppViewContainer"], [data-testid="stHeader"] { background: transparent; }
[data-testid="stHeader"] { background: rgba(5,10,20,.25); }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#09111f 0%,#0c1525 100%); border-right: 1px solid #253247; }
[data-testid="stSidebar"] * { color: #e8edf5; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#cbd5e1; }
h1,h2,h3 { color:#f8fafc !important; font-weight:750 !important; }
p, label, [data-testid="stCaptionContainer"] { color:#e2e8f0; }
[data-testid="stMetric"] { background:linear-gradient(135deg,rgba(255,255,255,.96),rgba(239,246,255,.94)); border:1px solid rgba(255,255,255,.55); border-radius:16px; padding:17px 19px; box-shadow:0 12px 30px rgba(0,0,0,.22); }
[data-testid="stMetric"] * { color:#172033 !important; }
[data-testid="stMetricLabel"] { font-weight:600; }
[data-testid="stMetricDelta"] { color:#10b981 !important; }
.stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"] button { background:#f59e0b; color:#111827; border:0; border-radius:10px; padding:9px 18px; font-weight:700; }
.stButton>button:hover,.stDownloadButton>button:hover { background:#fbbf24; color:#111827; border:0; }
.stTextInput input,.stNumberInput input,.stDateInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"] { background:#111c2d; color:#f8fafc; border:1px solid #344256; border-radius:9px; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid #344256; border-radius:12px; }
hr { border-color:#344256; }
[data-testid="stAlert"] { border-radius:12px; }
section[data-testid="stMain"] > div { padding-top:1.5rem; }
.dashboard-subtitle { color:#e2e8f0; font-size:1.05rem; margin-top:-8px; margin-bottom:1.35rem; }
.panel { background:rgba(8,16,29,.88); border:1px solid rgba(148,163,184,.28); border-radius:16px; padding:18px 20px; margin:8px 0 18px; box-shadow:0 12px 32px rgba(0,0,0,.22); }
.food-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }
.food-card { background:rgba(11,19,32,.94); border:1px solid #334155; border-radius:15px; padding:10px; text-align:center; min-width:0; }
.food-card img { width:100%; height:95px; object-fit:cover; border-radius:12px; }
.food-card .food-name { font-size:13px; font-weight:700; color:#f8fafc; margin-top:8px; min-height:32px; }
.food-card .food-price { font-size:15px; color:#fbbf24; font-weight:800; margin-top:4px; }
@media (max-width: 900px) { .food-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
</style>
""", unsafe_allow_html=True)




# =========================================================

# FILE LOCATIONS

# =========================================================



DATA_FOLDER = "data"



os.makedirs(DATA_FOLDER, exist_ok=True)



ORDER_FILE = os.path.join(DATA_FOLDER, "food_delivery_orders.csv")

FEEDBACK_FILE = os.path.join(DATA_FOLDER, "customer_feedback.csv")



ORDER_COLUMNS = [

    "Customer_ID",

    "Food",

    "City",

    "Quantity",

    "Amount",

    "Order_Date"

]



FEEDBACK_COLUMNS = [

    "Customer_ID",

    "Food",

    "Rating",

    "Feedback_Type",

    "Comment",

    "Feedback_Date"

]



# =========================================================

# FOOD MENU AND PRICES

# =========================================================



FOOD_PRICES = {

    "Burger": 100,

    "Cheese Burger": 130,

    "Veg Pizza": 180,

    "Chicken Pizza": 250,

    "Biryani": 200,

    "Fried Rice": 120,

    "Noodles": 100,

    "Sandwich": 80,

    "Dosa": 50,

    "Idli": 40,

    "French Fries": 90,

    "Chicken Curry": 220,

    "Ice Cream": 60,

    "Coffee": 30,

    "Tea": 20,

    "Other/Custom": 0

}



# =========================================================

# HELPER FUNCTIONS

# =========================================================



def load_orders():

    """Load saved order records."""



    if os.path.exists(ORDER_FILE):

        try:

            df = pd.read_csv(ORDER_FILE)



            for column in ORDER_COLUMNS:

                if column not in df.columns:

                    df[column] = None



            return df[ORDER_COLUMNS]



        except (pd.errors.EmptyDataError, pd.errors.ParserError):

            return pd.DataFrame(columns=ORDER_COLUMNS)



    return pd.DataFrame(columns=ORDER_COLUMNS)





def load_feedback():

    """Load saved customer feedback."""



    if os.path.exists(FEEDBACK_FILE):

        try:

            df = pd.read_csv(FEEDBACK_FILE)



            for column in FEEDBACK_COLUMNS:

                if column not in df.columns:

                    df[column] = None



            return df[FEEDBACK_COLUMNS]



        except (pd.errors.EmptyDataError, pd.errors.ParserError):

            return pd.DataFrame(columns=FEEDBACK_COLUMNS)



    return pd.DataFrame(columns=FEEDBACK_COLUMNS)





def save_order(order):

    """Append a new order to the CSV file."""



    new_order = pd.DataFrame([order], columns=ORDER_COLUMNS)



    if os.path.exists(ORDER_FILE) and os.path.getsize(ORDER_FILE) > 0:

        new_order.to_csv(

            ORDER_FILE,

            mode="a",

            header=False,

            index=False

        )

    else:

        new_order.to_csv(ORDER_FILE, index=False)





def save_feedback(feedback):

    """Append feedback to the CSV file."""



    new_feedback = pd.DataFrame(

        [feedback],

        columns=FEEDBACK_COLUMNS

    )



    if os.path.exists(FEEDBACK_FILE) and os.path.getsize(FEEDBACK_FILE) > 0:

        new_feedback.to_csv(

            FEEDBACK_FILE,

            mode="a",

            header=False,

            index=False

        )

    else:

        new_feedback.to_csv(FEEDBACK_FILE, index=False)





def prepare_orders(df):

    """Prepare order columns for analysis."""



    df = df.copy()



    if not df.empty:

        df["Amount"] = pd.to_numeric(

            df["Amount"], errors="coerce"

        ).fillna(0)



        df["Quantity"] = pd.to_numeric(

            df["Quantity"], errors="coerce"

        ).fillna(0)



        df["Order_Date"] = pd.to_datetime(

            df["Order_Date"], errors="coerce"

        )



    return df





def show_empty_message():

    st.info(

        "No order data available yet. "

        "Open the Add Order page and enter your first order."

    )





# =========================================================

# LOAD DATA

# =========================================================



orders = prepare_orders(load_orders())

feedback = load_feedback()



# =========================================================

# SIDEBAR NAVIGATION

# =========================================================



st.sidebar.title("🍽️ Food Delivery")

st.sidebar.write("Dashboard")



page = st.sidebar.radio(

    "Select a Page",

    [

        "🏠 Dashboard",

        "➕ Add Order",

        "🍕 Food Analysis",

        "👥 Customer Analysis",

        "🏙️ City Analysis",

        "💰 Revenue Analysis",

        "⭐ Customer Feedback",

        "📋 View Data"

    ]

)



st.sidebar.divider()

st.sidebar.caption("Food Delivery Data Analysis Project")



# =========================================================

# 1. DASHBOARD PAGE

# =========================================================



if page == "🏠 Dashboard":

    st.markdown("# 🍽️ Food Delivery Dashboard")
    st.markdown('<div class="dashboard-subtitle">Track your orders, customers, revenue and more — all in one place!</div>', unsafe_allow_html=True)

    total_orders = len(orders)
    total_revenue = float(orders["Amount"].sum()) if not orders.empty else 0
    total_customers = int(orders["Customer_ID"].nunique()) if not orders.empty else 0
    cities_served = int(orders["City"].nunique()) if not orders.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🍔  Total Orders", f"{total_orders:,}")
    c2.metric("👥  Total Customers", f"{total_customers:,}")
    c3.metric("₹  Total Revenue", f"₹{total_revenue:,.0f}")
    c4.metric("📍  Cities Served", f"{cities_served:,}")

    left, right = st.columns([1, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📊 Top Food Items")
        if not orders.empty:
            food_counts = orders.groupby("Food")["Quantity"].sum().sort_values(ascending=False).head(8)
            st.bar_chart(food_counts, color="#38bdf8")
        else:
            st.info("Add an order to see your most popular food items here.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("🥧 Revenue by Food Category")
        if not orders.empty:
            category_map = {
                "Biryani": "Biryani", "Chicken Biryani": "Biryani",
                "Veg Pizza": "Pizza", "Chicken Pizza": "Pizza", "Pizza": "Pizza",
                "Burger": "Burger", "Cheese Burger": "Burger",
                "Fried Rice": "Snacks", "Veg Fried Rice": "Snacks", "Chicken Fried Rice": "Snacks",
                "Noodles": "Snacks", "French Fries": "Snacks", "Sandwich": "Snacks",
                "Coffee": "Beverages", "Tea": "Beverages", "Ice Cream": "Beverages"
            }
            category_data = orders.copy()
            category_data["Category"] = category_data["Food"].map(category_map).fillna("Others")
            category_revenue = category_data.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            st.pyplot(category_revenue.plot.pie(autopct="%1.0f%%", ylabel="", figsize=(5, 3.3), legend=True).figure, use_container_width=True)
        else:
            st.info("Your category chart will appear after you save some orders.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>🍴 Our Food Items</h3>', unsafe_allow_html=True)
    food_cards = [
        ("Burger", 100, "photo-1568901346375-23c9450c58cd"),
        ("Cheese Burger", 130, "photo-1553979459-d2229ba7433a"),
        ("Veg Pizza", 180, "photo-1513104890138-7c749659a591"),
        ("Chicken Pizza", 250, "photo-1571407970349-bc81e7e96d47"),
        ("Biryani", 200, "photo-1563379091339-03246963d96c"),
        ("Fried Rice", 120, "photo-1603133872878-684f208fb84b"),
        ("Noodles", 100, "photo-1569718212165-3a8278d5f624"),
        ("Sandwich", 80, "photo-1528510138849-786a5feddf9b"),
    ]
    cards_html = '<div class="food-grid">'
    for food_name, price, photo_id in food_cards:
        image_url = f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=400&q=80"
        cards_html += f'<div class="food-card"><img src="{image_url}" alt="{food_name}"><div class="food-name">{food_name}</div><div class="food-price">₹{price}</div></div>'
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if not orders.empty:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("🧾 Recent Orders")
        recent_orders = orders.sort_values("Order_Date", ascending=False)
        st.dataframe(recent_orders.head(10), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No order data yet. Open **Add Order** in the sidebar to enter your first order.")

# =========================================================

# 2. ADD ORDER PAGE

# =========================================================



elif page == "➕ Add Order":



    st.title("➕ Add a New Order")

    st.write("Enter the order details using the form below.")



    with st.form("add_order_form"):



        customer_id = st.text_input(

            "Customer ID",

            placeholder="Example: C101"

        ).strip()



        food = st.selectbox(

            "Select Food",

            list(FOOD_PRICES.keys())

        )



        custom_food = ""



        if food == "Other/Custom":

            custom_food = st.text_input(

                "Enter Food Name",

                placeholder="Enter the food item"

            ).strip()



        city = st.text_input(

            "City",

            placeholder="Example: Vijayawada"

        ).strip()



        quantity = st.number_input(

            "Quantity",

            min_value=1,

            max_value=1000,

            value=1,

            step=1

        )



        unit_price = FOOD_PRICES[food]



        if food == "Other/Custom":

            unit_price = st.number_input(

                "Price per Item (₹)",

                min_value=0.0,

                value=100.0,

                step=10.0

            )

            displayed_food = custom_food

        else:

            displayed_food = food

            st.write(f"Price per item: ₹{unit_price:,.2f}")



        order_date = st.date_input(

            "Order Date",

            value=date.today()

        )



        total_amount = unit_price * quantity



        st.info(f"Total Order Amount: ₹{total_amount:,.2f}")



        submitted = st.form_submit_button("Save Order")



        if submitted:



            if not customer_id:

                st.error("Please enter a Customer ID.")



            elif not city:

                st.error("Please enter a city.")



            elif not displayed_food:

                st.error("Please enter or select a food item.")



            elif unit_price <= 0:

                st.error("Please enter a price greater than zero.")



            else:

                order = {

                    "Customer_ID": customer_id,

                    "Food": displayed_food,

                    "City": city,

                    "Quantity": int(quantity),

                    "Amount": round(total_amount, 2),

                    "Order_Date": order_date.isoformat()

                }



                save_order(order)



                st.success("Order saved successfully!")

                st.write(f"Customer ID: {customer_id}")

                st.write(f"Food: {displayed_food}")

                st.write(f"City: {city}")

                st.write(f"Quantity: {quantity}")

                st.write(f"Total Amount: ₹{total_amount:,.2f}")

                st.write(f"Order Date: {order_date}")



                st.rerun()



# =========================================================

# 3. FOOD ANALYSIS PAGE

# =========================================================



elif page == "🍕 Food Analysis":



    st.title("🍕 Food Analysis")

    st.write("Analyze food popularity and sales.")



    if orders.empty:

        show_empty_message()



    else:

        food_analysis = (

            orders.groupby("Food")

            .agg(

                Total_Quantity=("Quantity", "sum"),

                Total_Revenue=("Amount", "sum"),

                Number_of_Orders=("Food", "count")

            )

            .sort_values("Total_Quantity", ascending=False)

        )



        col1, col2 = st.columns(2)



        with col1:

            st.subheader("Most Ordered Foods")

            st.bar_chart(food_analysis["Total_Quantity"])



        with col2:

            st.subheader("Revenue by Food")

            st.bar_chart(

                food_analysis["Total_Revenue"].sort_values(

                    ascending=False

                )

            )



        st.subheader("Food Sales Details")



        st.dataframe(

            food_analysis.reset_index(),

            use_container_width=True,

            hide_index=True

        )



        popular_food = food_analysis["Total_Quantity"].idxmax()



        st.success(f"Most ordered food: {popular_food}")



# =========================================================

# 4. CUSTOMER ANALYSIS PAGE

# =========================================================



elif page == "👥 Customer Analysis":



    st.title("👥 Customer Analysis")

    st.write("Understand customer ordering patterns.")



    if orders.empty:

        show_empty_message()



    else:

        customer_analysis = (

            orders.groupby("Customer_ID")

            .agg(

                Total_Orders=("Customer_ID", "count"),

                Total_Items=("Quantity", "sum"),

                Total_Spent=("Amount", "sum")

            )

            .sort_values("Total_Spent", ascending=False)

        )



        col1, col2 = st.columns(2)



        with col1:

            st.subheader("Orders by Customer")

            st.bar_chart(customer_analysis["Total_Orders"])



        with col2:

            st.subheader("Spending by Customer")

            st.bar_chart(customer_analysis["Total_Spent"])



        st.subheader("Customer Details")



        st.dataframe(

            customer_analysis.reset_index(),

            use_container_width=True,

            hide_index=True

        )



        top_customer = customer_analysis["Total_Spent"].idxmax()

        top_spending = customer_analysis["Total_Spent"].max()



        st.success(

            f"Highest-spending customer: {top_customer} "

            f"(₹{top_spending:,.2f})"

        )



# =========================================================

# 5. CITY ANALYSIS PAGE

# =========================================================



elif page == "🏙️ City Analysis":



    st.title("🏙️ City Analysis")

    st.write("Compare orders and revenue across cities.")



    if orders.empty:

        show_empty_message()



    else:

        city_analysis = (

            orders.groupby("City")

            .agg(

                Total_Orders=("City", "count"),

                Total_Items=("Quantity", "sum"),

                Total_Revenue=("Amount", "sum"),

                Unique_Customers=("Customer_ID", "nunique")

            )

            .sort_values("Total_Revenue", ascending=False)

        )



        col1, col2 = st.columns(2)



        with col1:

            st.subheader("Orders by City")

            st.bar_chart(city_analysis["Total_Orders"])



        with col2:

            st.subheader("Revenue by City")

            st.bar_chart(city_analysis["Total_Revenue"])



        st.subheader("City Details")



        st.dataframe(

            city_analysis.reset_index(),

            use_container_width=True,

            hide_index=True

        )



        best_city = city_analysis["Total_Revenue"].idxmax()



        st.success(f"Highest-revenue city: {best_city}")



# =========================================================

# 6. REVENUE ANALYSIS PAGE

# =========================================================



elif page == "💰 Revenue Analysis":



    st.title("💰 Revenue Analysis")

    st.write("Review revenue generated from saved orders.")



    if orders.empty:

        show_empty_message()



    else:

        total_revenue = orders["Amount"].sum()

        average_order = orders["Amount"].mean()

        highest_order = orders["Amount"].max()



        col1, col2, col3 = st.columns(3)



        col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")

        col2.metric("Average Order Value", f"₹{average_order:,.2f}")

        col3.metric("Highest Order", f"₹{highest_order:,.2f}")



        st.divider()



        st.subheader("Revenue by Food")



        revenue_by_food = (

            orders.groupby("Food")["Amount"]

            .sum()

            .sort_values(ascending=False)

        )



        st.bar_chart(revenue_by_food)



        st.subheader("Revenue by City")



        revenue_by_city = (

            orders.groupby("City")["Amount"]

            .sum()

            .sort_values(ascending=False)

        )



        st.bar_chart(revenue_by_city)



        st.subheader("Revenue Over Time")



        daily_revenue = (

            orders.dropna(subset=["Order_Date"])

            .groupby(

                orders.dropna(subset=["Order_Date"])["Order_Date"].dt.date

            )["Amount"]

            .sum()

        )



        if not daily_revenue.empty:

            st.line_chart(daily_revenue)



        st.subheader("Order Revenue Details")



        st.dataframe(

            orders.sort_values("Order_Date", ascending=False),

            use_container_width=True,

            hide_index=True

        )



# =========================================================

# 7. CUSTOMER FEEDBACK PAGE

# =========================================================



elif page == "⭐ Customer Feedback":



    st.title("⭐ Customer Feedback")

    st.write("Submit and review customer feedback.")



    st.subheader("Submit Feedback")



    with st.form("feedback_form"):



        feedback_customer = st.text_input(

            "Customer ID",

            placeholder="Example: C101"

        ).strip()



        feedback_food = st.text_input(

            "Food Item",

            placeholder="Example: Burger"

        ).strip()



        rating = st.slider(

            "Rating",

            min_value=1,

            max_value=5,

            value=5

        )



        feedback_type = st.selectbox(

            "Feedback Type",

            [

                "Positive",

                "Negative",

                "Suggestion",

                "Other"

            ]

        )



        comment = st.text_area(

            "Comments",

            placeholder="Write your feedback here..."

        )



        feedback_date = st.date_input(

            "Feedback Date",

            value=date.today()

        )



        feedback_submitted = st.form_submit_button(

            "Save Feedback"

        )



        if feedback_submitted:



            if not feedback_customer:

                st.error("Please enter a Customer ID.")



            elif not feedback_food:

                st.error("Please enter the food item.")



            else:

                new_feedback = {

                    "Customer_ID": feedback_customer,

                    "Food": feedback_food,

                    "Rating": int(rating),

                    "Feedback_Type": feedback_type,

                    "Comment": comment,

                    "Feedback_Date": feedback_date.isoformat()

                }



                save_feedback(new_feedback)



                st.success("Customer feedback saved successfully!")

                st.rerun()



    st.divider()

    st.subheader("Saved Customer Feedback")



    feedback = load_feedback()



    if feedback.empty:

        st.info("No customer feedback has been submitted yet.")



    else:

        feedback["Rating"] = pd.to_numeric(

            feedback["Rating"], errors="coerce"

        )



        col1, col2 = st.columns(2)



        with col1:

            st.metric(

                "Total Feedback Records",

                len(feedback)

            )



        with col2:

            average_rating = feedback["Rating"].mean()



            if pd.notna(average_rating):

                st.metric(

                    "Average Rating",

                    f"{average_rating:.2f} / 5"

                )

            else:

                st.metric("Average Rating", "N/A")



        st.subheader("Feedback by Type")



        feedback_counts = feedback["Feedback_Type"].value_counts()



        if not feedback_counts.empty:

            st.bar_chart(feedback_counts)



        st.subheader("Feedback Records")



        st.dataframe(

            feedback.sort_values(

                "Feedback_Date", ascending=False

            ),

            use_container_width=True,

            hide_index=True

        )



# =========================================================

# 8. VIEW DATA PAGE

# =========================================================



elif page == "📋 View Data":



    st.title("📋 View Saved Data")

    st.write("View and download your stored orders and feedback.")



    st.subheader("All Orders")



    orders = prepare_orders(load_orders())



    if orders.empty:

        st.info("No orders have been saved yet.")



    else:

        st.dataframe(

            orders.sort_values("Order_Date", ascending=False),

            use_container_width=True,

            hide_index=True

        )



        orders_csv = load_orders().to_csv(index=False).encode("utf-8")



        st.download_button(

            label="⬇️ Download Orders CSV",

            data=orders_csv,

            file_name="food_delivery_orders.csv",

            mime="text/csv"

        )



    st.divider()



    st.subheader("All Customer Feedback")



    feedback = load_feedback()



    if feedback.empty:

        st.info("No customer feedback has been saved yet.")



    else:

        st.dataframe(

            feedback,

            use_container_width=True,

            hide_index=True

        )



        feedback_csv = feedback.to_csv(index=False).encode("utf-8")



        st.download_button(

            label="⬇️ Download Feedback CSV",

            data=feedback_csv,

            file_name="customer_feedback.csv",

            mime="text/csv"

        )



    st.divider()



    st.subheader("Data Storage Information")



    st.write(f"Orders file: `{ORDER_FILE}`")

    st.write(f"Feedback file: `{FEEDBACK_FILE}`")



    st.caption(

        "Your orders and feedback are saved locally in CSV files. "

        "Keep the data folder and its CSV files to retain your records."

    )