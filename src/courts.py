from src.database import get_connection


def create_court(name, location, sport_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO courts (
                    name,
                    location,
                    sport_id
                )
                VALUES (%s, %s, %s)
                RETURNING court_id, name, location, sport_id;
                """,
                (name, location, sport_id)
            )

            court = cursor.fetchone()
            connection.commit()

            return court


def get_courts():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    c.court_id,
                    c.name,
                    c.location,
                    sp.name AS sport
                FROM courts c
                JOIN sports sp
                    ON c.sport_id = sp.sport_id
                ORDER BY c.name;
                """
            )

            return cursor.fetchall()