import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Retail Sales Analyzer",
    page_icon="📊",
    layout="wide"
)

# ================= PAGE STYLE =================
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}
[data-testid="stMetric"] {
    background-color: #f7f7f7;
    border: 1px solid #dddddd;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ================= RETAIL ANALYZER =================
class RetailAnalyzer:

    def __init__(self):
        self.df = None

    def load_data(self, file_path):
        try:
            self.df = pd.read_csv(file_path)

            required_columns = [
                "Date", "Product", "Category",
                "Price", "Quantity Sold", "Total Sales"
            ]

            for column in required_columns:
                if column not in self.df.columns:
                    return False, f"Missing column: {column}"

            self.df["Date"] = pd.to_datetime(
                self.df["Date"], errors="coerce"
            )

            self.df["Price"] = pd.to_numeric(
                self.df["Price"], errors="coerce"
            )

            self.df["Quantity Sold"] = pd.to_numeric(
                self.df["Quantity Sold"], errors="coerce"
            )

            self.df["Total Sales"] = pd.to_numeric(
                self.df["Total Sales"], errors="coerce"
            )

            key_columns = [
                "Date", "Price", "Quantity Sold", "Total Sales"
            ]

            self.df = self.df.dropna(subset=key_columns)
            self.df = self.df.sort_values("Date").reset_index(drop=True)

            if len(self.df) == 0:
                return False, "No valid rows found after cleaning."

            return True, "Dataset loaded successfully!"

        except FileNotFoundError:
            return False, "File not found."
        except Exception as e:
            return False, f"Error: {e}"

    def calculate_metrics(self):
        total_sales = self.df["Total Sales"].sum()
        average_sales = self.df["Total Sales"].mean()
        total_quantity = self.df["Quantity Sold"].sum()

        popular_product = (
            self.df.groupby("Product")["Quantity Sold"]
            .sum()
            .idxmax()
        )

        sales_array = np.array(self.df["Total Sales"])
        numpy_average = np.mean(sales_array)

        return (
            total_sales,
            average_sales,
            total_quantity,
            popular_product,
            numpy_average
        )


# ================= HEADER =================
st.title("📊 Retail Sales Data Analyzer")
st.write("Analyze your retail sales dataset using Pandas, NumPy and visualizations.")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Retail CSV File",
    type=["csv"]
)

analyzer = RetailAnalyzer()

# Load uploaded file or default CSV
if uploaded_file is not None:
    success, message = analyzer.load_data(uploaded_file)
else:
    try:
        success, message = analyzer.load_data("retail_sales_dataset.csv")
    except Exception:
        success = False
        message = "Upload a CSV file to start."

if success:

    st.sidebar.success("Dataset loaded")

    # ================= TOP METRICS =================
    total_sales, average_sales, total_quantity, popular_product, numpy_average = (
        analyzer.calculate_metrics()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Sales", f"₹{total_sales:,.2f}")
    col2.metric("📈 Average Sale", f"₹{average_sales:,.2f}")
    col3.metric("📦 Quantity Sold", f"{total_quantity:,.0f}")
    col4.metric("🏆 Popular Product", popular_product)

    st.divider()

    # ================= MENU =================
    option = st.sidebar.selectbox(
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

    # ================= DASHBOARD =================
    if option == "Dashboard":

        st.subheader("📊 Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            category_sales = (
                analyzer.df.groupby("Category")["Total Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            fig, ax = plt.subplots(figsize=(7, 4))
            category_sales.plot(kind="bar", ax=ax)
            ax.set_title("Total Sales by Category")
            ax.set_xlabel("Category")
            ax.set_ylabel("Total Sales")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            daily_sales = (
                analyzer.df.groupby("Date")["Total Sales"]
                .sum()
            )

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(
                daily_sales.index,
                daily_sales.values,
                marker="o"
            )
            ax.set_title("Sales Trend Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Total Sales")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

    # ================= SHOW DATA =================
    elif option == "Show Data":

        st.subheader("📋 Retail Sales Data")
        st.dataframe(
            analyzer.df,
            use_container_width=True,
            hide_index=True
        )

    # ================= BASIC INFORMATION =================
    elif option == "Basic Information":

        st.subheader("ℹ️ Basic Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", analyzer.df.shape[0])
            st.metric("Columns", analyzer.df.shape[1])

        with col2:
            st.write("**Column Names:**")
            st.write(list(analyzer.df.columns))

        st.write("**Data Types:**")
        st.dataframe(
            analyzer.df.dtypes.astype(str).rename("Data Type"),
            use_container_width=True
        )

    # ================= STATISTICAL SUMMARY =================
    elif option == "Statistical Summary":

        st.subheader("📈 Statistical Summary")

        st.dataframe(
            analyzer.df.describe(),
            use_container_width=True
        )

    # ================= FILTER DATA =================
    elif option == "Filter Data":

        st.subheader("🔎 Filter Data")

        filter_type = st.radio(
            "Choose Filter",
            ["Category", "Date Range"],
            horizontal=True
        )

        if filter_type == "Category":

            categories = sorted(
                analyzer.df["Category"].astype(str).unique()
            )

            category = st.selectbox(
                "Select Category",
                categories
            )

            result = analyzer.df[
                analyzer.df["Category"].astype(str) == category
            ]

            st.write(f"**Records found:** {len(result)}")
            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        else:

            min_date = analyzer.df["Date"].min().date()
            max_date = analyzer.df["Date"].max().date()

            date_range = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            if len(date_range) == 2:
                start_date, end_date = date_range

                result = analyzer.df[
                    (analyzer.df["Date"].dt.date >= start_date)
                    & (analyzer.df["Date"].dt.date <= end_date)
                ]

                st.write(f"**Records found:** {len(result)}")
                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

    # ================= CATEGORY SALES =================
    elif option == "Category Sales":

        st.subheader("📊 Category Wise Sales")

        category_sales = (
            analyzer.df.groupby("Category")["Total Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        st.dataframe(
            category_sales.rename("Total Sales"),
            use_container_width=True
        )

        fig, ax = plt.subplots(figsize=(9, 5))
        category_sales.plot(kind="bar", ax=ax)
        ax.set_title("Total Sales by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

    # ================= SALES TREND =================
    elif option == "Sales Trend":

        st.subheader("📈 Sales Trend Over Time")

        daily_sales = (
            analyzer.df.groupby("Date")["Total Sales"]
            .sum()
        )

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(
            daily_sales.index,
            daily_sales.values,
            marker="o"
        )
        ax.set_title("Sales Trend Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

    # ================= HEATMAP =================
    elif option == "Correlation Heatmap":

        st.subheader("🔥 Sales Data Correlation")

        data = analyzer.df[
            ["Price", "Quantity Sold", "Total Sales"]
        ]

        correlation = data.corr()

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        ax.set_title("Sales Data Correlation")
        plt.tight_layout()

        st.pyplot(fig)

    # ================= NUMPY ANALYSIS =================
    elif option == "NumPy Analysis":

        st.subheader("🔢 NumPy Analysis")

        sales = np.array(analyzer.df["Total Sales"])

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Sales", f"₹{np.sum(sales):,.2f}")
        col2.metric("Average Sales", f"₹{np.mean(sales):,.2f}")
        col3.metric("Highest Sale", f"₹{np.max(sales):,.2f}")
        col4.metric("Lowest Sale", f"₹{np.min(sales):,.2f}")

        if len(sales) > 1 and sales[0] != 0:
            growth = ((sales[-1] - sales[0]) / sales[0]) * 100

            st.info(
                f"Growth Percentage from first to latest sale: "
                f"{growth:.2f}%"
            )
        elif len(sales) > 1:
            st.warning("Growth percentage cannot be calculated because the first sale is 0.")

else:
    st.warning(message)

    st.info(
        "Please upload your retail_sales_dataset.csv file from the sidebar."
    )

    st.markdown("""
    ### Required CSV Columns

    Your CSV should contain these columns:

    - Date
    - Product
    - Category
    - Price
    - Quantity Sold
    - Total Sales
    """)
