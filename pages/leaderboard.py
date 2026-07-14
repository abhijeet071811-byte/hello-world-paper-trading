import streamlit as st
import pandas as pd

from backend import generate_leaderboard
from admin import (
    get_current_round,
    next_round,
    open_trading,
    close_trading,
    trading_status,
    reset_game
)

st.set_page_config(
    page_title="Leaderboard",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Paper Trading Leaderboard")

round_no = get_current_round()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Current Round",
        round_no
    )

with col2:

    if trading_status():
        st.success("🟢 Trading OPEN")
    else:
        st.error("🔴 Trading CLOSED")

st.divider()

prices = pd.read_csv("data/prices.csv")
max_round = int(prices["Round"].max())

round_limit_reached = False

if round_no > max_round:
    round_limit_reached = True
    st.warning(
        f"Only {max_round + 1} rounds are available in prices.csv. Please reset the game or add more rounds."
    )
else:
    leaderboard = generate_leaderboard(round_no)

    st.dataframe(
        leaderboard,
        hide_index=True,
        use_container_width=True
    )

st.divider()

st.subheader("Admin Controls")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(
        "🟢 Open Trading",
        use_container_width=True
    ):
        open_trading()
        st.rerun()

with col2:
    if st.button(
        "🔴 Close Trading",
        use_container_width=True
    ):
        close_trading()
        st.rerun()

with col3:
    if st.button(
        "➡️ Next Round",
        use_container_width=True
    ):
        if round_limit_reached:
            st.warning("Maximum round reached. Please reset the game first.")
        else:
            next_round()
            st.rerun()

with col4:
    if st.button(
        "🔄 Reset Game",
        use_container_width=True
    ):
        reset_game()
        st.rerun()