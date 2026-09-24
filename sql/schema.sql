CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE sports (
    sport_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE courts (
    court_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    sport_id INTEGER NOT NULL,

    FOREIGN KEY (sport_id)
        REFERENCES sports(sport_id)
);

CREATE TABLE sessions (
    session_id SERIAL PRIMARY KEY,
    sport_id INTEGER NOT NULL,
    court_id INTEGER NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),

    FOREIGN KEY (sport_id)
        REFERENCES sports(sport_id),

    FOREIGN KEY (court_id)
        REFERENCES courts(court_id)
);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    booking_status VARCHAR(20) NOT NULL DEFAULT 'BOOKED',
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (session_id)
        REFERENCES sessions(session_id),

    UNIQUE (user_id, session_id)
);

CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    booking_id INTEGER UNIQUE NOT NULL,
    attended BOOLEAN NOT NULL,

    FOREIGN KEY (booking_id)
        REFERENCES bookings(booking_id)
);