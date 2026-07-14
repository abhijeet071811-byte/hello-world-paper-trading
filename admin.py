from pathlib import Path
import json
import pandas as pd

HOLDINGS_FILE = DATA_DIR / "holdings.csv"
TRADES_FILE = DATA_DIR / "trades.csv"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STATE_FILE = DATA_DIR / "game_state.json"

DEFAULT_STATE = {
    "current_round": 0,
    "trading_open": False
}


def initialize_game():
    if not STATE_FILE.exists():
        with open(STATE_FILE, "w") as f:
            json.dump(DEFAULT_STATE, f, indent=4)


def load_state():
    initialize_game()
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def get_current_round():
    return load_state()["current_round"]


def set_current_round(round_no):
    state = load_state()
    state["current_round"] = round_no
    save_state(state)
    return state["current_round"]

def next_round():
    state = load_state()
    state["current_round"] += 1
    save_state(state)


def open_trading():
    state = load_state()
    state["trading_open"] = True
    save_state(state)


def close_trading():
    state = load_state()
    state["trading_open"] = False
    save_state(state)


def trading_status():
    return load_state()["trading_open"]


def reset_game():
    # Reset game state
    save_state(DEFAULT_STATE.copy())

    # Reset holdings
    holdings = pd.read_csv(HOLDINGS_FILE)

    holdings["Cash"] = 10000

    for column in holdings.columns:
        if column not in ["Team", "team_name", "Cash"]:
            holdings[column] = 0

    holdings.to_csv(HOLDINGS_FILE, index=False)

    # Clear trade history while preserving headers
    trades = pd.read_csv(TRADES_FILE)
    trades = trades.iloc[0:0]
    trades.to_csv(TRADES_FILE, index=False)