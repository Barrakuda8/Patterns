import os
import re
from shogun.request import Request


FOR_PATTERN = re.compile(r'{% for (?P<variable>[a-zA-Z_]+) in (?P<seq>[a-zA-Z_]+) %}(?P<content>[\S\s]+)(?={% endblock %}){% endblock %}')
VAR_PATTERN = re.compile(r'{{ (?P<variable>[a-zA-Z_]+) }}')


class Engine:

    def __init__(self, base_dir: str, templates_dir_name: str):
        self.template_dir = os.path.join(base_dir, templates_dir_name)

    def get_template_as_string(self, template_name: str):
        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.isfile(template_path):
            raise Exception(f'{template_path} is not a file')
        with open(template_path) as f:
            return f.read()

    @staticmethod
    def build_block(context: dict, block: str) -> str:
        used_vars = VAR_PATTERN.findall(block)
        if not used_vars:
            return block

        for var in used_vars:
            template_var = '{{ %s }}' % var
            block = re.sub(template_var, str(context.get(var, '')), block)

        return block

    def build_for_block(self, context: dict, block: str) -> str:
        used_for = FOR_PATTERN.search(block)
        if not used_for:
            return block

        build_for = ''
        for i in context.get(used_for.group('seq'), []):
            build_for += self.build_block({**context, used_for.group('variable'): i}, used_for.group('content'))
        return FOR_PATTERN.sub(build_for, block)

    def build(self, context: dict, template_name: str) -> str:
        template = self.get_template_as_string(template_name)
        template = self.build_for_block(context, template)
        return self.build_block(context, template)


def build_template(request: Request, context: dict, template_name: str) -> str:
    assert request.settings.get('BASE_DIR')
    assert request.settings.get('TEMPLATES_DIR_NAME')

    engine = Engine(request.settings.get('BASE_DIR'), request.settings.get('TEMPLATES_DIR_NAME'))
    return engine.build(context, template_name)
