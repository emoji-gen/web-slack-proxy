#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import asyncio
import aioamqp

async def callback(channel, body, envelope, properties):
    print(" [x] Received %r" % body)
    await asyncio.sleep(body.count(b'.'))
    print(" [x] Done")
    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)

async def worker():
    try:
        transport, protocol = await aioamqp.connect()  # use default parameters
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    channel = await protocol.channel()
    await channel.queue_declare('messages', durable=True, no_wait=False)
    await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
    await channel.basic_consume(callback, queue_name='messages')


loop = asyncio.get_event_loop()
loop.run_until_complete(worker())
loop.run_forever()

