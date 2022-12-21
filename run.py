from shogun.main import Shogun
from urls import urls
import settings
from shogun.middleware import middlewares


def get_settings():
    settings_dict = {}
    for j in [i for i in dir(settings) if i.isupper()]:
        settings_dict[j] = getattr(settings, j)
    return settings_dict


shogun = Shogun(urls=urls, settings=get_settings(), middlewares=middlewares)
