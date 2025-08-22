# Django CQRS & EventBus Example

This is a minimal Django project demonstrating **Commands, Queries, and Events** with **low coupling, high cohesion**, and hybrid handler support (classes + functions).

It implements a **CQRS + EventBus architecture** suitable for Django or FastAPI projects.

---

## Problem: Tight Coupling

In large Django projects, apps often directly call each other's models or services to:

- **Write data** — e.g., one app calls another to create/update an object.
- **Read data** — e.g., one app queries another app's models directly.
- **React to changes** — e.g., one app relies on side effects of another app.

Direct calls lead to:

- Hard-to-maintain code
- Difficult testing and mocking
- Hidden side effects
- Reduced flexibility and slower refactoring

---

## Goal

We want **low coupling** and **high cohesion**:

- Apps communicate **through messages**, not direct calls.
- Each app depends **only on the public contracts** (commands, queries, events, DTOs).
- Logic is **encapsulated** in handlers, not scattered.
- Apps are **testable** in isolation and **extensible** without breaking others.

---

## Solution: CQRS + EventBus

This approach splits app behavior into three types of messages:

### Commands

- **Intent:** Tell the system to **do something** that **changes state**.
- **Handler:** Exactly one handler per command.
- **Example:** `CreateUserCommand(username, email)`

### Queries

- **Intent:** Ask the system for **information** (read-only).
- **Handler:** Exactly one handler per query.
- **Return:** Immutable **DTO**.
- **Example:** `GetUserQuery(user_id)` → `UserDTO(user_id, username, email)`

### Events

- **Intent:** Notify that **something happened**. Does not change state directly.
- **Handler:** Zero or more handlers can react.
- **Example:** `UserCreatedEvent(user_id, username)`

---

## Commands vs Queries vs Events

| Aspect         | Command                   | Query               | Event                    |
|----------------|---------------------------|--------------------|--------------------------|
| **Intent**     | Change state              | Read-only          | Notify about change      |
| **Who triggers** | Explicit                | Explicit           | After command executes   |
| **Handlers**   | Exactly 1                | Exactly 1          | 0 or more                |
| **Return**     | Optional (ID/result)      | DTO                | None (side-effects only) |
| **Example**    | `CreateOrderCommand`      | `GetOrderQuery`    | `OrderCreatedEvent`      |

---

## Visual Flow

```plaintext
[Client Request]
      |
      v
 +-----------+
 |  Command  | ----> [ CommandBus ] ----> [ CommandHandler ]
 +-----------+
      |
      v
 [ Emits Event ]
      |
      v
 +-----------+
 |   Event   | ----> [ EventBus ] ----> [ 0..n EventHandlers ]
 +-----------+

Read flow:
[Client Request]
      |
      v
 +-----------+
 |   Query   | ----> [ QueryBus ] ----> [ QueryHandler ] ---> [ DTO ]
 +-----------+
```

## Project Structure
```
command_event_query_project/
├── core/                  # Buses
│   ├── command_bus.py
│   ├── query_bus.py
│   ├── event_bus.py
│   ├── bus_instance.py
├── contracts/             # Immutable messages & DTOs
│   ├── commands.py
│   ├── queries.py
│   ├── events.py
│   ├── dtos.py
├── app1/                  # Feature logic
│   ├── command_handlers.py
│   ├── query_handlers.py
│   ├── event_handlers.py
│   ├── handler_registry.py
│   ├── apps.py              # Registers handlers
│   ├── views.py
│   ├── tests.py
├── manage.py
├── requirements.txt
```

## Example: Command + Event Flow
```python
# Command
command = CreateUserCommand(username="Jane", email="jane@example.com")
user_id = command_bus.handle(command)

# Automatically emits event
# Handlers react (e.g., log, send email)
```

## Example: Query
```python
query = GetUserQuery(user_id=42)
user_dto = query_bus.handle(query)

print(user_dto.username)
print(user_dto.email)
```

## Handler Registration
* Static maps in `handler_registry.py`
* Dynamic registration in `apps.py` using `AppConfig.ready()`
```python
# handler_registry.py
COMMAND_HANDLERS = {
    CreateUserCommand: CreateUserHandler()
}

QUERY_HANDLERS = {
    GetUserQuery: get_user_handler
}

EVENT_HANDLERS = {
    UserCreatedEvent: [
        log_user_created,
        SendWelcomeEmailHandler(),
    ]
}
```

```python
# apps.py
for cmd, handler in COMMAND_HANDLERS.items():
    command_bus.register_handler(cmd, handler)

for qry, handler in QUERY_HANDLERS.items():
    query_bus.register_handler(qry, handler)

for evt, handlers in EVENT_HANDLERS.items():
    for h in handlers:
        event_bus.register_handler(evt, h)
```

## Benefits
* Apps depend only on buses & contracts → low coupling
* Handlers encapsulate all logic → high cohesion
* Testable and extensible
* Adding a new reaction → just add an event handler


## Run the project
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Endpoints:
* http://127.0.0.1:8000/create/ → triggers command + event
* http://127.0.0.1:8000/get/ → query returns DTO

## Conclusion
This architecture allows clear separation of concerns:
* Commands: Write/Change
* Queries: Read-only, return DTOs
* Events: Side-effect notifications, multiple subscribers

It works in Django or FastAPI, and supports hybrid handler styles (classes + functions) with optional async support.
