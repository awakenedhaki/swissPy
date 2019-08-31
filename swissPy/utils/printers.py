import re
import json

from .loaders import load_problems
from .finders import find_next
from pathlib import Path
from blessings import Terminal
from click import echo
from operator import itemgetter
from typing import Dict, Union, Callable

TERMINAL = Terminal()
EULER: Path = Path.home() / '.euler'
PROBLEMS: Dict[str, Union[Dict[str, str], str]] = load_problems()


def _format(problem: Dict[str, str], created: bool, print_solution: bool, no_url: bool) -> str:
    '''
    Formats a give problem with indentations and ANSI colors.

    Keyword Arguments:
        - problem: The problem to be formatted
        - created: If already created problems should be marked
        - print_solution: If solution should be displayed
        - no_url: If URL should not be displayed
    '''
    values: Callable = itemgetter('title', 'id', 'solved_by', 'diff_rate')

    # Problem details
    # . title: Problem Title
    # . id: Problem ID
    # . solved_by: Number of people with solutions
    # . diff_rate: Difficulty rate
    title, id, solved_by, diff_rate = values(problem)
    title: str = TERMINAL.bold(title)

    diff_rate: str = TERMINAL.bold_bright_red(diff_rate)
    solved_by: str = TERMINAL.bold_bright_green(solved_by)

    if created:
        id = ' ' + str(id)

    output: str = f'''{id:<4} {TERMINAL.bright_blue("-->")} {title}
    {solved_by} - {diff_rate}'''

    # If URL is to be displayed
    if not no_url:
        output += f'\n    URL: {PROBLEMS["url"] % id}'

    # If soutions are to be displayed
    if print_solution:
        solution: str = TERMINAL.reverse(f'Solution: {problem["solution"]}')
        output += f'\n    {solution}'

    return output + '\n'


def find_and_format_problem(id: str,
                            *,
                            print_solution: bool,
                            no_url: bool,
                            exception: Callble = Exception,
                            msg: str = None) -> Tuple[Dict[str, str], str]:
    '''
    Finds and formats a problem for printing.

    Keyword Arguments:
        - id: Problem ID
        - print_solution: If solution should be displayed
        - no_url: If URL should not be displayed
        - exception: Exceptio to be raise if problem is not found
        - msg: Message to be printed if exception is raised
    '''
    for problem in PROBLEMS['data']:
        if problem['id'] == id:
            break
    else:
        raise exception(msg)
    created: bool = is_created(problem['id'])
    return problem, _format(problem, created, print_solution, no_url)


def is_created(id: str) -> bool:
    '''
    Determine if a problem has already been created.

    Keyword Argumnet:
        - id: Problem ID
    '''
    for file in EULER.glob('*.*'):
        if int(id) == int(file.stem):
            break
    else:
        return False
    return True


def print_range(range: str, **kwargs) -> None:
    '''
    Prints a range of problems.

    Keyword Arguments:
        - range: A numeric range between 1 and 667
        - kwargs: Additionary keyword arguments to be passed to other functions

    raises:
        - ValueError: If the range end is less than the start.
    '''
    # If the given string does not match expected range pattern
    # Provide a layer of security when calling eval
    if not re.match(r'^\d+:\d+$', range):
        raise ValueError(f'{range} does not conform with the expected format. Please write a range as `start:end`')

    # start: The first problem to be printed in the range
    # end: The last problem to be printed in the range
    start, end = map(int, range.split(':'))
    # If end is greater than start, run eval
    if end >= start:
        SLICE = eval(f'slice({start - 1}, {end})')
    # If end is less than start, raise ValueError
    elif end < start:
        raise ValueError('The end of a range should be greater than the start.')

    for problem in PROBLEMS['data'][SLICE]:
        created: bool = is_created(problem['id'])
        output: str = _format(problem, created, **kwargs)
        echo(output)


def print_id(id: str, **kwargs) -> None:
    '''
    Prints a problem given a problem ID.

    Keyword Arguments:
        - id: Problem ID
        - kwargs: Additionary keyword arguments to be passed to other functions

    raises:
        - ValueError: If problem ID is not numeric
    '''
    # Determine if id is a of numeric type
    if not re.match(r'\d+', id):
        raise ValueError('{id} is not of numeric type.')

    # output: str
    _, output = find_and_format_problem(id, **kwargs)
    echo(output)


def print_next(**kwargs) -> None:
    '''
    Prints the next problem.

    Keyword Arguments:
        - kwargs: Additionary keyword arguments to be passed to other functions
    '''
    next: str = find_next()

    # output: str
    _, output = find_and_format_problem(id=str(next), **kwargs)
    echo(output)


def printer(method=None, **kwargs):
    '''
    Dispatches imputs to respective printer functions, depending on specified method.

    Keyword Arguments:
        - method: The method of printing
        - kwargs: Additionary keyword arguments to be passed to other functions

    raises:
        - ValueError: If method is None, or if it does not match available methods
    '''
    if method is None:
        raise ValueError('A method was not specified.')

    if method == 'range':
        print_range(**kwargs)
    elif method == 'next':
        del kwargs['next']
        print_next(**kwargs)
    elif method == 'id':
        print_id(**kwargs)
    else:
        raise ValueError(f'{method} did not match any vailable printing method.')
