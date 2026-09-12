# 🏋️‍♂️ FitIntel AI — End-to-End Fitness Analytics & Coaching Platform

FitIntel AI is a full-stack, AI-powered health analytics platform built with Python, Streamlit, MySQL, Scikit-Learn, and Google Gemini API. It enables users to log daily fitness metrics, compute dynamic BMR/TDEE nutrition goals, track workout progression, forecast future weight trends using ML, and consult an AI Fitness Coach.

---

## 🌟 Key Features

1. **🔐 User Authentication**: Multi-user login and registration system with secure password hashing.
2. **👤 Profile & Goal Engine**: Dynamic Mifflin-St Jeor BMR and TDEE calculation with personalized caloric and protein targets.
3. **📝 Daily Fitness Logging**: Direct Database (MySQL) tracking for weight, calories, protein, steps, water, sleep, and workouts.
4. **🏋️ Workout Intelligence**: Exercise-level volume and strength tracking for progressive overload analytics.
5. **📊 Visual Dashboard**: Line charts and bar graphs for real-time progress monitoring.
6. **🔮 Machine Learning Forecast**: Scikit-Learn Linear Regression predicting future weight trends over 7 to 60 days.
7. **🤖 AI Fitness Coach**: Hybrid system combining Rule Engine insights with live Gemini LLM conversation.

---

## 🛠️ Tech Stack

* **Frontend & UI**: Streamlit
* **Database**: MySQL Server
* **Data Processing**: Pandas, NumPy
* **Machine Learning**: Scikit-Learn (Linear Regression)
* **Generative AI**: Google Gemini API (`google-generativeai`)
* **Environment**: Python 3.10+

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/FitIntel-AI-Fitness-Analytics.git](https://github.com/your-username/FitIntel-AI-Fitness-Analytics.git)
cd FitIntel-AI-Fitness-Analytics