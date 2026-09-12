import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="RAJOJHA@#$",
        database="fitintel"
    )

    return connection


if __name__ == "__main__":
    connection = get_connection()

    if connection.is_connected():
        print("MySQL Database Connected Successfully!")

    connection.close()