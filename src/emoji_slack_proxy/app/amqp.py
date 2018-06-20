# -*- encoding: utf-8 -*-

import asyncio

import aioamqp
from logzero import logger


_channel = None
_messages = []


async def connect():
    while True:
        try:
            transport, protocol = await aioamqp.connect()
        except aioamqp.AmqpClosedConnection as e:
            logger.error('closed AMQP connections : %s', e)
            disconnected()
            await asyncio.sleep(3)
            continue
        except OSError as e:
            logger.error('OSError : %s', e)
            disconnected()
            await asyncio.sleep(3)
            continue

        logger.debug('AMQP server connected')
        await connected(protocol)
        await protocol.wait_closed()


async def connected(protocol):
    global _channel
    _channel = await protocol.channel()
    await _channel.queue_declare('messages', durable=True, no_wait=False)
    await publish_queued()


async def disconnected():
    global _channel
    _channel = None


async def publish(message):
    if not _channel:
        _messages.append(message)
        return

    await _channel.publish(message, '', 'messages')
    logger.debug('published : message = %s', message)


async def publish_queued():
    for message in _messages:
        await _channel.publish(message, '', 'messages')
