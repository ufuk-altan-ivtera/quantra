import numpy as np


class MonteCarlo():
    
    def __init__(self, stocks_df):
        
        self.stocks_df = stocks_df
    
    def apply_logaritmic_transformation(self):
        log_return = np.log(self.stocks_df / self.stocks_df.shift(1))
        return log_return
    
    def calculate_sharpe_ratio(self, index, all_weights, log_return, return_arr, volatility_array, sharpe_ratio_array):
        
        shape = self.stocks_df.shape[0]
        stock_count = self.stocks_df.shape[1]
        
        # Weights
        weights = np.array(np.random.random(stock_count))
        weights = weights / np.sum(weights)

        # Save Weights
        all_weights[index, :] = weights

        # Expected Return
        return_arr[index] = np.sum( (log_return.mean() * weights) * shape)

        # Expected Volatility
        volatility_array[index] = np.sqrt(np.dot(weights.T, np.dot( log_return.cov() * shape, weights)))

        # Sharpe Ratio
        sharpe_ratio_array[index] = return_arr[index] / volatility_array[index]
        
        return index, all_weights, return_arr, volatility_array, sharpe_ratio_array
    
    def obtain_sharpe_ratio_array(self):

        log_return = self.apply_logaritmic_transformation()
        
        np.random.seed(101)
        
        number_of_portfolios = 5000
        all_weights = np.zeros((number_of_portfolios, len(self.stocks_df.columns)))
        return_arr = np.zeros(number_of_portfolios)
        volatility_array = np.zeros(number_of_portfolios)
        sharpe_ratio_array = np.zeros(number_of_portfolios)
        
        for index in range(number_of_portfolios):
        
            index, all_weights, return_arr, volatility_array, sharpe_ratio_array = self.calculate_sharpe_ratio(index, all_weights, log_return, return_arr, volatility_array, sharpe_ratio_array)
            
        optimized_portfolio_values = all_weights[sharpe_ratio_array.argmax(), :].tolist()
            
        return optimized_portfolio_values

