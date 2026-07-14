import streamlit as st
import pandas as pd

from backend import buy_stock, sell_stock
from admin import get_current_round, trading_status
from util import COMPANIES

# Initialize orders list in session state
if "orders" not in st.session_state:
    st.session_state.orders = []

st.title("📈 Trading Terminal")

round_no = get_current_round()

st.metric("Current Round", round_no)

if trading_status():
    st.success("🟢 Trading is OPEN")
else:
    st.error("🔴 Trading is CLOSED")

teams = pd.read_csv("data/teams.csv")

team = st.selectbox(
    "Select Team",
    teams["team_name"]
)

# Portfolio and holdings display
holdings = pd.read_csv("data/holdings.csv")
team_data = holdings.loc[holdings["team_name"] == team].iloc[0]

st.subheader("Current Portfolio")

col1, col2 = st.columns([1,2])
with col1:
    st.metric("Cash Remaining", f"₹{team_data['Cash']:.2f}")

with col2:
    portfolio = pd.DataFrame({
        "Company": COMPANIES,
        "Shares": [team_data[c] for c in COMPANIES]
    })
    st.dataframe(portfolio, hide_index=True, use_container_width=True)


st.subheader("Create Orders")
st.caption("Enter a quantity for any company you want to trade during this round.")

orders_to_add = []

header = st.columns([2, 2, 2, 2])
header[0].markdown("**Company**")
header[1].markdown("**Current Holdings**")
header[2].markdown("**Action**")
header[3].markdown("**Quantity**")

for company in COMPANIES:
    cols = st.columns([2, 2, 2, 2])

    cols[0].write(company)
    cols[1].write(int(team_data[company]))

    action = cols[2].selectbox(
        "",
        ["NONE", "BUY", "SELL"],
        key=f"action_{company}"
    )

    qty = cols[3].number_input(
        "",
        min_value=0,
        step=1,
        key=f"qty_{company}"
    )

    if action != "NONE" and qty > 0:
        orders_to_add.append({
            "team": team,
            "company": company,
            "action": action,
            "quantity": int(qty),
            "round_no": round_no
        })

if st.button("Add Orders"):
    st.session_state.orders.extend(orders_to_add)
    st.success(f"{len(orders_to_add)} order(s) added.")
    st.rerun()

st.subheader("Pending Orders")
if not st.session_state.orders:
    st.info("There are no pending orders.")
else:
    pending_df = pd.DataFrame(st.session_state.orders)
    pending_df = pending_df[["action", "company", "quantity"]]
    pending_df.columns = ["Action", "Company", "Quantity"]
    st.dataframe(pending_df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Clear Orders"):
            st.session_state.orders.clear()
            st.rerun()

    if st.button("Submit All Orders"):
        if not trading_status():
            st.error("Trading Closed")
        else:
            success_count = 0
            for order in st.session_state.orders:
                if order["action"] == "BUY":
                    success = buy_stock(
                        order["team"],
                        order["company"],
                        order["quantity"],
                        order["round_no"]
                    )
                else:
                    success = sell_stock(
                        order["team"],
                        order["company"],
                        order["quantity"],
                        order["round_no"]
                    )
                if success:
                    success_count += 1
            st.session_state.orders.clear()
            st.success(f"{success_count} trade(s) executed successfully.")