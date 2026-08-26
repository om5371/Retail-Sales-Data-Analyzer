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

            # Check missing values
            if self.df.isnull().sum().sum() > 0:
                print("\nMissing values found.")
                self.df = self.df.dropna()
                print("Missing rows removed.")

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

        if self.df is None:
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
                self.df["Category"].str.lower()
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

            except:
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
        if len(sales) > 1:

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

file_path = input(
    "Enter CSV file path: "
)

# Check file
if not os.path.exists(file_path):

    print("File does not exist.")

else:

    if analyzer.load_data(file_path):

        while True:

            print("\n================================")
            print("           MAIN MENU")
            print("================================")

            print("1. Calculate Metrics")
            print("2. Filter Data")
            print("3. Display Summary")
            print("4. Bar Chart")
            print("5. Line Graph")
            print("6. Heatmap")
            print("7. NumPy Analysis")
            print("8. Exit")

            choice = input(
                "\nEnter your choice: "
            )

            if choice == "1":

                analyzer.calculate_metrics()

            elif choice == "2":

                analyzer.filter_data()

            elif choice == "3":

                analyzer.display_summary()

            elif choice == "4":

                analyzer.bar_chart()

            elif choice == "5":

                analyzer.line_graph()

            elif choice == "6":

                analyzer.heatmap()

            elif choice == "7":

                analyzer.numpy_analysis()

            elif choice == "8":

                print(
                    "\nThank you for using "
                    "Retail Sales Data Analyzer!"
                )

                break

            else:

                print(
                    "Invalid choice. "
                    "Please enter 1 to 8."
                )