from .loaders import *
from operator import itemgetter
from pathlib import Path

EULER = Path.home() / '.euler'


def find_problem(id):
    problems = load_problems()

    for problem in problems['data']:
        if problem['id'] == id:
            break
    else:
        raise ValueError()

    values = itemgetter('title', 'content')
    url = problems['url'] % id

    title, content = values(problem)
    return id, title, content, url


def find_template(language):
    templates = load_template()
    return templates[language]


def find_next():
    def files():
        for file in EULER.glob('*.*'):
            yield int(file.stem)

    try:
        next = sorted(map(int, files()))[-1] + 1
    except IndexError:
        next = '1'

    return str(next)
