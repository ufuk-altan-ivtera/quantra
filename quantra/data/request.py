import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import aiohttp

from datetime import date
today_as_string = date.today()

class Client:

    async def get(self, url, query, headers):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as client:
            async with client.get(url, params=query, headers=headers) as response:
                if response.status == 204:
                    return {"message": "No content"}
                elif response.status // 100 == 2:  # Checks if status is 2xx
                    return await response.json()
                else:
                    response_text = await response.text()
                    raise Exception(f"Failed GET request: {response.status}, {response_text}")

    async def post(self, url, query, headers):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as client:
            async with client.post(url, json=query, headers=headers) as response:
                if response.status == 204:
                    return {"message": "No content"}
                elif response.status // 100 == 2:
                    return await response.json()
                else:
                    response_text = await response.text()
                    raise Exception(f"Failed POST request: {response.status}, {response_text}")

    async def put(self, url, query, headers):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as client:
            async with client.put(url, json=query, headers=headers) as response:
                if response.status == 204:
                    return {"message": "No content"}
                elif response.status // 100 == 2:
                    return await response.json()
                else:
                    response_text = await response.text()
                    raise Exception(f"Failed PUT request: {response.status}, {response_text}")

    async def delete(self, url, query, headers):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as client:
            async with client.delete(url, json=query, headers=headers) as response:
                if response.status == 204:
                    return {"message": "No content"}
                elif response.status // 100 == 2:
                    return await response.json()
                else:
                    response_text = await response.text()
                    raise Exception(f"Failed DELETE request: {response.status}, {response_text}")

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