import requests

from pathlib import Path
from .loaders import load_extensions
from .finders import find_problem, find_template


EULER = Path.home() / '.euler'


def make_problem_file(language, id):
    if not EULER.exists():
        raise FileNotFoundError()

    extensions = load_extensions()
    if language not in extensions:
        raise ValueError()

    id, title, content, url = find_problem(id)

    template = find_template(language)
    template = template % (id, title, url, content)

    extension = extensions[language]
    problem_path = EULER / f'{id:0>3}.{extension}'
    with problem_path.open('x') as f:
        f.write(template)


def _submit_test():
    url = 'https://projecteuler.net/problem={id}'
    payload = {f'guess_{id}': None, 'captcha': None}