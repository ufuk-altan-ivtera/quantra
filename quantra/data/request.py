import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import aiohttp

from datetime import date
today_as_string = date.today()

VERIFY_SSL = False # !!!!

class Client:

    async def get(self, url, query, headers):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=VERIFY_SSL)
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
            connector=aiohttp.TCPConnector(verify_ssl=VERIFY_SSL)
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
            connector=aiohttp.TCPConnector(verify_ssl=VERIFY_SSL)
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
            connector=aiohttp.TCPConnector(verify_ssl=VERIFY_SSL)
        ) as client:
            async with client.delete(url, json=query, headers=headers) as response:
                if response.status == 204:
                    return {"message": "No content"}
                elif response.status // 100 == 2:
                    return await response.json()
                else:
                    response_text = await response.text()
                    raise Exception(f"Failed DELETE request: {response.status}, {response_text}")

class Yahoo():
     
    async def financial_statements(self, ticker, freq='yearly'):
        
        stock = yf.Ticker(ticker)
        balance_sheet = stock.get_balance_sheet(freq = freq)
        income_statement = stock.get_income_stmt(freq = freq)
        cash_flow = stock.get_cash_flow(freq = freq)
        
        financial_statements = pd.concat([balance_sheet, income_statement, cash_flow])
        return financial_statements
    
    async def info(self, ticker):
        
        stock = yf.Ticker(ticker)
        info = stock.get_info()
        return info
    
    async def price_df(self, ticker, start, end):
        
        stock = yf.Ticker(ticker)
        price_df = stock.history(start=start, end=end)
        return price_df