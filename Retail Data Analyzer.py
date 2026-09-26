import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="Retail Sales Analyzer",
    page_icon="🛒",
    layout="wide"
)


class RetailAnalyzer:

    def __init__(self):
        self.df = None

    def load_data(self, file):
        try:
            self.df = pd.read_csv(file)

            required_columns = [
                "Date",
                "Product",
                "Category",
                "Price",
                "Quantity Sold",
                "Total Sales"
            ]

            for column in required_columns:
                if column not in self.df.columns:
                    return False, f"Missing column: {column}"

            self.df["Date"] = pd.to_datetime(
                self.df["Date"],
                errors="coerce"
            )

            self.df["Price"] = pd.to_numeric(
                self.df["Price"],
                errors="coerce"
            )

            self.df["Quantity Sold"] = pd.to_numeric(
                self.df["Quantity Sold"],
                errors="coerce"
            )

            self.df["Total Sales"] = pd.to_numeric(
                self.df["Total Sales"],
                errors="coerce"
            )

            key_columns = [
                "Date",
                "Price",
                "Quantity Sold",
                "Total Sales"
            ]

            self.df = self.df.dropna(
                subset=key_columns
            )

            self.df = self.df.sort_values(
                "Date"
            ).reset_index(drop=True)

            if len(self.df) == 0:
                return False, "No valid data found."

            return True, "Dataset loaded successfully!"

        except Exception as e:
            return False, str(e)

    def metrics(self):
        total_sales = self.df["Total Sales"].sum()
        average_sales = self.df["Total Sales"].mean()
        total_quantity = self.df["Quantity Sold"].sum()

        popular_product = (
            self.df.groupby("Product")["Quantity Sold"]
            .sum()
            .idxmax()
        )

        return (
            total_sales,
            average_sales,
            total_quantity,
            popular_product
        )


# =========================
# HEADER
# =========================

st.title("🛒 Retail Sales Data Analyzer")
st.write(
    "Analyze retail sales data using Pandas, NumPy, "
    "Matplotlib, Seaborn and Streamlit."
)

st.divider()


# =========================
# LOAD DATA
# =========================

analyzer = RetailAnalyzer()

uploaded_file = st.sidebar.file_uploader(
    "Upload Retail CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    success, message = analyzer.load_data(
        uploaded_file
    )

elif os.path.exists("retail_sales_dataset.csv"):

    success, message = analyzer.load_data(
        "retail_sales_dataset.csv"
    )

else:
    success = False
    message = "Please upload a CSV file."


if not success:

    st.warning(message)

    st.info(
        "CSV file must contain: Date, Product, "
        "Category, Price, Quantity Sold, Total Sales"
    )

    st.stop()


st.sidebar.success("Dataset Loaded")


# =========================
# SIDEBAR
# =========================

st.sidebar.header("📊 Navigation")

option = st.sidebar.radio(
    "Select Analysis",
    [
        "Dashboard",
        "Show Data",
        "Basic Information",
        "Statistical Summary",
        "Filter Data",
        "Category Sales",
        "Sales Trend",
        "Correlation Heatmap",
        "NumPy Analysis"
    ]
)


# =========================
# DASHBOARD
# =========================

if option == "Dashboard":

    st.header("📊 Sales Dashboard")

    total_sales, average_sales, total_quantity, popular_product = (
        analyzer.metrics()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Total Sales",
            f"{total_sales:,.2f}"
        )

    with col2:
        st.metric(
            "📈 Average Sales",
            f"{average_sales:,.2f}"
        )

    with col3:
        st.metric(
            "📦 Total Quantity",
            f"{total_quantity:,.0f}"
        )

    with col4:
        st.metric(
            "🏆 Popular Product",
            popular_product
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Category Wise Sales")

        category_sales = (
            analyzer.df
            .groupby("Category")["Total Sales"]
            .sum()
        )

        st.bar_chart(category_sales)

    with col2:

        st.subheader("Sales Trend")

        daily_sales = (
            analyzer.df
            .groupby("Date")["Total Sales"]
            .sum()
        )

        st.line_chart(daily_sales)


# =========================
# SHOW DATA
# =========================

elif option == "Show Data":

    st.header("📋 Retail Sales Data")

    st.dataframe(
        analyzer.df,
        use_container_width=True
    )


# =========================
# BASIC INFORMATION
# =========================

elif option == "Basic Information":

    st.header("ℹ️ Basic Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Rows",
            analyzer.df.shape[0]
        )

    with col2:
        st.metric(
            "Columns",
            analyzer.df.shape[1]
        )

    st.subheader("Column Names")

    for column in analyzer.df.columns:
        st.write("•", column)

    st.subheader("Data Types")

    st.dataframe(
        analyzer.df.dtypes.astype(str),
        use_container_width=True
    )


# =========================
# STATISTICAL SUMMARY
# =========================

elif option == "Statistical Summary":

    st.header("📈 Statistical Summary")

    st.dataframe(
        analyzer.df.describe(),
        use_container_width=True
    )

    st.subheader("Category Wise Sales")

    category_sales = (
        analyzer.df
        .groupby("Category")["Total Sales"]
        .sum()
        .reset_index()
    )

    st.dataframe(
        category_sales,
        use_container_width=True
    )


# =========================
# FILTER DATA
# =========================

elif option == "Filter Data":

    st.header("🔎 Filter Sales Data")

    col1, col2 = st.columns(2)

    with col1:

        categories = [
            "All"
        ] + sorted(
            analyzer.df["Category"]
            .astype(str)
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "Select Category",
            categories
        )

    with col2:

        min_date = analyzer.df["Date"].min().date()
        max_date = analyzer.df["Date"].max().date()

        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    filtered_df = analyzer.df.copy()

    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ]

    if len(date_range) == 2:

        start_date = pd.to_datetime(
            date_range[0]
        )

        end_date = pd.to_datetime(
            date_range[1]
        )

        filtered_df = filtered_df[
            (filtered_df["Date"] >= start_date)
            &
            (filtered_df["Date"] <= end_date)
        ]

    st.write(
        "Filtered Records:",
        len(filtered_df)
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# =========================
# CATEGORY SALES
# =========================

elif option == "Category Sales":

    st.header("📊 Category Wise Sales")

    data = (
        analyzer.df
        .groupby("Category")["Total Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(data)

    st.subheader("Category Sales Table")

    st.dataframe(
        data.reset_index(),
        use_container_width=True
    )


# =========================
# SALES TREND
# =========================

elif option == "Sales Trend":

    st.header("📈 Sales Trend Over Time")

    data = (
        analyzer.df
        .groupby("Date")["Total Sales"]
        .sum()
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        data.index,
        data.values,
        marker="o"
    )

    ax.set_title(
        "Sales Trend Over Time"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Total Sales")

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)


# =========================
# HEATMAP
# =========================

elif option == "Correlation Heatmap":

    st.header("🔥 Sales Data Correlation")

    data = analyzer.df[
        [
            "Price",
            "Quantity Sold",
            "Total Sales"
        ]
    ]

    correlation = data.corr()

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    ax.set_title(
        "Sales Data Correlation"
    )

    st.pyplot(fig)


# =========================
# NUMPY ANALYSIS
# =========================

elif option == "NumPy Analysis":

    st.header("🔢 NumPy Analysis")

    sales = np.array(
        analyzer.df["Total Sales"]
    )

    total_sales = np.sum(sales)
    average_sales = np.mean(sales)
    highest_sale = np.max(sales)
    lowest_sale = np.min(sales)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Sales",
            f"{total_sales:,.2f}"
        )

        st.metric(
            "Average Sales",
            f"{average_sales:,.2f}"
        )

    with col2:

        st.metric(
            "Highest Sale",
            f"{highest_sale:,.2f}"
        )

        st.metric(
            "Lowest Sale",
            f"{lowest_sale:,.2f}"
        )

    st.subheader("Growth Percentage")

    if len(sales) > 1:

        if sales[0] == 0:

            st.warning(
                "Growth cannot be calculated because "
                "the first sale value is 0."
            )

        else:

            growth = (
                (sales[-1] - sales[0])
                / sales[0]
            ) * 100

            st.metric(
                "Sales Growth",
                f"{growth:.2f}%"
            )

    st.subheader("NumPy Sales Array")

    st.write(sales)
