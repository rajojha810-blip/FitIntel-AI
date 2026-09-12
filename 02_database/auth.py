import hashlib
import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="RAJOJHA@#$",
            database="fitintel"
        )
        return connection
    except Exception as e:
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    if not conn:
        return False, "Database connection error."
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hash_password(password))
        )
        conn.commit()
        return True, "Account created successfully!"
    except Exception as e:
        return False, "Username already taken."
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, username FROM users WHERE username = %s AND password_hash = %s",
        (username, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    return user