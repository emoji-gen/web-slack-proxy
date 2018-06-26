# -*- encoding: utf-8 -*-

from pathlib import Path

import pytest

from emoji_slack_proxy import config


async def test_load_config(test_client):
    config.config_path = str(Path(__file__).parents[0].joinpath('data'))
    result = config.load_config()

    assert len(result) == 3
    assert result['foo'] == 'foo'
    assert result['bar'] == True
    assert result['baz'] == 12345
