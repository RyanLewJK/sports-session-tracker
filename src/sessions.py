from src.database import get_connection



def create_session(
    sport_id,
    court_id,
    session_date,
    start_time,
    end_time,
    capacity
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sessions (
                    sport_id,
                    court_id,
                    session_date,
                    start_time,
                    end_time,
                    capacity
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING
                    session_id,
                    sport_id,
                    court_id,
                    session_date,
                    start_time,
                    end_time,
                    capacity;
                """,
                (
                    sport_id,
                    court_id,
                    session_date,
                    start_time,
                    end_time,
                    capacity
                )
            )

            session = cursor.fetchone()
            connection.commit()

            return session


def get_sessions():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    s.session_id,
                    sp.name AS sport,
                    c.name AS court,
                    c.location,
                    s.session_date,
                    s.start_time,
                    s.end_time,
                    s.capacity
                FROM sessions s
                JOIN sports sp
                    ON s.sport_id = sp.sport_id
                JOIN courts c
                    ON s.court_id = c.court_id
                ORDER BY s.session_date, s.start_time;
                """
            )

            return cursor.fetchall()