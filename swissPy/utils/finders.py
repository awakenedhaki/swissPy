from .loaders import *
from operator import itemgetter
from pathlib import Path
from typing import Dict, Union, Callable, Tuple, Generator

EULER: Path = Path.home() / '.euler'


def find_problem(id: str) -> Tuple[str]:
    '''
    Finds a problem with the corresponding id value.

    KeyWord Arguments:
        - id: A problem ID

    Raises:
        - ValueError: If problem ID is not found
    '''
    problems: Dict[str, Union[Dict[str, str], str]] = load_problems()

    for problem in problems['data']:
        if problem['id'] == id:
            break
    else:
        raise ValueError(f'Problem ID {id} is not valid. Please supply an ID between 1 and 667.')

    values: Callable = itemgetter('title', 'content')
    url: str = problems['url'] % id

    # title: Problem title (str)
    # content: Problem prompt (str)
    title, prompt = values(problem)
    return id, title, prompt, url


def find_template(language: str) -> str:
    '''
    Find problem template corresponding to a given programming language.

    KeyWord Arguments:
        - language: A programming language
    '''
    try:
        templates: Dict[str, str] = load_template()
        return templates[language.lower()]
    except KeyError:
        print(f'{language} is currently not supported.')


def find_next() -> str:
    '''
    Finds the next problem to be completed.
    '''
    def files() -> Generator[int, None, None]:
        '''
        Convert file names into integers.
        '''
        for file in EULER.glob('*.*'):
            yield int(file.stem)

    try:
        next: int = sorted(map(int, files()))[-1] + 1
    except IndexError:
        next: int = 1

    return str(next)
