#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import click

from pathlib import Path
from utils.printers import printer
from utils.helpers import make_problem_file
from utils.loaders import load_extensions
from utils.finders import find_next


@click.group(name='euler')
def main():
    pass


@main.command(help='Createa $HOME/.euler/ directory for all problems to be stored in.')
def setup():
    try:
        euler = Path.home() / '.euler'
        euler.mkdir()
        click.echo(f'Created {euler} directory.')
    except FileExistsError as e:
        print(f'{euler} already exists')


@main.command(help='Display problems, given their IDs or next in line.')
@click.option('-r', '--range', default=None)
@click.option('-n', '--next', is_flag=True)
@click.option('-i', '--id', default=None)
@click.option('-s', '--print-solution', is_flag=True)
@click.option('--no-url', is_flag=True)
def show(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    if kwargs['next']:
        printer(method='next', **kwargs)
    elif 'id' in kwargs:
        del kwargs['next']
        printer(method='id', **kwargs)
    elif 'range' in kwargs:
        del kwargs['next']
        printer(method='range', **kwargs)


@main.command(help='Create a problem file given a programming language and problem ID.')
@click.argument('language')
@click.option('-n', '--next', is_flag=True)
@click.option('-i', '--id')
def mkproblem(language, next, id):
    if next:
        make_problem_file(language, find_next())
    else:
        make_problem_file(language, id)


@main.command(help='Test a problem\'s solution')
def test():
    pass


@main.command(help='Submit a problem to Project Euler.')
@click.option('--id')
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
    # response = request_with_solved_captcha(id)


if __name__ == "__main__":
    main()
