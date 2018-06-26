# -*- encoding: utf-8 -*-

from pathlib import Path

import pytest

from emoji_slack_proxy.config import load_config


async def test_load_config_zero(mocker):
    mocker.patch('emoji_slack_proxy.config.config_path',  str(Path(__file__).parents[0].joinpath('data/config0')))
    result = load_config()

    assert isinstance(result, dict)
    assert len(result) == 0


async def test_load_config_local_product(mocker):
    mocker.patch('emoji_slack_proxy.config.config_path', str(Path(__file__).parents[0].joinpath('data/config1')))
    result = load_config()

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result['foo'] == 'foo'
    assert result['bar'] == True
    assert result['baz'] == 12345
