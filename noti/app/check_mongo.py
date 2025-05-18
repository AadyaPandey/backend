import asyncio
from app.database import notifications_collection  # reuse same collection from worker

async def check_notifications():
    notifications = await notifications_collection.find().to_list(100)
    print("Notifications in MongoDB:")
    for n in notifications:
        print(n)

asyncio.run(check_notifications())
