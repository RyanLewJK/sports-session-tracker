from src.database import get_connection


def create_booking(user_id, session_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:

            # Check session exists
            cursor.execute(
                """
                SELECT capacity
                FROM sessions
                WHERE session_id = %s;
                """,
                (session_id,)
            )

            session = cursor.fetchone()

            if session is None:
                raise ValueError("Session does not exist")

            capacity = session[0]

            # Check duplicate booking FIRST
            cursor.execute(
                """
                SELECT booking_id
                FROM bookings
                WHERE user_id = %s
                AND session_id = %s;
                """,
                (user_id, session_id)
            )

            existing_booking = cursor.fetchone()

            if existing_booking:
                raise ValueError(
                    "User has already booked this session"
                )

            # Then check capacity
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM bookings
                WHERE session_id = %s
                AND booking_status = 'BOOKED';
                """,
                (session_id,)
            )

            current_bookings = cursor.fetchone()[0]

            if current_bookings >= capacity:
                raise ValueError("Session is full")

            # Create booking
            cursor.execute(
                """
                INSERT INTO bookings (
                    user_id,
                    session_id
                )
                VALUES (%s, %s)
                RETURNING
                    booking_id,
                    user_id,
                    session_id,
                    booking_status,
                    booked_at;
                """,
                (user_id, session_id)
            )

            booking = cursor.fetchone()
            connection.commit()

            return booking

def get_bookings():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    b.booking_id,
                    u.name,
                    sp.name AS sport,
                    c.name AS court,
                    c.location,
                    s.session_date,
                    s.start_time,
                    b.booking_status
                FROM bookings b
                JOIN users u
                    ON b.user_id = u.user_id
                JOIN sessions s
                    ON b.session_id = s.session_id
                JOIN sports sp
                    ON s.sport_id = sp.sport_id
                JOIN courts c
                    ON s.court_id = c.court_id
                ORDER BY s.session_date, s.start_time;
                """
            )

            return cursor.fetchall()
        
def cancel_booking(booking_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT booking_id, booking_status
                FROM bookings
                WHERE booking_id = %s;
                """,
                (booking_id,)
            )

            booking = cursor.fetchone()

            if booking is None:
                raise ValueError("Booking does not exist")

            if booking[1] == "CANCELLED":
                raise ValueError("Booking is already cancelled")

            cursor.execute(
                """
                UPDATE bookings
                SET booking_status = 'CANCELLED'
                WHERE booking_id = %s
                RETURNING booking_id, booking_status;
                """,
                (booking_id,)
            )

            updated_booking = cursor.fetchone()
            connection.commit()

            return updated_booking