import os

import streamlit as st
from google import genai

from retail_insights import get_summary


st.set_page_config(page_title="RetailStream AI Insights", page_icon="🛍️")

st.title("🛍️ RetailStream AI Sales Insights")
st.caption("AI-assisted analysis of synthetic retail sales data.")

summary = get_summary()

col1, col2, col3 = st.columns(3)
col1.metric("Sales Records", summary["record_count"])
col2.metric("Orders", summary["order_count"])
col3.metric("Total Sales", f"${summary['total_sales']:,.2f}")

st.subheader("Sales by Category")
st.bar_chart(summary["category_sales"].set_index("category"))

st.subheader("Sales by Region")
st.bar_chart(summary["region_sales"].set_index("region"))

st.subheader("Ask RetailStream AI")
question = st.text_input(
    "Ask a question about the sales data",
    placeholder="Example: Which category had the highest sales?",
)

if st.button("Get AI insight"):
    if not question:
        st.warning("Please type a question first.")
    elif not os.getenv("GEMINI_API_KEY"):
        st.error("Gemini API key is not available in this terminal session.")
    else:
        data_context = f"""
        This project uses synthetic retail sales data only.

        Dataset summary:
        - Sales records: {summary["record_count"]}
        - Unique orders: {summary["order_count"]}
        - Total sales: ${summary["total_sales"]:,.2f}

        Sales by category:
        {summary["category_sales"].to_string(index=False)}

        Sales by region:
        {summary["region_sales"].to_string(index=False)}
        """

        client = genai.Client()
        response = client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=f"""
            You are the RetailStream AI assistant.
            Answer only from the sales dataset details below.
            Be concise and do not invent facts.

            {data_context}

            User question: {question}
            """,
        )

        st.success(response.output_text)

st.subheader("Category Sales Table")
st.dataframe(summary["category_sales"], width="stretch")