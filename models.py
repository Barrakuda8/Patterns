import abc
from copy import deepcopy
from jsonpickle import dumps


class Observer(metaclass=abc.ABCMeta):

    def __init__(self, user):
        self.subject = None
        self.user = user

    @abc.abstractmethod
    def update(self, param, old, new):
        pass


class EmailObserver(Observer):

    def update(self, param, old, new):
        print(f'EMAIL (to {self.user.username}) >>> Course {self.subject.name}, {param} is changed from {old} to {new}')


class SMSObserver(Observer):

    def update(self, param, old, new):
        print(f'SMS (to {self.user.username}) >>> Course {self.subject.name}, {param} is changed from {old} to {new}')


class Subject:

    def __init__(self):
        self.observers = []

    def attach(self, observer):
        observer.subject = self
        self.observers.append(observer)

    def detach(self, observer):
        observer.subject = None
        self.observers.remove(observer)

    def notify(self, state, old, new):
        for observer in self.observers:
            observer.update(state, old, new)


class Category:
    auto_id = 0

    def __init__(self, name: str, category=None):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.courses = []
        self.subcategories = []
        self.category = category

    @property
    def courses_count(self):
        return len(self.courses)

    @property
    def get_category(self):
        return self.category.name if self.category else '-'


class Course(Subject):
    auto_id = 0

    def __init__(self, name: str, category):
        self.id = Course.auto_id
        Course.auto_id += 1
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.users = {'students': [], 'teachers': [], 'admins': []}
        super().__init__()

    def __str__(self):
        return self.name

    def clone(self):
        return deepcopy(self)

    def add_user(self, user):
        self.users[f'{user.type_}s'].append(user)

    def add_observer(self, user, method: str = 'email'):
        if method.lower() == 'sms':
            observer = SMSObserver(user)
        else:
            observer = EmailObserver(user)
        self.attach(observer)

    def edit(self, name, *args, **kwargs):
        if name != self.name:
            old = self.name
            self.name = name
            self.notify('name', old, self.name)
        self.edit_params(*args, **kwargs)

    def edit_params(self, *args, **kwargs):
        pass


class OfflineCourse(Course):

    __slots__ = ('address', )

    def __init__(self, address: str, *args):
        super().__init__(*args)
        self.address = address
        self.type_ = 'offline'

    def edit_params(self, address):
        if address != self.address:
            old = self.address
            self.address = address
            self.notify('address', old, self.address)


class OnlineCourse(Course):

    __slots__ = ('platform', )

    def __init__(self, platform: str, *args):
        super().__init__(*args)
        self.platform = platform
        self.type_ = 'online'

    def edit_params(self, platform):
        if platform != self.platform:
            old = self.platform
            self.platform = platform
            self.notify('platform', old, self.platform)


class CourseFactory:

    types = {
        'offline': OfflineCourse,
        'online': OnlineCourse
    }

    types_slots = {
        'offline': OfflineCourse.__slots__,
        'online': OnlineCourse.__slots__
    }

    @classmethod
    def create(cls, type_: str, *args, **kwargs):
        return cls.types[type_](*args, **kwargs)


class User:
    auto_id = 0

    def __init__(self, type_: str, username: str):
        self.id = User.auto_id
        User.auto_id += 1
        self.username = username
        self.type_ = type_
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)


class Student(User):
    pass


class Teacher(User):
    pass


class Admin(User):
    pass


class UserFactory:

    types = {
        'student': Student,
        'teacher': Teacher,
        'admin': Admin
    }

    @classmethod
    def create(cls, type_: str, *args, **kwargs):
        return cls.types[type_](type_, *args, **kwargs)


class Engine:

    def __init__(self):
        self.categories = []
        self.courses = []
        self.students = []
        self.teachers = []
        self.admins = []

    def create_category(self, name: str, parent_category=None):
        new_category = Category(name, parent_category)
        if not parent_category:
            self.categories.append(new_category)
        else:
            self.categories.insert(self.categories.index(parent_category) + 1, new_category)
            parent_category.subcategories.append(new_category)
        return new_category

    def create_course(self, type_: str, *args, **kwargs):
        course = CourseFactory.create(type_, *args, **kwargs)
        self.courses.append(course)
        return course

    def edit_course(self, id_: int, name: str, *args, **kwargs):
        course = self.get_course_by_id(id_)
        course.edit(name, *args, **kwargs)
        return course

    def copy_course(self, course_id: int, name: str):
        new_course = self.get_course_by_id(course_id).clone()
        new_course.id = Course.auto_id
        Course.auto_id += 1
        new_course.name = name
        new_course.users = {'students': [], 'teachers': [], 'admins': []}
        self.courses.append(new_course)
        new_course.category.courses.append(new_course)
        self.get_category_by_id(new_course.category.id).courses.append(new_course)
        return new_course

    def create_user(self, type_: str, username: str):
        user = UserFactory.create(type_, username)
        self.__getattribute__(f'{type_}s').append(user)
        return user

    def get_all_users(self):
        return [*self.students, *self.teachers, *self.admins]

    def get_category_by_id(self, id_: int):
        for category in self.categories:
            if category.id == id_:
                return category
        return None

    def get_course_by_id(self, id_: int):
        for course in self.courses:
            if course.id == id_:
                return course
        return None

    def get_user_by_id(self, id_: int):
        for user in self.get_all_users():
            if user.id == id_:
                return user
        return None

    @staticmethod
    def get_courses_types():
        return CourseFactory.types.keys()

    @staticmethod
    def get_users_types():
        return UserFactory.types.keys()

    @staticmethod
    def get_courses_slots():
        return CourseFactory.types_slots


class JSONSerializer:

    def __init__(self, obj):
        self.obj = obj

    def get_json(self):
        return dumps(self.obj)


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer):
        self.name = name
        self.writer = writer

    def log(self, text):
        self.writer.write(self.name, text)
