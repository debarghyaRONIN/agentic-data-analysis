import streamlit as st
import pandas as pd
import plotly.express as px

from agents.analysis_agent import AnalysisAgent
from agents.fuzzy_agent import FuzzyPredictionAgent
from agents.decision_agent import DecisionAgent


# Page Config (Responsive)
st.set_page_config(
    page_title="Agentic Data Analysis Dashboard",
    layout="wide"
)

st.title("🧠 Agentic Data Analysis & Decision System")
st.markdown("Multi-Agent AI with **Analysis → Fuzzy Prediction → RAG-based Decision**")

# Load Data
analysis_agent = AnalysisAgent("data/sales_data.csv")
summary, df = analysis_agent.analyze()


# Layout (Responsive Columns)
col1, col2 = st.columns(2)

# Visualization 1: Order Flow Over Time
with col1:
    st.subheader("📈 Order Flow Trend")
    fig1 = px.line(
        df,
        x="time",
        y="order_flow",
        markers=True,
        title="Order Flow vs Time"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Rating Distribution
with col2:
    st.subheader("⭐ Customer Ratings")
    fig2 = px.bar(
        df,
        x="time",
        y="rating",
        title="Ratings Over Time",
        color="rating"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Fuzzy Prediction Section
st.subheader("🔮 Fuzzy Demand Prediction")

order_flow_input = st.slider(
    "Order Flow",
    min_value=0,
    max_value=300,
    value=int(df["order_flow"].iloc[-1])
)

rating_input = st.slider(
    "Customer Rating",
    min_value=1,
    max_value=5,
    value=int(df["rating"].iloc[-1])
)

fuzzy_agent = FuzzyPredictionAgent()
prediction = fuzzy_agent.predict(order_flow_input, rating_input)

st.metric(
    label="Predicted Demand Level",
    value=prediction["demand_level"],
    delta=f"Score: {prediction['demand_score']}"
)

# Decision Agent Section
st.subheader("🧠 AI Decision (RAG + LLM Logic)")

decision_agent = DecisionAgent()
decision_text = decision_agent.decide(summary, prediction)

st.text_area(
    "Decision Explanation",
    decision_text,
    height=250
)


# Footer
st.markdown("---")
st.markdown("📌 Built using **Agentic AI + Fuzzy Logic + RAG + LLM Reasoning**")
