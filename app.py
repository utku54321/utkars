from flask import Flask, request, jsonify, render_template
import yfinance as yf
import pandas as pd
import bs4
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_financials', methods=['POST'])
def get_financials():
    ticker_name = request.form['ticker'].strip()
    ticker = yf.Ticker(ticker_name)

    def prepare_data(df):
        if df.empty:
            return {}
        df = df.fillna(0) / 1_000_000  # Convert to millions
        df = df.transpose()
        df.index = df.index.astype(str)
        return df.to_dict(orient='index')

    income_data = prepare_data(ticker.financials)
    balance_data = prepare_data(ticker.balance_sheet)
    cashflow_data = prepare_data(ticker.cashflow)

    # Directly return JSON (no to_json() or dumps needed!)
    return jsonify({
        'income_statement': income_data,
        'balance_sheet': balance_data,
        'cash_flow': cashflow_data
    })

if __name__ == '__main__':
    app.run(debug=True)






