import numpy as np
import pandas as pd

from ta.volatility import BollingerBands

from quantra.utils.operate import Calculate

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
        return rsi    
    
    def smi(self, df, k_length = 10, d_length = 3, ema_length = 3):
        """Calculates the Stochastic Momentum Index (SMI) using EMA."""

        def second_ema(series, length):
            """Calculates the EMA of the EMA for a given series."""
            first_ema = series.ewm(span=length, adjust=False).mean()
            second_ema = first_ema.ewm(span=length, adjust=False).mean()
            return second_ema
        
        highest_high = df['High'].rolling(window=k_length).max()
        lowest_low = df['Low'].rolling(window=k_length).min()

        highest_lowest_range = highest_high - lowest_low
        relative_range = df['Close'] - (highest_high + lowest_low) / 2

        # Calculating EMA of EMA
        double_ema_relative_range = second_ema(relative_range, d_length)
        double_ema_highest_lowest_range = second_ema(highest_lowest_range, d_length)

        # Calculating SMI
        smi_ = 200 * (double_ema_relative_range / double_ema_highest_lowest_range)

        # Calculating SMI-based EMA
        smi_ema = smi_.ewm(span=ema_length, adjust=False).mean()

        return smi_.values, smi_ema.values

class Volatility():

    def average_directional_index(self, data, period= 6):
        """
        Computes the ADX indicator.
        """
        
        df = data.copy()
        alpha = 1/period

        # TR
        df['H-L'] = df['High'] - df['Low']
        df['H-C'] = np.abs(df['High'] - df['Close'].shift(1))
        df['L-C'] = np.abs(df['Low'] - df['Close'].shift(1))
        df['TR'] = df[['H-L', 'H-C', 'L-C']].max(axis=1)
        del df['H-L'], df['H-C'], df['L-C']

        # ATR
        df['ATR'] = df['TR'].ewm(alpha=alpha, adjust=False).mean()

        # +-DX
        df['H-pH'] = df['High'] - df['High'].shift(1)
        df['pL-L'] = df['Low'].shift(1) - df['Low']
        df['+DX'] = np.where(
            (df['H-pH'] > df['pL-L']) & (df['H-pH']>0),
            df['H-pH'],
            0.0
        )
        df['-DX'] = np.where(
            (df['H-pH'] < df['pL-L']) & (df['pL-L']>0),
            df['pL-L'],
            0.0
        )
        del df['H-pH'], df['pL-L']

        # +- DMI
        df['S+DM'] = df['+DX'].ewm(alpha=alpha, adjust=False).mean()
        df['S-DM'] = df['-DX'].ewm(alpha=alpha, adjust=False).mean()
        df['+DMI'] = (df['S+DM']/df['ATR'])*100
        df['-DMI'] = (df['S-DM']/df['ATR'])*100
        del df['S+DM'], df['S-DM']

        # ADX
        df['DX'] = (np.abs(df['+DMI'] - df['-DMI'])/(df['+DMI'] + df['-DMI']))*100
        adx = df['DX'].ewm(alpha=alpha, adjust=False).mean()
        del df['DX'], df['ATR'], df['TR'], df['-DX'], df['+DX'], df['+DMI'], df['-DMI']

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
    
class Bar(Calculate):
    
    def obtain_bar_category(self, df, percentage_threshold_list = [2,4]):

        bar_category_list = []
        
        for current_index, current_value in enumerate(df['Close']):
            
            close_value = current_value
            open_value = df['Open'].iloc[current_index]
            
            percentage_difference = self.calculate_percentage_difference(close_value, open_value)
            
            if close_value > open_value and percentage_difference >= percentage_threshold_list[-1]:
                bar_category = 'GREEN3'
                
            elif close_value > open_value and percentage_difference >= percentage_threshold_list[0] and percentage_difference <= percentage_threshold_list[-1]:
                bar_category = 'GREEN2'
                
            elif close_value > open_value and percentage_difference <= percentage_threshold_list[0]:
                bar_category = 'GREEN1'
                
            elif close_value < open_value and percentage_difference * -1 >= percentage_threshold_list[-1]:
                bar_category = 'RED3'
                
            elif close_value < open_value and percentage_difference * -1 >= percentage_threshold_list[0] and percentage_difference <= percentage_threshold_list[-1]:
                bar_category = 'RED2'
                
            elif close_value < open_value and percentage_difference <= percentage_threshold_list[0]:
                bar_category = 'RED1'
            
            else:
                bar_category = "Stable"
                
            bar_category_list.append(bar_category)
            
        return bar_category_list

class Indicator(Momentum, Trend, Volatility):

    def apply_all_indicator_functions(self, df, indicators_types_list = ['ADX', 'STD', 'BB', 'TEMA', 'MA', 'SRSI', 'RSI', 'GREENBAR']):
        
        # VOLATILITY
        if 'ADX' in indicators_types_list:
        
            df['ADX1'] = self.average_directional_index(df, 5).values
            df['ADX2'] = self.average_directional_index(df, 8).values
        
        if 'STD' in indicators_types_list:
        
            df['STD1'] = self.standard_deviation(df, 5).values
            df['STD2'] = self.standard_deviation(df, 8).values
        
        if 'BB' in indicators_types_list:
            
            df['BBL'], df['BBH'] = self.bollinger_bands(df, period = 20)
            df['BBW'] = df['BBH'] - df['BBL']
            
        # TREND
        if 'TEMA' in indicators_types_list:

            df['TEMA1'] = self.triple_ema(df, 8).values
            df['TEMA2'] = self.triple_ema(df, 13).values
        
        if 'MA' in indicators_types_list:
        
            df['MA1'] = self.moving_average(df, 15).values
            
        # MOMENTUM
        if 'SRSI' in indicators_types_list:
            
            K, D = self.srsi(df['Close'], period=10, smoothK=2, smoothD=2)
            df['K'], df['D'] = K, D
            
        if 'RSI' in indicators_types_list:
            
            df['RSI1'] = self.rsi(df, 7).values
            df['RSI2'] = self.rsi(df, 15).values
            
        if 'GREENBAR' in indicators_types_list:
            df['GREENBAR'] = (df['Close'] > df['Open']).values

        return df
    
    
    
    



