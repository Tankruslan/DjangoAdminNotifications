import aiohttp
import aiohttp_cors
from aiohttp import web
from loguru import logger

WS_CLIENTS = {}
SUPER_ADMINS = ['administrator', ]


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    if request.match_info['username'] in SUPER_ADMINS:
        WS_CLIENTS[request.match_info['username']] = ws

    logger.debug('Actor: ' + request.match_info['username'] +
                 " ; Status: " + str(ws.status))

    async for message in ws:
        if message.type == aiohttp.WSMsgType.TEXT:
            if message.data == 'close':
                await ws.close()
        elif message.type == aiohttp.WSMsgType.ERROR:
            logger.error('ws connection closed with exception %s'
                         % ws.exception())

    logger.debug('websocket connection closed')
    return ws


async def get_messages(request):
    data = await request.post()
    json_data = {
        'id': data['id'],
        'actor': data['actor'],
        'verb': data['verb'],
        'action_object': data['action_object']
    }
    logger.debug(WS_CLIENTS)
    for ws_client in WS_CLIENTS.values():
        await ws_client.send_json(json_data)
    return web.Response(status=200)


def main():
    app = aiohttp.web.Application()

    app.router.add_route('POST', '/get-messages', get_messages)
    app.router.add_route('GET', '/ws/{username}', websocket_handler)

    # Alternative way to add routes
    # app.add_routes([web.post('/get-messages', get_messages),
    #                 web.get('/ws/{username}', websocket_handler)
    #                 ])

    # Adding CORS support
    cors = aiohttp_cors.setup(app, defaults={
        # Use 'localhost' if you are out of docker, or 'socket_server' if you are in docker
        "http://socket_server:8002/": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    # Use 'localhost' if you are out of docker, or 'socket_server' if you are in docker
    aiohttp.web.run_app(app, host='socket_server', port=8002)


if __name__ == '__main__':
    main()
