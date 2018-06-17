#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import asyncio
import aioamqp

async def connect():
    try:
        transport, protocol = await aioamqp.connect()  # use default parameters
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    print("connected !")
    await asyncio.sleep(1)

    channel = await protocol.channel()
    await channel.publish('Hello', '', 'messages')
    await channel.publish('Hello', '', 'messages')
    await channel.publish('Hello', '', 'messages')
    await channel.publish('Hello', '', 'messages')
    await channel.publish('Hello', '', 'messages')

    print("close connection")
    await protocol.close()
    transport.close()


asyncio.get_event_loop().run_until_complete(connect())
