import streamlit as st
import pdfplumber
import re
import requests
import pandas as pd

st.set_page_config(page_title="Fact-Check Agent", layout="wide")

st.title("🧠 Fact-Check Agent")
st.write("Upload a PDF to automatically extract and verify claims")

# -------------------------------
# 📄 Extract text from PDF
# -------------------------------
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

# -------------------------------
# 🧠 Extract claims (numbers, stats, dates)
# -------------------------------
def extract_claims(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    claims = []

    for sentence in sentences:
        if re.search(r'\d+', sentence):  # sentences with numbers
            claims.append(sentence.strip())

    return claims

# -------------------------------
# 🌐 Verify claim using DuckDuckGo
# -------------------------------
def verify_claim(claim):
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": claim,
            "format": "json",
            "no_redirect": 1,
            "no_html": 1
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        # Decision logic
        if data.get("AbstractText"):
            return "✅ Verified", data["AbstractText"]

        elif data.get("RelatedTopics"):
            return "⚠️ Inaccurate / Partial", "Some related information found"

        else:
            return "❌ False", "No reliable evidence found"

    except Exception as e:
        return "⚠️ Error", str(e)

# -------------------------------
# 📂 File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        text = extract_text(uploaded_file)

    st.success("Text extracted successfully!")

    # Extract claims
    claims = extract_claims(text)

    if not claims:
        st.warning("No claims detected.")
    else:
        st.subheader("📄 Extracted Claims")
        for i, claim in enumerate(claims):
            st.write(f"{i+1}. {claim}")

        # -------------------------------
        # 🔍 Verify Claims
        # -------------------------------
        st.subheader("🔍 Fact-Check Results")

        results = []

        for claim in claims:
            status, evidence = verify_claim(claim)

            results.append({
                "Claim": claim,
                "Status": status,
                "Evidence": evidence
            })

        df = pd.DataFrame(results)

        # Show table
        st.dataframe(df, use_container_width=True)

        # Download option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Results as CSV",
            data=csv,
            file_name="fact_check_results.csv",
            mime="text/csv"
        )