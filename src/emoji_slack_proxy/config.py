# -*- encoding: utf-8 -*-

import yaml
from pathlib import Path


config_path = str(Path(__file__).resolve().parents[2].joinpath('config'))


def load_config():
    config = {}

    # config/production.yml
    production_config_path = str(Path(config_path).joinpath('production.yml'))
    try:
        production_config = yaml.load(open(production_config_path, 'r', encoding='utf-8'))
    except FileNotFoundError:
        production_config = None
    if isinstance(production_config, dict):
        config.update(production_config)

    # config/local.yml
    local_config_path = str(Path(config_path).joinpath('local.yml'))
    try:
        local_config = yaml.load(open(local_config_path, 'r', encoding='utf-8'))
    except FileNotFoundError:
        local_config = None
    if isinstance(local_config, dict):
        config.update(local_config)

    return config
