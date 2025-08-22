from dataclasses import dataclass

@dataclass(frozen=True)
class UserDTO:
    user_id: int
    username: str
    email: str

