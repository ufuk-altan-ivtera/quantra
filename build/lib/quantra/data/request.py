import yfinance as yf
import pandas as pd
import aiohttp
import asyncio

from quantra.utils.servant import Format

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

    def __init__(self):

        self.format_ = Format()
     
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
        
        tasks = [self.format_.format_tz_date_object(index) for index in price_df.index]
        index = await asyncio.gather(*tasks)
        price_df.index = index

        return price_df