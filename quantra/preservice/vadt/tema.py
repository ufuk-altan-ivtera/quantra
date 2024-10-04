
from ...utils.servant import Check
from ...utils.operate import Calculate

from ...technical.indicators import Indicator
from ...mark.signal import StandardSignal
from ...ai.preprocess.sequence_pipeline import CreateSequencePipeline

import pandas as pd
import numpy as np

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

class Apply(Calculate,
            Indicator, 
            StandardSignal,  
            CreateSequencePipeline):
    
    def __init__(self):
        
        self.throwback_period = 4
        self.training_columns = ['Volume', 'ADX1', 'ADX2', 'RSI1', 'RSI2', 'RSI%', 'ADX%', 'BBWP']
        
        CreateSequencePipeline.__init__(self, self.throwback_period, self.training_columns)
    
    def apply_tema_functions(self, df):
        df = df.copy()

        df['TEMA1'] = self.triple_ema(df, 8).values
        df['TEMA2'] = self.triple_ema(df, 13).values
        return df
    
    def apply_standard_signalling(self, indicator_df):

        signal_list = []

        for current_index, current_value in enumerate(indicator_df['Close']):

            index_is_not_out_of_range = self.check_if_index_is_not_out_of_range(current_index, indicator_df)
            current_index_is_higher_than_zero = self.check_if_value_is_higher(current_index, 0)

            if current_index_is_higher_than_zero and index_is_not_out_of_range:
                cross3 = self.cross_signal(indicator_df, 'TEMA1', 'TEMA2', current_index)
            else: 
                cross3 = ""

            signal_list.append(cross3)

        return signal_list
    
    def apply_indicator_functions(self, df):
        
        df['ADX1'] = self.average_directional_index(df, 5).values
        df['ADX2'] = self.average_directional_index(df, 8).values
            
        df['BBL'], df['BBH'] = self.bollinger_bands(df, period = 20)
        df['BBW'] = df['BBH'] - df['BBL']

        df['RSI1'] = self.rsi(df, 7).values
        df['RSI2'] = self.rsi(df, 15).values

        return df
    
    def apply_expanded_sequentialization(self, df, column, expansion_period = 8):

        sequence_list = []

        for current_index, current_value in enumerate(df['Close']):

            expansion_index = current_index + expansion_period

            index_is_not_out_of_range =  self.check_if_index_is_not_out_of_range(expansion_index, df)

            if index_is_not_out_of_range:
                
                sequence = self.sequentialize_expansion(df, column, current_index, expansion_index)

            else:
                sequence = [""] * expansion_period

            sequence_list.append(sequence)
            
        return sequence_list
    
    def apply_preprocessing(self, df,  expansion_period = 8):

        columns = self.create_column_names()
        columns.append('Label')

        df['Index'] = range(1,len(df)+ 1)

        # Indicators
        df = self.apply_indicator_functions(df)
        df['RSI%'] = df['RSI1'].pct_change()
        df['ADX%'] = df['ADX1'].pct_change()
        df['BBWP'] = [self.calculate_percentage_difference(row[1]['BBH'], row[1]['BBL']) for row in df.iterrows()]

        # Labelling
        df['ChangeBoolean'] = df['Close'].pct_change() > 0
        df['ChangeBooleanSequence'] = self.apply_expanded_sequentialization(df, 'ChangeBoolean', expansion_period = expansion_period)
        df['BooleanPercentage'] = [np.count_nonzero(sequence) / len(sequence) * 100 for sequence in df['ChangeBooleanSequence']]
        df['Label'] = df['BooleanPercentage'].apply(lambda value: self.create_sequence_label(value))

        # Clean up
        df = df.dropna()

        filtered_df = df[df['TemaCross'] != ""]

        # Sequences
        flattened_values_lol = self.create_flattened_values_lol(filtered_df, df)
        sequence_df = pd.DataFrame(flattened_values_lol, columns = columns)
            
        return sequence_df, df
    
    def apply_testing(self, ticker, df):
        
        df = self.apply_tema_functions(df)
        df['TemaCross'] = self.apply_standard_signalling(df)
        
        sequence_df, _ = self.apply_preprocessing(df)
        sequence_df = sequence_df.dropna()

        X = sequence_df.drop('Label', axis=1)
        y = sequence_df['Label']
        
        smote = SMOTE(random_state=0)
        X_res, y_res = smote.fit_resample(X, y)

        X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state = 0)

        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        classifier = RandomForestClassifier(n_estimators=100, random_state=0)
        classifier.fit(X_train_scaled, y_train)

        y_pred = classifier.predict(X_test_scaled)

        report = classification_report(y_test, y_pred, output_dict=True)
        keys = ['accuracy', 'macro avg', 'weighted avg']

        for key in keys: report.pop(key)

        result_list = []
        for key in report.keys(): 
            result_list.append(key)
            result_list.append(report[key]['precision'])

        result_list.insert(0, ticker)

        value_counts = y.value_counts().values.tolist()
        labels = list(y.value_counts().index)
        result_list = result_list + labels + value_counts
        
        return result_list
    
    def apply_training(self, ticker, df):
        
        sequence_df, df = self.apply_preprocessing(df)
        sequence_df = sequence_df.dropna()
        
        # Training
        X = sequence_df.drop('Label', axis=1)
        y = sequence_df['Label']
        
        smote = SMOTE(random_state=0)
        X_res, y_res = smote.fit_resample(X, y)
        
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_res)
        
        classifier = RandomForestClassifier(n_estimators=100, random_state=0)
        classifier.fit(X_train_scaled, y_res)
        
        # Prediction
        sequence_length = self.throwback_period + 1
        prediction_df = df[self.training_columns].iloc[-sequence_length:]
        
        flattened_values = self.sequentialize_flattened_values(prediction_df, self.training_columns)
        flattened_values = np.array(flattened_values)
        flattened_values_reshaped =  np.reshape(flattened_values, (1, flattened_values.shape[0]))
        flattened_values_transformed = scaler.transform(flattened_values_reshaped)
            
        prediction = classifier.predict(flattened_values_transformed)
        result = [ticker, prediction[0]]
        
        return result

    def apply_trading(self, ticker, df):
        
        df = self.apply_tema_functions(df)
        df['TemaCross'] = self.apply_standard_signalling(df)
        
        final_signal = df['TemaCross'].iloc[-1]
        if final_signal != "":
            result = self.apply_training(ticker, df)
            
        else:
            result = [ticker, ""]
            
        return result
            

    