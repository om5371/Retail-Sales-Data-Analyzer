import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Retail Sales Data Analyzer",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for modern UI cards
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px;
        font-weight: 700;
        color: #1e3a8a;
    }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(file_path_or_buffer):
  df = pd.read_csv(file_path_or_buffer)
  # Clean column headers
  df.columns = df.columns.str.strip()

  # Handle variations in column names if any
  rename_map = {
      "Product Category": "Product",
      "Quantity Sold": "Quantity",
      "Price": "Price per Unit",
      "Total Sales": "Total Amount",
  }
  df = df.rename(columns=rename_map)

  # Convert Date column to datetime
  if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

  return df


# App Header
st.title("🛒 Retail Sales Data Analyzer")
st.markdown(
    "Analyze retail sales trends, customer demographics, and product"
    " performance."
)
st.write("---")

# Sidebar Configuration
st.sidebar.header("📁 Data Source & Filters")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

# Load file: either from uploader or fallback to default local file
try:
  if uploaded_file is not None:
    df = load_data(uploaded_file)
  else:
    df = load_data("retail_sales_dataset.csv")
except Exception as e:
  st.error(
      f"Could not load data file. Please ensure 'retail_sales_dataset.csv' is"
      f" present or upload a file. Error: {e}"
  )
  st.stop()

# Ensure mandatory columns exist
required_columns = [
    "Transaction ID",
    "Date",
    "Customer ID",
    "Gender",
    "Age",
    "Product",
    "Quantity",
    "Price per Unit",
    "Total Amount",
]

missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
  st.error(f"Missing required columns in dataset: {', '.join(missing_cols)}")
  st.stop()

# Sidebar Filters
st.sidebar.subheader("Filter Dataset")

# Product Filter
products = sorted(df["Product"].dropna().unique().tolist())
selected_products = st.sidebar.multiselect(
    "Select Products", options=products, default=products
)

# Gender Filter
genders = sorted(df["Gender"].dropna().unique().tolist())
selected_genders = st.sidebar.multiselect(
    "Select Gender", options=genders, default=genders
)

# Date Filter
min_date = df["Date"].min()
max_date = df["Date"].max()

if pd.notnull(min_date) and pd.notnull(max_date):
  date_range = st.sidebar.date_input(
      "Select Date Range",
      value=(min_date.date(), max_date.date()),
      min_value=min_date.date(),
      max_value=max_date.date(),
  )
else:
  date_range = None

# Apply Filters
filtered_df = df[
    (df["Product"].isin(selected_products))
    & (df["Gender"].isin(selected_genders))
]

if date_range and len(date_range) == 2:
  start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(
      date_range[1]
  )
  filtered_df = filtered_df[
      (filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)
  ]

# Top KPI Metric Cards
total_revenue = filtered_df["Total Amount"].sum()
total_transactions = filtered_df["Transaction ID"].nunique()
total_units_sold = filtered_df["Quantity"].sum()
avg_order_value = (
    filtered_df["Total Amount"].mean() if not filtered_df.empty else 0
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Transactions", f"{total_transactions:,}")
col3.metric("Units Sold", f"{total_units_sold:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.write("---")

# Visualizations Row 1: Sales Trends & Product Performance
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
  st.subheader("📈 Monthly Sales Trend")
  if not filtered_df.empty:
    trend_df = (
        filtered_df.set_index("Date")
        .resample("M")["Total Amount"]
        .sum()
        .reset_index()
    )
    trend_df["Month"] = trend_df["Date"].dt.strftime("%b %Y")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(
        data=trend_df,
        x="Month",
        y="Total Amount",
        marker="o",
        color="#2563eb",
        ax=ax,
    )
    plt.xticks(rotation=45)
    plt.ylabel("Revenue ($)")
    plt.xlabel("")
    plt.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)
  else:
    st.info("No data available for the selected filters.")

with chart_col2:
  st.subheader("🏷️ Revenue by Product")
  if not filtered_df.empty:
    prod_sales = (
        filtered_df.groupby("Product")["Total Amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(
        data=prod_sales,
        x="Total Amount",
        y="Product",
        palette="Blues_r",
        ax=ax,
    )
    plt.xlabel("Revenue ($)")
    plt.ylabel("")
    st.pyplot(fig)
  else:
    st.info("No data available for the selected filters.")

# Visualizations Row 2: Customer Demographics
st.write("---")
demo_col1, demo_col2 = st.columns(2)

with demo_col1:
  st.subheader("👥 Sales by Gender")
  if not filtered_df.empty:
    gender_sales = filtered_df.groupby("Gender")["Total Amount"].sum()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(
        gender_sales,
        labels=gender_sales.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#3b82f6", "#ec4899", "#10b981"],
    )
    st.pyplot(fig)
  else:
    st.info("No data available for the selected filters.")

with demo_col2:
  st.subheader("🎂 Age Distribution")
  if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(
        filtered_df["Age"],
        bins=15,
        kde=True,
        color="#4f46e5",
        ax=ax,
    )
    plt.xlabel("Customer Age")
    plt.ylabel("Frequency")
    st.pyplot(fig)
  else:
    st.info("No data available for the selected filters.")

# Detailed Data Table
st.write("---")
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)
