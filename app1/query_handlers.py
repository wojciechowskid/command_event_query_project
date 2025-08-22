from contracts.queries import GetUserQuery
from contracts.dtos import UserDTO

def get_user_handler(query: GetUserQuery) -> UserDTO:
    print(f"[QUERY] Getting user with id={query.user_id}")
    return UserDTO(user_id=query.user_id, username="Jane", email="jane@example.com")

