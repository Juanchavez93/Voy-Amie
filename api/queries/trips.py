from pydantic import BaseModel
from typing import Optional, List, Union
from queries.pool import pool


class TripIn(BaseModel):
    trip_name: str
    city: str
    country: str
    start_date: str
    end_date: str


class TripOut(BaseModel):
    trip_id: int
    planner: str
    trip_name: str
    city: str
    country: str
    start_date: str
    end_date: str


class MyTripOut(BaseModel):
    trip_id: int
    trip_name: str
    city: str
    country: str
    start_date: str
    end_date: str
    planner: str


class Error(BaseModel):
    message: str


class CreateTripError(ValueError):
    pass


class TripsRepository:
    def create_trip(
        self,
        trip: TripIn,
        planner,
    ) -> TripOut:
        with pool.connection() as conn:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    INSERT INTO trips
                        (planner,
                        trip_name,
                        city,
                        country,
                        start_date,
                        end_date)
                    VALUES
                       (%s, %s, %s, %s, %s, %s)
                    RETURNING trip_id;
                    """,
                    [
                        planner,
                        trip.trip_name,
                        trip.city,
                        trip.country,
                        trip.start_date,
                        trip.end_date,
                    ],
                )
                trip_id = result.fetchone()[0]
                old_data = trip.dict()
                return TripOut(trip_id=trip_id, planner=planner, **old_data)

    def get_trip(self, trip_id: int) -> Optional[TripOut]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT trip_id,
                            planner,
                            trip_name,
                            city,
                            country,
                            start_date,
                            end_date
                        FROM trips
                        WHERE trip_id=%s
                        """,
                        [trip_id],
                    )
                    record = result.fetchone()
                    if record is None:
                        return None
                    return TripOut(
                        trip_id=record[0],
                        planner=record[1],
                        trip_name=record[2],
                        city=record[3],
                        country=record[4],
                        start_date=record[5],
                        end_date=record[6],
                    )
        except Exception as e:
            print(e)
            return {"message": "Could not get trip."}

    def update_trip(
        self, trip_id: int, trip: TripIn, planner
    ) -> Union[TripOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        UPDATE trips
                        SET trip_name=%s,
                        city=%s,
                        country=%s,
                        start_date=%s,
                        end_date=%s
                        WHERE trip_id=%s
                        """,
                        [
                            trip.trip_name,
                            trip.city,
                            trip.country,
                            trip.start_date,
                            trip.end_date,
                            trip_id,
                        ],
                    )
                    old_data = trip.dict()
                    return TripOut(
                        trip_id=trip_id, planner=planner, **old_data
                    )
        except Exception as e:
            print(e)
            return {"message": "Could not update trip."}

    def get_all_trips(self, planner) -> Union[Error, List[TripOut]]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT *
                        FROM trips
                        WHERE planner = %s
                        """,
                        [planner],
                    )
                    trips = result.fetchall()
                    trip_list = []
                    for record in trips:
                        trip = TripOut(
                            trip_id=record[0],
                            planner=record[1],
                            trip_name=record[2],
                            city=record[3],
                            country=record[4],
                            start_date=record[5],
                            end_date=record[6],
                        )
                        trip_list.append(trip)
                    return trip_list
        except Exception as e:
            print(e)
            return {"message": "Could not get all trips"}

    def get_all_my_trips(self, user_id) -> Union[Error, List[MyTripOut]]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT
                            trips.trip_id,
                            trips.trip_name,
                            trips.city,
                            trips.country,
                            trips.start_date,
                            trips.end_date,
                            trips.planner,
                            users.user_id
                        FROM trip_participants
                        JOIN trips ON trip_participants.trip_id = trips.trip_id
                        JOIN users ON users.user_id = trip_participants.user_id
                        WHERE users.user_id = %s
                        """,
                        [user_id],
                    )
                    trips = result.fetchall()
                    trip_list = []
                    for record in trips:
                        trip = TripOut(
                            trip_id=record[0],
                            trip_name=record[1],
                            city=record[2],
                            country=record[3],
                            start_date=record[4],
                            end_date=record[5],
                            planner=record[6],
                            user_id=record[7],
                        )
                        trip_list.append(trip)
                    return trip_list
        except Exception as e:
            print(e)
            return {"message": "Could not get all trips"}

    def delete_trip(self, trip_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM trips
                        WHERE trip_id=%s
                        """,
                        [trip_id],
                    )
                    return True
        except Exception as e:
            print(e)
            return False
