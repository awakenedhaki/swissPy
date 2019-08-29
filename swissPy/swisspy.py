import json
import click

from pathlib import Path
from helpers import make_problem_file, load_extensions
from printers import printer


@click.group()
def main():
    pass


@main.command()
def setup():
    euler = Path.home() / '.euler'
    if not euler.exists():
        euler.mkdir()
    else:
        return AssertionError()


@main.command()
@click.option('-r', '--range', default=None)
@click.option('-n', '--next', is_flag=True)
@click.option('-i', '--id', default=None)
@click.option('-s', '--print-solution', is_flag=True)
@click.option('--no-url', is_flag=True)
def show(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    if 'range' in kwargs:
        del kwargs['next']
        printer(method='range', **kwargs)
    elif 'id' in kwargs:
        del kwargs['next']
        printer(method='id', **kwargs)
    elif next:
        printer(method='next', **kwargs)


@main.command()
@click.option('-l', '--langauge')
@click.option('-n', '--next')
@click.option('-i', '--id')
def mkproblem(language, next, id):
    make_problem_file(language, id)


@main.command()
def answer():
    pass


@main.command()
@click.option('--id')
@click.option('-l', '--language')
def submit(id, language):
    rosalind = Path.home() / '.rosalind' / f'{id:>03}.{language}'
    extensions = load_extensions()

    if (not rosalind.exists()):
        raise ValueError(
            'You must first run the setup command to submit your solution.')
    if (language not in extensions):
        raise ValueError(f'{language} is not yet supported in swissPy.')
    if (0 >= int(id) >= 667):
        raise ValueError(f'{id} is not a valid problem ID.')

    output = exec(rosalind)
    response = request_with_solved_captcha(id)


if __name__ == "__main__":
    main()
