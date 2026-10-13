from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import Dict, Any

app = FastAPI(title="CardioVision ML Engine")

# Load models and preprocessing artifacts
models = {}
for target in ['Cath', 'LAD', 'LCX', 'RCA']:
    try:
        models[target] = joblib.load(f'model_{target}.pkl')
    except:
        print(f"Warning: model_{target}.pkl not found.")

imputer = joblib.load('imputer.pkl')
feature_names = joblib.load('feature_names.pkl')
global_feature_importances = joblib.load('feature_importances.pkl')

class PatientPayload(BaseModel):
    features: Dict[str, Any]

@app.post("/predict")
def predict(payload: PatientPayload):
    input_data = payload.features
    df_input = pd.DataFrame([input_data])
    
    # Fill any missing columns with 0
    for col in feature_names:
        if col not in df_input.columns:
            df_input[col] = 0
            
    df_input = df_input[feature_names]
    
    # Transform
    X_processed = imputer.transform(df_input)
    
    predictions = {}
    
    # Helper for mapping internal names to UI names
    name_map = {'Cath': 'CAD', 'LAD': 'LAD', 'LCX': 'LCX', 'RCA': 'RCA'}
    
    for key, model in models.items():
        ui_key = name_map[key]
        pred_class = int(model.predict(X_processed)[0])
        probabilities = model.predict_proba(X_processed)[0]
        risk_score = float(probabilities[1]) if len(probabilities) > 1 else float(pred_class)
        
        status = "HIGH_RISK" if risk_score >= 0.5 else "LOW_RISK"
        color = "#FF3333" if risk_score >= 0.5 else "#33FF77"
        
        predictions[ui_key] = {
            "status": status,
            "probability": round(risk_score * 100, 2),
            "color": color,
            "topRiskFactors": global_feature_importances.get(key, {})
        }
        
    return {
        "status": "success",
        "overallCAD": predictions['CAD'],
        "arteries": {
            "LAD": predictions['LAD'],
            "LCX": predictions['LCX'],
            "RCA": predictions['RCA']
        }
    }