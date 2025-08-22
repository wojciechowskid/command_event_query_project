from contracts.commands import CreateUserCommand
from contracts.events import UserCreatedEvent
from core.bus_instance import event_bus

class CreateUserHandler:
    def handle(self, command: CreateUserCommand) -> int:
        print(f"[COMMAND] Creating user {command.username}")
        new_user_id = 42
        event_bus.publish(UserCreatedEvent(user_id=new_user_id, username=command.username))
        return new_user_id

