import json
import os

from aiokafka import AIOKafkaProducer
from bson import ObjectId

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
STATUS_TOPIC = "status_updates"

producer = None


def json_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


async def get_producer():
    global producer
    if not producer:
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v, default=json_serializer).encode("utf-8"),
        )
        await producer.start()
    return producer


async def send_status_changed_event(status_data: dict):
    prod = await get_producer()
    await prod.send_and_wait(STATUS_TOPIC, status_data)
