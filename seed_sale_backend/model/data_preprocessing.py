import pandas as pd


class DataPreprocessing:
    def __init__(self, df):
        self.df = df

    def handle_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    def handle_missing_val(self):
        missing_values = self.df.isnull().sum()

        rows_before_drop = self.df.shape[0]
        self.df.dropna(inplace=True)

        print((1 - self.df.shape[0] / rows_before_drop) * 100)

    def handle_aggregations(self):
        target_col = 'UNITS'
        cols = [col for col in self.df.columns if col != target_col]
        self.df = self.df.groupby(cols)[target_col].sum().reset_index()

    def handle_outlier(self):
        Q1 = self.df['UNITS'].quantile(0.25)
        Q3 = self.df['UNITS'].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        self.df = self.df[(self.df['UNITS'] >= lower_bound) & (self.df['UNITS'] <= upper_bound)]

    def remove_lifecycle_violations(self):
        lifecycle_order = ['INTRODUCTION', 'ESTABLISHED', 'EXPANSION', 'PHASEOUT']
        self.df['LIFECYCLE'] = pd.Categorical(self.df['LIFECYCLE'], categories=lifecycle_order, ordered=True)

        self.df = self.df.sort_values(by=['PRODUCT', 'SALESYEAR']).reset_index(drop=True)

        def drop_lifecycle_violations(group):
            max_code = -1
            mask = []
            for lc in group['LIFECYCLE'].cat.codes:
                if lc < max_code:
                    mask.append(False)  # invalid
                else:
                    max_code = max(max_code, lc)
                    mask.append(True)   # valid
            return group[mask]

        self.df = self.df.groupby(['PRODUCT'], group_keys=False).apply(drop_lifecycle_violations)

        self.df = self.df.sort_values(by=['PRODUCT', 'SALESYEAR', 'LIFECYCLE']).reset_index(drop=True)
        
    def preprocessing_fit(self):
        print("df shape before preprocessing", self.df.shape)
        self.handle_duplicates()
        self.handle_missing_val()
        self.handle_aggregations()
        self.handle_outlier()
        # self.remove_lifecycle_violations()
        print("df shape after preprocessing", self.df.shape)
        return self.df

    def preprocessing_score(self):
        self.handle_missing_val()
        return self.df