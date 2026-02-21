# 🚀 ETL Pipeline – Web Scraping to Multi-Destination Storage

## 📌 Overview

This project implements an **ETL (Extract, Transform, Load) Pipeline** that performs web scraping from:

```
https://fashion-studio.dicoding.dev
```

The pipeline extracts product data, cleans and transforms it into structured format, and loads the processed data into multiple destinations:

- 📁 CSV File
- 🗄 PostgreSQL Database
- 📊 Google Sheets

This project demonstrates practical data engineering skills including modular pipeline design, data cleaning, validation, and multi-destination data loading.

---

## 🎯 Project Objectives

- Perform automated web scraping
- Clean and standardize raw product data
- Structure data for analysis
- Load processed data into multiple storage systems
- Build modular and maintainable ETL architecture

---

## 📦 Load Phase

The cleaned dataset is loaded into:

### 1️⃣ CSV File
- Stores processed dataset locally

### 2️⃣ PostgreSQL Database
- Structured storage for querying and analytics
- Enables scalable data persistence

### 3️⃣ Google Sheets
- Cloud-based storage
- Easy sharing and visualization

---

## 🛠️ Technologies Used

- Python
- Pandas
- Requests / BeautifulSoup (for web scraping)
- PostgreSQL
- Google Sheets API
- SQLAlchemy 
- dotenv (if environment variables used)

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/farisgp/ETL-Pipeline.git
cd ETL-Pipeline
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Run the ETL pipeline using:

```bash
python main.py
```

The script will:

1. Scrape product data
2. Clean and transform dataset
3. Load data into:
   - CSV file
   - PostgreSQL
   - Google Sheets

---

## 🔐 Environment Configuration

PostgreSQL and Google Sheets credentials are required, create a `.env` file:

```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASS=

GOOGLE_SHEET_ID=
GOOGLE_APPLICATION_CREDENTIALS=
```

---

## 📊 Output

- Structured CSV file
- Data stored in PostgreSQL table
- Data uploaded to Google Sheets
  
---

## 🧪 Testing

Unit tests are available in the `tests/` directory.

Run tests using:

```bash
python -m unittest discover -s tests
```

See the testing report :
```
# run coverage
coverage run -m unittest discover tests

# show report
coverage report -m
```

Save to html :
```
coverage html
```

---

## 🚀 Future Improvements

- Add logging system
- Add error handling & retry mechanism
- Containerize using Docker
- Automate scheduling (Airflow / Cron)
- Implement data validation framework

---
