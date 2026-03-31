# 🛒 Unified Sales Intelligence Dashboard

> End-to-end E-Commerce BI pipeline integrating multiple data sources using Python ETL → PostgreSQL → Power BI Dashboard.

---

## 📌 Overview

This project builds a full Business Intelligence pipeline that collects data from multiple sources (REST APIs + synthetic data), processes and loads it into a PostgreSQL database, and visualizes it through an interactive Power BI dashboard with sales, customer, and regional insights.

---

## 🏗️ Architecture

```
Fake Store API ──┐
                 ├──► Python ETL ──► PostgreSQL ──► Power BI Dashboard
Exchange Rate API┤       │
Faker Library ───┘    transform.py
                       load.py
```

---

## 🔌 Data Sources

| Source | Data | Type |
|---|---|---|
| [Fake Store API](https://fakestoreapi.com) | Products & Orders | REST API |
| [ExchangeRate API](https://exchangerate-api.com) | Currency Conversion | REST API |
| Faker Library | Customers & Regions | Synthetic |
| Open Holidays API | Seasonality | REST API |

---

## 📁 Project Structure

```
ecommerce-bi-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── etl/
│   ├── extract.py        # Fetch data from APIs
│   ├── transform.py      # Clean & merge data
│   └── load.py           # Load into PostgreSQL
│
├── sql/
│   ├── schema.sql        # Table definitions
│   └── queries.sql       # KPI queries
│
├── dashboard/
│   └── sales_dashboard.pbix
│
├── notebooks/
│   └── EDA.ipynb
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📊 Dashboard Pages

- **Page 1 — Executive Summary:** Total Revenue, Orders, Avg Order Value, MoM Growth
- **Page 2 — Sales Analysis:** Revenue by Category, Monthly Trend, Top Products, Regional Map
- **Page 3 — Customer Insights:** Segments, New vs Returning, Top Customers by Revenue

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/OmarSharafeldin/ecommerce-bi-pipeline.git
cd ecommerce-bi-pipeline
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 4. Run the pipeline
```bash
python etl/load.py
```

### 5. Open the dashboard
Open `dashboard/sales_dashboard.pbix` in Power BI Desktop and connect to your PostgreSQL database.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![Pandas](https://img.shields.io/badge/Pandas-ETL-green)

---

## 👤 Author

**Omar Sharafeldin Mohamed Abdelfatah**  
[GitHub](https://github.com/OmarSharafeldin) · [LinkedIn](https://linkedin.com/in/omarsharafeldin)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
