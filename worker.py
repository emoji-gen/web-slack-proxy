#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import asyncio
import logging
import os

import aioamqp
import logzero
from logzero import logger


async def start():
    while True:
        try:
            transport, protocol = await aioamqp.connect()
        except aioamqp.AmqpClosedConnection as e:
            logger.error('closed connections : %s', e)
            await asyncio.sleep(3)
            continue
        except OSError as e:
            logger.error('OSError : %s', e)
            await asyncio.sleep(3)
            continue

        channel = await protocol.channel()
        await channel.queue_declare('messages', durable=True, no_wait=False)
        await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
        await channel.basic_consume(consume, queue_name='messages')
        await protocol.wait_closed()


async def consume(channel, body, envelope, properties):
    logger.info('received : %s', body)
    await asyncio.sleep(1)
    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()

    env = os.getenv('PYTHON_ENV')
    if env == 'production':
        logzero.loglevel(logging.ERROR)
    else:
        logzero.loglevel(logging.DEBUG)

