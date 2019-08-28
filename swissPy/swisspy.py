import json
import click
import blessings

from pathlib import Path


@click.group()
def main():
    pass


@main.command()
def show():
    pass