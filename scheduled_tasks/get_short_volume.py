from datetime import datetime
import sqlite3

from helpers import *

conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()


def full_ticker_list():
    """
    List of all the popular tickers identified. Add more to the list if you wish to
    """
    list_of_tickers = ["GME", "AMC", "BB", "CLOV", "UWMC", "NIO", "TSLA", "AAPL", "SPY", "NOK", "AMD", "NVDA", "MSFT",
                       "RBLX", "F", "PLTR", "COIN", "RKT", "MVIS", "FUBO", "DISCA", "VIAC", "SNDL", "SPCE", "FB", "SNAP",
                       "OCGN", "QQQ", "TQQQ", "ROKU", "TWTR", "ARKK", "ARKF", "ARKG", "ARKQ", "SQQQ", "INTC", "BABA",
                       "IWM", "ROOT", "BA", "SQ", "SHOP", "SE", "VOO", "PYPL", "EXPR", "KOSS", "SOFI", "WKHS", "DIA", "GM",
                       "TLRY", "CLNE", "WISH", "CLF", "GOEV", "DKNG", "RIDE", "AMZN", "GOOG"]
    return list_of_tickers


def short_volume(symbol):
    url = "http://shortvolumes.com/?t={}".format(symbol)
    table = pd.read_html(url)
    try:
        shorted_vol_daily = table[3].iloc[2:]

        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1mo", interval="1d")

        for index, row in shorted_vol_daily.iterrows():
            date = datetime.strptime(row[0], "%Y-%m-%d")
            close_price = round(history.loc[date]["Close"], 2)
            db.execute("INSERT OR IGNORE INTO short_volume VALUES (?, ?, ?, ?, ?, ?)",
                       (symbol, row[0], close_price, row[1], row[2], row[3]))
            conn.commit()
        print("{} INSERTED INTO SHORT-VOLUME DATABASE SUCCESSFULLY".format(symbol))
    except IndexError:
        print("{} NOT FOUND!".format(symbol))


if __name__ == '__main__':
    for i in full_ticker_list():
        short_volume(i)
