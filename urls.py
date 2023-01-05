from shogun.url import Url
from views import *

urls = [
    Url('^$', Index),
    Url('^about$', About),
    Url('^contacts$', Contacts),
    Url('^categories/create$', CategoryCreate),
    Url('^courses/create$', CourseCreate),
    Url('^courses/copy', CourseCopy),
    Url('^users/create$', UserCreate),
]
