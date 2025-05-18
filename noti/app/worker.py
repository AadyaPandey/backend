import asyncio
import json
import aio_pika
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo_client["notifications_db"]
notifications_collection = db["notifications"]

RABBITMQ_URL = "amqp://guest:guest@localhost/"
QUEUE_NAME = "notification_queue"
MAX_RETRIES = 3

async def send_email(notification):
    # Simulate sending email (or SMS)
    print(f"📧 Simulating sending email to {notification['user_id']}: {notification['message']}")

async def process_message(data):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            await notifications_collection.insert_one(data)
            print(f"✅ Notification saved to MongoDB")
            await send_email(data)  # Simulate sending notification
            return True
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            await asyncio.sleep(2)
    print("❌ Failed to save notification after retries.")
    return False

async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    print("📡 Worker started and waiting for messages...")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode())
                print("📨 Notification received:", data)
                success = await process_message(data)
                if not success:
                    # If you want to requeue, you can do it here or log permanently
                    pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Worker stopped by user")
