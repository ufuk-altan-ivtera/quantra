from ..utils.servant import Check

class Label(Check):
    
    def __init__(self, df, expansion_period = 10, threshold_true_percentage = 70, ma_parameter = 1.04):
        
        self.expansion_period = expansion_period 
        self.threshold_true_percentage = threshold_true_percentage
        
        self.close_series = df['Close']
        self.open_series = df['Open']

        self.boolean_bull_series = self.close_series > self.open_series
        self.boolean_bear_series = self.open_series > self.close_series

        self.close_percentage_change_series = df['Close'].pct_change()

        self.moving_average_series = df['MA15']
        self.ma_parameter = 1.04
        
    def mountain_label(self, current_index):
        
        expansion_index = current_index + self.expansion_period
        
        boolean_price_series = self.boolean_bull_series.iloc[current_index:expansion_index] # [False, True, True, True, ..., False]
        
        expanded_percentage_series = self.close_percentage_change_series.iloc[current_index:expansion_index]
        boolean_percentage_series = expanded_percentage_series > 0 # [False, True, True, True, ..., False]
        
        expanded_close_series = self.close_series.iloc[current_index:expansion_index]
        expanded_ma_series = self.moving_average_series.iloc[current_index:expansion_index]
        boolean_ma_series = (expanded_close_series > expanded_ma_series * self.ma_parameter)
        
        true_in_price_series = self.check_if_value_in_data(True, boolean_price_series.values)
        true_in_percentage_series = self.check_if_value_in_data(True, boolean_percentage_series.values)
        true_in_ma_series = self.check_if_value_in_data(True, boolean_ma_series.values)
        
        if true_in_price_series and true_in_percentage_series and true_in_ma_series:
            
            price_true_percentage = (boolean_price_series.value_counts()[True] / self.expansion_period) * 100
            percentage_diff_true_percentage = (boolean_percentage_series.value_counts()[True] / self.expansion_period) * 100
            ma_true_percentage = (boolean_ma_series.value_counts()[True] / self.expansion_period) * 100
            
            price_percentage_is_higher = self.check_if_value_is_higher(price_true_percentage, self.threshold_true_percentage)
            percentage_diff_is_higher = self.check_if_value_is_higher(percentage_diff_true_percentage, self.threshold_true_percentage)
            ma_percentage_is_higher = self.check_if_value_is_higher(ma_true_percentage, self.threshold_true_percentage)
            
            if price_percentage_is_higher and percentage_diff_is_higher and ma_percentage_is_higher:
                signal = 'mountain'
                
            else:
                signal = ""
        else:
            signal = ""
            
        return signal
    
    def waterfall_label(self, current_index):
        
        expansion_index = current_index + self.expansion_period
        
        boolean_price_series = self.boolean_bear_series.iloc[current_index:expansion_index]
        
        expanded_percentage_series = self.close_percentage_change_series.iloc[current_index:expansion_index]
        boolean_percentage_series = expanded_percentage_series < 0
        
        expanded_close_series = self.close_series.iloc[current_index:expansion_index]
        expanded_ma_series = self.moving_average_series.iloc[current_index:expansion_index]
        boolean_ma_series = (expanded_close_series < expanded_ma_series / self.ma_parameter)
        
        true_in_price_series = self.check_if_value_in_data(True, boolean_price_series.values)
        true_in_percentage_series = self.check_if_value_in_data(True, boolean_percentage_series.values)
        true_in_ma_series = self.check_if_value_in_data(True, boolean_ma_series.values)
        
        if true_in_price_series and true_in_percentage_series and true_in_ma_series:
            
            price_true_percentage = (boolean_price_series.value_counts()[True] / self.expansion_period) * 100
            percentage_diff_true_percentage = (boolean_percentage_series.value_counts()[True] / self.expansion_period) * 100
            ma_true_percentage = (boolean_ma_series.value_counts()[True] / self.expansion_period) * 100
            
            price_percentage_is_higher = self.check_if_value_is_higher(price_true_percentage, self.threshold_true_percentage)
            percentage_diff_is_higher = self.check_if_value_is_higher(percentage_diff_true_percentage, self.threshold_true_percentage)
            ma_percentage_is_higher = self.check_if_value_is_higher(ma_true_percentage, self.threshold_true_percentage)
            
            if price_percentage_is_higher and percentage_diff_is_higher and ma_percentage_is_higher:
                signal = 'waterfall'
                
            else:
                signal = ""
        else:
            signal = ""
            
        return signal
    
    def label(self):
        
        label_list = []
        
        for current_index, current_value in enumerate(self.close_series):
    
            index_is_not_out_of_range = self.check_if_index_is_not_out_of_range(current_index, self.close_series)

            if index_is_not_out_of_range:
                
                waterfall = self.waterfall_label(current_index)
                mountain = self.mountain_label(current_index)
                
                labels = [waterfall, mountain]
                
            else:
                labels = ['', '']
            
            label_list.append(labels)
        return label_list
                