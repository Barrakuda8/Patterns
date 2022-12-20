from urllib.parse import parse_qs
from uuid import uuid4
from shogun.request import Request
from shogun.response import Response


class BaseMiddleware:

    def to_request(self, request: Request):
        pass

    def to_response(self, response: Response):
        pass


class Session(BaseMiddleware):

    def to_request(self, request: Request):
        cookie = request.environ.get('HTTP_COOKIE', None)
        if not cookie:
            return
        session_id = parse_qs(cookie)['session_id'][0]
        request.extra['session_id'] = session_id

    def to_response(self, response: Response):
        if not response.request.session_id:
            response.update_headers({'Set-Cookie': f'session_id={uuid4()}'})


middlewares = [Session]