import re
import json

from swissPy.utils.finders import find_next
from pathlib import Path
from blessings import Terminal
from click import echo
from operator import itemgetter

TERMINAL = Terminal()
EULER = Path.home() / '.euler'
PROBLEMS_PATH = Path(__file__).parent / 'jsons' / 'problems.json'
with PROBLEMS_PATH.open('r') as f:
    PROBLEMS = json.load(f)


def _format(problem, created, print_solution, no_url):
    values = itemgetter('title', 'id', 'solved_by', 'diff_rate')

    title, id, solved_by, diff_rate = values(problem)
    title = TERMINAL.bold(title)

    diff_rate = TERMINAL.bold_bright_red(diff_rate)
    solved_by = TERMINAL.bold_bright_green(solved_by)

    if created:
        id = ' ' + str(id)

    output = f'''{id:<4} {TERMINAL.bright_blue("-->")} {title}
    {solved_by} - {diff_rate}'''

    if not no_url:
        output += f'\n    URL: {PROBLEMS["url"] % id}'

    if print_solution:
        solution = TERMINAL.reverse(f'Solution: {problem["solution"]}')
        output += f'\n    {solution}'

    return output + '\n'


def find_and_format_problem(id,
                            *,
                            print_solution,
                            no_url,
                            exception=Exception,
                            msg=None):
    for problem in PROBLEMS['data']:
        if problem['id'] == id:
            break
    else:
        raise exception(msg)
    created = is_created(problem['id'])
    return problem, _format(problem, created, print_solution, no_url)


def is_created(id):
    for file in EULER.glob('*.*'):
        if int(id) == int(file.stem):
            break
    else:
        return False
    return True


def print_range(range: str, **kwargs):
    if not re.match(r'^\d+:\d+$', range):
        raise ValueError()

    start, end = map(int, range.split(':'))
    if end >= start:
        SLICE = eval(f'slice({start - 1}, {end})')
    elif end < start:
        raise ValueError()

    for problem in PROBLEMS['data'][SLICE]:
        created = is_created(problem['id'])
        output = _format(problem, created, **kwargs)
        echo(output)


def print_id(id, **kwargs):
    if not re.match(r'\d+', id):
        raise ValueError()
    _, output = find_and_format_problem(id, **kwargs)

    echo(output)


def print_next(**kwargs):
    next = find_next()
    _, output = find_and_format_problem(id=str(next), **kwargs)

    echo(output)


def printer(method=None, **kwargs):
    if method is None:
        raise ValueError()

    if method == 'range':
        print_range(**kwargs)
    elif method == 'next':
        del kwargs['next']
        print_next(**kwargs)
    elif method == 'id':
        print_id(**kwargs)
    else:
        pass
