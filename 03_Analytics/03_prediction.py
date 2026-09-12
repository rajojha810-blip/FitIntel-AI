import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import sys
import os

# Root path resolution
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_path not in sys.path:
    sys.path.append(base_path)

from progress_analytics import get_daily_metrics

def predict_future_weight(days_to_predict=30):
    df = get_daily_metrics()
    
    # Feature Engineering (Days from start)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['day_index'] = (df['date'] - df['date'].min()).dt.days

    X = df[['day_index']]
    y = df['weight_kg']

    # Train Linear Regression Model
    model = LinearRegression()
    model.fit(X, y)

    # Future Days Prediction
    last_day = df['day_index'].max()
    future_days = np.array([last_day + i for i in range(1, days_to_predict + 1)]).reshape(-1, 1)
    predicted_weights = model.predict(future_days)

    # Future Dates Generation
    last_date = df['date'].max()
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, days_to_predict + 1)]

    # Combine Actual & Predicted into clean DataFrame
    df_actual = df[['date', 'weight_kg']].copy()
    df_actual['Type'] = 'Actual'

    df_future = pd.DataFrame({
        'date': future_dates,
        'weight_kg': np.round(predicted_weights, 2),
        'Type': 'Predicted'
    })

    combined_df = pd.concat([df_actual, df_future], ignore_index=True)
    
    target_pred_weight = round(predicted_weights[-1], 2)
    current_w = round(df['weight_kg'].iloc[-1], 2)
    diff = round(target_pred_weight - current_w, 2)

    return combined_df, current_w, target_pred_weight, diff