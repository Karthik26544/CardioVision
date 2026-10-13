import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
import joblib

print("Starting Model Training for CardioVision...")

# 1. Load Excel Dataset
try:
    df = pd.read_excel('Z-Alizadeh_Sani.xlsx') 
except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit()

# Clean column names (strip whitespace)
df.columns = df.columns.str.strip()

print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")

# Target columns
target_cols = ['Cath', 'LAD', 'LCX', 'RCA']

# 2. Automatically Convert ALL text/string columns into numeric values
label_encoders = {}
for col in df.columns:
    # If the column is not already numeric (int or float)
    if not pd.api.types.is_numeric_dtype(df[col]):
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le
        print(f"Encoded text column: {col}")

# Save label encoders for later use
joblib.dump(label_encoders, 'label_encoders.pkl')

# 3. Separate Features (Input) and Targets
# CRITICAL RULE: Drop Cath, LAD, LCX, RCA to prevent Target Leakage!
X = df.drop(columns=[col for col in target_cols if col in df.columns])
targets = df[[col for col in target_cols if col in df.columns]]

# Encode targets if they contain text (e.g., 'Normal'/'Stenosis' or 'Cad'/'Normal')
for target in targets.columns:
    if not pd.api.types.is_numeric_dtype(targets[target]):
        le = LabelEncoder()
        targets[target] = le.fit_transform(targets[target].astype(str))

# Save feature names order
feature_names = list(X.columns)
joblib.dump(feature_names, 'feature_names.pkl')

# Preprocess missing values
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)
joblib.dump(imputer, 'imputer.pkl')

# 4. Train 4 Random Forest Models
trained_models = {}
feature_importances = {}

for target in targets.columns:
    print(f"Training Classifier for: {target}...")
    y = targets[target]
    
    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Calculate Feature Importances for Clinical Interpretability
    importances = clf.feature_importances_
    top_indices = np.argsort(importances)[::-1][:5] # Top 5 factors
    top_factors = {feature_names[i]: float(importances[i]) for i in top_indices}
    
    # Save Model & Importances
    joblib.dump(clf, f'model_{target}.pkl')
    feature_importances[target] = top_factors
    
    print(f"✅ Saved model_{target}.pkl | Top Feature: {list(top_factors.keys())[0]}")

joblib.dump(feature_importances, 'feature_importances.pkl')
print("\n🎉 Training Pipeline Complete! All 4 models trained successfully.")