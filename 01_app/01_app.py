import streamlit as st
import sys
import os
import importlib.util
import pandas as pd

# 1. Dynamic Path Resolution
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# System path me Analytics and Database folders add karein
analytics_path = os.path.join(base_path, "03_Analytics")
db_path = os.path.join(base_path, "02_database")

if analytics_path not in sys.path:
    sys.path.append(analytics_path)
if db_path not in sys.path:
    sys.path.append(db_path)

# .env configuration load (03_Analytics folder se)
#load_dotenv(dotenv_path=os.path.join(analytics_path, ".env"))
env_api_key = os.getenv("GEMINI_API_KEY")

def load_module(module_name, relative_path):
    file_path = os.path.join(base_path, relative_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Modules Loaded
db_connection = load_module("db_connection", os.path.join("02_database", "db_connection.py"))
analytics = load_module("progress_analytics", os.path.join("03_Analytics", "progress_analytics.py"))
rule_engine = load_module("rule_engine", os.path.join("03_Analytics", "rule_engine.py"))
prediction = load_module("prediction", os.path.join("03_Analytics", "03_prediction.py"))
ai_coach = load_module("ai_coach", os.path.join("03_Analytics", "ai_coach.py"))
auth = load_module("auth", os.path.join("02_database", "auth.py"))

get_connection = db_connection.get_connection

# 2. Page Configuration
st.set_page_config(page_title="FitIntel AI Platform", page_icon="🏋️‍♂️", layout="wide")

# -------------------------------------------------------------
# USER AUTHENTICATION & SESSION MANAGEMENT
# -------------------------------------------------------------
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

# If user is NOT logged in, show Sign In / Sign Up Tabs
if st.session_state["user_id"] is None:
    st.title("🏋️‍♂️ Welcome to FitIntel AI Platform")
    st.markdown("Please sign in or register to access your personal fitness analytics.")
    st.divider()

    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Register"])

    with tab1:
        st.subheader("Login to your Account")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In", type="primary"):
            user = auth.authenticate_user(login_user, login_pass)
            if user:
                st.session_state["user_id"] = user["user_id"]
                st.session_state["username"] = user["username"]
                st.success(f"Welcome back, {user['username']}!")
                st.rerun()
            else:
                st.error("❌ Invalid Username or Password")

    with tab2:
        st.subheader("Create a New Account")
        reg_user = st.text_input("Choose Username", key="reg_user")
        reg_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        
        if st.button("Create Account"):
            if reg_user and reg_pass:
                success, msg = auth.register_user(reg_user, reg_pass)
                if success:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")
            else:
                st.warning("⚠️ Please fill out all fields.")

    st.stop()  # Stop execution here until user logs in

# -------------------------------------------------------------
# AUTHENTICATED USER SIDEBAR & NAVIGATION
# -------------------------------------------------------------
current_user_id = st.session_state["user_id"]
current_username = st.session_state["username"]

st.sidebar.title("🏋️‍♂️ FitIntel Platform")
st.sidebar.markdown(f"👤 Logged in as: **{current_username}**")

if st.sidebar.button("🚪 Logout"):
    st.session_state["user_id"] = None
    st.session_state["username"] = None
    st.rerun()

st.sidebar.divider()

# Automatic .env key resolution with manual override support
if env_api_key:
    st.sidebar.success("✅ Gemini API Key Auto-Loaded")
    gemini_api_key = env_api_key
else:
    gemini_api_key = st.sidebar.text_input("🔑 Gemini API Key (For AI Coach)", type="password")

# UPDATED: Added "🏋️ Workout Tracker" to the radio menu list
page = st.sidebar.radio("Navigation Menu", [
    "👤 User Profile",
    "📝 Daily Tracking",
    "🏋️ Workout Tracker",
    "📊 Dashboard Analytics",
    "🔮 ML Weight Prediction",
    "🤖 AI Coach"
])

# -------------------------------------------------------------
# PAGE 0: USER PROFILE & GOAL CALCULATOR
# -------------------------------------------------------------
if page == "👤 User Profile":
    st.title("👤 User Profile & Fitness Goals")
    st.markdown("Set up your physical metrics to calculate accurate BMR, TDEE, and daily nutrition targets.")
    st.divider()

    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age (Years)", min_value=10, max_value=100, value=25)
            gender = st.selectbox("Gender", ["Male", "Female"])
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=175.0, step=0.5)
            current_weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=73.0, step=0.5)

        with col2:
            target_weight = st.number_input("Target Weight (kg)", min_value=30.0, max_value=200.0, value=68.0, step=0.5)
            activity_level = st.selectbox("Activity Level", [
                "Sedentary (Little or no exercise)",
                "Lightly Active (1-3 days/week)",
                "Moderately Active (3-5 days/week)",
                "Very Active (6-7 days/week)"
            ])
            fitness_goal = st.selectbox("Primary Fitness Goal", [
                "🔥 Fat Loss",
                "💪 Muscle Gain",
                "⚖️ Weight Maintenance"
            ])

        submit_profile = st.form_submit_button("💾 Save Profile & Calculate Targets")

    if submit_profile:
        # BMR Calculation (Mifflin-St Jeor Equation)
        if gender == "Male":
            bmr = (10 * current_weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * current_weight) + (6.25 * height) - (5 * age) - 161

        # TDEE Multiplier
        multipliers = {
            "Sedentary (Little or no exercise)": 1.2,
            "Lightly Active (1-3 days/week)": 1.375,
            "Moderately Active (3-5 days/week)": 1.55,
            "Very Active (6-7 days/week)": 1.725
        }
        tdee = bmr * multipliers[activity_level]

        # Target Calorie & Protein Logic
        if "Fat Loss" in fitness_goal:
            target_calories = tdee - 500  # 500 kcal deficit
            target_protein = current_weight * 2.0  # 2.0g per kg
        elif "Muscle Gain" in fitness_goal:
            target_calories = tdee + 300  # 300 kcal surplus
            target_protein = current_weight * 2.2  # 2.2g per kg
        else:
            target_calories = tdee
            target_protein = current_weight * 1.6  # 1.6g per kg

        st.session_state["target_calories"] = int(target_calories)
        st.session_state["target_protein"] = int(target_protein)
        st.session_state["user_bmr"] = int(bmr)
        st.session_state["user_tdee"] = int(tdee)

        st.success("✅ Profile Updated & Targets Calculated Successfully!")
        
        # Display Calculated Output Cards
        st.divider()
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Base BMR", f"{int(bmr)} kcal")
        with col_m2:
            st.metric("TDEE", f"{int(tdee)} kcal")
        with col_m3:
            st.metric("Daily Target Calories", f"{int(target_calories)} kcal")
        with col_m4:
            st.metric("Daily Target Protein", f"{int(target_protein)} g")

# -------------------------------------------------------------
# PAGE 1: DAILY DATA LOGGING
# -------------------------------------------------------------
elif page == "📝 Daily Tracking":
    st.title("📝 Daily Fitness & Nutrition Logging")
    st.markdown("Record daily health metrics directly into your MySQL database.")
    st.divider()

    with st.form("daily_tracking_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            log_date = st.date_input("Log Date")
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, step=0.1, value=73.0)
            calories = st.number_input("Calories Consumed (kcal)", min_value=0, max_value=10000, step=50, value=2200)
            protein = st.number_input("Protein Intake (g)", min_value=0, max_value=500, step=1, value=130)
            
        with col2:
            steps = st.number_input("Steps Count", min_value=0, max_value=100000, step=500, value=8000)
            water = st.number_input("Water Intake (Liters)", min_value=0.0, max_value=10.0, step=0.5, value=3.0)
            sleep = st.number_input("Sleep Duration (Hours)", min_value=0.0, max_value=24.0, step=0.5, value=7.5)
            workout_done = st.selectbox("Workout Completed Today?", ["Yes", "No"])

        submit_btn = st.form_submit_button("💾 Save Daily Metrics")

    if submit_btn:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO daily_metrics (user_id, date, weight_kg, calories_consumed, protein_consumed_g, steps, water_liters, sleep_hours, workout_completed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                weight_kg = VALUES(weight_kg),
                calories_consumed = VALUES(calories_consumed),
                protein_consumed_g = VALUES(protein_consumed_g),
                steps = VALUES(steps),
                water_liters = VALUES(water_liters),
                sleep_hours = VALUES(sleep_hours),
                workout_completed = VALUES(workout_completed);
            """
            workout_bool = 1 if workout_done == "Yes" else 0
            values = (current_user_id, log_date, weight, calories, protein, steps, water, sleep, workout_bool)
            
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            
            st.success(f"✅ Data for {log_date} successfully logged into Database!")
        except Exception as e:
            st.error(f"❌ Database Insertion Error: {e}")

# -------------------------------------------------------------
# PAGE 1.5: WORKOUT INTELLIGENCE & EXERCISE TRACKER
# -------------------------------------------------------------
elif page == "🏋️ Workout Tracker":
    st.title("🏋️ Workout Intelligence & Strength Tracker")
    st.markdown("Log specific exercises, weight lifted, and sets to track progressive overload.")
    st.divider()

    with st.form("workout_log_form", clear_on_submit=True):
        col_w1, col_w2 = st.columns(2)
        
        with col_w1:
            workout_date = st.date_input("Workout Date")
            muscle_group = st.selectbox("Muscle Group", ["Chest", "Back", "Legs", "Shoulders", "Arms", "Core"])
            exercise_name = st.text_input("Exercise Name (e.g., Bench Press, Squats)", value="Bench Press")

        with col_w2:
            sets_count = st.number_input("Sets Completed", min_value=1, max_value=20, value=3)
            reps_count = st.number_input("Reps per Set", min_value=1, max_value=100, value=10)
            weight_lifted = st.number_input("Weight Lifted (kg)", min_value=0.0, max_value=500.0, step=2.5, value=60.0)

        submit_workout = st.form_submit_button("💾 Log Exercise Session")

    if submit_workout:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if workouts table exists, create if missing
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_workouts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    workout_date DATE,
                    muscle_group VARCHAR(50),
                    exercise_name VARCHAR(100),
                    sets INT,
                    reps INT,
                    weight_kg DECIMAL(5,2)
                );
            """)

            query = """
                INSERT INTO user_workouts (user_id, workout_date, muscle_group, exercise_name, sets, reps, weight_kg)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (current_user_id, workout_date, muscle_group, exercise_name, sets_count, reps_count, weight_lifted))
            conn.commit()
            cursor.close()
            conn.close()

            st.success(f"✅ Logged {exercise_name} ({weight_lifted} kg) successfully!")
        except Exception as e:
            st.error(f"❌ Failed to log workout: {e}")

    # Display logged workouts
    try:
        conn = get_connection()
        df_workouts = pd.read_sql("SELECT workout_date, muscle_group, exercise_name, sets, reps, weight_kg FROM user_workouts WHERE user_id = %s ORDER BY workout_date DESC", conn, params=(current_user_id,))
        conn.close()

        if not df_workouts.empty:
            st.divider()
            st.subheader("📋 Your Exercise Log & Volume History")
            st.dataframe(df_workouts, use_container_width=True)
    except Exception:
        pass

# -------------------------------------------------------------
# PAGE 2: DASHBOARD & CHARTS
# -------------------------------------------------------------
elif page == "📊 Dashboard Analytics":
    st.title("🏋️‍♂️ FitIntel — Health & Progress Dashboard")
    st.markdown("Automated health analytics & visual metrics.")
    st.divider()

    data = analytics.get_daily_metrics()
    
    # Filter dataset for logged-in user if column exists
    if "user_id" in data.columns:
        data = data[data["user_id"] == current_user_id]

    if data.empty:
        st.warning("⚠️ No fitness metrics logged yet for your account. Go to 'Daily Tracking' to log data!")
    else:
        weight_info = analytics.analyze_weight(data)
        protein_info = analytics.analyze_protein(data)
        activity_info = analytics.analyze_calories_and_steps(data)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Current Weight", value=f"{weight_info['Current Weight']} kg", delta=f"{weight_info['Weight Change']} kg")
        with col2:
            st.metric(label="Avg Daily Protein", value=f"{protein_info['Average Protein']} g")
        with col3:
            st.metric(label="Avg Daily Steps", value=f"{activity_info['Average Steps']}")
        with col4:
            st.metric(label="Avg Daily Calories", value=f"{activity_info['Average Calories']} kcal")

        st.divider()

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("📉 Weight Progress Trend")
            st.line_chart(data.set_index("date")["weight_kg"])

        with col_chart2:
            st.subheader("🚶 Daily Steps Tracker")
            st.bar_chart(data.set_index("date")["steps"])

# -------------------------------------------------------------
# PAGE 3: ML WEIGHT PREDICTION
# -------------------------------------------------------------
elif page == "🔮 ML Weight Prediction":
    st.title("🔮 Machine Learning Weight Forecast")
    st.markdown("Scikit-Learn Linear Regression model predicting future weight trends based on historic rate of change.")
    st.divider()

    days_slider = st.slider("Select Days to Forecast into Future:", min_value=7, max_value=60, value=30, step=1)

    try:
        df_pred, current_w, pred_w, diff = prediction.predict_future_weight(days_to_predict=days_slider)

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.metric(label="Current Logged Weight", value=f"{current_w} kg")
        with col_p2:
            st.metric(label=f"Predicted Weight ({days_slider} Days)", value=f"{pred_w} kg", delta=f"{diff} kg")
        with col_p3:
            st.metric(label="Model Algorithm", value="Linear Regression")

        st.divider()
        st.subheader("📉 Actual vs Predicted Weight Trend Chart")
        
        # FIX: Duplicate dates cleanup kar ke pivot table apply karein
        df_clean = df_pred.drop_duplicates(subset=['date', 'Type'])
        chart_data = df_clean.pivot(index='date', columns='Type', values='weight_kg')
        st.line_chart(chart_data)

    except Exception as e:
        st.error(f"❌ Could not compute ML Forecast: {e}")

# -------------------------------------------------------------
# PAGE 4: AI COACH RECOMMENDATIONS & LLM CHATBOT
# -------------------------------------------------------------
elif page == "🤖 AI Coach":
    st.title("🤖 FitIntel AI Coach Panel")
    st.markdown("Automated Rule Engine Insights + Live Generative AI Fitness Assistant")
    st.divider()

    st.subheader("⚡ Automated Rule Engine Recommendations")
    insights = rule_engine.generate_insights()
    for insight in insights:
        st.info(insight)

    st.divider()
    st.subheader("💬 Ask Your AI Fitness Coach")

    # Initialize session state for chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box
    if user_input := st.chat_input("Ask about your diet, workouts, or weight progress..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("AI Coach is analyzing your database metrics & thinking..."):
                response_text = ai_coach.generate_ai_response(user_input, gemini_api_key)
                st.markdown(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})