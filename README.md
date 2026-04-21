# 🧠 Fact-Check Agent

A smart web application that automatically extracts and verifies claims from PDF documents using live web data.

---

## 🚀 Features

- 📄 Upload PDF documents
- 🧠 Automatically extract factual claims (numbers, stats, dates)
- 🌐 Verify claims using real-time web search
- 📊 Classify results into:
  - ✅ Verified
  - ⚠️ Inaccurate / Partial
  - ❌ False
- 📥 Download results as CSV

---

## 🎯 Problem Statement

Marketing and informational documents often contain outdated, incorrect, or hallucinated statistics. This tool acts as a **"Truth Layer"** to validate such claims automatically.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **PDF Processing:** pdfplumber  
- **Web Verification:** DuckDuckGo API  
- **Data Handling:** Pandas  

---

## ⚙️ How It Works

1. Upload a PDF
2. Extract text from document
3. Identify claims using pattern detection
4. Search live web data for verification
5. Classify each claim and display results

---

## 📦 Installation

```bash
cd fact-check-agent
python -m venv venv
source venv/bin/activate  # (Mac/Linux)
venv\Scripts\activate     # (Windows)

pip install -r requirements.txt

To Run Locally:
streamlit run app.py
