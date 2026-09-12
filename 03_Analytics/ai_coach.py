import os
import sys
import requests
import streamlit as st
from dotenv import load_dotenv

# 1. Environment variables load karein
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# .env se API key auto-fetch karein
ENV_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Dynamic Path Setup
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_path not in sys.path:
    sys.path.append(base_path)

# Same folder module import fix
try:
    from progress_analytics import get_daily_metrics
except ImportError:
    from .progress_analytics import get_daily_metrics

# 3. AI Response Generator Function
def generate_ai_response(user_prompt, api_key=None):
    active_key = api_key if api_key else ENV_API_KEY

    if not active_key:
        return "⚠️ Gemini API Key missing! Please add GEMINI_API_KEY in your .env file."

    try:
        df = get_daily_metrics()
        
        if df is None or df.empty:
            return "⚠️ No health data found in the database. Please log some data first."
            
        latest = df.iloc[-1]
        
        system_context = f"""
        You are FitIntel AI — an expert AI Health & Fitness Coach.
        The user's latest logged health metrics are:
        - Date: {latest.get('date', 'N/A')}
        - Weight: {latest.get('weight_kg', 'N/A')} kg
        - Daily Calories Consumed: {latest.get('calories_consumed', 'N/A')} kcal
        - Daily Protein Intake: {latest.get('protein_consumed_g', 'N/A')} g
        - Steps Count: {latest.get('steps', 'N/A')}

        Give precise, actionable fitness and diet advice.
        """

        # Exact model endpoint required by Google API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={active_key}"
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_context}\n\nUser Question: {user_prompt}"}]
            }]
        }

        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()

        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ API Error: {res_json.get('error', {}).get('message', 'Unknown Error')}"

    except Exception as e:
        return f"❌ Error communicating with AI Engine: {str(e)}"