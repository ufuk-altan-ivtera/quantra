import os
import pickle

class SaveFile():
    
    def __init__(self):
    
        self.path = os.getcwd() + '/FinancialReports/'
    
    def save_file(self, file_path, dataframe):
        """
        Save dataframe into a parquet file. xxx
        """
        dataframe.to_parquet(file_path)
        print('SAVED')
        
    def save_pickle_file(self, filename, python_object):
        """
        Save any python object as a pickle file. For example, a dictionary or a list.
        
        Parameters
        ----------
        filename: str
            File name of the pickle file
            
        python_object: dict, list, etc.
            Object to be saved
        """
        with open(f'{filename}', 'wb') as file:
            pickle.dump(python_object, file, protocol=pickle.HIGHEST_PROTOCOL)
            
        print('SAVED')
            
class LoadFile():
    
    def load_pickle_file(self, file_path):
        
        with open(file_path, 'rb') as file:
            pickle_file = pickle.load(file)
            
        return pickle_file