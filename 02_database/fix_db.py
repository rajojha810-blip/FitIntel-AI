import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="RAJOJHA@#$",
        database="fitintel"
    )
    cursor = conn.cursor()
    
    # Foreign key checks OFF karo
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    # Table drop aur recreate karo
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Foreign key checks wapas ON karo
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    conn.commit()
    print("✅ TABLE RECREATED SUCCESSFULLY!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")