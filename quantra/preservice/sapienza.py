from ..utils.servant import Check
from ..utils.operate import Calculate

from ..fundamental.financials import ObtainFinancials, CalculateFinancials
from ..fundamental.vocabulary  import financial_statements_vocabulary_dict

import pandas as pd

# Different ways of calculating CurrentRatio !!
# Some values are negative some are positive in the same criterion

class Phase1(ObtainFinancials, CalculateFinancials):
    
    def __init__(self):
        self.financial_columns_list = ['Ticker', 'Date', 'Period', # main_list
                          'Name', 'Currency', 'Industry', 'Sector', # info_list
                          
                          'CurrentRatio', 'Debt2EquityRatio', 'QuickRatio', 'GrossProfitMargin', # Phase1
                          'OperatingProfitMargin', 'NetProfitMargin', 'ProfitRatio', 'DepreciationRatio', 
                          'DebtRatio', 'AssetDebtRatio', 'DebtProfitRatio', 'LiabilityEquityRatio', 
                          'SplitRatio', 'ProfitEquityRatio', 
                          
                          'InvestingCashFlow', 'FinancingCashFlow', 'OperatingCashFlow', 'FreeCashFlow', # Phase2
                          'TotalEquity', 'GrossProfit', 'NetIncome', 'TotalRevenue',
                          
                          0, 3, 5, 7, 10, 15, 30 , 45, 60, 85 # Phase3
                                        ]
    
    def establish_financials(self, financial_statements_df, column):
        
        # ObtainFinancials
        total_current_assets = self.obtain_single_financial_statement(financial_statements_df, column, 'TotalAssets')
        
        total_liability_list = financial_statements_vocabulary_dict['TotalLiability']
        total_current_liabilities = self.obtain_financial_statements_summation(financial_statements_df, column, total_liability_list)
        
        total_stockholder_equity = self.obtain_single_financial_statement(financial_statements_df, column, 'StockholdersEquity')
        
        inventory = self.obtain_single_financial_statement(financial_statements_df, column, 'Inventory')
        
        total_revenue = self.obtain_single_financial_statement(financial_statements_df, column, 'TotalRevenue')
        
        cost_of_revenue = self.obtain_single_financial_statement(financial_statements_df, column, 'CostOfRevenue')
        
        operating_income = self.obtain_single_financial_statement(financial_statements_df, column, 'OperatingIncome')
        
        net_income = self.obtain_single_financial_statement(financial_statements_df, column, 'NetIncome')

        capital_expenditures = self.obtain_single_financial_statement(financial_statements_df, column, 'CapitalExpenditure')

        cash_flow_from_investing_activities = self.obtain_single_financial_statement(financial_statements_df, column, 'InvestingCashFlow')
        cash_flow_from_financing_activities = self.obtain_single_financial_statement(financial_statements_df, column, 'FinancingCashFlow')
        cash_flow_from_operating_activities = self.obtain_single_financial_statement(financial_statements_df, column, 'OperatingCashFlow')

        gross_profit = self.obtain_single_financial_statement(financial_statements_df, column, 'GrossProfit')
        depreciation = self.obtain_single_financial_statement(financial_statements_df, column, 'DepreciationAndAmortization')

        short_term_debt = self.obtain_single_financial_statement(financial_statements_df, column, 'NetShortTermDebtIssuance')
        long_term_debt = self.obtain_single_financial_statement(financial_statements_df, column, 'NetLongTermDebtIssuance')
        
        share_issued = self.obtain_single_financial_statement(financial_statements_df, column, 'ShareIssued')
        
        # CalculateFinancials
        TotalEquity = self.calculate_difference(total_current_assets, total_current_liabilities)

        CurrentRatio = self.calculate_ratio(total_current_assets, total_current_liabilities)
        
        Debt2EquityRatio = self.calculate_ratio(total_current_liabilities, total_stockholder_equity)
        
        difference1 = self.calculate_difference(total_current_assets, inventory) 
        QuickRatio = self.calculate_ratio(difference1, total_current_liabilities)
        
        difference2 = self.calculate_difference(total_revenue, cost_of_revenue) 
        GrossProfitMargin = self.calculate_ratio(difference2, total_revenue)
        
        CostRevenueRatio = self.calculate_ratio(cost_of_revenue, total_revenue)
        
        OperatingProfitMargin = self.calculate_ratio(operating_income, total_revenue) 
        
        NetProfitMargin = self.calculate_ratio(net_income, total_revenue)

        InvestingCashFlow = cash_flow_from_investing_activities
        FinancingCashFlow = cash_flow_from_financing_activities
        OperatingCashFlow = cash_flow_from_operating_activities

        FreeCashFlow = self.calculate_difference(OperatingCashFlow, capital_expenditures)
        
        ProfitRatio = self.calculate_ratio(gross_profit, total_revenue) * 100 # 1

        DepreciationRatio = self.calculate_ratio(depreciation, gross_profit) * 100 # 4
        
        DebtRatio = self.calculate_ratio(short_term_debt, long_term_debt) # 15
        
        AssetDebtRatio = self.calculate_ratio(total_current_assets, short_term_debt) # 16
        
        DebtProfitRatio = self.calculate_ratio(long_term_debt, gross_profit) # 17
        
        LiabilityEquityRatio = self.calculate_ratio(total_current_liabilities, TotalEquity) 
        
        SplitRatio = self.calculate_ratio(net_income, share_issued)
        
        ProfitEquityRatio = self.calculate_ratio(net_income, TotalEquity)
        
        # ReturnFinancials
        financials_list = [CurrentRatio, Debt2EquityRatio, QuickRatio, GrossProfitMargin, 
                           OperatingProfitMargin, NetProfitMargin,  ProfitRatio, DepreciationRatio, 
                           DebtRatio, AssetDebtRatio, DebtProfitRatio, LiabilityEquityRatio, 
                           SplitRatio, ProfitEquityRatio, 
                           
                           InvestingCashFlow, FinancingCashFlow, OperatingCashFlow, FreeCashFlow,
                           TotalEquity, gross_profit, net_income, total_revenue]
        
        return financials_list
    
    def establish_phase1(self, financial_statements_dict, price_df_dict, info_dict, days = [0, 3, 5, 7, 10, 15, 30 , 45, 60, 85], period = 'annually'):
        financials_lol = []
        
        tickers = financial_statements_dict.keys()
        
        for ticker in tickers:
        
            dates = financial_statements_dict[ticker][period].columns
            
            for date in dates:
            
                # Obtain Info
                info = info_dict[ticker]
                info_list = self.obtain_info(info)

                # Obtain Price
                price_df = price_df_dict[ticker]

                future_price_list = [self.obtain_future_price(price_df, date, day = day) for day in days]

                # Obtain Financial Statements
                financial_statements_df = financial_statements_dict[ticker][period]

                # Obtain Analysis
                financials_list = self.establish_financials(financial_statements_df, date)

                main_list = [ticker, date, period]
                assembled_list = main_list + info_list + financials_list + future_price_list
                financials_lol.append(assembled_list)
        
        financials_df = pd.DataFrame(financials_lol, columns= self.financial_columns_list)
        
        return financials_df
    
# Apply Logging

class Phase2(Calculate, Check):
    
    def __init__(self):
        
        self.phase2_columns = ['Ticker', 'Date', 'TotalEquity','InvestingCashFlow', 
                              'FinancingCashFlow', 'OperatingCashFlow', 'FreeCashFlow',
                              'GrossProfit', 'NetIncome', 'TotalRevenue']
    
    def establish_percentage_difference_calculation(self, current_value, next_value):
        
        if (next_value != 0 or current_value != 0) and current_value != 0 and next_value != 0 :
                    
            percentage_difference = self.calculate_percentage_difference(current_value, next_value)
            if next_value > current_value:
                percentage_difference = percentage_difference * -1
                
        elif (next_value != 0 and current_value == 0) or (current_value != 0 and next_value == 0):
            percentage_difference = 0

        else:
            percentage_difference = 0
            
        return percentage_difference

    def establish_percentage_difference_list(self, phase2_single_ticker, column):

        percentage_difference_list = []
        for current_index, current_value in enumerate(phase2_single_ticker[column]):

            next_index = current_index + 1
            index_is_not_out_of_range = self.check_if_index_is_not_out_of_range(next_index, phase2_single_ticker[column])

            if index_is_not_out_of_range:

                next_value = phase2_single_ticker[column].iloc[next_index]

                percentage_difference = self.establish_percentage_difference_calculation(current_value, next_value)

            else:
                percentage_difference = 0

            percentage_difference_list.append(percentage_difference)
            
        return percentage_difference_list
    
    def establish_percentage_difference_lol(self, phase2, ticker):
        
        phase2_single_ticker = phase2[phase2['Ticker'] == ticker].sort_values('Date', ascending=False)
        phase2_single_ticker_numeric_data = phase2_single_ticker.iloc[:, 2:]
        
        tickers_list = phase2_single_ticker['Ticker'].values
        date_list = phase2_single_ticker['Date'].values
        
        percentage_difference_lol = [tickers_list, date_list]
        
        for column in phase2_single_ticker_numeric_data.columns:

            percentage_difference_list = self.establish_percentage_difference_list(phase2_single_ticker_numeric_data, column)

            percentage_difference_lol.append(percentage_difference_list)
        
        return percentage_difference_lol
    
    def establish_single_ticker_percentage_change_df(self, phase2, ticker):
        
        percentage_difference_lol = self.establish_percentage_difference_lol(phase2, ticker)

        single_ticker_percentage_change_df = pd.DataFrame(percentage_difference_lol).transpose()
        single_ticker_percentage_change_df.columns = self.phase2_columns
        
        return single_ticker_percentage_change_df
    
    def establish_phase2(self, phase2):
        
        phase2_percentage_change_df = pd.DataFrame()
        
        for ticker in phase2['Ticker'].unique():
            single_ticker_percentage_change_df = self.establish_single_ticker_percentage_change_df(phase2, ticker)
            phase2_percentage_change_df = pd.concat([phase2_percentage_change_df, single_ticker_percentage_change_df])

        return phase2_percentage_change_df
            
class Sapienza(Phase1, Phase2):
    
    def __init__(self):
        
        self.phase2_columns = ['Ticker', 'Date',
                               'InvestingCashFlow', 'FinancingCashFlow', 'OperatingCashFlow', 'FreeCashFlow', # Phase2
                               'TotalEquity', 'GrossProfit', 'NetIncome', 'TotalRevenue',]
        
    def phase1(self, financial_statements_dict, price_df_dict, info_dict):
        
        financials_df = self.establish_phase1(financial_statements_dict, price_df_dict, info_dict)
        return financials_df
    
    def phase2(self, financials_df):
        
        phase2_df = financials_df[self.phase2_columns]
        phase2_percentage_change_df = self.establish_phase2(phase2_df)
        
        return phase2_percentage_change_df
    
    def sapienza(self, tickers):
        
        financials_df = self.phase1(tickers)
        phase2_percentage_change_df = self.phase2(financials_df)
        
        financials_df = financials_df.drop([self.phase2_columns], axis = 1)
        
        return {'phase2_df': phase2_percentage_change_df.values.tolist(), 'financials_df': financials_df.values.tolist()}
        
        
    

            
    
    

