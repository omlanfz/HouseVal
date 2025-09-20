# retrain_model.py
import pandas as pd
import numpy as np
import pickle
import json
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

def retrain_and_save():
    print("Loading and preprocessing data...")
    
    # 1. LOAD THE DATASET
    df1 = pd.read_csv("property_listing_data_in_Bangladesh.csv")
    
    # 2. DATA CLEANING - Remove missing values
    df2 = df1.dropna()
    
    # 3. FEATURE ENGINEERING - Standardize beds and bath
    df2['beds_standardized'] = df2['beds'].apply(lambda x: int(x.split(' ')[0]))
    df2['bath_standardized'] = df2['bath'].apply(lambda x: int(x.split(' ')[0]))
    df2 = df2.drop(['beds', 'bath'], axis=1)
    
    # 4. CONVERT AREA AND PRICE TO NUMERIC
    def convert_sqft_to_num(x):
        x = ''.join(c for c in x if c.isdigit() or c == '-')
        tokens = x.split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        try:
            return float(x)
        except:
            return None
    
    def convert_price_to_float(price):
        tokens = price.replace(',', '').split()
        if 'Thousand' in tokens:
            return float(tokens[0]) * 1000
        elif 'Lakh' in tokens:
            return float(tokens[0]) * 100000
        else:
            return None
    
    df3 = df2.copy()
    df3.area = df3.area.apply(convert_sqft_to_num)
    df3 = df3[df3.area.notnull()]
    df3.price = df3.price.apply(convert_price_to_float)
    df3 = df3[df3.price.notnull()]
    
    # 5. ADD PRICE PER SQFT
    df4 = df3.copy()
    df4['price_per_sqft'] = df4['price']/df4['area']
    
    # 6. DROP UNNECESSARY COLUMNS
    df5 = df4.drop(['title','type','purpose','flooPlan','url','lastUpdated'], axis='columns')
    
    # 7. PROCESS ADDRESS COLUMN
    df5.address = df5.address.apply(lambda x: x.strip())
    address_stats = df5['address'].value_counts(ascending=False)
    address_stats_less_than_10 = address_stats[address_stats <= 10]
    df5.address = df5.address.apply(lambda x: 'other' if x in address_stats_less_than_10 else x)
    
    # 8. REMOVE UNREALISTIC BED/BATH VALUES
    def remove_unrealistic_bed_bath(df, max_bedrooms=8, max_baths=6):
        df['beds_standardized'] = pd.to_numeric(df['beds_standardized'], errors='coerce')
        df['bath_standardized'] = pd.to_numeric(df['bath_standardized'], errors='coerce')
        df = df[(df['beds_standardized'] <= max_bedrooms) & (df['bath_standardized'] <= max_baths)]
        return df
    
    df6 = remove_unrealistic_bed_bath(df5)
    
    # 9. REMOVE AREA OUTLIERS
    df7 = df6[(df6.area / df6.beds_standardized <= 736.67) & (df6.area / df6.beds_standardized >= 176.67)]
    
    # 10. REMOVE PRICE PER SQFT OUTLIERS
    def remove_pps_outliers(df):
        df_out = pd.DataFrame()
        for key, subdf in df.groupby('address'):
            m = np.mean(subdf.price_per_sqft)
            st = np.std(subdf.price_per_sqft)
            reduced_df = subdf[(subdf.price_per_sqft > (m-st)) & (subdf.price_per_sqft <= (m+st))]
            df_out = pd.concat([df_out, reduced_df], ignore_index=True)
        return df_out
    
    df8 = remove_pps_outliers(df7)
    
    # 11. ONE-HOT ENCODING FOR ADDRESS
    dummies = pd.get_dummies(df8.address, dtype=int)
    df9 = pd.concat([df8, dummies.drop('other', axis='columns')], axis='columns')
    df10 = df9.drop('address', axis='columns')
    
    # 12. PREPARE FINAL DATASET
    df11 = df10.drop(['price_per_sqft'], axis='columns')  # Drop price_per_sqft as it was used for outlier removal
    
    X = df11.drop(['price'], axis='columns')
    y = df11.price
    
    print(f"Final dataset shape: {X.shape}")
    
    # 13. TRAIN THE GRADIENT BOOSTING MODEL
    print("Training Gradient Boosting model...")
    gb_model = GradientBoostingRegressor(random_state=42, n_estimators=100)
    gb_model.fit(X, y)
    print("Model trained successfully!")
    
    # 14. SAVE THE NEW MODEL
    with open('./artifacts/house_prices_model.pickle', 'wb') as f:
        pickle.dump(gb_model, f)
    print("New model saved to './artifacts/house_prices_model.pickle'")
    
    # 15. SAVE COLUMN INFORMATION
    columns = {
        'data_columns': [col for col in X.columns]
    }
    with open("./artifacts/columns.json", "w") as f:
        f.write(json.dumps(columns))
    print("Column information saved to './artifacts/columns.json'")
    
    # 16. TEST THE MODEL
    print("\nTesting the model with sample prediction...")
    
    def predict_price(address, area, beds_standardized, bath_standardized):    
        address_index = np.where(X.columns == address)[0][0]
        x = np.zeros(len(X.columns))
        x[0] = area
        x[1] = beds_standardized
        x[2] = bath_standardized
        if address_index >= 0:
            x[address_index] = 1
        return gb_model.predict([x])[0]
    
    # Test prediction
    sample_prediction = predict_price('Block A, Bashundhara R-A, Dhaka', 2200, 3, 4)
    print(f"Sample prediction for 'Block A, Bashundhara R-A, Dhaka', 2200 sqft, 3 beds, 4 baths: {sample_prediction:,.2f} BDT")

if __name__ == '__main__':
    retrain_and_save()