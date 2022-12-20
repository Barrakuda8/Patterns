from shogun.url import Url
from views import Index, About

urls = [
    Url('^$', Index),
    Url('^about$', About)
]
