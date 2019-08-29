import re
import json

from pathlib import Path
from blessings import Terminal
from click import echo
from operator import itemgetter

TERMINAL = Terminal()
EULER = Path.home() / '.euler'
PROBLEMS_PATH = Path(__file__).parent / 'jsons' / 'problems.json'
with PROBLEMS_PATH.open('r') as f:
    PROBLEMS = json.load(f)


def _format(problem, print_solution, no_url):
    values = itemgetter('title', 'id', 'solved_by', 'diff_rate')

    title, id, solved_by, diff_rate = values(problem)
    title = TERMINAL.bold(title)

    diff_rate = TERMINAL.bold_bright_red(diff_rate)
    solved_by = TERMINAL.bold_bright_green(solved_by)

    output = f'''{id:<3} {TERMINAL.bright_blue("-->")} {title}
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
    return problem, _format(problem, print_solution, no_url)


def print_range(range: str, **kwargs):
    if not re.match(r'\d+:\d+', range):
        raise ValueError()

    start, end = map(int, range.split(':'))
    if end >= start:
        SLICE = eval(f'slice({start - 1}, {end})')
    elif end < start:
        raise ValueError()

    for problem in PROBLEMS['data'][SLICE]:
        output = _format(problem, **kwargs)
        echo(output)


def print_id(id, **kwargs):
    if not re.match(r'\d+', id):
        raise ValueError()
    _, output = find_and_format_problem(id, **kwargs)

    echo(output)


def print_next(**kwargs):
    def files():
        for file in EULER.glob('*.*'):
            yield int(file.stem)

    try:
        next = sorted(map(int, files()))[-1] + 1
    except IndexError:
        next = '1'

    del kwargs['next']
    _, output = find_and_format_problem(id=str(next), **kwargs)

    echo(output)


def printer(method=None, **kwargs):
    if method is None:
        raise ValueError()

    if method == 'range':
        print_range(**kwargs)
    elif method == 'next':
        print_next(**kwargs)
    elif method == 'id':
        print_id(**kwargs)
    else:
        pass
