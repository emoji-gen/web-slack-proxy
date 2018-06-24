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
import os

import logzero

from emoji_slack_proxy.worker import connect


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
loop.run_forever()
