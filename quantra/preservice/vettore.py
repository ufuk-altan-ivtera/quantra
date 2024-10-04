from ..technical.indicators import Indicator
from ..mark.signal import StandardSignal, Sequentialize

import pandas as pd
from datetime import date

class Apply(Indicator, StandardSignal, Sequentialize):
    
    def apply_all_indicator_functions(self, df, indicators_types_list = ['ADX', 'STD', 'BB', 'TEMA', 'MA', 'SRSI', 'RSI', 'GREENBAR']):
        
        # VOLATILITY
        if 'ADX' in indicators_types_list:
        
            df['ADX5'] = self.average_directional_index(df, 5)
        
        # TREND
        if 'TEMA' in indicators_types_list:

            df['TEMA1'] = self.triple_ema(df, 8).values
            df['TEMA2'] = self.triple_ema(df, 21).values
        
        # MOMENTUM
        if 'RSI' in indicators_types_list:
            
            df['RSI7'] = self.rsi(df, 7).values
            df['RSI15'] = self.rsi(df, 15).values

        return df
    
    def apply_standard_signalling(self, indicator_df):

        signal_lol = []

        for current_index, current_value in enumerate(indicator_df['Close']):

            index_is_not_out_of_range = self.check_if_index_is_not_out_of_range(current_index, indicator_df)
            current_index_is_higher_than_zero = self.check_if_value_is_higher(current_index, 0)

            if current_index_is_higher_than_zero and index_is_not_out_of_range:

                # cross3 (TEMA1 - TEMA2)
                cross3 = self.cross_signal(indicator_df, 'TEMA1', 'TEMA2', current_index)
                
                # pyramid1 (RSI7)
                pyramid1 = self.pyramid_ratio_signal(indicator_df, 'RSI7', current_index, ratio=5) 
                
                # pyramid2 (ADX5)
                pyramid2 = self.pyramid_ratio_signal(indicator_df, 'ADX5', current_index, ratio=4) # False --> True

                signal_list = [cross3, pyramid1, pyramid2]

            else: 

                signal_list = [""] * 3

            signal_lol.append(signal_list)
            
        signal_df = pd.DataFrame(signal_lol, columns = ['cross3', 'pyramid1', 'pyramid2'])
        signal_df.index = indicator_df.index

        return signal_df
        
    def apply_sequentialization(self, signal_df, throwback_period1 = 3, throwback_period2 = 8):

        sequence_lol = []

        for current_index, current_value in enumerate(signal_df['cross3']):

            throwback_index1 = current_index - throwback_period1
            throwback_index2 = current_index - throwback_period2

            current_index_is_higher_than_throwback_period =  self.check_if_value_is_higher(current_index, throwback_period2)

            if current_index_is_higher_than_throwback_period:

                cross3_sequence = self.sequentialize_throwback(signal_df, 'cross3', throwback_index2, current_index)

                pyramid1_sequence = self.sequentialize_throwback(signal_df, 'pyramid1', throwback_index1, current_index)
                
                pyramid2_sequence = self.sequentialize_throwback(signal_df, 'pyramid2', throwback_index1, current_index)
                
                sequence_list = [cross3_sequence, pyramid1_sequence, pyramid2_sequence]

            else:
                sequence_list = [[]] * 3

            sequence_lol.append(sequence_list)
            
        sequence_df = pd.DataFrame(sequence_lol, columns = ['cross3_sequence', 'pyramid1_sequence', 'pyramid2_sequence'])
        sequence_df.index = signal_df.index
            
        return sequence_df
                
    def apply_decision_extraction(self, signal_df, indicator_df):

        decision_lol = []
        for current_index, current_value in enumerate(signal_df['cross3']):

            date = indicator_df.index[current_index]
            price = indicator_df['Close'][current_index]

            cross3 = current_value

            # TEMA False signal should not be in the last throwback sequence
            #cross3_false = False in signal_df['cross3_sequence'].iloc[current_index]
            
            pyramid1_true = True in signal_df['pyramid1_sequence'].iloc[current_index]
            pyramid2_true = True in signal_df['pyramid2_sequence'].iloc[current_index]
            
            #if pyramid1_true and pyramid2_true and cross3_false != True:
            if pyramid1_true and pyramid2_true:

                decision = True

            elif cross3 == False:

                decision = False

            else:
                decision = ""

            decision_list = [date, price, decision]
            decision_lol.append(decision_list)
            
        decision_df =pd.DataFrame(decision_lol, columns= ['Date', 'Close', 'Decision'])
            
        return decision_df
    
    def apply_decision_filteration(self, decision_df):
    
        filtered_decision_df1 = decision_df[decision_df['Decision'] != ""]

        filtered_decision_lol2 = []

        for current_index, current_value in enumerate(filtered_decision_df1['Decision']):

            previous_index = current_index - 1

            current_decision = current_value
            previous_decision = filtered_decision_df1['Decision'].iloc[previous_index]

            if current_decision != previous_decision:

                date = filtered_decision_df1['Date'].iloc[current_index]
                price = filtered_decision_df1['Close'].iloc[current_index]
                filtered_decision_lol2.append([date, price, current_decision])

            else:
                pass
            
        filtered_decision_df2 = pd.DataFrame(filtered_decision_lol2, columns = ['Date', 'Close', 'Decision'])
        return filtered_decision_df2
    
class Backtest(Apply):

    def backtest_results(self, filtered_decision_df2, budget = 1000):
        
        win, loss = 0, 0
        budget_lol = []

        for current_index, current_value in enumerate(filtered_decision_df2['Close']):

            next_index = current_index + 1
            
            decision = filtered_decision_df2['Decision'].iloc[current_index]
            index_is_not_out_of_range = self.check_if_index_is_not_out_of_range(next_index, filtered_decision_df2)
            
            if decision == True and index_is_not_out_of_range:
                
                buying_price = current_value
                selling_price = filtered_decision_df2['Close'].iloc[next_index]
                
                date1 = filtered_decision_df2['Date'].iloc[current_index]
                date2 = filtered_decision_df2['Date'].iloc[next_index]
                
                
                budget = budget / buying_price * selling_price
                budget_list = [date1, buying_price, date2, selling_price, budget] 
                budget_lol.append(budget_list)
                
                if buying_price > selling_price:
                    loss += 1
                    
                elif selling_price > buying_price:
                    win += 1
                
                else:
                    pass
        
        budget_df = pd.DataFrame(budget_lol, columns = ['Date1', 'BuyingPrice', 'Date2', 'SellingPrice', 'Budget'])
        
        total_trade = win + loss
        
        if total_trade != 0:
            win_rate = win / total_trade * 100
            min_budget =  min(budget_df['Budget'])
            max_budget =  max(budget_df['Budget'])
            
        else:
            win_rate = 0
            min_budget =  budget
            max_budget =  budget
        
        final_budget = budget
        
        result_list = [total_trade, win_rate, min_budget, max_budget, final_budget]
        
        return result_list, budget_df
    
    def backtest(self, tickers_list, main_financial_dictionary, filter_date = pd.to_datetime(date(2020, 1, 1))):
        
        backtest_result_lol = []
        backtest_budget_dict = {}

        backtest_failed_tickers_list = []

        for ticker in tickers_list:
            
                df = main_financial_dictionary[ticker]['price_df']
                df = df[df.index >= filter_date]
                
                indicator_df = self.apply_all_indicator_functions(df)

                signal_df = self.apply_standard_signalling(indicator_df)
                signal_df['pyramid2'] = signal_df['pyramid2'].replace({False: True})

                sequence_df = self.apply_sequentialization(signal_df, throwback_period1 = 6, throwback_period2=4)
                signal_df = pd.concat([signal_df, sequence_df], axis= 1)

                decision_df = self.apply_decision_extraction(signal_df, indicator_df)

                filtered_decision_df2 = self.apply_decision_filteration(decision_df)

                backtest_result_list, budget_df = self.backtest_results(filtered_decision_df2, budget = 1000)
                backtest_result_list.insert(0, ticker)
                backtest_result_lol.append(backtest_result_list)
                
                backtest_budget_dict[ticker] = {'budget_df': budget_df, 'shape': df.shape, 'decision_df': decision_df, 'signal_df': signal_df, 'indicator_df': indicator_df}
                backtest_failed_tickers_list.append(ticker)
                
        return backtest_result_lol, backtest_budget_dict, backtest_failed_tickers_list

                        
