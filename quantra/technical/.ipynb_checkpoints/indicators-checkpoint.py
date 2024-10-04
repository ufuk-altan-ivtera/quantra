import numpy as np
import pandas as pd

from ta.volatility import BollingerBands
from ta.trend import ADXIndicator

class Momentum():

    def srsi(self, series, period=10, smoothK=2, smoothD=2):

        # Calculate RSI 
        delta = series.diff().dropna()
        ups = delta * 0
        downs = ups.copy()
        ups[delta > 0] = delta[delta > 0]
        downs[delta < 0] = -delta[delta < 0]
        ups[ups.index[period-1]] = np.mean( ups[:period] ) #first value is sum of avg gains
        ups = ups.drop(ups.index[:(period-1)])
        downs[downs.index[period-1]] = np.mean( downs[:period] ) #first value is sum of avg losses
        downs = downs.drop(downs.index[:(period-1)])
        rs = ups.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() / \
             downs.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() 
        rsi = 100 - 100 / (1 + rs)

        # Calculate StochRSI 
        stochrsi  = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
        k = stochrsi.rolling(smoothK).mean() * 100
        d = k.rolling(smoothD).mean()

        return k, d
    
    def rsi(self, df, periods = 14, ema = True):
        """
        Returns a pd.Series with the relative strength index.
        """
        close_delta = df['Close'].diff()

        # Make two series: one for lower closes and one for higher closes
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)

        if ema == True:
            # Use exponential moving average
            ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
            ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        else:
            # Use simple moving average
            ma_up = up.rolling(window = periods, adjust=False).mean()
            ma_down = down.rolling(window = periods, adjust=False).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        return rsi    def rsi(self, df, window):

class Volatility():
        
    def average_directional_index(self, data, period = 9):
        """
        Requires High and Low columns inside the data
        """
       
        high = pd.Series(np.reshape(data['High'].values, (data.shape[0],)))
        low = pd.Series(np.reshape(data['Low'].values, (data.shape[0],)))
        close = pd.Series(np.reshape(data['Close'].values, (data.shape[0],)))

        adxI = ADXIndicator(high, low, close, period, True)
        adx = adxI.adx()
        
        return adx
    
    def standard_deviation(self, data, period = 9):
        std = data['Close'].rolling(window = period).std() 
        return std
    
    def bollinger_bands(self, data, period = 20):

        bb = BollingerBands(data['Close'], period, 2)
        bbl = bb.bollinger_lband()
        bbh = bb.bollinger_hband()

        return pd.Series(bbl), pd.Series(bbh)
    
    def create_periodic_volatility(self, data, period_list, indicator):

        periods = {}

        for period in period_list:

            if indicator == 'STD':
                periods['period' + str(period)] = self.standard_deviation(data, 'Close', period=period)

            elif indicator == 'ADX':

                periods['period' + str(period)] = self.average_directional_index(data, period=period)

        return periods

class Trend():
    
    def moving_average(self, data, window = 13):

        ma = data['Close'].rolling(window=window).mean()
        return ma
    
    def triple_ema(self, data, span = 13):

        ema1 = data['Close'].ewm(span = span ,adjust = False).mean()
        ema2 = ema1.ewm(span = span, adjust = False).mean()
        ema3 = ema2.ewm(span = span, adjust = False).mean()

        tema = (3*ema1)-(3*ema2) + ema3
        return tema
    
    def heikin_ashi(self, df):

        df_ha = df.copy()
        for i in range(df_ha.shape[0]):
            if i > 0:
                df_ha.loc[df_ha.index[i],'Open'] = (df['Open'][i-1] + df['Close'][i-1])/2
                df_ha.loc[df_ha.index[i],'Close'] = (df['Open'][i] + df['Close'][i] + df['Low'][i] +  df['High'][i])/4

        df_ha = df_ha.iloc[1:,:]
        return df_ha
    
class Indicator(Momentum, Trend, Volatility):
    
    def __str__(self):
        return "Assemble all indicators into a single class "
        


    
    



