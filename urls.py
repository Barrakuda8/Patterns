from shogun.url import Url
from views import Index, About, Contacts

urls = [
    Url('^$', Index),
    Url('^about$', About),
    Url('^contacts$', Contacts)
]
