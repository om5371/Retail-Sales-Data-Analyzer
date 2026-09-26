import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# PAGE SETUP & MODERN DASHBOARD STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Retail Performance Analytics Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 14px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
    }
    /* Section Headers */
    .section-header {
        font-size: 19px;
        font-weight: 700;
        color: #1e293b;
        margin-top: 10px;
        margin-bottom: 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DATA INGESTION & PIPELINE ENGINE
# ---------------------------------------------------------
@st.cache_data
def get_datasource():
  dataset_path = "retail_sales_dataset.csv"
  if not os.path.exists(dataset_path):
    st.error(
        f"Critical Error: Data source '{dataset_path}' not detected in the root"
        " directory."
    )
    st.stop()

  df = pd.read_csv(dataset_path)
  df.columns = df.columns.str.strip()

  # Harmonize column signatures
  schema_mapping = {
      "Product Category": "Product",
      "Quantity Sold": "Quantity",
      "Price": "Price per Unit",
      "Total Sales": "Total Amount",
  }
  df = df.rename(columns=schema_mapping)

  # Cast temporal attributes
  if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

  return df


df_raw = get_datasource()

# ---------------------------------------------------------
# SIDEBAR CONTROLLER & SMART FILTERS
# ---------------------------------------------------------
st.sidebar.image(
    "https://img.icons8.com/fluency/96/shop.png",
    width=64,
)
st.sidebar.title("Data Controls")
st.sidebar.markdown("Refine your analytics view dynamically.")

# 1. Product Filter with Quick Reset
available_products = sorted(df_raw["Product"].dropna().unique().tolist())
selected_products = st.sidebar.multiselect(
    "Filter by Category / Product",
    options=available_products,
    default=available_products,
)

# 2. Gender Segment Filter
available_genders = sorted(df_raw["Gender"].dropna().unique().tolist())
selected_genders = st.sidebar.multiselect(
    "Filter by Customer Demographics",
    options=available_genders,
    default=available_genders,
)

# 3. Dynamic Date Window
min_date = df_raw["Date"].min()
max_date = df_raw["Date"].max()

if pd.notnull(min_date) and pd.notnull(max_date):
  date_selection = st.sidebar.date_input(
      "Reporting Period",
      value=(min_date.date(), max_date.date()),
      min_value=min_date.date(),
      max_value=max_date.date(),
  )
else:
  date_selection = None

# Smart Fallback Logic: Protect dashboard from zero-selection collapse
filter_products = (
    selected_products if selected_products else available_products
)
filter_genders = selected_genders if selected_genders else available_genders

filtered_df = df_raw[
    (df_raw["Product"].isin(filter_products))
    & (df_raw["Gender"].isin(filter_genders))
]

if date_selection and len(date_selection) == 2:
  start_bound, end_bound = pd.to_datetime(date_selection[0]), pd.to_datetime(
      date_selection[1]
  )
  filtered_df = filtered_df[
      (filtered_df["Date"] >= start_bound) & (filtered_df["Date"] <= end_bound)
  ]

# ---------------------------------------------------------
# APPLICATION HEADER
# ---------------------------------------------------------
st.title("Executive Retail Performance Suite")
st.caption(
    "Enterprise Diagnostic Platform • Revenue Patterns, Customer Segmentation"
    " & Basket Analysis"
)
st.markdown("---")

# ---------------------------------------------------------
# HIGH-IMPACT KPI METRICS ROW
# ---------------------------------------------------------
total_revenue = (
    filtered_df["Total Amount"].sum() if not filtered_df.empty else 0
)
total_orders = (
    filtered_df["Transaction ID"].nunique() if not filtered_df.empty else 0
)
units_moved = filtered_df["Quantity"].sum() if not filtered_df.empty else 0
avg_basket_value = (
    filtered_df["Total Amount"].mean() if not filtered_df.empty else 0
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Gross Revenue", f"${total_revenue:,.2f}")
kpi2.metric("Executed Orders", f"{total_orders:,}")
kpi3.metric("Total Units Sold", f"{units_moved:,}")
kpi4.metric("Average Ticket Size", f"${avg_basket_value:,.2f}")

st.markdown("---")

# ---------------------------------------------------------
# ANALYTIC ROW 1: TIME SERIES & PRODUCT CONTRIBUTION
# ---------------------------------------------------------
col_left, col_right = st.columns((6, 4))

with col_left:
  st.markdown(
      '<div class="section-header">📈 Revenue Trend Over Time</div>',
      unsafe_allow_html=True,
  )
  if not filtered_df.empty and filtered_df["Date"].notnull().any():
    trend_df = (
        filtered_df.dropna(subset=["Date"])
        .set_index("Date")
        .resample("ME")["Total Amount"]
        .sum()
        .reset_index()
    )
    trend_df["Period"] = trend_df["Date"].dt.strftime("%b %Y")

    fig_trend = px.line(
        trend_df,
        x="Period",
        y="Total Amount",
        markers=True,
        labels={"Total Amount": "Gross Sales ($)", "Period": "Reporting Cycle"},
        template="plotly_white",
    )
    fig_trend.update_traces(
        line=dict(color="#2563eb", width=3),
        marker=dict(size=8, color="#1e40af"),
    )
    fig_trend.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
    )
    st.plotly_chart(fig_trend, use_container_width=True)
  else:
    st.info("No transactional records found matching this criterion.")

with col_right:
  st.markdown(
      '<div class="section-header">🏷️ Product Contribution Breakdown</div>',
      unsafe_allow_html=True,
  )
  if not filtered_df.empty:
    cat_df = (
        filtered_df.groupby("Product")["Total Amount"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig_bar = px.bar(
        cat_df,
        x="Total Amount",
        y="Product",
        orientation="h",
        text_auto="$,.0f",
        labels={"Total Amount": "Revenue ($)", "Product": ""},
        template="plotly_white",
        color="Total Amount",
        color_continuous_scale="Blues",
    )
    fig_bar.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# ANALYTIC ROW 2: DEMOGRAPHIC DYNAMICS & BEHAVIOR
# ---------------------------------------------------------
col_demo1, col_demo2 = st.columns(2)

with col_demo1:
  st.markdown(
      '<div class="section-header">👥 Demographics: Revenue by Gender</div>',
      unsafe_allow_html=True,
  )
  if not filtered_df.empty:
    gender_df = (
        filtered_df.groupby("Gender")["Total Amount"].sum().reset_index()
    )
    fig_pie = px.pie(
        gender_df,
        values="Total Amount",
        names="Gender",
        hole=0.45,
        color_discrete_sequence=["#3b82f6", "#ec4899", "#10b981"],
        template="plotly_white",
    )
    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hoverinfo="label+value+percent",
    )
    fig_pie.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5
        ),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_demo2:
  st.markdown(
      '<div class="section-header">🎂 Customer Age Cohort Distribution</div>',
      unsafe_allow_html=True,
  )
  if not filtered_df.empty:
    fig_hist = px.histogram(
        filtered_df,
        x="Age",
        nbins=16,
        marginal="box",
        labels={"Age": "Customer Age", "count": "Transactions"},
        template="plotly_white",
        color_discrete_sequence=["#6366f1"],
    )
    fig_hist.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# COMPREHENSIVE DATA ENGINE & EXPORT CAPABILITY
# ---------------------------------------------------------
st.markdown(
    '<div class="section-header">📋 Granular Transaction Registry</div>',
    unsafe_allow_html=True,
)

# Convert formatted preview for reporting
display_df = filtered_df.copy()
if "Date" in display_df.columns:
  display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)

# CSV Export Feature
csv_download = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Export Filtered Dataset to CSV",
    data=csv_download,
    file_name="filtered_retail_analytics.csv",
    mime="text/csv",
)
