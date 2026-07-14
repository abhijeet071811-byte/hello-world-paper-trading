from pathlib import Path
import pandas as pd
from util import COMPANIES

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

HOLDINGS_FILE = DATA_DIR / "holdings.csv"
PRICES_FILE = DATA_DIR / "prices.csv"
TRADES_FILE = DATA_DIR / "trades.csv"

# def load_holdings():
#     return pd.read_csv(HOLDINGS_FILE)


# def save_holdings(df):
#     df.to_csv(HOLDINGS_FILE, index=False)


# def load_prices():
#     return pd.read_csv(PRICES_FILE)


# def load_trades():
#     return pd.read_csv(TRADES_FILE)

# import sys
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(str(BASE_DIR))

# import pandas as pd
# from util import COMPANIES
# DATA_DIR = BASE_DIR / "data"
# PRICES_FILE = DATA_DIR / "prices.csv"
# HOLDINGS_FILE = DATA_DIR / "holdings.csv"
# PRICES_FILE = DATA_DIR / "prices.csv"
# TRADES_FILE = DATA_DIR / "trades.csv"

def get_price(round_no,company):

    df = pd.read_csv(PRICES_FILE)
    price = df.loc[df["Round"] == round_no, company].iloc[0]
    return float(price)

def buy_stock(team_name,company,quantity,round_no):

    if quantity <= 0:
        return False

    current_price = get_price(round_no, company)
    df = pd.read_csv(HOLDINGS_FILE)
    cash_reqd = quantity * current_price
    cash = df.loc[df["team_name"] == team_name, "Cash"].iloc[0]
    if cash_reqd <= cash:
        df.loc[df["team_name"] == team_name, "Cash"] -= cash_reqd
        df.loc[df["team_name"] == team_name, company] += quantity
        df.to_csv(HOLDINGS_FILE, index=False)
        record_trade(team_name, round_no, company, "BUY", quantity, current_price)
        return True
    return False


# Sell stock function
def sell_stock(team_name, company, quantity, round_no):

    if quantity <= 0:
        return False
        
    current_price = get_price(round_no, company)
    df = pd.read_csv(HOLDINGS_FILE)

    shares = df.loc[df["team_name"] == team_name, company].iloc[0]

    if quantity <= shares:
        df.loc[df["team_name"] == team_name, company] -= quantity
        df.loc[df["team_name"] == team_name, "Cash"] += quantity * current_price
        df.to_csv(HOLDINGS_FILE, index=False)
        record_trade(team_id, round_no, company, "SELL", quantity, current_price)
        return True

    return False

def calculate_portfolio(team_name, round_no):
    holdings = pd.read_csv(HOLDINGS_FILE)
    prices = pd.read_csv(PRICES_FILE)

    team = holdings.loc[holdings["team_name"] == team_name].iloc[0]
    current_prices = prices.loc[prices["Round"] == round_no].iloc[0]

    total = float(team["Cash"])

    for company in COMPANIES:
        total += team[company] * current_prices[company]

    return total


def generate_leaderboard(round_no):
    holdings = pd.read_csv(HOLDINGS_FILE)

    leaderboard = []

    for team_name in holdings["team_name"]:
        value = calculate_portfolio(team_name, round_no)
        leaderboard.append({"team_name": team_name, "Portfolio Value": value})

    leaderboard_df = pd.DataFrame(leaderboard)
    leaderboard_df = leaderboard_df.sort_values("Portfolio Value", ascending=False).reset_index(drop=True)
    leaderboard_df.insert(0, "Rank", leaderboard_df.index + 1)

    return leaderboard_df

def record_trade(team_name, round_no, company, action, quantity, price):
    df = pd.read_csv(TRADES_FILE)

    new_trade = {
        "Team": team_name,
        "Round": round_no,
        "Company": company,
        "Action": action,
        "Quantity": quantity,
        "Price": price
    }

    df.loc[len(df)] = new_trade
    df.to_csv(TRADES_FILE, index=False)

def next_round(round_no):
    return round_no + 1