#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os
from pathlib import Path

src_path = str(Path(__file__).resolve().parent.joinpath('src'))
sys.path.append(src_path)

# ------------------------------------------------------------------------------

import asyncio
import logging

import logzero
from aiohttp.web import run_app

from emoji_slack_proxy import parse_amqp_url
from emoji_slack_proxy.app.web import provide_app
from emoji_slack_proxy.app.amqp import connect


# Setup logger
env = os.getenv('PYTHON_ENV')
if env == 'production':
    logzero.loglevel(logging.ERROR)
else:
    logzero.loglevel(logging.DEBUG)


# Connect AMQP server
if 'RABBITMQ_BIGWIG_TX_URL' in os.environ:
    amqp_kwargs = parse_amqp_url(os.getenv('RABBITMQ_BIGWIG_TX_URL'))
else:
    amqp_kwargs = {}

loop = asyncio.get_event_loop()
loop.create_task(connect(**amqp_kwargs))


# Run aiohttp server
app = provide_app()

if __name__ == '__main__':
    run_app(app, host='0.0.0.0', port=5002)

