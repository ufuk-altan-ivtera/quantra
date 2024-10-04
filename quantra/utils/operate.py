from quantra.utils.servant import Check

from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Calculate():

    def calculate_percentage_difference(self, first_value, next_value):
        
        if first_value == 0:
            raise ValueError("The first value cannot be zero to calculate percentage difference.")
        
        percentage_difference = round(((next_value - first_value) / first_value) * 100, 3)
        
        return percentage_difference
    
    def calculate_results(self, df_filtered6, budget = 1000):

        win, loss = 0,0
        budget_flow_list = []

        for row in df_filtered6.iterrows():
            
            row  = row[1]

            if row['Sell'] > row['Buy']:
                win += 1
            
            else:
                loss += 1
                
            budget = budget / row['Buy'] * row['Sell']
            budget_flow_list.append(budget)

        df_filtered6['Budget'] = budget_flow_list
        df_filtered6 = df_filtered6.dropna()

        if len(df_filtered6) > 0:
            budget = df_filtered6['Budget'].iloc[-1]
        else:
            budget = 1000

        return budget, win, loss, df_filtered6
    
    def calculate_percentage_rate(self, array, throwback_period):

        true_count = np.count_nonzero(array > 0)
        true_rate = true_count / throwback_period * 100
        return true_rate

class Obtain():

    def obtain_by_index(self, df, index):
        
        value = df.loc[index]
        return value
    
class Generate():
    
    def generate_dataframe(self, length, value):
        data = [value] * length
        generated_df = pd.DataFrame(data, columns=['Label'])
        return generated_df

class Process( Check):
    
    def process_statement_dictionary(self, ticker, statement_dictionary):
    
        statement_dictionary_processed = {}
        statement_dictionary_processed[ticker] = {statement_dictionary[key]['term']: statement_dictionary[key]['results'] for key in statement_dictionary.keys()}

        for term in statement_dictionary_processed[ticker].keys():
            statement_dictionary_processed[ticker][term] = self.format_dict_to_df(statement_dictionary_processed[ticker][term], ['Results'])

        return statement_dictionary_processed
    
    def process_percentage_value(self, value1, value2, percentage):
        
        value1_is_higher = self.check_if_value_is_higher(value1, value2)
        
        if value1_is_higher:
            percentage = percentage
        else:
            percentage = percentage * -1
            
        return percentage
    
class Assemble(Generate):
    
    def __init__(self):
    
        self.statements = {}
        
    def assemble_dictionaries(self, dict1, dict2):
        """
        Assemble two dictionaries into a single dictionary
        """
        final_dict = dict1.copy()
        final_dict.update(dict2)
        return final_dict
    
    def assemble_label_columns(self, label_df):
        
        length = label_df.shape[0]
        value = 0
    
        generated_label_df = self.generate_dataframe(length, value)
        label_columns = label_df.columns

        for column in label_columns:
            generated_label_df['Label'] = generated_label_df['Label'] + label_df[column]
            
        return generated_label_df
        
class Transform():

    def __init__(self):
        self.eda_scaler = MinMaxScaler(feature_range=(1,100))
    
    def transform_to_scaled_df(self, df):
        
        scaled_array = self.eda_scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_array, columns= df.columns, index = df.index)
        return scaled_df

