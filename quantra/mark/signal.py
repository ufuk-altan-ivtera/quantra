from ..utils.servant import Check

class StandardSignal(Check):
    
    def cross_signal(self, df, column1, column2, current_index):
        """
        Generates a signal based on a simple crossover condition between two columns of data.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column1 (str): The name of the first column for comparison.
            column2 (str): The name of the second column for comparison.
            current_index (int): The index at which the comparison is made.

        Returns:
            signal: True if the condition is met, False if the inverse condition is met, or an empty string.
        """
        previous_index = current_index - 1

        current_value1 = df[column1][current_index]
        current_value2 = df[column2][current_index]

        previous_value1 = df[column1][previous_index]
        previous_value2 = df[column2][previous_index]

        # K1 <= D1 and K2 > D2
        if previous_value1 <= previous_value2 and current_value1 > current_value2: 
            signal = True

        # K1 >= D1 and K2 < D2
        elif previous_value1 >= previous_value2 and current_value1 < current_value2: 
            signal = False

        else:
            signal = ""

        return signal

    
    def limited_cross_signal(self, df, column1, column2, current_index, bottom_limit, top_limit):

        """
        Generates a signal based on a crossover condition within specified limits.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column1 (str): The name of the first column for comparison.
            column2 (str): The name of the second column for comparison.
            current_index (int): The index at which the comparison is made.
            bottom_limit (float): The lower limit for the crossover condition.
            top_limit (float): The upper limit for the crossover condition.

        Returns:
            signal: True if the condition is met within the limits,
                    False if the inverse condition is met within the limits,
                    or an empty string.
        """
        previous_index = current_index - 1

        current_value1 = df[column1][current_index]
        current_value2 = df[column2][current_index]

        previous_value1 = df[column1][previous_index]
        previous_value2 = df[column2][previous_index]

        # K1 <= D1 and K2 > D2
        if previous_value1 <= previous_value2 and current_value1 > current_value2 and current_value1 <= bottom_limit:  
            signal = True

        # K1 >= D1 and K2 < D2
        elif previous_value1 >= previous_value2 and current_value1 < current_value2 and current_value1 >= top_limit:   
            signal = False

        else:
            signal = ""

        return signal
    
    def pyramid_signal(self, df, column, current_index):
        """
        Generates a signal based on a pyramid pattern condition within the data column.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column (str): The name of the column for the pyramid pattern comparison.
            current_index (int): The index at which the comparison is made.

        Returns:
            signal: True if the pyramid pattern condition is met, False if the inverse condition is met, or an empty string.
        """
        series = df[column]

        current_index_is_higher_than_two = self.check_if_value_is_higher(current_index, 2)

        if current_index_is_higher_than_two:
            
            gamma = series[current_index - 2]
            pyramid = series[current_index - 1]
            beta = series[current_index]

            gamma_is_not_none = self.check_if_value_is_not_none(gamma)
            pyramid_is_not_none = self.check_if_value_is_not_none(pyramid)
            beta_is_not_none = self.check_if_value_is_not_none(beta)
            
            if beta_is_not_none and pyramid_is_not_none and gamma_is_not_none:

                if pyramid < gamma and pyramid < beta and pyramid:
                    
                    signal = True

                elif pyramid > gamma and pyramid > beta and pyramid:
                    signal = False

                else:
                    signal = ""
                    
            else:
                signal = ""

        else:
            signal = ""
            
        return signal
    
    def limited_pyramid_signal(self, df, column, current_index, bottom_limit, top_limit):
        """
        Generates a signal based on a pyramid pattern condition within the data column.

        This method checks for a pyramid pattern condition within a specified data column at the given index.
        The condition compares the value at the current index with its adjacent values and specified limits.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column (str): The name of the column for the pyramid pattern comparison.
            current_index (int): The index at which the comparison is made.
            bottom_limit (float): The lower limit for the pyramid pattern condition.
            top_limit (float): The upper limit for the pyramid pattern condition.

        Returns:
            signal: True if the pyramid pattern condition is met within the limits,
                    False if the inverse condition is met within the limits,
                    or an empty string if conditions are not met or values are missing.
        """
        series = df[column]

        current_index_is_higher_than_two = self.check_if_value_is_higher(current_index, 2)

        if current_index_is_higher_than_two:
            
            gamma = series[current_index - 2]
            pyramid = series[current_index - 1]
            beta = series[current_index]

            gamma_is_not_none = self.check_if_value_is_not_none(gamma)
            pyramid_is_not_none = self.check_if_value_is_not_none(pyramid)
            beta_is_not_none = self.check_if_value_is_not_none(beta)
            
            if beta_is_not_none and pyramid_is_not_none and gamma_is_not_none:

                if pyramid < gamma and pyramid < beta and pyramid < bottom_limit:
                    
                    signal = True

                elif pyramid > gamma and pyramid > beta and pyramid > top_limit:
                    signal = False

                else:
                    signal = ""
                    
            else:
                signal = ""

        else:
            signal = ""
            
        return signal
    
    def pyramid_ratio_signal(self, df, column, current_index, ratio = 2):
        """
        Generates a signal based on a pyramid pattern condition within the data column, considering a specified ratio.

        This method checks for a pyramid pattern condition within a specified data column at the given index.
        The condition compares the value at the current index with a straight pyramid and an inverse pyramid value
        computed using a specified ratio.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column (str): The name of the column for the pyramid pattern comparison.
            current_index (int): The index at which the comparison is made.
            ratio (float, optional): The ratio used to compute straight and inverse pyramid values.
                                     Default is 2, meaning straight pyramid is double the current value, and inverse pyramid is half.

        Returns:
            signal: True if the pyramid pattern condition is met, False if the inverse condition is met, or an empty string.
        """
        series = df[column]
        multiplication_factor = (ratio / 100) + 1
        
        current_index_is_higher_than_two = self.check_if_value_is_higher(current_index, 2)

        if current_index_is_higher_than_two:
            
            gamma = series[current_index - 2] 
            pyramid = series[current_index - 1]
            beta = series[current_index]
            
            factor_is_not_none_list = [self.check_if_value_is_not_none(factor) for factor in [gamma, pyramid, beta]]
            
            if False not in factor_is_not_none_list:
            
                if pyramid * multiplication_factor < gamma  and pyramid * multiplication_factor < beta:

                    signal = True

                elif pyramid * multiplication_factor > gamma and pyramid * multiplication_factor > beta:
                    signal = False

                else:
                    signal = ""
            else:
                signal = ""

        else:
            signal = ""
            
        return signal
    
    def limited_pyramid_ratio_signal(self, df, column, current_index, ratio = 7, limit = 20, sign = '<'):
        """
        Generates a signal based on a pyramid pattern condition within the data column, considering a specified ratio.

        This method checks for a pyramid pattern condition within a specified data column at the given index.
        The condition compares the value at the current index with a straight pyramid and an inverse pyramid value
        computed using a specified ratio.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column (str): The name of the column for the pyramid pattern comparison.
            current_index (int): The index at which the comparison is made.
            ratio (float, optional): The ratio used to compute straight and inverse pyramid values.
                                     Default is 2, meaning straight pyramid is double the current value, and inverse pyramid is half.

        Returns:
            signal: True if the pyramid pattern condition is met, False if the inverse condition is met, or an empty string.
        """
        series = df[column]
        multiplication_factor = (ratio / 100) + 1
        
        current_index_is_higher_than_two = self.check_if_value_is_higher(current_index, 2)

        if current_index_is_higher_than_two:
            
            gamma = series[current_index - 2] 
            pyramid = series[current_index - 1]
            beta = series[current_index]
            
            factor_is_not_none_list = [self.check_if_value_is_not_none(factor) for factor in [gamma, pyramid, beta]]
            
            if False not in factor_is_not_none_list:
                
                limit_confirms = eval(f"pyramid {sign} limit")
                
                if pyramid * multiplication_factor < gamma  and pyramid * multiplication_factor < beta and limit_confirms:

                    signal = True

                elif pyramid * multiplication_factor > gamma and pyramid * multiplication_factor > beta and limit_confirms:
                    signal = False

                else:
                    signal = ""
            else:
                signal = ""

        else:
            signal = ""
            
        return signal
    
class Sequentialize():
    """
    A class for creating sequential data sequences from a DataFrame column.

    This class provides methods to extract sequential data sequences from a specified column
    of a DataFrame based on a throwback or expansion approach.

    Args:
        None

    Methods:
        sequentialize_throwback(df, column, throwback_index, current_index):
            Extracts a sequential data sequence using a throwback approach.
            
        sequentialize_expansion(df, column, current_index, expansion_index):
            Extracts a sequential data sequence using an expansion approach.

    Attributes:
        None

    Example:
        sequencer = Sequentialize()
        throwback_sequence = sequencer.sequentialize_throwback(data_frame, 'Column1', 5, 10)
        expansion_sequence = sequencer.sequentialize_expansion(data_frame, 'Column2', 15, 20)
    """
    def sequentialize_throwback(self, df, column, throwback_index, current_index):
        """
        Extracts a sequential data sequence using a throwback approach.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column (str): The name of the column to extract the sequence from.
            throwback_index (int): The starting index for the sequence (inclusive).
            current_index (int): The ending index for the sequence (exclusive).

        Returns:
            sequence: A numpy array containing the extracted sequential data sequence.
        """
        sequence = df[column].iloc[throwback_index:current_index].values.tolist()
        return sequence
    
    def sequentialize_expansion(self, df, column, current_index, expansion_index):
        """
        Extracts a sequential data sequence using an expansion approach.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column (str): The name of the column to extract the sequence from.
            current_index (int): The starting index for the sequence (inclusive).
            expansion_index (int): The ending index for the sequence (exclusive).

        Returns:
            sequence: A numpy array containing the extracted sequential data sequence.
        """
        sequence = df[column].iloc[current_index:expansion_index].values.tolist()
        return sequence
        
    def sequentialize_flattened_values(self, subdf, columns):

        values_lol = []
        for column in columns:
            values_list = subdf[column].values.tolist()
            values_lol = values_lol + values_list

        return values_lol

        
    
