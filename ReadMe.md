# SmartRetail 360 — Analytics & AI Support Platform

An end-to-end data and AI intelligence platform for e-commerce businesses. Built as a capstone project covering data engineering, machine learning, generative AI, and API development.

---

## Architecture Overview

```
sales_data.csv  ──→  PostgreSQL BRONZE.SALES   ──→  GOLD.SALES (monthly aggregated)
reviews.tsv     ──→  PostgreSQL BRONZE.REVIEWS  ──→  GOLD.REVIEWS (cleaned)
                              ↓                              ↓
                       ML Pipeline                  Knowledge Base
                   (Linear Regression)          (FAISS + Embeddings)
                              ↓                              ↓
                         FastAPI Backend (port 8000)
                         ├── POST /predict-sales
                         └── POST /ask-assistant (RAG)
                                      ↓
                         Streamlit Frontend (port 8501)
                         ├── Business Dashboard
                         └── AI Assistant Chat
```

---

## Project Structure

```
├── app.py                        # Streamlit entry point / Home page
├── Pages/                        # Streamlit navigation pages
│   ├── 1_Ingest.py               # Load raw data into PostgreSQL Bronze
│   ├── 2_Transform.py            # Bronze → Gold transformation
│   ├── 3_Visualize.py            # EDA charts
│   ├── 4_ML.py                   # Model training + evaluation
│   ├── 5_KnowledgeBase.py        # Embeddings + FAISS index builder + search
│   ├── 6_Dashboard.py            # Business analytics + revenue prediction form
│   └── 7_Assistant.py            # Conversational AI review assistant
├── Services/                     # Business logic layer
│   ├── dbconnector.py            # PostgreSQL connection factory
│   ├── ingestservice.py          # Load CSV/TSV → Bronze tables
│   ├── transformservice.py       # Bronze → Gold (clean + aggregate)
│   ├── visualizeservice.py       # Chart generation functions
│   ├── mlservice.py              # Feature engineering + model training + prediction
│   ├── embeddingservice.py       # Embeddings + FAISS index + semantic search
│   └── ragservice.py             # RAG pipeline (retrieve + generate)
├── api/                          # FastAPI backend
│   ├── main.py                   # App entry point + router registration
│   ├── routes/
│   │   ├── predict.py            # /predict-sales endpoint
│   │   └── assistant.py          # /ask-assistant endpoint
│   └── models/
│       └── schemas.py            # Pydantic input/output schemas
├── data/                         # Raw data files (not committed to git)
│   ├── sales.csv                 # UCI Online Retail II dataset
│   └── review.tsv                # Amazon Gift Card reviews dataset
├── appsettings.json              # Non-sensitive config (file paths)
├── requirements.txt              # Python dependencies
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data Source | UCI Online Retail II + Amazon Gift Card Reviews |
| Database | PostgreSQL (local) |
| Data Processing | Python, Pandas, SQLAlchemy |
| Machine Learning | Scikit-learn (Linear Regression, StandardScaler) |
| Embeddings | Hugging Face `paraphrase-multilingual-MiniLM-L12-v2` |
| Vector Store | FAISS (local, Facebook AI Similarity Search) |
| LLM | Google `flan-t5-base` (local, free, no API cost) |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Version Control | Git + GitHub |

---

## Datasets

### Sales Data — UCI Online Retail II
- **Source:** UCI Machine Learning Repository via Kaggle
- **Period:** December 2009 — December 2011 (25 months)
- **Rows:** ~1,067,371 raw transactions → 779,425 after cleaning
- **Key columns:** Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
- **Revenue derived as:** `Quantity × Price`

### Reviews Data — Amazon Gift Card Reviews
- **Source:** Amazon US Customer Reviews Dataset via Kaggle
- **Rows:** 148,310 reviews → 148,303 after cleaning
- **Key columns:** review_id, product_title, star_rating, review_headline, review_body, review_date

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 17 installed and running locally
- DBeaver (optional, for DB inspection)

### 1. Clone the repository
```bash
git clone https://github.com/Tjeeiv/SmartRetail.git
cd SmartRetail
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smartretail
DB_USER=postgres
DB_PASSWORD=yourpassword
```

### 4. Create the database
In PostgreSQL (via DBeaver or psql):
```sql
CREATE DATABASE smartretail;
```

### 5. Add data files
Place these files in the `data/` folder:
- `data/sales.csv` — UCI Online Retail II dataset
- `data/review.tsv` — Amazon Gift Card reviews (TSV format)

### 6. Run the Streamlit app
```bash
streamlit run app.py
```

Then follow the sidebar steps in order:
1. **Ingest** — loads raw data into PostgreSQL Bronze tables
2. **Transform** — cleans and aggregates Bronze → Gold
3. **Visualize** — view EDA charts
4. **ML** — trains Linear Regression model, saves `.pkl` files
5. **Knowledge Base** — generates embeddings, builds FAISS index
6. **Dashboard** — view charts + get revenue predictions
7. **AI Assistant** — chat with your review data

### 7. Start the FastAPI backend (separate terminal)
```bash
python -m uvicorn api.main:app --reload --port 8000
```

View auto-generated API docs: `http://localhost:8000/docs`

---

## API Reference

### `POST /predict-sales`
Predicts next month's revenue based on current month's business metrics.

**Request:**
```json
{
  "MonthlyRevenue": 650000.0,
  "Invoicecount": 1300,
  "monAvgRev": 23.5,
  "monthnumber": 11
}
```

**Response:**
```json
{
  "predictedrevenue": 672450.32
}
```

### `POST /ask-assistant`
Accepts a natural language question, retrieves semantically relevant reviews via FAISS, and returns an AI-generated answer.

**Request:**
```json
{
  "question": "Are customers happy with gift cards?"
}
```

**Response:**
```json
{
  "answer": "Always happy with gift cards",
  "sources": [
    "always satisfied with the gift cards",
    "Always happy with gift cards",
    "Everyone loves gift cards!"
  ]
}
```

---

## Model Performance

| Metric | Value |
|---|---|
| R² Score | 0.884 |
| MAE | £70,182 |
| RMSE | £82,069 |

The Linear Regression model achieves R² = 0.884, explaining 88.4% of variance in monthly revenue. The UCI Online Retail II dataset has a consistent seasonal pattern across 2 years, making it well-suited for Linear Regression forecasting.

---

## Milestones

| Milestone | Description | Status |
|---|---|---|
| 1 — Data Pipeline | Load sales + reviews → PostgreSQL Bronze | ✅ Complete |
| 2 — EDA & ML | 3 visualizations + feature engineering + Linear Regression (R²=0.884) | ✅ Complete |
| 3 — Vector Embeddings | Multilingual embeddings + FAISS semantic search (148,303 reviews) | ✅ Complete |
| 4 — Backend API | FastAPI with `/predict-sales` and `/ask-assistant` endpoints | ✅ Complete |
| 5 — Streamlit UI | 7-page app: pipeline steps + Business Dashboard + AI Assistant | ✅ Complete |

---

## Design Decisions

### Why PostgreSQL instead of SQLite/MongoDB?
The project specification suggested SQLite for sales data and MongoDB for reviews. This implementation uses PostgreSQL for both — a production-grade relational database that handles both structured (sales) and semi-structured (reviews) data well. Using one database instead of two simplifies the architecture and reflects real-world engineering practice.

### Why multilingual embeddings for English reviews?
The `paraphrase-multilingual-MiniLM-L12-v2` model works excellently for English and also future-proofs the system — if the dataset is later expanded to include reviews in other languages, no changes to the embedding pipeline are needed.

### Why local LLM (flan-t5)?
Google's `flan-t5-base` runs entirely locally with no API cost, no rate limits, and no data leaving your machine. For production use, replacing it with Claude or GPT-4 via API would significantly improve answer quality.

---

## Author
Built by Siddhu as part of the SmartRetail 360 capstone project.