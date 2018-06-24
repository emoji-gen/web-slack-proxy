# -*- encoding: utf-8 -*-

import asyncio

import aioamqp
from logzero import logger


async def connect(**kwargs):
    while True:
        try:
            logger.debug('connecting AMQP server : %s', kwargs)
            transport, protocol = await aioamqp.connect(**kwargs)
        except aioamqp.AmqpClosedConnection as e:
            logger.error('closed AMQP connections : %s', e)
            await asyncio.sleep(3)
            continue
        except OSError as e:
            logger.error('OSError : %s', e)
            await asyncio.sleep(3)
            continue

        logger.debug('AMQP server connected')
        await connected(protocol)
        await protocol.wait_closed()


async def connected(protocol):
    channel = await protocol.channel()
    await channel.queue_declare('messages', durable=True, no_wait=False)
    await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
    await channel.basic_consume(consume, queue_name='messages')


async def consume(channel, body, envelope, properties):
    logger.info('received : %s', body)
    await notify(body)
    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)
    await asyncio.sleep(1)


async def notify(body):
    pass
