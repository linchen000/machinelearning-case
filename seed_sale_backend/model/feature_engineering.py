class FeatureEngineering:
    def __init__(self):
        pass
    
    def feature_engineering(self, df):
        # Date-based features
        if 'SALESYEAR' in df.columns and 'RELEASE_YEAR' in df.columns:
            df['PRODUCT_AGE'] = df['SALESYEAR'] - df['RELEASE_YEAR']

        if 'PLANT_HEIGHT' in df.columns:
            df['PLANT_HEIGHT_SQ'] = df['PLANT_HEIGHT'] ** 2
            df['PLANT_HEIGHT_CUBE'] = df['PLANT_HEIGHT'] ** 3

    
        if 'PRODUCT' in df.columns and 'STATE' in df.columns:
            df['PRODUCT_STATE'] = df['PRODUCT'].astype(str) + "_" + df['STATE'].astype(str)
        
        df['STATE_AVG_PLANT_HEIGHT'] = df.groupby('STATE')['PLANT_HEIGHT'].transform('mean')
        df['STATE_AVG_REL_MAT'] = df.groupby('STATE')['RELATIVE_MATURITY'].transform('mean')
        
        df["STRUCTURAL_SCORE"] = (df["BRITTLE_STALK"] + df["PLANT_HEIGHT"]) / 2

  
        df["DEFENSIVE_INDEX"] = (
            df["DISEASE_RESISTANCE"] + df["INSECT_RESISTANCE"] + df["PROTECTION"]
        )
        df["STRESS_INDEX"] = df["DROUGHT_TOLERANCE"] + (6 - df["BRITTLE_STALK"])  # inverse brittle stalk
        df["PRODUCT_DEFENSE_SCORE"] = df["PRODUCT"].astype(str) + "_DEF_" + df["DEFENSIVE_INDEX"].astype(str)
     
     
        df["MATURITY_TO_HEIGHT_RATIO"] = df["RELATIVE_MATURITY"] / df["PLANT_HEIGHT"]
        df["STALK_STRENGTH_TO_HEIGHT"] = df["BRITTLE_STALK"] / df["PLANT_HEIGHT"]

        df["STATE_DEFENSE_SCORE"] = df["STATE"].astype(str) + "_DEF_" + df["DEFENSIVE_INDEX"].astype(str)

        df.drop(columns=['SALESYEAR', 'RELEASEYEAR'], inplace=True, errors='ignore')
        return df
