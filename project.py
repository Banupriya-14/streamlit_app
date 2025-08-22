import os
import streamlit as st
import PyPDF2
import google.generativeai as genai
import groq 

# Google Gemini API Key
GEMINI_API_KEY = "AIzaSyAx9n3BPc6xHSyVXs24Rp4r9OePF9af_K4"
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit UI name
st.set_page_config(page_title="AI Personal Finance Assistant")

# Styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        #font-size: 34px;
        font-weight: bold;
        #color: #4CAF50;
        #text-shadow: 2px 2px 5px rgba(76, 175, 80, 0.4);
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        #color: #ddd;
        margin-bottom: 20px;
    }
    .stButton button {
        background: linear-gradient(to right, #4CAF50, #388E3C);
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(to right, #388E3C, #2E7D32);
    }
    .result-card {
        background: rgba(0, 150, 136, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 8px rgba(0, 150, 136, 0.2);
    }
    .success-banner {
        background: linear-gradient(to right, #2E7D32, #1B5E20);
        color: white;
        padding: 15px;
        font-size: 18px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0px 2px 8px rgba(0, 150, 136, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title('💰 AI-Powered Personal Finance Assistant')



st.sidebar.title(" Instructions to Use This Tool")
st.sidebar.write("- Upload your Transaction History PDF.")
st.sidebar.write("- The AI will analyze your transactions and You will receive financial insights including income, expenses, savings, and spending trends.")
st.sidebar.write("- Use this data to plan your finances effectively.")

st.markdown('<h1 class="main-title">💰 AI-Powered Personal Finance Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload your Transaction History PDF for Financial Insights</p>', unsafe_allow_html=True)

# PDF File upload
uploaded_file = st.file_uploader("📂 Upload PDF File", type=["pdf"], help="Only PDF files are supported")

def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as pdffile:
        reader = PyPDF2.PdfReader(pdffile)
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    text += f"[⚠️ Page {page_num} has no readable text]\n"
            except Exception as e:
                text += f"[❌ Error reading page {page_num}: {str(e)}]\n"
    return text.strip()

def analyze_financial_data(text):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = f"""
Analyze the following bank transaction history and generate financial insights:
{text}
Provide a detailed breakdown in the following format:

**Financial Insights for [User Name]**

**Key Details:**
- **Overall Monthly Income & Expenses:**
  - Month: [Month]
  - Total Credits (Income): ₹[Amount]
  - Total Debits (Expenses): ₹[Amount]
  - Sources of Income: [Salary, Interest, Refunds, Transfers...]
  - Regularity of Income: [On time / Delays noted]
  - Income Change from Previous Month: [Increase/Decrease %]

- **Expense Breakdown:**
  - Top Expense Categories: 
    1. [Category] - ₹[Amount]
    2. [Category] - ₹[Amount]
  - Recurring Payments: [Rent, EMI, Subscriptions...]
  - One-Time Big Spends: [Details]
  - Unnecessary/Impulse Spending: [Details & Amount]

- **Cash Flow & Savings:**
  - Net Savings: ₹[Amount]
  - Savings Rate: [Percentage] %
  - Months with Negative Cash Flow: [Yes/No, Details]

- **Spending Behavior:**
  - Daily/Weekly/Monthly Trends: [Pattern]
  - Weekend vs Weekday Spending: [Comparison]
  - Impulse Spending Detection: [Details]

- **Bank Charges & Fees:**
  - Total Charges: ₹[Amount]
  - Type of Charges: [ATM, Service, Late Fees...]
  - Suggestions to Reduce Charges: [Details]

- **Payment Patterns:**
  - Preferred Payment Method: [UPI, Card, Cheque...]
  - Average Transaction Size: ₹[Amount]
  - Largest Single Transaction: ₹[Amount]

- **Loan & Credit Card Analysis (if applicable):**
  - EMI Amount & Payment Dates: [Details]
  - Interest Paid: ₹[Amount]
  - Missed/Delayed Payments: [Yes/No]

- **Alerts & Anomalies:**
  - Unusually Large Transactions: [Details]
  - Duplicate Charges: [Details]
  - Unexpected Deductions: [Details]

- **Balance Trends:**
  - Opening Balance: ₹[Amount]
  - Closing Balance: ₹[Amount]
  - Minimum Balance Maintained: ₹[Amount]
  - Days with Lowest Balance: [Details]

- **Financial Health Indicators:**
  - Expense-to-Income Ratio: [Ratio]
  - Emergency Fund Adequacy: [Yes/No, Details]
  - Debt-to-Income Ratio: [Ratio]

"""

    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠️ Error processing financial data."

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as file1:
        file1.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text from document..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠️ Failed to extract text. Ensure the document is not a scanned image PDF.")
    else:
        #progress_bar = st.progress(0)
        with st.spinner("🧠 AI is analyzing your financial data..."):
            insights = analyze_financial_data(extracted_text)

        #progress_bar.progress(100)

        st.subheader("📊 Financial Insights Report")
        #st.markdown(f'<div class="result-card"><b>📄 Financial Report for {uploaded_file.name}</b></div>', unsafe_allow_html=True)

        st.write(insights)
        st.balloons()
        st.markdown('<div class="success-banner">🎉 Analysis Completed! Plan your finances wisely. 🚀</div>', unsafe_allow_html=True)





    
    
