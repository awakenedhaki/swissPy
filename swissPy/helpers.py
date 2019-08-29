import json
import requests

from operator import itemgetter
from pathlib import Path


EXTENSIONS = Path(__file__).parent / 'extensions.json'
PROBLEMS = Path(__file__).parent / 'jsons' / 'problems.json'
TEMPLATES = Path(__file__).parent / 'templates'
EULER = Path.home() / '.euler'


def load_extensions():
    with EXTENSIONS.open('r') as f:
        return json.load(f)


def _find_problem(id):
    with PROBLEMS.open('r') as f:
        problems = json.load(f)

    for problem in problems['data']:
        if problem['id'] == id:
            break
    else:
        raise ValueError()

    values = itemgetter('title', 'content')
    url = problems['url'] % id

    title, content = values(problem)
    return id, title, content, url


def _find_template(language):
    with (TEMPLATES / f'{language}.txt').open('r') as f:
        return f.read()


def make_problem_file(language, id):
    if not EULER.exists():
        raise FileNotFoundError()
    extensions = load_extensions()
    if language not in extensions:
        raise ValueError()

    id, title, content, url = _find_problem(id)

    template = _find_template(language)
    template = template % id, title, url, content

    extension = extensions[language]
    problem_path = EULER / f'{id:<0}.{extension}'
    with problem_path.open('x') as f:
        f.write(template)



def _submit_test():
    url = 'https://projecteuler.net/problem={id}'
    payload = {
        f'guess_{id}': output,
        'captcha': None
    }
    with requests.post(url, data=payload) as response:
        pass
