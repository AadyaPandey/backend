# 📬 Notification Service

A simple notification system that supports sending notifications via Email, SMS, and In-App using FastAPI, MongoDB, and RabbitMQ.

---

## 🚀 Features

- Send Notification API (`POST /notifications`)
- Get User Notifications API (`GET /users/{id}/notifications`)
- Notification types: Email, SMS, In-App
- Async worker with RabbitMQ for queue-based processing
- Retry mechanism for failed notifications

---

## 🛠 Technologies Used

- FastAPI
- MongoDB (via `motor`)
- RabbitMQ (via `aio-pika`)
- Docker (for services)
- Python dotenv for environment config

---

## 📦 Setup Instructions

1. 📂 Clone the repo or create project folder
2. 🐍 Install dependencies

```bash
pip install -r requirements.txt
