import time

import jwt
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route

from database import Database

SECRET = 'password1'
db = Database()


async def index(request):
    return PlainTextResponse('Zdraviya jelau')


async def is_authenticated(request):
    try:
        jwt_string = request.headers['Authorization']
    except KeyError:
        return PlainTextResponse('ERROR', status_code=403)

    if not jwt_string.startswith('Bearer '):
        return PlainTextResponse('ERROR', status_code=400)
    jwt_string = jwt_string[7:]

    try:
        jwt_data = jwt.decode(jwt_string, SECRET, algorithms=['HS256'])
    except BaseException:
        return PlainTextResponse('ERROR', status_code=400)

    if await db.user_exists(jwt_data['username']):
        return PlainTextResponse('OK')
    return PlainTextResponse('NONE', status_code=403)


async def authenticate(request):
    request_data = await request.json()
    try:
        username = request_data['username']
        password = request_data['password']
    except KeyError:
        return PlainTextResponse('ERROR', status_code=400)

    if await db.check_user_password(username, password):
        return JSONResponse({
            'result': 'OK',
            'data': jwt.encode({
                'username': username,
                'timestamp': time.time()
            }, SECRET, algorithm='HS256').decode('ascii')
        })
    return JSONResponse({
        'result': 'FALSE',
        'data': 'NONE'
    })


async def register(request):
    request_data = await request.json()
    try:
        username = request_data['username']
        password = request_data['password']
    except KeyError:
        return PlainTextResponse('ERROR', status_code=400)

    if await db.register(username, password):
        return PlainTextResponse('OK')
    return PlainTextResponse('ERROR', status_code=400)


app = Starlette(routes=[
    Route('/', endpoint=index),
    Route('/is_auth', endpoint=is_authenticated),
    Route('/auth', endpoint=authenticate, methods=['POST']),
    Route('/register', endpoint=register, methods=['POST']),
])
