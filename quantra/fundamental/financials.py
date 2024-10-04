from ..utils.servant import Check, Format

from datetime import timedelta

class ObtainFinancials(Check, Format):

    def obtain_single_financial_statement(self, financial_statements_df, column, statement):
        
        statement_exists = self.check_if_element_exists(statement, financial_statements_df.index)

        if statement_exists:

            financial_value = financial_statements_df[column].loc[statement]
            
            value_is_iterable = self.check_if_value_is_iterable(financial_value)            
            if value_is_iterable:
                financial_value = financial_value[0]
                
            else:
                pass
            
        else:
            financial_value = 0

        return financial_value
    
    def obtain_financial_statements_summation(self, financial_statements_df, column, statements_list):
        
        financial_value_list = [self.obtain_single_financial_statement(financial_statements_df, column, statement) for statement in statements_list]
        
        empty_string_exists = self.check_if_element_exists(0, financial_value_list)
        
        if empty_string_exists:
            empty_string_count = financial_value_list.count(0)
            
            for index in range(empty_string_count):
                financial_value_list.remove(0)
                
        else:
            pass
        
        total_value_of_statements = sum(financial_value_list)
        
        return total_value_of_statements
    
    def obtain_info(self, info):
        
        keys = ['shortName', 'currency', 'industry', 'sector']
        info_list = [info[key] if key in info else 0 for key in keys]
        
        return info_list
    
    def obtain_future_price(self, price_df, date, day = 0):
        
        future_date = date + timedelta(days = day)
        future_price_array = price_df[price_df.index >= future_date]['Close'].values
            
        if len(future_price_array) > 0:
            future_price = future_price_array[0]
            
        else:
            future_price = 0
            
        return future_price
            
class CalculateFinancials(Check):
    
    def calculate_difference(self, value1, value2):
        
        value1_is_numerical = self.check_if_value_is_numerical(value1)
        value2_is_numerical = self.check_if_value_is_numerical(value2)
        
        if value1_is_numerical and value2_is_numerical:
            
            difference = value1 - value2
            
        else:
            difference = 0
            
        return difference
    
    def calculate_ratio(self, value1, value2):
        
        value1_is_numerical = self.check_if_value_is_numerical(value1)
        value2_is_numerical = self.check_if_value_is_numerical(value2)
        
        if value1_is_numerical and value2_is_numerical:
            value2_is_not_zero = self.check_if_value_is_not_zero(value2)
            
            if value2_is_not_zero:
            
                ratio = value1 / value2
            else:
                ratio = 0
            
        else:
            ratio = 0
            
        return ratio
    



