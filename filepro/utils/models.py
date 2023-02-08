from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    email: str
    password: str


@dataclass
class File:
    id: int
    userid: int
    uuid: str
    filename: str
    date_uploaded: str
    is_public: int
