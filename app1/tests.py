from core.bus_instance import command_bus, query_bus
from contracts.commands import CreateUserCommand
from contracts.queries import GetUserQuery

def test_create_and_get_user():
    user_id = command_bus.handle(CreateUserCommand(username="Jane", email="x@x.com"))
    assert user_id == 42

    user_dto = query_bus.handle(GetUserQuery(user_id=user_id))
    assert user_dto.username == "Jane"
    assert user_dto.email == "jane@example.com"

