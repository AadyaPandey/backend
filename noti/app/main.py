from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aio_pika
import json
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# MongoDB setup
mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo_client["notifications_db"]
notifications_collection = db["notifications"]

# RabbitMQ config
RABBITMQ_URL = "amqp://guest:guest@localhost/"
QUEUE_NAME = "notification_queue"

class Notification(BaseModel):
    user_id: str
    type: str
    message: str

@app.on_event("startup")
async def startup():
    # Connect to RabbitMQ
    app.state.rabbitmq_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    app.state.channel = await app.state.rabbitmq_connection.channel()
    await app.state.channel.declare_queue(QUEUE_NAME, durable=True)

@app.on_event("shutdown")
async def shutdown():
    # Close RabbitMQ connection
    await app.state.rabbitmq_connection.close()

@app.post("/notifications")
async def send_notification(notification: Notification):
    try:
        message = json.dumps(notification.dict()).encode()
        await app.state.channel.default_exchange.publish(
            aio_pika.Message(body=message),
            routing_key=QUEUE_NAME
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to queue notification: {e}")
    return {"status": "Queued!"}

@app.get("/users/{user_id}/notifications")
async def get_notifications(user_id: str):
    notifications = await notifications_collection.find({"user_id": user_id}).to_list(100)
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for this user")
    return {"notifications": notifications}
