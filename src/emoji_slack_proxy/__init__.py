# -*- encoding: utf-8 -*-

from urllib.parse import urlparse

def parse_amqp_url(url):
    parts = urlparse(url)
    return {
        'host': parts.hostname,
        'port': parts.port,
        'login': parts.username,
        'password': parts.password,
        'virtualhost': parts.path[1:],
    }

