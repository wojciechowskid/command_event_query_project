from contracts.events import UserCreatedEvent
import asyncio

def log_user_created(event: UserCreatedEvent):
    print(f"[EVENT] User created: id={event.user_id}")

class SendWelcomeEmailHandler:
    async def handle(self, event: UserCreatedEvent):
        print(f"[EVENT] Sending welcome email to {event.username}...")
        await asyncio.sleep(1)
        print("[EVENT] Welcome email sent.")

