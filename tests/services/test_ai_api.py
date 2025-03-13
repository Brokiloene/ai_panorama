import asyncio
import uuid
from unittest.mock import AsyncMock, Mock, patch

import aio_pika
import pytest

from app.services.ai_api import AIApiService


@pytest.fixture
def ai_service() -> AIApiService:
    return AIApiService()


async def test_start_connection(ai_service):
    with patch(
        "aio_pika.connect_robust",
        new_callable=AsyncMock,
    ) as mock_connect:
        mock_connection = AsyncMock(spec_set=aio_pika.abc.AbstractRobustConnection)
        mock_channel = AsyncMock(spec_set=aio_pika.abc.AbstractChannel)
        mock_exchange = AsyncMock(spec_set=aio_pika.abc.AbstractExchange)
        mock_queue = AsyncMock(spec_set=aio_pika.abc.AbstractQueue)

        mock_connect.return_value = mock_connection
        mock_connection.channel = AsyncMock(return_value=mock_channel)
        mock_channel.declare_exchange = AsyncMock(return_value=mock_exchange)
        mock_channel.declare_queue = AsyncMock(return_value=mock_queue)

        await ai_service.start_connection()

        mock_connect.assert_awaited_once()
        mock_connection.channel.assert_awaited_once()
        mock_channel.declare_exchange.assert_awaited_once()
        mock_channel.declare_queue.assert_awaited_once()
        mock_queue.bind.assert_awaited_once()
        mock_queue.consume.assert_awaited_once()


async def test_close_connection(ai_service):
    ai_service.channel = AsyncMock(spec_set=aio_pika.abc.AbstractChannel)
    ai_service.connection = AsyncMock(spec_set=aio_pika.abc.AbstractRobustConnection)

    ai_service.channel.close = AsyncMock(return_value=None)
    ai_service.connection.close = AsyncMock(return_value=None)

    await ai_service.close_connection()

    ai_service.connection.close.assert_awaited_once()
    ai_service.channel.close.assert_awaited_once()


async def test_send_request_success(ai_service):
    ai_service.exchange = AsyncMock(spec_set=aio_pika.abc.AbstractExchange)
    ai_service.exchange.publish = AsyncMock(return_value=None)
    ai_service.response_queue = Mock()
    ai_service.response_queue.name = "test queue"

    test_uuid = uuid.uuid4()
    with patch("uuid.uuid4", return_value=test_uuid):
        # Вызов send_request в отдельной Task, т.к. нужно проверить добавление
        # соотвествующей future в self.pending_requests
        task = asyncio.create_task(
            ai_service.send_request(b"test msg", "test routing_key")
        )
        # Даём немного времени, чтобы send_request создал future
        await asyncio.sleep(0.1)
        corr_id = str(test_uuid)
        future = ai_service.pending_requests.get(corr_id)
        assert future is not None, "Future не был создан"
        future.set_result(b"test response")
        result = await task
        assert result == b"test response"

    ai_service.exchange.publish.assert_awaited_once()
    # Первый (и единственный) call, первый аргумент в нём -- published_msg
    published_msg = ai_service.exchange.publish.call_args[0][0]
    _, kwargs = ai_service.exchange.publish.call_args
    assert kwargs.get("routing_key") == "test routing_key"
    assert published_msg.body == b"test msg"
    assert published_msg.correlation_id == str(test_uuid)
    assert published_msg.reply_to == ai_service.response_queue.name


async def test_send_request_timeout(ai_service):
    ai_service.exchange = AsyncMock(spec_set=aio_pika.abc.AbstractExchange)
    ai_service.exchange.publish = AsyncMock(return_value=None)
    ai_service.response_queue = Mock()

    test_uuid = uuid.uuid4()
    with patch("uuid.uuid4", return_value=test_uuid):
        with pytest.raises(TimeoutError):
            await ai_service.send_request(b"test msg", "test routing_key", timeout=0.1)

    assert str(test_uuid) not in ai_service.pending_requests
