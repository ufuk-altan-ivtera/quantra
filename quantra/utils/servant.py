import os
from datetime import datetime, date
import pandas as pd

class Check:
    async def check_if_value_is_not_none(self, value):
        """
        Check if a value is not None and can be converted to float.

        Parameters
        ----------
        value : any
            The value to be checked.

        Returns
        -------
        bool
            True if value is convertible to float, False otherwise.
        """
        try:
            float(value)
            return True
        except:
            return False

    async def check_if_value_is_not_zero(self, value):
        """
        Check if a value is not zero.

        Parameters
        ----------
        value : numeric
            The value to be checked.

        Returns
        -------
        bool
            True if value is not zero, False otherwise.
        """
        return value != 0

    async def check_if_element_exists(self, element, data):
        """
        Check if an element exists in a data structure (list, dict, etc.).

        Parameters
        ----------
        element : any
            The element to search for.
        data : iterable
            The data structure to search in.

        Returns
        -------
        bool
            True if element is in data, False otherwise.
        """
        return element in data

    async def check_if_folder_exist(self, folder_path):
        """
        Check if a folder exists.

        Parameters
        ----------
        folder_path : str
            Path to the folder.

        Returns
        -------
        bool
            True if folder exists, False otherwise.
        """
        return os.path.exists(folder_path)

    async def check_if_data_is_string(self, data):
        """
        Check if the data is of type string.

        Parameters
        ----------
        data : any
            The data to check.

        Returns
        -------
        bool
            True if data is string, False otherwise.
        """
        return isinstance(data, str)

    async def check_if_index_is_not_out_of_range(self, index, data):
        """
        Check if index is within the bounds of a list or similar structure.

        Parameters
        ----------
        index : int
        data : list or similar

        Returns
        -------
        bool
            True if index is in range, False otherwise.
        """
        return index < len(data)

    async def check_if_value_is_higher(self, value1, value2):
        """
        Check if one value is higher than another.

        Parameters
        ----------
        value1 : numeric
        value2 : numeric

        Returns
        -------
        bool
            True if value1 > value2, False otherwise.
        """
        return value1 > value2

    async def check_if_value_is_numerical(self, value):
        """
        Check if a value is numerical (can be converted to float).

        Parameters
        ----------
        value : any

        Returns
        -------
        bool
            True if value is numerical, False otherwise.
        """
        try:
            float(value)
            return True
        except:
            return False

    async def check_if_value_is_iterable(self, value):
        """
        Check if a value is iterable.

        Parameters
        ----------
        value : any

        Returns
        -------
        bool
            True if value is iterable, False otherwise.
        """
        try:
            len(value)
            return True
        except:
            return False

    async def check_if_data_does_not_contain_negative_value(self, data):
        """
        Check if all values in the iterable are non-negative.

        Parameters
        ----------
        data : iterable of numeric

        Returns
        -------
        bool
            True if all values are >= 0, False if any are negative.
        """
        return all(value >= 0 for value in data)


class Format:
    async def format_datetime_to_string(self, datetime_object):
        """
        Convert a datetime object to string format 'YYYY-MM-DD'.

        Parameters
        ----------
        datetime_object : datetime

        Returns
        -------
        str
            String representation of the date.
        """
        return datetime_object.strftime('%Y-%m-%d')

    async def format_string_to_datetime(self, string):
        """
        Convert a string in 'YYYY-MM-DD' format to a datetime object.

        Parameters
        ----------
        string : str

        Returns
        -------
        datetime
        """
        return datetime.strptime(string, '%Y-%m-%d')

    async def format_dict_to_df(self, data, columns):
        """
        Convert a dictionary to a pandas DataFrame.

        Parameters
        ----------
        data : dict
        columns : list of str

        Returns
        -------
        pd.DataFrame
        """
        return pd.DataFrame.from_dict(data=data, columns=columns, orient='index')

    async def format_timezone_to_timestamp(self, timezone):
        """
        Remove timezone info from a datetime object.

        Parameters
        ----------
        timezone : pd.Timestamp

        Returns
        -------
        pd.Timestamp
        """
        return timezone.tz_localize(None)

    async def format_tz_timestamp2utc(self, tz):
        """
        Convert timezone-aware timestamp to UTC and strip tz info.

        Parameters
        ----------
        tz : pd.Timestamp

        Returns
        -------
        pd.Timestamp
        """
        utc_timestamp = tz.tz_convert('UTC')
        timestamp = utc_timestamp.tz_localize(None)
        return pd.to_datetime(timestamp.date())

    async def format_tz_date_object(self, tz):
        """
        Extract date from a datetime object and return a date object.

        Parameters
        ----------
        tz : datetime or pd.Timestamp

        Returns
        -------
        date
        """
        return date(tz.year, tz.month, tz.day)
