from fastapi import FastAPI

from src.sports import get_sports
from src.courts import get_courts
from src.sessions import get_sessions
from src.bookings import get_bookings
from src.attendance import get_attendance


app = FastAPI(
    title="Sports Session Booking API",
    description="API for sports sessions, court listings, bookings and attendance",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Sports Session Booking API is running"
    }


@app.get("/sports")
def list_sports():
    sports = get_sports()

    return [
        {
            "sport_id": sport[0],
            "name": sport[1]
        }
        for sport in sports
    ]


@app.get("/courts")
def list_courts():
    courts = get_courts()

    return [
        {
            "court_id": court[0],
            "name": court[1],
            "location": court[2],
            "sport": court[3]
        }
        for court in courts
    ]


@app.get("/sessions")
def list_sessions():
    sessions = get_sessions()

    return [
        {
            "session_id": session[0],
            "sport": session[1],
            "court": session[2],
            "location": session[3],
            "session_date": session[4],
            "start_time": session[5],
            "end_time": session[6],
            "capacity": session[7]
        }
        for session in sessions
    ]


@app.get("/bookings")
def list_bookings():
    bookings = get_bookings()

    return [
        {
            "booking_id": booking[0],
            "user": booking[1],
            "sport": booking[2],
            "court": booking[3],
            "location": booking[4],
            "session_date": booking[5],
            "start_time": booking[6],
            "status": booking[7]
        }
        for booking in bookings
    ]


@app.get("/attendance")
def list_attendance():
    attendance = get_attendance()

    return [
        {
            "attendance_id": record[0],
            "user": record[1],
            "sport": record[2],
            "session_date": record[3],
            "attended": record[4]
        }
        for record in attendance
    ]