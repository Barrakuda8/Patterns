from shogun.view import View
from shogun.request import Request
from shogun.response import Response
from shogun.template_engine import build_template
from models import Engine, Logger


engine = Engine()
course_logger = Logger('course logger')
category_logger = Logger('category logger')
user_logger = Logger('user logger')


class Index(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'categories': engine.categories, 'courses': engine.courses,
                                        'users': engine.get_all_users(), 'base_url': request.base_url,
                                        'session_id': request.session_id}, 'index.html')
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


class CategoryCreate(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'base_url': request.base_url, 'session_id': request.session_id}, 'create_category.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        name = request.POST.get('name')[0]
        engine.create_category(name)
        category_logger.log(f'{name} is created')
        body = build_template(request, {'type': 'category', 'name': name, 'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class CourseCreate(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'categories': engine.categories, 'types': engine.get_courses_types(), 'base_url': request.base_url, 'session_id': request.session_id}, 'create_course.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        type_ = request.POST.get('type')[0]
        name = request.POST.get('name')[0]
        slots = engine.get_courses_slots()[type_]
        params = []
        for slot in slots:
            try:
                params.append(request.POST.get(slot)[0])
            except IndexError:
                params.append('')
        category = engine.get_category_by_id(int(request.POST.get('category_id')[0]))
        engine.create_course(type_, *params, name, category)
        course_logger.log(f'{name} (category: {category.name}, type: {type_}) is created')
        body = build_template(request, {'type': 'course', 'name': name, 'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class CourseCopy(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        course = engine.get_course_by_id(int(request.GET.get('course_id')[0]))
        body = build_template(request, {'course': course, 'base_url': request.base_url, 'session_id': request.session_id}, 'copy_course.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        course_id = int(request.GET.get('course_id')[0])
        name = request.POST.get('name')[0]
        engine.copy_course(course_id, name)
        course_logger.log(f'{name} is copied from {engine.get_course_by_id(course_id).name}')
        body = build_template(request, {'type': 'course', 'name': name, 'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class UserCreate(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'types': engine.get_users_types(), 'base_url': request.base_url, 'session_id': request.session_id}, 'create_user.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        type_ = request.POST.get('type')[0]
        username = request.POST.get('username')[0]
        engine.create_user(type_, username)
        user_logger.log(f'{username} (type: {type_}) is created')
        body = build_template(request, {'type': 'user', 'name': username, 'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)
