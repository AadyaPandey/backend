# 📬 Notification Service

A simple notification system built with FastAPI, MongoDB, and RabbitMQ to send Email, SMS, and In-App notifications asynchronously.

---

## 🚀 Features

- Send Notification API (`POST /notifications`)
- Get User Notifications API (`GET /users/{user_id}/notifications`)
- Supports Email, SMS, and In-App notification types
- Uses RabbitMQ queue for asynchronous processing
- Worker with retry mechanism for failed notifications
- Stores notifications in MongoDB

---

## 🛠 Technologies Used

- Python 3.9+
- FastAPI
- MongoDB (with `motor`)
- RabbitMQ (with `aio-pika`)
- Docker (optional for MongoDB & RabbitMQ)
- Python-dotenv (for environment variables)

---

## 📦 Setup Instructions

```
1.Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
2. Setup MongoDB and RabbitMQ
You can install MongoDB and RabbitMQ locally or run them via Docker:

bash
Copy
Edit
docker run -d --name mongodb -p 27017:27017 mongo
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
3. Run FastAPI app
bash
Copy
Edit
uvicorn app.main:app --reload
4. Run Worker
bash
Copy
Edit
python -m app.worker
🧩 API Endpoints
Send Notification
URL: POST /notifications

Body:

json
Copy
Edit
{
  "user_id": "string",
  "type": "email|sms|in-app",
  "message": "string"
}
Response:

json
Copy
Edit
{
  "status": "Queued!"
}
Get User Notifications
URL: GET /users/{user_id}/notifications

Response:

json
Copy
Edit
{
  "notifications": [
    {
      "_id": "mongo_id",
      "user_id": "string",
      "type": "email|sms|in-app",
      "message": "string"
    },
    ...
  ]
}
⚙️ How it works
POST /notifications publishes notification data to RabbitMQ.

The Worker consumes messages from the queue and saves them to MongoDB.

GET /users/{user_id}/notifications fetches saved notifications for that user from MongoDB.

🚧 Assumptions & Notes
MongoDB runs at mongodb://localhost:27017

RabbitMQ runs at amqp://guest:guest@localhost/

Notifications are stored as received; no actual email/SMS sending implemented (extendable)

Worker implements retries on failure (can be improved)
