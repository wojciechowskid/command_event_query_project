from contracts.commands import CreateUserCommand
from contracts.queries import GetUserQuery
from contracts.events import UserCreatedEvent

from .command_handlers import CreateUserHandler
from .query_handlers import get_user_handler
from .event_handlers import log_user_created, SendWelcomeEmailHandler

COMMAND_HANDLERS = {
    CreateUserCommand: CreateUserHandler(),
}

QUERY_HANDLERS = {
    GetUserQuery: get_user_handler,
}

EVENT_HANDLERS = {
    UserCreatedEvent: [
        log_user_created,
        SendWelcomeEmailHandler(),
    ]
}

