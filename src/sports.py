from database import get_connection


def create_sport(name):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sports (name)
                VALUES (%s)
                RETURNING sport_id, name;
                """,
                (name,)
            )

            sport = cursor.fetchone()
            connection.commit()

            return sport


def get_sports():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT sport_id, name
                FROM sports
                ORDER BY sport_id;
                """
            )

            return cursor.fetchall()
