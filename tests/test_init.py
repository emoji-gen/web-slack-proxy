# -*- encoding: utf-8 -*-

import pytest

from emoji_slack_proxy import parse_amqp_url


async def test_parse_amqp_url(test_client):
    url = 'amqp://username:password@example.com:12345/vhost'
    parts = parse_amqp_url(url)

    assert parts['host'] == 'example.com'
    assert parts['port'] == 12345
    assert parts['login'] == 'username'
    assert parts['password'] == 'password'
    assert parts['virtualhost'] == 'vhost'
