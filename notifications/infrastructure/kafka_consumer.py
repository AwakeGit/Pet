import json
import os

from aiokafka import AIOKafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
STATUS_TOPIC = "status_updates"


async def consume_status_updates(handler):
    consumer = AIOKafkaConsumer(
        STATUS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="notifications-group",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            await handler(msg.value)
    finally:
        await consumer.stop()
