steps = [
    [
        # "Up" SQL statement
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY NOT NULL,
            username VARCHAR(20) NOT NULL UNIQUE,
            hashed_password VARCHAR(250) NOT NULL,
            email VARCHAR(100) NOT NULL,
            bio TEXT,
            profile_pic TEXT
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE users;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE trips (
            trip_id SERIAL PRIMARY KEY NOT NULL,
            planner VARCHAR(20) REFERENCES users(username) NOT NULL,
            trip_name VARCHAR(50) NOT NULL,
            city VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL,
            start_date VARCHAR(50) NOT NULL,
            end_date VARCHAR(50) NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE trips;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE activities (
            activity_id SERIAL PRIMARY KEY NOT NULL,
            trip INT REFERENCES trips(trip_id) ON DELETE CASCADE  NOT NULL,
            title VARCHAR(50) NOT NULL,
            url VARCHAR(250),
            date VARCHAR(50) NOT NULL,
            time VARCHAR(50) NOT NULL,
            status VARCHAR(50) DEFAULT 'Pending',
            vote SMALLINT DEFAULT 0
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE activities;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE countries (
            country_id SERIAL PRIMARY KEY NOT NULL,
            country_name VARCHAR(50) NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE countries;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE comments (
            comment_id SERIAL PRIMARY KEY NOT NULL,
            trip INT REFERENCES trips(trip_id) ON DELETE CASCADE NOT NULL,
            commenter VARCHAR(20) REFERENCES users(username) NOT NULL,
            comment TEXT NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE comments;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE friends (
            friendship_id SERIAL PRIMARY KEY NOT NULL,
            user1_id INT REFERENCES users(user_id) NOT NULL,
            user2_id INT REFERENCES users(user_id) NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE friends;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE trip_participants (
            participant_id SERIAL PRIMARY KEY NOT NULL,
            user_id INT REFERENCES users(user_id) NOT NULL,
            trip_id INT REFERENCES trips(trip_id) NOT NULL
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE trip_participants;
        """,
    ],
    [
        # "Up" SQL statement
        """
        CREATE TABLE votes (
            vote_id SERIAL PRIMARY KEY NOT NULL,
            voter_id INT REFERENCES users(user_id) NOT NULL,
            activity_id INT NOT NULL REFERENCES activities(activity_id) ON DELETE CASCADE,
            UNIQUE (voter_id, activity_id)
        );
        """,
        # "Down" SQL statement
        """
        DROP TABLE votes;
        """,
    ],
]
