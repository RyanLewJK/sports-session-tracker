import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.sports import create_sport, get_sports
from src.users import create_user, get_users
from src.courts import create_court, get_courts
from src.sessions import create_session, get_sessions
from src.bookings import (
    create_booking,
    get_bookings,
    cancel_booking
)
from src.attendance import (
    mark_attendance,
    get_attendance
)


def run_tests():
    print("=== SPORTS ===")
    badminton = create_sport("Badminton")
    football = create_sport("Football")

    print("Created:", badminton)
    print("Created:", football)

    print("\nAll sports:")
    for sport in get_sports():
        print(sport)

    print("\n=== COURTS ===")

    badminton_court = create_court(
        "Court 1",
        "Sports Hall A",
        badminton[0]
    )

    football_pitch = create_court(
        "Pitch 1",
        "University Sports Centre",
        football[0]
    )

    print("Created:", badminton_court)
    print("Created:", football_pitch)

    for court in get_courts():
        print(court)

    print("\n=== USERS ===")
    ryan = create_user("Ryan", "ryan@example.com")
    alex = create_user("Alex", "alex@example.com")

    print("Created:", ryan)
    print("Created:", alex)

    print("\nAll users:")
    for user in get_users():
        print(user)

    print("\n=== SESSIONS ===")
    badminton_session = create_session(
    badminton[0],
    badminton_court[0],
    "2026-09-28",
    "18:00",
    "20:00",
    2
)

    football_session = create_session(
        football[0],
        football_pitch[0],
        "2026-09-29",
        "17:00",
        "19:00",
        10
    )

    print("Created:", badminton_session)
    print("Created:", football_session)

    print("\nAll sessions:")
    for session in get_sessions():
        print(session)

    print("\n=== BOOKINGS ===")

    booking1 = create_booking(
        ryan[0],
        badminton_session[0]
    )

    print("Created:", booking1)

    booking2 = create_booking(
        alex[0],
        badminton_session[0]
    )

    print("Created:", booking2)

    print("\nAll bookings:")
    for booking in get_bookings():
        print(booking)

    print("\n=== DUPLICATE BOOKING TEST ===")

    try:
        create_booking(
            ryan[0],
            badminton_session[0]
        )
    except ValueError as error:
        print("Expected error:", error)

    print("\n=== CAPACITY TEST ===")

    third_user = create_user(
        "Jamie",
        "jamie@example.com"
    )

    try:
        create_booking(
            third_user[0],
            badminton_session[0]
        )
    except ValueError as error:
        print("Expected error:", error)

    print("\n=== TESTS COMPLETE ===")

    print("\n=== CANCELLATION TEST ===")

    cancelled_booking = cancel_booking(booking2[0])
    print("Cancelled:", cancelled_booking)


    print("\n=== ATTENDANCE TEST ===")

    attendance = mark_attendance(
        booking1[0],
        True
    )

    print("Marked attendance:", attendance)

    print("\nAttendance records:")

    for record in get_attendance():
        print(record)

    print("\n=== CANCELLED BOOKING ATTENDANCE TEST ===")

    try:
        mark_attendance(
            booking2[0],
            True
        )
    except ValueError as error:
        print("Expected error:", error)

if __name__ == "__main__":
    run_tests()