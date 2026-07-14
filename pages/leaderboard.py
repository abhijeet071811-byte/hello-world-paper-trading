import streamlit as st

from backend import generate_leaderboard
from admin import (
    get_current_round,
    next_round,
    open_trading,
    close_trading
)

st.title("🏆 Leaderboard")

round_no = get_current_round()

st.metric(
    "Current Round",
    round_no
)

leaderboard = generate_leaderboard(round_no)

st.dataframe(
    leaderboard,
    use_container_width=True
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Open Trading"):
        open_trading()
        st.rerun()

with col2:
    if st.button("Close Trading"):
        close_trading()
        st.rerun()

with col3:
    if st.button("Next Round"):
        next_round()
        st.rerun()