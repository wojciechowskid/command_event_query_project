from django.http import JsonResponse
from core.bus_instance import command_bus, query_bus
from contracts.commands import CreateUserCommand
from contracts.queries import GetUserQuery

def create_user_view(request):
    command = CreateUserCommand(username="Jane", email="jane@example.com")
    user_id = command_bus.handle(command)
    return JsonResponse({"user_id": user_id})

def get_user_view(request):
    query = GetUserQuery(user_id=42)
    user_dto = query_bus.handle(query)
    return JsonResponse({
        "user_id": user_dto.user_id,
        "username": user_dto.username,
        "email": user_dto.email,
    })

