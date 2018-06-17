# -*- encoding: utf-8 -*-


from aiohttp.web import Application, Response

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
    app.router.add_get('/{token:.*}/post', healthcheck)
    return app
