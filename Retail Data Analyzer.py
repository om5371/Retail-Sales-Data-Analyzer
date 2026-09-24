import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


class RetailAnalyzer:

    def __init__(self):
        self.df = None

    # ================= LOAD DATA =================
    def load_data(self, file_path):

        try:
            self.df = pd.read_csv(file_path)

            # Required columns
            required_columns = [
                "Date",
                "Product",
                "Category",
                "Price",
                "Quantity Sold",
                "Total Sales"
            ]

            # Check columns
            for column in required_columns:
                if column not in self.df.columns:
                    print("Missing column:", column)
                    return False

            # Convert date
            self.df["Date"] = pd.to_datetime(
                self.df["Date"],
                errors="coerce"
            )

            # Convert numeric columns
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

            # BUG FIX #3: only drop rows where the columns we actually
            # need for calculations are missing, not ANY column at all.
            key_columns = ["Date", "Price", "Quantity Sold", "Total Sales"]

            if self.df[key_columns].isnull().sum().sum() > 0:
                print("\nMissing values found in key columns.")
                self.df = self.df.dropna(subset=key_columns)
                print("Missing rows removed.")

            # BUG FIX #2: sort by date so growth/line-graph calculations
            # are chronological instead of whatever order the CSV happened
            # to be in.
            self.df = self.df.sort_values("Date").reset_index(drop=True)

            if len(self.df) == 0:
                print("\nNo valid rows left after cleaning the data.")
                return False

            print("\nDataset loaded successfully!")
            print("Total Records:", len(self.df))

            return True

        except FileNotFoundError:
            print("File not found!")
            return False

        except Exception as e:
            print("Error:", e)
            return False

    # ================= CALCULATE METRICS =================
    def calculate_metrics(self):

        if self.df is None or len(self.df) == 0:
            print("Please load dataset first.")
            return

        total_sales = self.df["Total Sales"].sum()

        average_sales = self.df["Total Sales"].mean()

        popular_product = (
            self.df.groupby("Product")["Quantity Sold"]
            .sum()
            .idxmax()
        )

        total_quantity = self.df["Quantity Sold"].sum()

        # NumPy calculation
        sales_array = np.array(self.df["Total Sales"])

        numpy_average = np.mean(sales_array)

        print("\n========== SALES METRICS ==========")
        print("Total Sales       :", round(total_sales, 2))
        print("Average Sales     :", round(average_sales, 2))
        print("Total Quantity    :", total_quantity)
        print("Popular Product   :", popular_product)
        print("NumPy Average     :", round(numpy_average, 2))

    # ================= FILTER DATA =================
    def filter_data(self):

        if self.df is None:
            print("Please load dataset first.")
            return

        print("\n1. Filter by Category")
        print("2. Filter by Date")

        choice = input("Enter choice: ")

        if choice == "1":

            print("\nAvailable Categories:")
            print(self.df["Category"].unique())

            category = input("Enter category: ")

            result = self.df[
                self.df["Category"].astype(str).str.lower()
                == category.lower()
            ]

            if len(result) == 0:
                print("No data found.")
            else:
                print("\nFiltered Data:")
                print(result.to_string(index=False))

        elif choice == "2":

            start = input("Enter start date (YYYY-MM-DD): ")
            end = input("Enter end date (YYYY-MM-DD): ")

            try:
                start = pd.to_datetime(start)
                end = pd.to_datetime(end)

                result = self.df[
                    (self.df["Date"] >= start)
                    & (self.df["Date"] <= end)
                ]

                if len(result) == 0:
                    print("No data found.")
                else:
                    print("\nFiltered Data:")
                    print(result.to_string(index=False))

            except Exception:
                print("Invalid date format.")

        else:
            print("Invalid choice.")

    # ================= SUMMARY =================
    def display_summary(self):

        if self.df is None:
            print("Please load dataset first.")
            return

        print("\n========== DATA SUMMARY ==========")

        print("Number of Records:", len(self.df))

        print(
            "Total Sales:",
            round(self.df["Total Sales"].sum(), 2)
        )

        print(
            "Average Sales:",
            round(self.df["Total Sales"].mean(), 2)
        )

        print(
            "Maximum Sale:",
            round(self.df["Total Sales"].max(), 2)
        )

        print(
            "Minimum Sale:",
            round(self.df["Total Sales"].min(), 2)
        )

        print("\nCategory Wise Sales:")

        category_sales = (
            self.df.groupby("Category")["Total Sales"]
            .sum()
        )

        print(category_sales)

    # ================= BAR CHART =================
    def bar_chart(self):

        if self.df is None:
            print("Please load dataset first.")
            return

        data = (
            self.df.groupby("Category")["Total Sales"]
            .sum()
        )

        plt.figure(figsize=(8, 5))

        data.plot(kind="bar")

        plt.title("Total Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Sales")

        plt.tight_layout()
        plt.show()

    # ================= LINE GRAPH =================
    def line_graph(self):

        if self.df is None:
            print("Please load dataset first.")
            return

        data = (
            self.df.groupby("Date")["Total Sales"]
            .sum()
        )

        plt.figure(figsize=(10, 5))

        plt.plot(
            data.index,
            data.values,
            marker="o"
        )

        plt.title("Sales Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Sales")

        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    # ================= HEATMAP =================
    def heatmap(self):

        if self.df is None:
            print("Please load dataset first.")
            return

        # Select numerical columns
        data = self.df[
            ["Price", "Quantity Sold", "Total Sales"]
        ]

        correlation = data.corr()

        plt.figure(figsize=(7, 5))

        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm"
        )

        plt.title("Sales Data Correlation")

        plt.tight_layout()
        plt.show()

    # ================= NUMPY ANALYSIS =================
    def numpy_analysis(self):

        if self.df is None:
            print("Please load dataset first.")
            return

        sales = np.array(
            self.df["Total Sales"]
        )

        print("\n========== NUMPY ANALYSIS ==========")

        print(
            "Total Sales:",
            np.sum(sales)
        )

        print(
            "Average Sales:",
            np.mean(sales)
        )

        print(
            "Highest Sale:",
            np.max(sales)
        )

        print(
            "Lowest Sale:",
            np.min(sales)
        )

        # Growth percentage
        # BUG FIX #1 + #2: self.df is already sorted by Date (done in
        # load_data), so sales[0] is the earliest sale and sales[-1] is
        # the latest. Also guard against dividing by zero.
        if len(sales) > 1:

            if sales[0] == 0:
                print("Growth Percentage: N/A (first sale value is 0)")
            else:
                growth = (
                    (sales[-1] - sales[0])
                    / sales[0]
                ) * 100

                print(
                    "Growth Percentage:",
                    round(growth, 2), "%"
                )


# ==================================================
# MAIN PROGRAM
# ==================================================

analyzer = RetailAnalyzer()

print("======================================")
print("       RETAIL SALES DATA ANALYZER")
print("======================================")

file_path = "retail_sales_dataset.csv"

if os.path.exists(file_path):

    if analyzer.load_data(file_path):
        st.success("CSV file loaded successfully!")

else:

    st.error("CSV file not found.")

st.header("Retail Sales Data Analyzer")

if analyzer.df is not None:

    st.success("CSV file loaded successfully!")

    option = st.selectbox(
        "Select Analysis",
        [
            "Show Data",
            "Basic Information",
            "Statistical Summary"
        ]
    )

    if option == "Show Data":
        st.dataframe(analyzer.df)

    elif option == "Basic Information":
        st.write("Rows:", analyzer.df.shape[0])
        st.write("Columns:", analyzer.df.shape[1])
        st.write("Column Names:", list(analyzer.df.columns))

    elif option == "Statistical Summary":
        st.dataframe(analyzer.df.describe())
