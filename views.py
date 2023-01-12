from shogun.view import View
from shogun.request import Request
from shogun.response import Response
from shogun.template_engine import build_template
from shogun.log_writers import ConsoleWriter, FileWriter
from models import Engine, Logger, JSONSerializer


engine = Engine()
course_logger = Logger('course logger', FileWriter)
category_logger = Logger('category logger', ConsoleWriter)
user_logger = Logger('user logger', FileWriter)


class Index(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'categories': engine.categories, 'courses': engine.courses,
                                        'students': engine.students, 'teachers': engine.teachers,
                                        'admins': engine.admins, 'base_url': request.base_url,
                                        'session_id': request.session_id}, 'index.html')
        return Response(request, body=body)


class About(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'var': 'Why?', 'chars': ['a', 'b', 'c', 'd', 'e'],
                                        'base_url': request.base_url}, 'about.html')
        return Response(request, body=body)


class Contacts(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'var': 'What?', 'base_url': request.base_url}, 'contacts.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        title = request.POST.get('title')[0]
        text = request.POST.get('text')[0]
        email = request.POST.get('email')[0]
        body = build_template(request, {'var': 'Message', 'title': title, 'text': text, 'email': email,
                                        'base_url': request.base_url}, 'contacts_show.html')
        return Response(request, body=body)


class CategoryCreate(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'categories': engine.categories, 'base_url': request.base_url,
                                        'session_id': request.session_id}, 'create_category.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        name = request.POST.get('name')[0]
        category_id = int(request.POST.get('category_id')[0])
        category = engine.get_category_by_id(category_id) if category_id >= 0 else None
        engine.create_category(name, category)
        category_logger.log(f'{name} is created')
        body = build_template(request, {'type': 'category', 'name': name, 'action': 'created',
                                        'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class CourseCreate(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'categories': engine.categories, 'types': engine.get_courses_types(),
                                        'base_url': request.base_url, 'session_id': request.session_id},
                              'create_course.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        type_ = request.POST.get('type')[0]
        name = request.POST.get('name')[0]
        slots = engine.get_courses_slots()[type_]
        params = []
        for slot in slots:
            try:
                params.append(request.POST.get(slot)[0])
            except (IndexError, TypeError):
                params.append('')
        category = engine.get_category_by_id(int(request.POST.get('category_id')[0]))
        engine.create_course(type_, *params, name, category)
        course_logger.log(f'{name} (category: {category.name}, type: {type_}) is created')
        body = build_template(request, {'type': 'course', 'name': name, 'action': 'created',
                                        'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class CourseEdit(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        course = engine.get_course_by_id(int(request.GET.get('course_id')[0]))
        body = build_template(request, {'course': course, 'base_url': request.base_url,
                                        'session_id': request.session_id}, 'edit_course.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        id_ = int(request.POST.get('course_id')[0])
        name = request.POST.get('name')[0]
        slots = engine.get_course_by_id(id_).__slots__
        params = []
        for slot in slots:
            try:
                params.append(request.POST.get(slot)[0])
            except (IndexError, TypeError):
                params.append('')
        engine.edit_course(id_, name, *params)
        course_logger.log(f'{name} is edited')
        body = build_template(request, {'type': 'course', 'name': name, 'action': 'edited',
                                        'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class CourseCopy(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        course = engine.get_course_by_id(int(request.GET.get('course_id')[0]))
        body = build_template(request, {'course': course, 'base_url': request.base_url,
                                        'session_id': request.session_id}, 'copy_course.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        course_id = int(request.GET.get('course_id')[0])
        name = request.POST.get('name')[0]
        engine.copy_course(course_id, name)
        original = engine.get_course_by_id(course_id).name
        course_logger.log(f'{name} is copied from {original}')
        body = build_template(request, {'type': 'course', 'name': name, 'action': f'copied from {original}',
                                        'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class UserCreate(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(request, {'types': engine.get_users_types(), 'base_url': request.base_url,
                                        'session_id': request.session_id}, 'create_user.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        type_ = request.POST.get('type')[0]
        username = request.POST.get('username')[0]
        engine.create_user(type_, username)
        user_logger.log(f'{username} (type: {type_}) is created')
        body = build_template(request, {'type': 'user', 'name': username, 'action': 'created',
                                        'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class UserCourses(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        user = engine.get_user_by_id(int(request.GET.get('user_id')[0]))
        courses = [i for i in engine.courses if i not in user.courses]
        body = build_template(request, {'user': user, 'courses': courses, 'base_url': request.base_url,
                                        'session_id': request.session_id}, 'user_course.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        course_id = int(request.POST.get('course_id')[0])
        user_id = int(request.POST.get('user_id')[0])
        user = engine.get_user_by_id(user_id)
        course = engine.get_course_by_id(course_id)
        course.add_user(user)
        user.add_course(course)
        course.add_observer(user, request.POST.get('notification_method')[0])
        user_logger.log(f'{user.username} is added to course {course.name}')
        body = build_template(request, {'type': 'user', 'name': user.username,
                                        'action': f'added to course {course.name}',
                                        'base_url': request.base_url}, 'ok_page.html')
        return Response(request, body=body)


class APICourses(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = JSONSerializer(engine.courses).get_json()
        return Response(request, body=body)
