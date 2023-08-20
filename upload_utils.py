# upload_utils.py
import pandas as pd
import yfinance as yf  # Replace with the appropriate library for fetching data

def check_isin(isin):
    try:
        _ = yf.Ticker(isin)
        return True
    except:
        return False

def process_isins(isin_list):
    processed = 0
    for isin in isin_list:
        if check_isin(isin):
            processed += 1
    return processed
