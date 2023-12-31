from pydantic import BaseModel
from typing import Union, List
from queries.pool import pool


class ParticipantsIn(BaseModel):
    user_id: int
    trip_id: int


class CreateParticipantsOut(BaseModel):
    participant_id: int
    user_id: int
    trip_id: int


class ParticipantsOut(BaseModel):
    participant_id: int
    user_id: int
    username: str
    trip_id: int


class Error(BaseModel):
    message: str


class CreateParticipantError(ValueError):
    pass


class ParticipantRepository:
    def create_participants(
        self, participant: ParticipantsIn
    ) -> Union[CreateParticipantsOut, Error]:
        with pool.connection() as conn:
            with conn.cursor() as db:
                result = db. execute(
                    """
                    INSERT INTO trip_participants
                        (user_id, trip_id)
                    VALUES
                        (%s, %s)
                    RETURNING participant_id;
                    """,
                    [
                        participant.user_id,
                        participant.trip_id,
                    ]
                )
                participant_id = result.fetchone()[0]
                old_data = participant.dict()
                return CreateParticipantsOut(
                    participant_id=participant_id, **old_data
                )

    def delete_participant(self, participant_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM trip_participants
                        WHERE participant_id=%s
                        """,
                        [participant_id],
                    )
                    return True
        except Exception as e:
            print(e)
            return False

    def get_all_participants(
        self, trip_id
    ) -> Union[Error, List[ParticipantsOut]]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT trip_participants.participant_id,
                            trip_participants.user_id,
                            users.username,
                            trip_participants.trip_id
                        FROM trip_participants
                        JOIN users
                        ON trip_participants.user_id = users.user_id
                        WHERE trip_id=%s
                        ORDER BY participant_id
                        """,
                        [trip_id]
                        )
                    records = result.fetchall()
                    return [ParticipantsOut(
                            participant_id=record[0],
                            user_id=record[1],
                            username=record[2],
                            trip_id=record[3]
                            )
                            for record in records
                            ]

        except Exception as e:
            print(e)
            return {"message": "Could not get all trip participants"}
