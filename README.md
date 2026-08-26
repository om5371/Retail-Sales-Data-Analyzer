## Retail Sales Data Analyzer

---

## 📌 Project Overview

**Retail Sales Data Analyzer** is a menu-driven Python application designed to process, analyze, and visualize retail sales data stored in a CSV file.

The project demonstrates practical implementation of:

* 🐍 Python Programming
* 🔄 Control Structures
* 📦 Arrays
* 🏗️ Object-Oriented Programming
* 🐼 Pandas
* 🔢 NumPy
* 📈 Matplotlib
* 🎨 Seaborn
* 📄 CSV Data Handling
* 📊 Data Analysis & Visualization

The application helps users understand sales performance using meaningful statistics and graphical representations.

---

## 🎯 Project Objectives

The main objectives of this project are:

* Load retail sales data from a CSV file.
* Validate the dataset and required columns.
* Detect and handle missing values.
* Calculate important sales metrics.
* Find the most popular product.
* Filter data by category or date.
* Perform numerical calculations using NumPy.
* Generate useful sales visualizations.
* Demonstrate OOP concepts through a `RetailAnalyzer` class.
* Provide a simple menu-driven user interface.

---

## ✨ Features

### 📂 1. CSV Data Loading

The program allows the user to enter a CSV file path and loads the dataset using Pandas.

```text
Enter CSV file path: retail_sales.csv

Dataset loaded successfully!
Total Records: 15
```

---

### 🔍 2. Data Validation

The program checks:

* File existence
* Required columns
* Missing values
* Numeric values
* Date format

Required columns:

```text
Date
Product
Category
Price
Quantity Sold
Total Sales
```

---

### 📊 3. Sales Metrics

The application calculates:

* 💰 Total Sales
* 📈 Average Sales
* 📦 Total Quantity Sold
* 🏆 Most Popular Product
* 🔢 NumPy Average

Example:

```text
========== SALES METRICS ==========

Total Sales       : 353400
Average Sales     : 23560
Total Quantity    : 59
Popular Product   : Mobile
NumPy Average     : 23560
```

---

### 🔎 4. Data Filtering

Users can filter the dataset using:

#### Category Filter

```text
1. Filter by Category
2. Filter by Date
```

Example:

```text
Available Categories:
['Electronics' 'Clothing' 'Footwear' 'Accessories']

Enter category: Electronics
```

#### Date Filter

Users can provide:

```text
Start Date
End Date
```

to analyze sales within a specific date range.

---

### 📋 5. Data Summary

The program displays:

* Number of records
* Total sales
* Average sales
* Maximum sale
* Minimum sale
* Category-wise sales

Example:

```text
========== DATA SUMMARY ==========

Number of Records: 15
Total Sales: 353400
Average Sales: 23560
Maximum Sale: 100000
Minimum Sale: 4000

Category Wise Sales:
Category
Accessories     12000
Clothing        31400
Electronics    222000
Footwear        22000
```

---

## 📈 Data Visualization

The project provides three major visualizations.

### 📊 Bar Chart

Displays total sales by product category.

```text
Category → Total Sales
```

Useful for comparing the performance of different categories.

---

### 📈 Line Graph

Displays sales trends over time.

```text
Date → Total Sales
```

Useful for understanding sales growth and fluctuations.

---

### 🔥 Heatmap

Displays correlations between:

* Price
* Quantity Sold
* Total Sales

This helps identify relationships between numerical variables.

---

## 🔢 NumPy Analysis

NumPy is used for numerical calculations such as:

```python
np.sum()
np.mean()
np.max()
np.min()
```

The program also calculates a basic sales growth percentage.

```text
Growth Percentage: XX.XX %
```

---

## 🏗️ Object-Oriented Programming

The project uses a class called:

```python
RetailAnalyzer
```

### Available Methods

| Method                | Purpose                      |
| --------------------- | ---------------------------- |
| `load_data()`         | Load and validate CSV data   |
| `calculate_metrics()` | Calculate sales metrics      |
| `filter_data()`       | Filter sales records         |
| `display_summary()`   | Display data summary         |
| `bar_chart()`         | Generate category bar chart  |
| `line_graph()`        | Generate sales trend graph   |
| `heatmap()`           | Generate correlation heatmap |
| `numpy_analysis()`    | Perform NumPy calculations   |

---

## 🛠️ Technologies Used

| Technology    | Purpose                       |
| ------------- | ----------------------------- |
| 🐍 Python     | Main programming language     |
| 🐼 Pandas     | Data loading and manipulation |
| 🔢 NumPy      | Numerical calculations        |
| 📊 Matplotlib | Data visualization            |
| 🎨 Seaborn    | Statistical visualization     |
| 📄 CSV        | Dataset storage               |
| 🏗️ OOP       | Project structure             |

---

## 📁 Project Structure

```text
Retail-Sales-Data-Analyzer/
│
├── 📄 retail_analyzer.py
├── 📊 retail_sales.csv
├── 📖 README.md
└── 📷 screenshots/
    ├── dashboard.png
    ├── bar_chart.png
    ├── line_graph.png
    └── heatmap.png
```

---

## 📋 Dataset Format

The CSV dataset should contain the following columns:

```text
Date
Product
Category
Price
Quantity Sold
Total Sales
```

### Example Dataset

```csv
Date,Product,Category,Price,Quantity Sold,Total Sales
2026-01-01,Laptop,Electronics,50000,2,100000
2026-01-02,Mouse,Electronics,800,5,4000
2026-01-03,Shirt,Clothing,1200,4,4800
2026-01-04,Shoes,Footwear,2500,3,7500
2026-01-05,Mobile,Electronics,20000,3,60000
```

---

# 🚀 Installation & Setup

## 1️⃣ Clone the Repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/Retail-Sales-Data-Analyzer.git
```

Move into the project directory:

```bash
cd Retail-Sales-Data-Analyzer
```

---

## 2️⃣ Install Required Libraries

Run:

```bash
pip install pandas numpy matplotlib seaborn
```

Or install everything from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Add Dataset

Place your CSV file in the project folder:

```text
retail_sales.csv
```

---

## 4️⃣ Run the Program

Run:

```bash
python retail_analyzer.py
```

---

# 🖥️ Program Menu

After running the program, the following menu appears:

```text
======================================
       RETAIL SALES DATA ANALYZER
======================================

================================
           MAIN MENU
================================

1. Calculate Metrics
2. Filter Data
3. Display Summary
4. Bar Chart
5. Line Graph
6. Heatmap
7. NumPy Analysis
8. Exit

Enter your choice:
```

---

# 🔄 Example Workflow

```text
        📂 CSV Dataset
              │
              ▼
       🔍 Data Validation
              │
              ▼
        📊 Load Data
              │
              ▼
      ┌───────┴────────┐
      │                │
      ▼                ▼
  📈 Analysis       🔎 Filtering
      │                │
      └───────┬────────┘
              ▼
       📊 Visualization
              │
              ▼
       💡 Sales Insights
```

---

# 📸 Screenshots

Add your project screenshots inside the `screenshots` folder.

### 🏠 Main Menu

![Main Menu](screenshots/dashboard.png)

### 📊 Bar Chart

![Bar Chart](screenshots/bar_chart.png)

### 📈 Sales Trend

![Line Graph](screenshots/line_graph.png)

### 🔥 Correlation Heatmap

![Heatmap](screenshots/heatmap.png)

> 💡 Replace the image files with your actual screenshots after uploading them to GitHub.

---

# 🧠 Concepts Demonstrated

This project demonstrates the following Python concepts:

```text
✓ Variables
✓ Input / Output
✓ if-else
✓ for / while loops
✓ Lists / Arrays
✓ Functions
✓ Classes & Objects
✓ Exception Handling
✓ File Handling
✓ Pandas DataFrame
✓ NumPy Arrays
✓ Data Cleaning
✓ Data Aggregation
✓ Data Filtering
✓ Data Visualization
```

---

# 📊 Analysis Capabilities

The analyzer can answer questions such as:

* 💰 What is the total sales amount?
* 📈 What is the average sale?
* 🏆 Which product is most popular?
* 📦 How many products were sold?
* 🛍️ Which category generated the highest sales?
* 📅 How did sales change over time?
* 🔗 What is the correlation between price and quantity?
* 📊 What are the minimum and maximum sales?

---

# 🔮 Future Improvements

Possible future enhancements include:

* [ ] Add a graphical user interface using Tkinter
* [ ] Add user login system
* [ ] Add Excel file support
* [ ] Add PDF report generation
* [ ] Add interactive dashboard
* [ ] Add monthly and yearly reports
* [ ] Add automatic sales forecasting
* [ ] Add product-wise visualization
* [ ] Add export-to-Excel functionality
* [ ] Add database support

---

# 🎓 Educational Purpose

This project was created as a practical Python/Data Analytics project to demonstrate the use of:

**Python + OOP + NumPy + Pandas + Matplotlib + Seaborn**

It is suitable for students learning:

* Python Programming
* Data Analytics
* Data Visualization
* Object-Oriented Programming
* Pandas & NumPy

---
