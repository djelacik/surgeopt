# tests/test_consumer.py

from unittest.mock import patch, MagicMock
from src.consumer.consumer import start_consumer


@patch("src.consumer.consumer.Consumer")
def test_kafka_consumer_reads_messages(MockKafkaConsumer):
    mock_consumer = MagicMock()
    mock_message = MagicMock()
    mock_message.value.return_value = b'{"order_id": "order_test", "lat": 60.0, "lon": 24.0, "timestamp": 1234567890.0}'
    mock_message.error.return_value = None

    mock_consumer.poll.side_effect = [mock_message, KeyboardInterrupt()]
    MockKafkaConsumer.return_value = mock_consumer

    start_consumer(topic="order_created", bootstrap_servers="localhost:9092")
    mock_consumer.subscribe.assert_called_with(["order_created"])
