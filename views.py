from shogun.view import View
from shogun.request import Request
from shogun.response import Response
from shogun.template_engine import build_template


class Index(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'var': 'Hello!', 'numbers': [1, 2, 3, 4, 5], 'base_url': request.base_url, 'session_id': request.session_id}, 'index.html')
        return Response(request, body=body)


class About(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'var': 'Why?', 'chars': ['a', 'b', 'c', 'd', 'e'], 'base_url': request.base_url}, 'about.html')
        return Response(request, body=body)
