from ..data.request import Request
import pandas as pd





def xxx(price_df_dict, ticker):
    
    df = price_df_dict[ticker]
    final_date = df.iloc[-1].index
    
    final_date