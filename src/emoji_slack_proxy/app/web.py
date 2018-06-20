# -*- encoding: utf-8 -*-

import json

from aiohttp.web import Application, Response
from logzero import logger

from emoji_slack_proxy.app.amqp import publish


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
    token = request.match_info['token']
    query_string = request.query_string
    body = await request.read()

    message = json.dumps({
        'query_string': query_string,
        'body': body.decode('utf-8'),
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
    app.router.add_post('/{token:.*}', post)
    return app
