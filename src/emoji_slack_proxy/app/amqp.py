# -*- encoding: utf-8 -*-

import asyncio

import aioamqp
from logzero import logger

_channel = None

async def connect():
    global protocol

    while True:
        try:
            transport, protocol = await aioamqp.connect()
        except aioamqp.AmqpClosedConnection as e:
            logger.error('closed connections : %s', e)
            channel = None
            await asyncio.sleep(3)
            continue
        except OSError as e:
            logger.error('OSError : %s', e)
            channel = None
            await asyncio.sleep(3)
            continue

        _channel = await protocol.channel()
        await _channel.queue_declare('messages', durable=True, no_wait=False)
        await protocol.wait_closed()


async def publish(payload):
    pass
