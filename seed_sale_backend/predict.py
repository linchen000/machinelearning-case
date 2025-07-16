
from model.data_sourcing import DataSourcing
from model.data_preprocessing import DataPreprocessing
from model.feature_engineering import FeatureEngineering
import joblib

def load_model(filename='best_model.pkl'):

    loaded_model = joblib.load(filename)
    return loaded_model


def pred(df_test, model=None):
    if model is None:
        model = load_model()

    # Read test data
    # df_test = DataSourcing(file_path='synthetic_test_data.csv').read_data_local()
    # print("Data sourcing for evaluation completed.")

    df_test = DataPreprocessing(df_test).preprocessing_score()   
    print("Data preprocessing for evaluation completed.")

    df_test = FeatureEngineering().feature_engineering(df_test)
    print("Feature engineering completed.")

    df_test = df_test[model.feature_names_in_]
    # Use the model to predict
    predictions = model.predict(df_test)  # X_new is your input features as a DataFrame or ndarray
    return predictions