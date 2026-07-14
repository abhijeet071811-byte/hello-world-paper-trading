import streamlit as st
import pandas as pd

from backend import buy_stock, sell_stock, get_price
from admin import get_current_round, trading_status
from util import COMPANIES

st.set_page_config(page_title="Trading", page_icon="📈", layout="wide")

st.title("📈 Trading Terminal")

# ----------------------------
# Current Round
# ----------------------------

round_no = get_current_round()

st.metric("Current Round", round_no)

if trading_status():
    st.success("🟢 Trading Open")
else:
    st.error("🔴 Trading Closed")

# ----------------------------
# Team Selection
# ----------------------------

teams = pd.read_csv("data/teams.csv")

team = st.selectbox(
    "Select Team",
    teams["team_name"]
)

# ----------------------------
# Portfolio
# ----------------------------

holdings = pd.read_csv("data/holdings.csv")

team_data = holdings.loc[
    holdings["team_name"] == team
].iloc[0]

st.subheader("Current Portfolio")

col1, col2 = st.columns([1,2])

with col1:
    st.metric(
        "Cash Remaining",
        f"₹{team_data['Cash']:.2f}"
    )

with col2:

    portfolio = pd.DataFrame({
        "Company": COMPANIES,
        "Holdings":[team_data[c] for c in COMPANIES]
    })

    st.dataframe(
        portfolio,
        use_container_width=True,
        hide_index=True
    )

# ----------------------------
# Order Entry
# ----------------------------

st.subheader("Place Orders")

prices = pd.read_csv("data/prices.csv")

current_prices = prices.loc[
    prices["Round"] == round_no
].iloc[0]

orders=[]

header=st.columns([2,1,1,1,1])

header[0].markdown("**Company**")
header[1].markdown("**Price**")
header[2].markdown("**Holding**")
header[3].markdown("**Buy**")
header[4].markdown("**Sell**")

for company in COMPANIES:

    cols=st.columns([2,1,1,1,1])

    cols[0].write(company)

    cols[1].write(
        f"₹{current_prices[company]}"
    )

    cols[2].write(
        int(team_data[company])
    )

    buy_qty=cols[3].number_input(
        "",
        min_value=0,
        step=1,
        key=f"buy_{company}"
    )

    sell_qty=cols[4].number_input(
        "",
        min_value=0,
        step=1,
        key=f"sell_{company}"
    )

    if buy_qty>0:

        orders.append(
            ("BUY",company,int(buy_qty))
        )

    if sell_qty>0:

        orders.append(
            ("SELL",company,int(sell_qty))
        )

st.markdown("---")

if st.button("Submit Orders",use_container_width=True):

    if not trading_status():

        st.error("Trading is Closed.")

    else:

        success=0

        for action,company,qty in orders:

            if action=="BUY":

                if buy_stock(
                    team,
                    company,
                    qty,
                    round_no
                ):
                    success+=1

            else:

                if sell_stock(
                    team,
                    company,
                    qty,
                    round_no
                ):
                    success+=1

        st.success(
            f"{success} trade(s) executed successfully."
        )

        st.rerun()