from pathlib import Path
from .loaders import load_extensions
from .finders import find_problem, find_template
from typing import Dict

EULER: Path = Path.home() / '.euler'


def make_problem_file(language: str, id: str) -> None:
    '''
    Keyword Arguments:
        - language: A programming langauge
        - id: A problem ID
    '''
    if not EULER.exists():
        print('The .euler directory is not present in $HOME. Please run `euler setup` before using this CLI.')

    extensions: Dict[str, str] = load_extensions()
    if language not in extensions:
        print(f'{language} is currently not supported.')

    # Problem details:
    # . id: A problem ID (str)
    # . title: A problem title (str)
    # . prompt: A problem prompt (str) 
    # . url: A problem URL (str)
    id, title, prompt, url = find_problem(id)

    template: str = find_template(language)
    # Fill template with corresponding values
    template: str = template % (id, title, url, prompt)

    extension: str = extensions[language]
    problem_path: Path = EULER / f'{id:0>3}.{extension}'

    print(f'Creating file {problem_path}')
    with problem_path.open('x') as f:
        f.write(template)
