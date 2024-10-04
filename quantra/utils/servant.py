import os
from datetime import datetime
import pandas as pd
from datetime import date

class Check:

    def check_if_value_is_not_none(self, value):
        
        try:
            value = float(value)
            is_not_null = True
        except:
            is_not_null = False

        return is_not_null
    
    def check_if_value_is_not_zero(self, value):
        
        if value != 0:
            value_is_not_zero = True
            
        else:
            value_is_not_zero = False
            
        return value_is_not_zero 
    
    def check_if_element_exists(self, element, data): # -
        
        if element in data:
            element_exists = True
            
        else:
            element_exists = False
            
        return element_exists
    
    def check_if_folder_exist(self, folder_path):
        """
        Check if a folder exists or not
        
        Parameters
        ----------
        folder_path: str
            Folder location to save statements
        
        """
        folder_exists = os.path.exists(folder_path)
        return folder_exists
    
    def check_if_data_is_string(self, data):
        """
        Check if data is string
        
        Parameters
        ----------
        data: datetime, str, etc.
            Data to be checked
        """
        type_ = type(data)
        is_string = type_ == str
        return is_string

    def check_if_index_is_not_out_of_range(self, index, data):

        if index < len(data):
            index_is_not_out_of_range = True
        else:
            index_is_not_out_of_range = False

        return index_is_not_out_of_range 

    def check_if_value_is_higher(self, value1, value2):

        if value1 > value2:
            value_is_higher = True
        else:
            value_is_higher = False

        return value_is_higher 

    def check_if_value_is_numerical(self, value):
        
        try: 
            value_ = float(value)
            value_is_numerical = True
            
        except:
            value_is_numerical = False

        return value_is_numerical
    
    def check_if_value_is_iterable(self, value):
        
        try:
            length = len(value)
            value_is_iterable = True
            
        except:
            value_is_iterable = False
            
        return value_is_iterable 
    
    def check_if_data_does_not_contain_negative_value(self, data):
    
        values_are_positive = [value >= 0 for value in data]
        
        data_does_not_contain_negative_value = False not in values_are_positive
        return data_does_not_contain_negative_value
    
class Format():
    
    def format_datetime_to_string(self, datetime_object):
        """
        Change datetime into string format

        Parameters
        ----------
        datetime_object: datetime
        """
        date_string = datetime_object.strftime('%Y-%m-%d')
        return date_string
    
    def format_string_to_datetime(self, string):

        datetime_object = datetime.strptime(string, '%Y-%m-%d')
        return datetime_object
    
    def format_dict_to_df(self, data, columns):
        
        df = pd.DataFrame.from_dict(data = data, columns = columns, orient = 'index')
        return df
    
    def format_timezone_to_timestamp(self, timezone):
    
        timestamp = timezone.tz_localize(None)
        return timestamp    
    
    def format_tz_timestamp2utc(self, tz):

        utc_timestamp = tz.tz_convert('UTC')
        timestamp = utc_timestamp.tz_localize(None)
        timestamp_date = pd.to_datetime(timestamp.date)
        return timestamp_date
    
    def format_tz_date_object(self, tz):
        year = tz.year
        month = tz.month
        day = tz.day

        datey = date(year, month, day)
        return datey






