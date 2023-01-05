from copy import deepcopy
import os
import datetime
from settings import BASE_DIR, LOGS_DIR_NAME


class Category:
    auto_id = 0

    def __init__(self, name: str):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.courses = []

    @property
    def courses_count(self):
        return len(self.courses)


class Course:
    auto_id = 0

    def __init__(self, name: str, category):
        self.id = Course.auto_id
        Course.auto_id += 1
        self.name = name
        self.category = category
        self.category.courses.append(self)

    def __str__(self):
        return self.name

    def clone(self):
        return deepcopy(self)


class OfflineCourse(Course):

    __slots__ = ('address', )

    def __init__(self, address: str, *args):
        super().__init__(*args)
        self.address = address


class OnlineCourse(Course):

    __slots__ = ('platform', )

    def __init__(self, platform: str, *args):
        super().__init__(*args)
        self.platform = platform


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

    def __init__(self, username: str):
        self.id = User.auto_id
        User.auto_id += 1
        self.username = username


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
        return cls.types[type_](*args, **kwargs)


class Engine:

    def __init__(self):
        self.categories = []
        self.courses = []
        self.students = []
        self.teachers = []
        self.admins = []

    def create_category(self, name: str):
        category = Category(name)
        self.categories.append(category)
        return category

    def create_course(self, type_: str, *args, **kwargs):
        course = CourseFactory.create(type_, *args, **kwargs)
        self.courses.append(course)
        return course

    def copy_course(self, course_id: int, name: str):
        new_course = self.get_course_by_id(course_id).clone()
        new_course.id = Course.auto_id
        Course.auto_id += 1
        new_course.name = name
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

    @staticmethod
    def get_courses_types():
        return CourseFactory.types.keys()

    @staticmethod
    def get_users_types():
        return UserFactory.types.keys()

    @staticmethod
    def get_courses_slots():
        return CourseFactory.types_slots


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

    def __init__(self, name):
        self.name = name

    def log(self, text):
        with open(os.path.join(BASE_DIR, LOGS_DIR_NAME, f'{self.name.replace(" ", "_")}_log.txt'), 'a') as f:
            f.writelines(f'{datetime.datetime.now()}\t{self.name}\t\t{text}\n')
