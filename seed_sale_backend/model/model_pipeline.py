from data_sourcing import DataSourcing
from data_preprocessing import DataPreprocessing
from feature_engineering import FeatureEngineering
from get_best_model import GetBestModel


class ModelPipeline:
    def __init__(self):
        self.best_model = None

    def fit(self):
        df = DataSourcing().read_data_local()
        print("Data sourced successfully.")
        print("=" * 50)
       
        df = DataPreprocessing(df).preprocessing_fit()
        print("Data preprocessing completed.")
        print("=" * 50)
    
        # df = remove_lifecycle_violations(df)  # Assuming remove_lifecycle is defined elsewhere
        df = FeatureEngineering().feature_engineering(df)
        print("Feature engineering completed.")
        print("=" * 50)
    
        self.best_model = GetBestModel(df).get_best_model()
        print("Best model training completed.")
        print("=" * 50)
    
        return self.best_model
    
    def score(self):
        df_test = DataSourcing(file_path='synthetic_test_data.csv').read_data_local()
        print("Data sourcing for evaluation completed.")
        print("=" * 50)
    
        df_test = DataPreprocessing(df_test).preprocessing_score()   
        print("Data preprocessing for evaluation completed.")
        print("=" * 50)
    
        df_test = FeatureEngineering().feature_engineering(df_test)
        print("Feature engineering completed.")
        print("=" * 50)
    
        df_test = df_test[self.best_model.feature_names_in_]
        pred = self.best_model.predict(df_test)
        print("Prediction:", pred)
        print("Prediction completed.")
        return pred