from dataclasses import dataclass

@dataclass(frozen=True)
class UserCreatedEvent:
    user_id: int
    username: str

