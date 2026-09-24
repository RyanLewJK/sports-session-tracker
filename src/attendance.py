from database import get_connection


def mark_attendance(booking_id, attended):
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
                raise ValueError(
                    "Cannot mark attendance for a cancelled booking"
                )

            cursor.execute(
                """
                INSERT INTO attendance (
                    booking_id,
                    attended
                )
                VALUES (%s, %s)
                ON CONFLICT (booking_id)
                DO UPDATE SET attended = EXCLUDED.attended
                RETURNING attendance_id, booking_id, attended;
                """,
                (booking_id, attended)
            )

            attendance = cursor.fetchone()
            connection.commit()

            return attendance


def get_attendance():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    a.attendance_id,
                    u.name,
                    sp.name AS sport,
                    s.session_date,
                    a.attended
                FROM attendance a
                JOIN bookings b
                    ON a.booking_id = b.booking_id
                JOIN users u
                    ON b.user_id = u.user_id
                JOIN sessions s
                    ON b.session_id = s.session_id
                JOIN sports sp
                    ON s.sport_id = sp.sport_id
                ORDER BY s.session_date, u.name;
                """
            )

            return cursor.fetchall()