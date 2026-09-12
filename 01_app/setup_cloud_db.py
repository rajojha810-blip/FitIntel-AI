import pymysql

# Aiven Connection Details Paste Karein
DB_HOST = "mysql-3e61aa38-rajojha810-04fb.a.aivencloud.com"  # Apka Host
DB_PORT = 26029 # Apka Port (Integer bina quotes ke)
DB_USER = "avnadmin"  # Default User
DB_PASSWORD = "AVNS_xZvSMG-2trOykqLxlfE"  # Apka Password
DB_NAME = "defaultdb"

try:
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Daily Metrics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_metrics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        date DATE NOT NULL,
        weight_kg DECIMAL(5,2),
        calories_consumed INT,
        protein_consumed_g INT,
        steps INT,
        water_liters DECIMAL(4,2),
        sleep_hours DECIMAL(4,2),
        workout_completed TINYINT(1),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        UNIQUE KEY user_date (user_id, date)
    );
    """)

    # 3. User Workouts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_workouts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        workout_date DATE,
        muscle_group VARCHAR(50),
        exercise_name VARCHAR(100),
        sets INT,
        reps INT,
        weight_kg DECIMAL(5,2),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    conn.commit()
    print("✅ Cloud Database Tables Created Successfully!")
    conn.close()

except Exception as e:
    print("❌ Error:", e)