from statsmodels.tsa.stattools import grangercausalitytests

class Causality():
    
    def pearson_correlation_coefficient(self, df):
        coefficient = df.corr().iloc[:,0][1]
        return coefficient
    
    def granger_causality_score(self, df, lag):
        granger_results_dict = grangercausalitytests(df, [lag], verbose=False)
        granger_results_dict = granger_results_dict[lag][0]
        granger_results_list = [granger_results_dict[test][0] for test in granger_results_dict.keys()]
        return granger_results_list