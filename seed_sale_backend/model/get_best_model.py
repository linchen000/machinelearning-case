from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from training import Training
from simple_nn_regressor import SimpleNNRegressor


class GetBestModel:
    def __init__(self, df):
        self.df = df
    
    def train_test_split_data(self, target_col='UNITS', test_size=0.2, random_state=42):
        X = self.df.drop(columns=[target_col])
        y = self.df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        return X_train, X_test, y_train, y_test

    def get_encoding_col(self):
        cat_cols = self.df.select_dtypes(include=["object", "category"]).columns.tolist()

        # cat_cols += ['RELEASE_YEAR', 'SALESYEAR']
        
        cat_cols_ordinal = ['LIFECYCLE']
        cat_cols_target = [col for col in cat_cols if col not in cat_cols_ordinal]
        cat_cols = {
            'cat_cols_target': cat_cols_target,
            'cat_cols_ordinal': cat_cols_ordinal
        }

        return cat_cols

    def get_best_model(self):
        model_param_list = [
            (RandomForestRegressor, {
                'model__n_estimators': [100, 200, 300],         
                'model__max_depth': [None, 10, 20, 30],         
                'model__min_samples_split': [2, 5, 10],          
                'model__min_samples_leaf': [1, 2, 4],            
            }),
            (GradientBoostingRegressor, {
                'model__n_estimators': [100, 200],
                'model__learning_rate': [0.05, 0.1],
            }),
            (Lasso, {
                'model__alpha': [0.01, 0.1, 1.0],
            }),
            (Ridge, {
                'model__alpha': [0.01, 0.1, 1.0],
            }),
            (SimpleNNRegressor, {
                'model__hidden_dim': [32, 64],
                'model__lr': [0.01, 0.001],
                'model__epochs': [10],  # Reduce for tuning speed
                'model__batch_size': [32]
            })
        ]

        cat_cols = self.get_encoding_col()
       
        X_train, X_test, y_train, y_test = self.train_test_split_data()

        training = Training(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            cat_cols=cat_cols
        )

        best_result = training.tune_multiple_models_with_gridsearch(
            model_param_list=model_param_list
        )
        return best_result['best_model']