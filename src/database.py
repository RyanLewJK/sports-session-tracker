import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


if __name__ == "__main__":
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()

            print("Connected successfully!")
            print(version[0])

        connection.close()

    except Exception as error:
        print("Database connection failed:")
        print(error)