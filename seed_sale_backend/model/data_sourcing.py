import pandas as pd


class DataSourcing:
    def __init__(self, file_path='case_study_data.csv'):
        self.file_path = file_path

    def read_data_local(self):
        df = pd.read_csv(self.file_path)
        return df

    # Customized read_data method to read from a different source