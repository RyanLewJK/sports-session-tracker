from database import get_connection


def create_user(name, email):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                RETURNING user_id, name, email;
                """,
                (name, email)
            )

            user = cursor.fetchone()
            connection.commit()

            return user


def get_users():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id, name, email
                FROM users
                ORDER BY user_id;
                """
            )

            return cursor.fetchall()