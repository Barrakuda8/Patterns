from urllib.parse import parse_qs


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.environ = environ
        self.GET = {}
        self.POST = {}
        self.build_get_params_dict(environ['QUERY_STRING'])
        self.build_post_params_dict(environ['wsgi.input'].read())
        print(self.POST)
        self.settings = settings
        self.extra = {}
        self.set_base_url()

    def __getattr__(self, item):
        return self.extra.get(item, '')

    def build_get_params_dict(self, raw_params: str):
        self.GET = parse_qs(raw_params)

    def build_post_params_dict(self, raw_bytes: bytes):
        raw_post = raw_bytes.decode('utf-8')
        self.POST = parse_qs(raw_post)

    def set_base_url(self):
        self.extra['base_url'] = f"http://{self.environ['HTTP_HOST']}/"
