import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/Sample - Superstore.csv",
        encoding="latin1"
    )

    # FIX: pastikan datetime aman
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    return df

df = load_data()

# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.header("🔍 Filters")

selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

selected_categories = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

df_filtered = df[
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories))
]

# ==================================================
# KPI CALCULATIONS
# ==================================================
total_sales = df_filtered["Sales"].sum()
total_profit = df_filtered["Profit"].sum()
total_orders = df_filtered["Order ID"].nunique()
total_customers = df_filtered["Customer ID"].nunique()

profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

# ==================================================
# HEADER
# ==================================================
st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive Business Intelligence Dashboard built with Python, Pandas, Plotly, and Streamlit")

# ==================================================
# KPI CARDS
# ==================================================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Customers", f"{total_customers:,}")
col5.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# ==================================================
# MONTHLY SALES TREND (FIXED)
# ==================================================
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    df_filtered
    .dropna(subset=["Order Date"])
    .groupby(pd.Grouper(key="Order Date", freq="MS"))  # FIX: pakai MS
    ["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# ==================================================
# SALES BY REGION & PROFIT BY CATEGORY
# ==================================================
col_left, col_right = st.columns(2)

region_sales = (
    df_filtered.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region"
)

col_left.plotly_chart(fig_region, use_container_width=True)

category_profit = (
    df_filtered.groupby("Category")["Profit"]
    .sum()
    .reset_index()
)

fig_profit = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    title="Profit by Category"
)

col_right.plotly_chart(fig_profit, use_container_width=True)

# ==================================================
# TOP PRODUCTS
# ==================================================
st.subheader("🏆 Top 10 Products")

top_products = (
    df_filtered.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products"
)

st.plotly_chart(fig_products, use_container_width=True)

# ==================================================
# TOP CUSTOMERS
# ==================================================
st.subheader("👥 Top 10 Customers")

top_customers = (
    df_filtered.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_customers = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    title="Top 10 Customers"
)

st.plotly_chart(fig_customers, use_container_width=True)

# ==================================================
# EXECUTIVE SUMMARY
# ==================================================
st.subheader("📋 Executive Summary")

best_region = df_filtered.groupby("Region")["Sales"].sum().idxmax()
best_category = df_filtered.groupby("Category")["Profit"].sum().idxmax()

st.info(
    f"""
    ✅ Best Sales Region: {best_region}
    
    ✅ Most Profitable Category: {best_category}
    
    ✅ Total Profit Generated: ${total_profit:,.0f}
    
    ✅ Profit Margin: {profit_margin:.2f}%
    """
)
