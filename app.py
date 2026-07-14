import streamlit as st

st.set_page_config(
    page_title="Fin Club Paper Trading",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Fin Club Paper Trading Challenge")

st.markdown("---")

st.header("Rules")

st.markdown("""
- Every team starts with **₹10,000**
- Each round a news headline will be shown.
- Based on the news, buy/sell stocks.
- Trading closes after each round.
- Highest portfolio value after all rounds wins.
""")

st.info("Use the sidebar to open the Trading page.")