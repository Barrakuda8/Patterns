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


class Contacts(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'var': 'What?', 'base_url': request.base_url}, 'contacts.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        title = request.POST.get('title')[0]
        text = request.POST.get('text')[0]
        email = request.POST.get('email')[0]
        body = build_template(request, {'var': 'Message', 'title': title, 'text': text, 'email': email, 'base_url': request.base_url}, 'contacts_show.html')
        return Response(request, body=body)
