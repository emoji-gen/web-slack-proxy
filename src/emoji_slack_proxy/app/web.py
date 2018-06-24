# -*- encoding: utf-8 -*-

import json

from aiohttp.web import Application, Response
from aiohttp.web_exceptions import HTTPBadRequest
from logzero import logger

from emoji_slack_proxy.app.amqp import publish
from emoji_slack_proxy.config import load_config


config = load_config()
security_headers = {
    'X-XSS-Protection': '1; mode=block',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
}


async def healthcheck(request):
    return Response(
        body='OK',
        headers={
            'Cache-Control': 'private, no-store, no-cache, must-revalidate',
            **security_headers,
        },
        content_type='text/plain',
        charset='utf-8'
    )


async def post(request):
    # Find target WebHook URL
    token = request.match_info['token']
    name = request.match_info['name']

    hook = _find_hook(token, name)
    if not hook:
        return HTTPBadRequest()

    # Publish message
    body = await request.read()

    message = json.dumps({
        'body': body.decode('utf-8'),
        'hook_url': hook['url'],
    })
    await publish(message.encode('utf-8'))

    return Response(
        body='OK',
        headers={
            'Cache-Control': 'private, no-store, no-cache, must-revalidate',
            **security_headers,
        },
        content_type='text/plain',
        charset='utf-8'
    )


def provide_app():
    app = Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/{token:.*}/{name:.*}', post)
    return app


def _find_hook(token, name):
    for hook in config['hooks']:
        if hook['token'] == token and name == hook['name']:
            return hook

