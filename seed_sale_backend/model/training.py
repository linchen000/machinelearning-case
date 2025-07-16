import inspect
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from category_encoders import TargetEncoder
import numpy as np

class Training:
    def __init__(self, X_train, y_train, X_test, y_test, cat_cols, scoring='r2', cv=5, random_state=42):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.cat_cols = cat_cols
        self.scoring = scoring
        self.cv = cv
        self.random_state = random_state

    def tune_model_with_gridsearch(self, model_class, param_grid):
        model_params = {}
        if 'random_state' in inspect.signature(model_class).parameters:
            model_params['random_state'] = self.random_state

        model_instance = model_class(**model_params)

        preprocessor = ColumnTransformer(transformers=[
            ('target_enc', TargetEncoder(cols=self.cat_cols['cat_cols_target']), self.cat_cols['cat_cols_target']),
            ('ordinal_enc', OrdinalEncoder(), self.cat_cols['cat_cols_ordinal'])
        ])

        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', model_instance)
        ])
        
        grid_search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(self.X_train, self.y_train)

        # Best model
        best_model = grid_search.best_estimator_

        y_pred = best_model.predict(self.X_test)
        test_r2 = r2_score(self.y_test, y_pred)
        test_rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))

        print("Best Parameters:", grid_search.best_params_)
        print("Best CV R² Score:", grid_search.best_score_)
        print("Test R² Score:", test_r2)
        print("Test RMSE:", test_rmse)

        return {
            "model_class": model_class,
            "best_model": best_model,
            "best_params": grid_search.best_params_,
            "cv_score": grid_search.best_score_,
            "test_r2": test_r2,
            "test_rmse": test_rmse
        }

    def tune_multiple_models_with_gridsearch(self, model_param_list):
        results = []

        for model_class, param_grid in model_param_list:
            result = self.tune_model_with_gridsearch(model_class, param_grid)
            results.append(result)

        best_result = max(results, key=lambda x: x['cv_score'])
        print("=== Best Overall Model ===")
        print(f"Model: {best_result['model_class'].__name__}")
        print(f"Best CV R² Score: {best_result['cv_score']}")
        print(f"Test R² Score: {best_result['test_r2']}")
        print(f"Test RMSE: {best_result['test_rmse']}")

        return best_result