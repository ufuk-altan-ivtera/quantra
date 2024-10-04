import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

from datetime import date
today_as_string = date.today()

class Request():
     
    def __init__(self, ticker):
        self.stock = yf.Ticker(ticker)
        

    def request_financial_statements(self, freq='yearly'):

        balance_sheet = self.stock.get_balance_sheet(freq = freq)
        income_statement = self.stock.get_income_stmt(freq = freq)
        cash_flow = self.stock.get_cash_flow(freq = freq)
        
        financial_statements = pd.concat([balance_sheet, income_statement, cash_flow])
        
        return financial_statements
    
    def request_info(self):
        
        info = self.stock.get_info()
        return info
    
    def request_price_df(self, start, end):
        
        price_df = self.stock.history(start=start, end=end)
        return price_df